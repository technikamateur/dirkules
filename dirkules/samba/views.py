from django.shortcuts import render
from .models import SambaShare


def index(request):
    shares = SambaShare.objects.order_by('name')
    return render(request, 'samba/index.html')


def config(request):
    return render(request, 'samba/config.html')


def add(request):
    return render(request, 'samba/add.html')
