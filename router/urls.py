from django.urls import path

from router import views

urlpatterns = [
    path('', views.index),
    ]
