from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.entry_list, name='entry_list'),
    path('entry/edit/<int:pk>/', views.edit_entry, name='edit_entry'),
    path('entry/<int:pk>/', views.entry_detail, name='entry_detail'),
    path('delete-entry/<int:pk>/', views.delete_entry, name='delete_entry'),
    path('entry-details/<int:pk>/', views.entry_details, name='entry_details'),
    path('login/', views.custom_login, name='toph_lawfirm_login'),
    path('logout/', views.custom_logout.as_view(), name='toph_lawfirm_logout'),

]
