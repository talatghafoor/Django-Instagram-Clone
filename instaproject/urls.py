
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.models import Profile
from accounts.views import UserProfile, follow

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('post.urls')),
    path('profile/', include('accounts.urls')),
    path('message/', include('chat.urls')),
    

    #Profile 
    path('<username>/', UserProfile, name='profile'),
    path('<username>/saved/', UserProfile, name='profilefavourite'),
    path('<username>/follow/<option>/', follow, name='follow'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

