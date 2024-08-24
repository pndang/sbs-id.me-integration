from django.urls import path
from . import views 

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('idme/', views.idme_callback, name='idme_callback'),
    path('success/', views.success_page, name='success'),
    path('welcome/', views.welcome_page, name='welcome_page'),
    path('negative-availability/', views.neg_avai_page, name='neg_avai_page'),
    path('line/', views.virtual_line_page, name='virtual_line_page')
]