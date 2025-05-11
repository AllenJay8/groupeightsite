from django.urls import path
from . import views

urlpattern = [
    path('index', views.index),
    path('testing', views.testing),
]
