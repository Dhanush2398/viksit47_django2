"""
URL configuration for viksit_47 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.conf import settings



urlpatterns = [
    path('', views.home, name='home'),
    path('exams/', views.exams, name='exams'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('subscribe/<int:course_id>/', views.subscribe_1year, name='subscribe_1year'),
    path('subscription-return/<str:uid>/', views.subscription_return, name='subscription_return'),
    path('mock/<int:mock_id>/', views.mock, name='mock'),
    path('submit-mock/<int:mock_id>/', views.submit_mock, name='submit_mock'),
    path('studymaterials/', views.studymaterials_view, name='studymaterials'),
    path('studymaterials/<int:pk>/', views.studymaterial_detail, name='studymaterial_detail'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('buy_course/<int:course_id>/', views.buy_course_payment, name='buy_course_payment'),
    path('terms-and-conditions/', views.terms_view, name='terms'),
    path('privacy-policy/', views.privacy_view, name='privacy'),
    path('refund-policy/', views.refund_view, name='refund'),
]

