from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('get_cv/', views.get_cv, name='get_cv')
]