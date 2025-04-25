from django import forms
from .models import Dataset, DataTable

class DatasetUploadForm(forms.ModelForm):
    """Form for uploading CSV files"""
    class Meta:
        model = Dataset
        fields = ['name', 'file']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv'})
        }

class GraphSelectionForm(forms.Form):
    """Form for selecting graph type and columns"""
    GRAPH_TYPES = [
        ('scatter', 'Scatter Plot'),
        ('bar', 'Bar Chart'),
        ('line', 'Line Chart'),
        ('area', 'Area Chart'),
        ('heatmap', 'Heatmap'),
        ('contour', 'Contour Plot'),
        ('pie', 'Pie Chart'),
    ]
    
    graph_type = forms.ChoiceField(
        choices=GRAPH_TYPES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    x_column = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    y_column = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def __init__(self, *args, columns=None, **kwargs):
        super().__init__(*args, **kwargs)
        if columns:
            column_choices = [(col, col) for col in columns]
            self.fields['x_column'].choices = column_choices
            self.fields['y_column'].choices = column_choices
