from django.urls import path
from . import views

app_name = 'data_viz_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_file, name='upload_file'),
    path('process_data/', views.process_data, name='process_data'),
    path('get_columns/', views.get_columns, name='get_columns'),
    path('generate_graph/', views.generate_graph, name='generate_graph'),
    path('save_data/', views.save_data, name='save_data'),
]