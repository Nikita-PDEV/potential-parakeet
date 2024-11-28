from django.contrib import admin  
from django.urls import path, include  
from django.views.generic import TemplateView  

urlpatterns = [  
    path('admin/', admin.site.urls),  
    path('accounts/', include('django.contrib.auth.urls')),   
    path('register/', register_view, name='register'),  
    path('article/create/', article_create_view, name='article_create'),  
    path('', home_view, name='home'),  
]  