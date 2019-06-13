from django.shortcuts import render


def home(request):
    context = {
        'home_page': 'active',
    }
    return render(request, 'home.html', context)
