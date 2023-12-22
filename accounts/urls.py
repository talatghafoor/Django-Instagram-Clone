from django.urls import path
from . import views

urlpatterns = [
    path('edit', views.EditProfile, name='editprofile'),
]
