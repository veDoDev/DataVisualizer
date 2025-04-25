import plotly.graph_objects as go
import plotly.express as px
import json
import numpy as np
import pandas as pd
import traceback

def generate_plotly_figure(df, graph_type, x_column, y_column):
    """Generate a Plotly figure based on the selected graph type and columns"""
    # Print extensive debug information
    print(f"DEBUG: Generating {graph_type} figure with x={x_column}, y={y_column}")
    print(f"DEBUG: DataFrame shape: {df.shape}")
    print(f"DEBUG: DataFrame columns: {df.columns.tolist()}")
    print(f"DEBUG: DataFrame head:\n{df.head().to_string()}")
    
    # Check if columns exist
    if x_column not in df.columns:
        raise ValueError(f"Column '{x_column}' not found in DataFrame")
    if y_column not in df.columns:
        raise ValueError(f"Column '{y_column}' not found in DataFrame")
    
    # Print data types and sample values
    print(f"DEBUG: X column '{x_column}' dtype: {df[x_column].dtype}")
    print(f"DEBUG: Y column '{y_column}' dtype: {df[y_column].dtype}")
    print(f"DEBUG: X column sample: {df[x_column].head().tolist()}")
    print(f"DEBUG: Y column sample: {df[y_column].head().tolist()}")
    
    # Check for empty or all-NaN columns
    if df[x_column].isna().all():
        raise ValueError(f"X column '{x_column}' contains only NaN values")
    if df[y_column].isna().all():
        raise ValueError(f"Y column '{y_column}' contains only NaN values")
    
    # Force conversion to numeric, replacing non-numeric with NaN
    try:
        # Make a copy of the dataframe to avoid modifying the original
        df_plot = df.copy()
        
        # Convert columns to numeric, coercing errors to NaN
        df_plot[x_column] = pd.to_numeric(df_plot[x_column], errors='coerce')
        df_plot[y_column] = pd.to_numeric(df_plot[y_column], errors='coerce')
        
        print(f"DEBUG: After conversion - X sample: {df_plot[x_column].head().tolist()}")
        print(f"DEBUG: After conversion - Y sample: {df_plot[y_column].head().tolist()}")
    except Exception as e:
        print(f"ERROR: Numeric conversion failed: {str(e)}")
        print(traceback.format_exc())
        df_plot = df.copy()  # Use original if conversion fails
    
    # Drop NaN values and check if we still have data
    df_clean = df_plot.dropna(subset=[x_column, y_column])
    print(f"DEBUG: Clean DataFrame shape: {df_clean.shape}")
    
    if df_clean.empty:
        print("WARNING: No valid data points after cleaning")
        # Create an empty figure with a message
        fig = go.Figure()
        fig.update_layout(
            title="No Valid Data Points",
            annotations=[
                dict(
                    text="No valid numeric data points found for the selected columns",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5
                )
            ]
        )
        return fig
    
    # Print clean data sample
    print(f"DEBUG: Clean X sample: {df_clean[x_column].head().tolist()}")
    print(f"DEBUG: Clean Y sample: {df_clean[y_column].head().tolist()}")
    
    try:
        # Create figure based on graph type with explicit marker settings
        if graph_type == 'scatter':
            # Create a scatter plot with explicit marker settings
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=df_clean[x_column].tolist(),  # Convert to list to ensure serialization
                    y=df_clean[y_column].tolist(),  # Convert to list to ensure serialization
                    mode='markers',
                    marker=dict(
                        size=10,
                        color='rgba(0, 123, 255, 0.8)',
                        line=dict(width=1, color='rgb(0, 0, 0)')
                    ),
                    name=y_column
                )
            )
            fig.update_layout(
                title=f'Scatter Plot of {y_column} vs {x_column}',
                xaxis_title=x_column,
                yaxis_title=y_column
            )
        elif graph_type == 'line':
            # Create a line chart with explicit line and marker settings
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=df_clean[x_column].tolist(),  # Convert to list to ensure serialization
                    y=df_clean[y_column].tolist(),  # Convert to list to ensure serialization
                    mode='lines+markers',
                    line=dict(width=3, color='rgb(0, 123, 255)'),
                    marker=dict(
                        size=8,
                        color='rgb(0, 123, 255)',
                        line=dict(width=1, color='rgb(0, 0, 0)')
                    ),
                    name=y_column
                )
            )
            fig.update_layout(
                title=f'Line Chart of {y_column} vs {x_column}',
                xaxis_title=x_column,
                yaxis_title=y_column
            )
        elif graph_type == 'bar':
            # Create a bar chart with explicit color
            fig = go.Figure()
            fig.add_trace(
                go.Bar(
                    x=df_clean[x_column].tolist(),  # Convert to list to ensure serialization
                    y=df_clean[y_column].tolist(),  # Convert to list to ensure serialization
                    marker_color='rgb(0, 123, 255)',
                    name=y_column
                )
            )
            fig.update_layout(
                title=f'Bar Chart of {y_column} vs {x_column}',
                xaxis_title=x_column,
                yaxis_title=y_column
            )
        elif graph_type == 'area':
            # Create an area chart
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=df_clean[x_column].tolist(),  # Convert to list to ensure serialization
                    y=df_clean[y_column].tolist(),  # Convert to list to ensure serialization
                    mode='lines',
                    fill='tozeroy',
                    line=dict(width=1, color='rgb(0, 123, 255)'),
                    fillcolor='rgba(0, 123, 255, 0.3)',
                    name=y_column
                )
            )
            fig.update_layout(
                title=f'Area Chart of {y_column} vs {x_column}',
                xaxis_title=x_column,
                yaxis_title=y_column
            )
        elif graph_type == 'heatmap':
            # For heatmap, we need to pivot the data
            # This is a simplified version, might need adjustment based on your data
            fig = px.density_heatmap(
                df_clean, 
                x=x_column, 
                y=y_column, 
                title=f'Heatmap of {y_column} vs {x_column}',
                color_continuous_scale='Blues'
            )
        elif graph_type == 'contour':
            fig = px.density_contour(
                df_clean, 
                x=x_column, 
                y=y_column, 
                title=f'Contour Plot of {y_column} vs {x_column}'
            )
        elif graph_type == 'pie':
            # For pie chart, we use x as labels and y as values
            fig = px.pie(
                df_clean, 
                names=x_column, 
                values=y_column, 
                title=f'Pie Chart of {y_column} by {x_column}'
            )
        else:
            # Default to scatter plot
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=df_clean[x_column].tolist(),  # Convert to list to ensure serialization
                    y=df_clean[y_column].tolist(),  # Convert to list to ensure serialization
                    mode='markers',
                    marker=dict(
                        size=10,
                        color='rgba(0, 123, 255, 0.8)',
                        line=dict(width=1, color='rgb(0, 0, 0)')
                    ),
                    name=y_column
                )
            )
            fig.update_layout(
                title=f'Scatter Plot of {y_column} vs {x_column}',
                xaxis_title=x_column,
                yaxis_title=y_column
            )
        
        # Update layout for better appearance
        fig.update_layout(
            template='plotly_white',
            margin=dict(l=40, r=40, t=50, b=40),
            autosize=True,
            height=500,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        print("DEBUG: Figure created successfully")
        return fig
    
    except Exception as e:
        print(f"ERROR: Figure creation failed: {str(e)}")
        print(traceback.format_exc())
        # Create an error figure
        fig = go.Figure()
        fig.update_layout(
            title="Error Creating Visualization",
            annotations=[
                dict(
                    text=f"Error: {str(e)}",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5
                )
            ]
        )
        return fig

class PlotlyJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for Plotly figures"""
    def default(self, obj):
        try:
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, pd.Series):
                return obj.tolist()
            if isinstance(obj, pd.DataFrame):
                return obj.to_dict('records')
            if isinstance(obj, (np.int64, np.int32, np.float64, np.float32)):
                return float(obj)
            if pd.isna(obj):  # Handle NaN values
                return None
            return json.JSONEncoder.default(self, obj)
        except Exception as e:
            print(f"ERROR in JSON encoding: {str(e)}")
            return None

def get_plotly_json(fig):
    """Convert a Plotly figure to JSON for rendering in the browser"""
    try:
        # Convert the figure to a dictionary
        fig_dict = fig.to_dict()
        
        # Serialize the dictionary to JSON using the custom encoder
        json_str = json.dumps(fig_dict, cls=PlotlyJSONEncoder)
        
        print(f"DEBUG: JSON string length: {len(json_str)}")
        # Print a sample of the JSON to verify it contains data
        print(f"DEBUG: JSON sample (first 200 chars): {json_str[:200]}...")
        
        return json_str
    except Exception as e:
        print(f"ERROR: JSON conversion failed: {str(e)}")
        print(traceback.format_exc())
        return json.dumps({"error": str(e)})
