from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .views import UserProfile, EditProfile

urlpatterns = [
    path('edit', views.EditProfile, name='editprofile'),
    # User Authentication
    path('signup/', views.register, name="signup"),
    path('signin/', auth_views.LoginView.as_view(template_name="signin.html", redirect_authenticated_user=True), name='signin'),
    path('signout/', auth_views.LogoutView.as_view(template_name="signout.html"), name='signout'), 
]
