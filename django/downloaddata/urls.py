from django.urls import path
from . import views

app_name = 'downloaddata'

urlpatterns = [
    path('excel/', views.download_data_excel, name='excel'),
]
