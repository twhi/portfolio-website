from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import FileResponse, Http404

def get_cv(request):
    # try:
    #     return FileResponse(open('static/home_static/CV.pdf', 'rb'), content_type='application/pdf')
    # except FileNotFoundError:
    #     raise Http404()
    p = FileResponse(open('static/home_static/CV.pdf', 'rb'), content_type='application/pdf')
    return p

class Home(TemplateView):
    home_page = 'active'
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        context = locals()
        context['home_page'] = self.home_page
        return render(request, self.template_name, context)
