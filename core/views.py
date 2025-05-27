from django.shortcuts import render
from core.data import *

# Create your views here.

def landing(request):
    context = {
        'masters': masters,
        'services': services,
    }
    return render(request, "landing.html", context)

def thanks(request):
    context = {
    'masters': masters,
    'services': services,
    }
    return render(request, 'thanks.html', context)