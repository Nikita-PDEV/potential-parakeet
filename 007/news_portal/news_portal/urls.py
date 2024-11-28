from django.contrib import admin  
from django.urls import path, include  
from articles.views import home_view, register_view, article_create_view

urlpatterns = [  
    path('admin/', admin.site.urls),  
    path('register/', register_view, name='register'),   
    path('article/create/', article_create_view, name='article_create'),   
    path('', home_view, name='home'),  # Добавляем маршрут для корневого URL  
]  