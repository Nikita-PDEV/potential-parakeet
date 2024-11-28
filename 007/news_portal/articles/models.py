from django.db import models  
from django.contrib.auth.models import User  

class Category(models.Model):  
    name = models.CharField(max_length=100)  

    def __str__(self):  
        return self.name  


class Article(models.Model):  
    title = models.CharField(max_length=200)  
    content = models.TextField()  
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):  
        return self.title

    def get_absolute_url(self):  
        from django.urls import reverse  
        return reverse('article_detail', args=[str(self.id)])  


class Subscription(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  

    def __str__(self):  
        return f"{self.user.username} - {self.category.name}"