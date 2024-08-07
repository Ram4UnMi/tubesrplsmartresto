from django.urls import path, include
from . import views


urlpatterns = [
    path('',views.index, name='pesan'),
    path('cart/',views.cart, name='cart'),
    path('konfirmasi-pesanan', views.konfirmasiPesanan, name='konfirmasi'),
    path('pesanan-dimasak', views.pesananDimasak, name='dimasak'),
    path('pesanan-disajikan', views.pesananDisajikan, name='disajikan'),
    path('konfirmasi-pembayaran', views.konfirmasiPembayaran, name='pembayaran'),
    path('kelola-menu', views.kelolaMenu, name='menu'),

]