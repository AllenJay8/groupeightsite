from django.urls import path
from . import views

urlpatterns = [
    path('', views.gender_list, name='gender_list'),
    path('gender/add/', views.add_gender, name='add_gender'),
    path('gender/edit/<int:id>/', views.edit_gender, name='edit_gender'),
    path('gender/delete/<int:id>/', views.delete_gender, name='delete_gender'),
]