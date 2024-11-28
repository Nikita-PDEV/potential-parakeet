from django.shortcuts import render, redirect, get_object_or_404  
from django.contrib.auth.decorators import login_required  
from django.contrib.auth.mixins import UserPassesTestMixin  
from django.views.generic import ListView, UpdateView  
from .forms import UserRegistrationForm, ArticleForm  
from .models import Category, Article, Subscription  
from django.core.mail import send_mail  
from django.utils import timezone  
from django.contrib.auth import login  

def home_view(request):  
    return render(request, 'articles/home.html')  

def register_view(request):  
    if request.method == 'POST':  
        form = UserRegistrationForm(request.POST)  
        if form.is_valid():  
            user = form.save(commit=False)  
            user.set_password(form.cleaned_data['password'])  
            user.save()  
            login(request, user)  
            send_welcome_email(user)  
            return redirect('home')  
        else:  
            print(form.errors)  # Вывод ошибок в консоль для отладки  
    else:  
        form = UserRegistrationForm()  
    return render(request, 'articles/register.html', {'form': form})  

def send_welcome_email(user):  
    subject = 'Добро пожаловать на новостной портал'  
    message = f'Здравствуйте, {user.username}! Спасибо за регистрацию на нашем портале!'  
    send_mail(subject, message, 'from@example.com', [user.email])  

@login_required  
def article_create_view(request):  
    if request.method == 'POST':  
        form = ArticleForm(request.POST)  
        if form.is_valid():  
            article = form.save(commit=False)  
            article.author = request.user  # Устанавливаем текущего пользователя как автора  
            article.save()  
            # Вызов функции отправки email после добавления статьи  
            send_new_article_email(article)  
            return redirect('news')  # Перенаправление на страницу новостей  
    else:  
        form = ArticleForm()  
    return render(request, 'articles/article_form.html', {'form': form})  

def send_new_article_email(article):  
    subscriptions = Subscription.objects.filter(category=article.category)  
    for subscription in subscriptions:  
        subject = f'Новая статья в категории {subscription.category.name}'  
        message = f'Добавлена новая статья: {article.title}\nЧитать здесь: {article.get_absolute_url()}'  
        send_mail(subject, message, 'from@example.com', [subscription.user.email])  

def send_weekly_updates():  
    one_week_ago = timezone.now() - timezone.timedelta(weeks=1)  
    subscriptions = Subscription.objects.all()  

    for subscription in subscriptions:  
        new_articles = Article.objects.filter(category=subscription.category, created_at__gte=one_week_ago)  
        if new_articles.exists():  
            article_links = '\n'.join(  
                [f'{article.title}: {article.get_absolute_url()}' for article in new_articles]  
            )  
            subject = 'Новинки в вашей подписке'  
            message = f'В этой категории появились новые статьи:\n{article_links}'  
            send_mail(subject, message, 'from@example.com', [subscription.user.email])  

# Представление для отображения всех статей (новостей)  
class NewsListView(ListView):  
    model = Article  
    template_name = 'articles/news.html'  # Шаблон для отображения статей  
    context_object_name = 'articles'  
    ordering = ['-created_at']  # Сортировка статей по времени создания  

# Представление для редактирования статьи  
class ArticleUpdateView(UserPassesTestMixin, UpdateView):  
    model = Article  
    form_class = ArticleForm  
    template_name = 'articles/edit_article.html'  # Шаблон для редактирования статьи  

    def test_func(self):  
        article = self.get_object()  
        return self.request.user == article.author  # Проверка, является ли текущий пользователь автором статьи  

    def get_success_url(self):  
        return redirect('news')  # Перенаправление на страницу новостей после успешного редактирования