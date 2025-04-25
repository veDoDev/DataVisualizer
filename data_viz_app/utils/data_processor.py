import pandas as pd
import numpy as np
import json

def process_uploaded_file(file_path):
    """Process an uploaded CSV file and return a pandas DataFrame"""
    try:
        df = pd.read_csv(file_path)
        # Convert numeric columns to float where possible
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            except:
                pass
        return df
    except Exception as e:
        raise Exception(f"Error processing CSV file: {str(e)}")

def get_dataframe_from_json(data_json):
    """Convert JSON data to a pandas DataFrame"""
    try:
        return pd.DataFrame(data_json)
    except Exception as e:
        raise Exception(f"Error converting JSON to DataFrame: {str(e)}")

def get_column_types(df):
    """Get the data types of each column in the DataFrame"""
    column_types = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            column_types[col] = 'numeric'
        elif pd.api.types.is_datetime64_dtype(df[col]):
            column_types[col] = 'datetime'
        else:
            column_types[col] = 'categorical'
    return column_types

def dataframe_to_json(df):
    """Convert a DataFrame to JSON for storage or transmission"""
    try:
        # Handle NaN values and convert to list of dictionaries
        return json.loads(df.fillna('').to_json(orient='records'))
    except Exception as e:
        raise Exception(f"Error converting DataFrame to JSON: {str(e)}")

def get_column_stats(df, column):
    """Get basic statistics for a column"""
    stats = {}
    try:
        if pd.api.types.is_numeric_dtype(df[column]):
            stats['min'] = float(df[column].min())
            stats['max'] = float(df[column].max())
            stats['mean'] = float(df[column].mean())
            stats['median'] = float(df[column].median())
            stats['std'] = float(df[column].std())
        elif pd.api.types.is_datetime64_dtype(df[column]):
            stats['min'] = df[column].min().isoformat()
            stats['max'] = df[column].max().isoformat()
        else:
            # For categorical data, get value counts
            value_counts = df[column].value_counts().head(5).to_dict()
            stats['value_counts'] = {str(k): int(v) for k, v in value_counts.items()}
    except Exception as e:
        stats['error'] = str(e)
    
    return stats