from django.urls import path
from . import views
from .feeds import ArticleFeed

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_us, name='about_us'),
    path('programs/', views.programs, name='programs'),
    path('agency/', views.agency, name='agency'),
    path('account/', views.account_details, name='account_details'),
    path('articles/', views.articles_list, name='articles_list'),
    path('articles/rss/', ArticleFeed(), name='articles_rss'),
    path('articles/<slug:slug>/', views.article_detail, name='article_detail'),
    path('action/', views.action, name='action'),
    path('impact-reports/', views.impact_reports, name='impact_reports'),
    path('mentor/', views.join_mentor, name='join_mentor'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
]