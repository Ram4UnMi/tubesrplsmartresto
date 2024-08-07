from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

from meja.models import Meja
from order.models import OrderItem, Order

# Create your views here.
def index(request) :
    return render(request, 'index.html')


@login_required(login_url='/login')
def home(request) :
    meja_kosong_count = Meja.objects.filter(status="Kosong").count()
    pesanan_siap_disajikan = OrderItem.objects.filter(order_status="Selesai Dimasak").count()
    pesanan_perlu_dimasak = OrderItem.objects.filter(order_status="Sedang Dimasak").count()
    pesanan_belum_terkonfirmasi = OrderItem.objects.filter(order_status='Menunggu Konfirmasi').count()
    pesanan_belum_dibayar = Order.objects.filter(status='Belum Dibayar').count()
    context ={
        'meja_kosong': meja_kosong_count,
        'pesanan_siap_disajikan' : pesanan_siap_disajikan,
        'pesanan_perlu_dimasak' : pesanan_perlu_dimasak,
        'pesanan_belum_terkonfirmasi' : pesanan_belum_terkonfirmasi,
        'pesanan_belum_dibayar' : pesanan_belum_dibayar
    }

    if request.method == "POST":
        if 'status' in request.POST:
            nama_meja = request.POST['nama_meja']
            obj = get_object_or_404(Meja, nama_meja=nama_meja)
            obj.status = 'Terisi'
            obj.save()
            return redirect('pesan')

    return render(request, 'home.html', context)
