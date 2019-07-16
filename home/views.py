from django.shortcuts import render
from .models import About
from django.views.generic import TemplateView


def home(request):
    about = About.objects.all()
    context = {
        'about': about,
        'home_page': 'active',
    }
    return render(request, 'home.html', context)


class Home(TemplateView):
    about = About.objects.all()
    home_page = 'active'
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        context = locals()
        context['about'] = self.about
        context['home_page'] = self.home_page
        return render(request, self.template_name, context)
