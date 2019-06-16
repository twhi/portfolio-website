from django.shortcuts import render
from django.core.mail import EmailMessage, BadHeaderError
from django.http import HttpResponse
from .forms import ContactForm
from django.shortcuts import render, redirect


# Create your views here.
def contact(request):

    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            try:
                email = EmailMessage(name, message, email, ['***REMOVED***'], reply_to=[email])
                email.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('./thanks/')

    context = {
        'form': form,
        'contact_page': 'active',
    }
    return render(request, 'contact.html', context)


def thanks(request):
    context = {
        'contact_page': 'active'
    }
    return render(request, 'thanks.html', context)
