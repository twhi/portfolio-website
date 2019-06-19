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
            subject = '[WEBSITE] Message received from website contact form!'
            email = form.cleaned_data['email']
            message = 'Sender name: ' + form.cleaned_data['name'] + \
                      '\nMessage from: ' + form.cleaned_data['email'] + \
                      '\nMessage text: ' + form.cleaned_data['message']
            try:
                email = EmailMessage(subject, message, email, ['***REMOVED***'], reply_to=[email])
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
