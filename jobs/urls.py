from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_index, name='job_index'),
    path('<int:job_id>', views.job_detail, name='job_detail')
]