from django.db import models
import uuid
import os

def get_file_path(instance, filename):
    """Generate a unique file path for uploaded files"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('datasets', filename)

class Dataset(models.Model):
    """Model to store information about uploaded datasets"""
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_file_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class DataTable(models.Model):
    """Model to store data entered manually through the UI"""
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    data_json = models.JSONField()
    
    def __str__(self):
        return self.name