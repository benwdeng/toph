from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.document_upload, name='document_upload'),
    path('download/<int:pk>/', views.document_download, name='document_download'),
    path('', views.landing_page, name='landing_page'),
]
