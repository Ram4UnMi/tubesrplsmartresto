from django.shortcuts import render, redirect
from.models import MenuItem, Cart, Order, OrderItem
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from meja.models import Meja



def isPelayan(request):
     if request.user.groups.filter(name='pelayan').exists():
        return True
def isKoki(request):
     if request.user.groups.filter(name='koki').exists():
        return True
def isKasir(request):
     if request.user.groups.filter(name='kasir').exists():
        return True
def isOwner(request):
     if request.user.groups.filter(name='owner').exists():
        return True
     

# Create your views here.
@login_required(login_url='/login')
def index(request) :
    list_menu = MenuItem.objects.all()
    cart_items_count = Cart.objects.filter(user = request.user).count()
    context = {
        'list_menu' : list_menu,
        'cart_items_count' : cart_items_count
    }
    if request.method == 'POST':
        user = request.POST['user']
        item_id = int(request.POST['id'])  # Assuming 'id' is the key in the POST data
        menu_item = MenuItem.objects.get(pk=item_id)  # Retrieve the MenuItem object

        item = menu_item.name
        price = menu_item.price
        quantity = int(request.POST['quantity'])
        sub_total = price * quantity
        try:
            existing_item = Cart.objects.get(user=user, items=item)
            existing_item.quantity += quantity  
            existing_item.sub_total = existing_item.price * existing_item.quantity  
            existing_item.save()
            return redirect('pesan')
        except Cart.DoesNotExist:
            new_item = Cart(user=user, items=item, price=price, quantity=quantity,sub_total=sub_total)
            new_item.save()
            return redirect('pesan')
    return render(request, 'order/index.html', context)

@login_required(login_url='/login')
def cart(request) :
    cart_items = Cart.objects.filter(user = request.user)
    cart_items_count = Cart.objects.filter(user = request.user).count()
    total = 0
    for item in cart_items :
        total += item.sub_total
    context = {
        'total' : total,
        'cart_items' : cart_items,
        'cart_items_count' : cart_items_count
    }
    if 'items' in request.POST :
        item_name = request.POST['items']
        cart_item = Cart.objects.get(items=item_name, user=request.user)
        cart_item.delete()
        return redirect('cart')
    
    if request.method == 'POST' :
        cart_items = Cart.objects.filter(user=request.user)
        order_items = []

        for cart_item in cart_items:
            product_name = cart_item.items
            quantity = cart_item.quantity
            item_details = {'nama_barang': product_name, 'quantity': quantity}
            order_items.append(item_details)

        order_item = OrderItem.objects.create(user=request.user, order_details=order_items, order_status='Menunggu Konfirmasi')
        order_item = Order.objects.create(user=request.user, total=total, status='Belum Dibayar')
        Cart.objects.filter(user=request.user).delete()
        return redirect('home')       
    return render(request,'order/cart.html', context)

@login_required(login_url='/login')
def konfirmasiPesanan(request) :
    if isPelayan(request) :
        order_items = OrderItem.objects.filter(order_status='Menunggu Konfirmasi')
        context = {
            'order_items': order_items
            }
        if request.method == 'POST' :
            id = request.POST['id']
            obj = get_object_or_404(OrderItem, pk=id)
            if 'konfirmasi' in request.POST :
                obj.order_status = 'Sedang Dimasak'
                obj.save()
                return redirect('konfirmasi')
            elif 'batal' in request.POST :
                obj.order_status = 'Dibatalkan'
                obj.save()
                return redirect('konfirmasi')

        return render(request, 'order/konfirmasi_pesanan.html', context)
    else :
        return redirect('home')

@login_required(login_url='/login')
def pesananDimasak(request) :
    if isKoki(request) :
        order_items = OrderItem.objects.filter(order_status='Sedang Dimasak')
        context = {
            'order_items': order_items
            }
        if request.method == "POST" :
            id = request.POST['id']
            obj = get_object_or_404(OrderItem, pk=id)
            obj.order_status = 'Selesai Dimasak'
            obj.save()
            return redirect('dimasak')

        return render(request, 'order/pesanan_dimasak.html', context)
    else :
        return redirect('home')


@login_required(login_url='/login')
def pesananDisajikan(request) :
    if isPelayan(request) :
        order_items = OrderItem.objects.filter(order_status='Selesai Dimasak')
        context = {
            'order_items': order_items
            }
        if request.method == "POST" :
            id = request.POST['id']
            meja = request.POST['meja']
            obj = get_object_or_404(OrderItem, pk=id)
            obj.order_status = 'Selesai'
            obj.save()

            obj1 = get_object_or_404(Meja, nama_meja=meja)
            obj1.status = 'Kosong'
            obj1.save()
            return redirect('disajikan')

        return render(request, 'order/pesanan_dikirim.html', context)
    else :
        return redirect('home')

@login_required(login_url='/login')
def konfirmasiPembayaran(request) :
    if isKasir(request) :
        list_pembayaran = Order.objects.filter(status='Belum Dibayar')
        context = {
            'list_pembayaran' : list_pembayaran
        }

        if request.method == 'POST':
            id = request.POST['id']
            meja = request.POST['user']
            obj = get_object_or_404(Order, pk=id)
            obj.status = 'Dibayar'
            obj.save()
            obj2 = get_object_or_404(Meja, nama_meja=meja)
            obj2.status = 'Kosong'
            obj2.save()
            return redirect('pembayaran')
        return render(request, 'order/konfirmasi_pembayaran.html', context)
    else :
        return redirect('home')

@login_required(login_url='/login')
def kelolaMenu(request) :
    if isOwner(request) :
        list_menu = MenuItem.objects.all()
        context = {
            'list_menu':list_menu
        }
        if request.method == 'POST' :
            if 'update' in request.POST :
                item_id = request.POST['id']
                price = request.POST['price']
                obj = get_object_or_404(MenuItem, id=item_id)
                if request.POST['type']=='Update':
                    obj.price = price
                    obj.save()
                    return redirect('menu')
                elif request.POST['type'] == "Delete":
                    item = MenuItem.objects.get(id=item_id)
                    item.delete()
                    return redirect('menu')
            elif 'tambah' in request.POST  :
                print(request.POST)
                new_name = request.POST['name']
                new_price = request.POST['price']

                new_item = MenuItem(name = new_name, price=new_price)
                new_item.save()
                return redirect('menu')
        
        return render(request,'order/kelola_menu.html', context)
    else :
        return redirect('home')