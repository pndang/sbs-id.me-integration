from django.urls import path
from . import views 

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('idme/', views.idme_callback, name='idme_callback'),
    path('success/', views.success_page, name='success'),
    path('welcome/', views.welcome_page, name='welcome_page'),
]