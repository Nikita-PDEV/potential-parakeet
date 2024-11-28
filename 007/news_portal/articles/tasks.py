from celery import shared_task  
from .views import send_weekly_updates  

@shared_task  
def send_weekly_email():  
    send_weekly_updates()