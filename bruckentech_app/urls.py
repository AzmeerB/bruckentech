from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_us, name='about_us'),
    path('programs/', views.programs, name='programs'),
    path('agency/', views.agency, name='agency'),
    path('donation/', views.donation, name='donation'),
    path('donation/complete/', views.donation_complete, name='donation_complete'),
    path('action/', views.action, name='action'),
    path('impact-reports/', views.impact_reports, name='impact_reports'),
    path('mentor/', views.join_mentor, name='join_mentor'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
]