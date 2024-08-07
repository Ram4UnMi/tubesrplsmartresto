from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Meja

#Untuk mengecek group user
def isPelayan(request):
     if request.user.groups.filter(name='pelayan').exists():
        return True

    

# Create your views here.
@login_required(login_url='/login')
def index(request) :
    if isPelayan(request) :
        list_meja = Meja.objects.all()
        context = {
            'list_meja' : list_meja
        }
        if request.method == "POST":
            nama_meja = request.POST['nama_meja']
            print(request.POST)
            if request.POST['status'] == 'Kosongkan':
                obj = get_object_or_404(Meja, nama_meja=nama_meja)
                obj.status = 'Kosong'
                obj.save()
                return redirect('meja')
        return render(request, 'meja/index.html', context)
    else :
        return redirect('home')