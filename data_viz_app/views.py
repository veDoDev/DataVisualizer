import os
import json
import pandas as pd
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Dataset, DataTable
from .forms import DatasetUploadForm, GraphSelectionForm
from .utils.data_processor import (
    read_and_preprocess_csv,
    create_dataframe_from_preprocessed_data,
    get_dataframe_from_json,
    get_column_types,
    dataframe_to_json,
    get_column_stats
)
from .utils.visualizer import generate_plotly_figure, get_plotly_json

# Global variable to store the current dataframe
# In a production app, you'd use sessions or database storage
current_df = None

def index(request):
    """Main view for the data visualization dashboard"""
    upload_form = DatasetUploadForm()
    graph_form = GraphSelectionForm()
    
    context = {
        'upload_form': upload_form,
        'graph_form': graph_form,
        'has_data': current_df is not None,
    }
    
    return render(request, 'data_viz_app/index.html', context)

def upload_file(request):
    """Handle file upload with preprocessing"""
    if request.method == 'POST':
        form = DatasetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            dataset = form.save()
            
            try:
                global current_df
                
                # Use the new preprocessing function
                uploaded_file = request.FILES['file']
                
                # Reset file pointer to beginning (in case it was read during form validation)
                uploaded_file.seek(0)
                
                # Preprocess the CSV file
                header, cleaned_data = read_and_preprocess_csv(uploaded_file)
                
                # Create DataFrame from preprocessed data
                current_df = create_dataframe_from_preprocessed_data(header, cleaned_data)
                
                # Save processed status
                dataset.processed = True
                dataset.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'File uploaded and preprocessed successfully',
                    'columns': list(current_df.columns),
                    'file_name': dataset.name,
                    'rows_processed': len(cleaned_data),
                })
            except Exception as e:
                # Delete the dataset if processing fails
                dataset.delete()
                return JsonResponse({
                    'success': False,
                    'message': f'Error processing file: {str(e)}',
                })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid form submission',
                'errors': form.errors,
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def process_data(request):
    """Process data from the spreadsheet interface"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            table_data = data.get('data', [])
            
            global current_df
            current_df = pd.DataFrame(table_data)
            
            return JsonResponse({
                'success': True,
                'message': 'Data processed successfully',
                'columns': list(current_df.columns),
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error processing data: {str(e)}',
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def get_columns(request):
    """Get columns from the current dataframe"""
    if current_df is None:
        return JsonResponse({
            'success': False,
            'message': 'No data available',
        })
    
    columns = list(current_df.columns)
    column_types = get_column_types(current_df)
    
    # Convert DataFrame to JSON for the spreadsheet
    data_json = dataframe_to_json(current_df)
    
    return JsonResponse({
        'success': True,
        'columns': columns,
        'column_types': column_types,
        'data': data_json,  # Return the data for the spreadsheet
    })

@csrf_exempt
def generate_graph(request):
    """Generate a graph based on user selections"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            graph_type = data.get('graph_type')
            x_column = data.get('x_column')
            y_column = data.get('y_column')
            
            if current_df is None:
                return JsonResponse({
                    'success': False,
                    'message': 'No data available',
                })
            
            # Print debug information
            print(f"Generating {graph_type} graph with x={x_column}, y={y_column}")
            print(f"DataFrame shape: {current_df.shape}")
            print(f"DataFrame columns: {current_df.columns.tolist()}")
            
            # Check if columns exist
            if x_column not in current_df.columns:
                return JsonResponse({
                    'success': False,
                    'message': f'Column {x_column} not found in data',
                })
                
            if y_column not in current_df.columns:
                return JsonResponse({
                    'success': False,
                    'message': f'Column {y_column} not found in data',
                })
            
            # Print sample data for debugging
            print(f"Sample data for {x_column}: {current_df[x_column].head().tolist()}")
            print(f"Sample data for {y_column}: {current_df[y_column].head().tolist()}")
            
            # Make a copy of the dataframe to avoid modifying the original
            df_for_plot = current_df.copy()
            
            # Generate the figure
            fig = generate_plotly_figure(df_for_plot, graph_type, x_column, y_column)
            plot_json = get_plotly_json(fig)
            
            # Print the JSON length for debugging
            print(f"Plot JSON length: {len(plot_json)}")
            
            return JsonResponse({
                'success': True,
                'plot': plot_json,
                'x_stats': get_column_stats(current_df, x_column),
                'y_stats': get_column_stats(current_df, y_column),
            })
        except Exception as e:
            import traceback
            print(f"Error generating graph: {str(e)}")
            print(traceback.format_exc())
            return JsonResponse({
                'success': False,
                'message': f'Error generating graph: {str(e)}',
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def save_data(request):
    """Save the current data to the database"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', 'Untitled Dataset')
            
            if current_df is None:
                return JsonResponse({
                    'success': False,
                    'message': 'No data available to save',
                })
            
            # Convert DataFrame to JSON and save
            data_json = dataframe_to_json(current_df)
            data_table = DataTable.objects.create(
                name=name,
                data_json=data_json
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Data saved successfully',
                'id': data_table.id,
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error saving data: {str(e)}',
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

print("Views created with preprocessing integration")
