from celery import Celery  
import os  

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_portal.settings')  

app = Celery('news_portal')  
app.config_from_object('django.conf:settings', namespace='CELERY')  
app.autodiscover_tasks()