from django.shortcuts import render
from django.views.generic import TemplateView


class Home(TemplateView):
    home_page = 'active'
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        context = locals()
        context['home_page'] = self.home_page
        return render(request, self.template_name, context)
