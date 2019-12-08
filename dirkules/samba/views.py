from django.shortcuts import render
from .models import SambaShare
from .forms import SambaConfigForm
from django.http import HttpResponseRedirect


def index(request):
    shares = SambaShare.objects.all()
    context = {'shares': shares}
    return render(request, 'samba/index.html', context)


def config(request):
    if request.method == 'POST':
        form = SambaConfigForm(request.POST)
        if form.is_valid():
            print("SambaConfig valid")
            return HttpResponseRedirect('samba:index')
    else:
        form = SambaConfigForm()
    context = {'form': form}
    return render(request, 'samba/config.html', context)


def add(request):
    return render(request, 'samba/add.html')
