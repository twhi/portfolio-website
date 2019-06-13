from django.shortcuts import render, get_object_or_404
from .models import Job


def job_index(request):
    jobs = Job.objects
    context = {
        'jobs': jobs,
        'job_page': 'active'
    }
    return render(request, 'job_index.html', context)


def job_detail(request, job_id):
    detail = get_object_or_404(Job, pk=job_id)
    context = {
        'job': detail,
        'job_page': 'active'
    }
    return render(request, 'job_detail.html', context)
