from django.urls import path
from . import views

urlpatterns = [
    path('', views.connect, name='tracklist'),
    path('customise/', views.customise, name='customise'),
    path('complete/', views.complete, name='complete'),
]