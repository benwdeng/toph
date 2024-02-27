from django.urls import path
from . import views

urlpatterns = [
    path('', views.entry_list, name='entry_list'),
    path('entry/edit/<int:pk>/', views.edit_entry, name='edit_entry'),
    path('entry/<int:pk>/', views.entry_detail, name='entry_detail'),
]
