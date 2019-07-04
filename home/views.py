from django.shortcuts import render
from .models import About


def home(request):
    about = About.objects.all()
    context = {
        'about': about,
        'home_page': 'active',
    }
    return render(request, 'home.html', context)
