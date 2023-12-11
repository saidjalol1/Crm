from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from products.models import Product, ProductCategory, ProductTag, Aksiyalar_qoshish
from django.http import HttpResponse
from main.models import Orders, CartItems, OrderItems, WishList, Packages, PackageItems
from django.views import View
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login , authenticate
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from products.views import add_to_cart
from django.db.models import Prefetch
from django.contrib import messages
# class TrendiView(TemplateView):
#     template_name = "trendi.html"

class TrendiView(ListView):
    model = Product
    template_name = "trendi.html"
    paginate_by = 6
    success_url = reverse_lazy('/')

    def get_queryset(self):
        queryset = super().get_queryset().select_related('category')
        if 'billur_products' in self.request.GET:
            queryset = queryset.filter(category__name='Billur')
        elif 'extra_products' in self.request.GET:
            queryset = queryset.filter(category__name='Boshqalar')
        elif 'filter' in self.request.GET:
            filter_object = self.request.GET.get("object")
            filter_by = self.request.GET.get("filter_by")
            if filter_by == "Eng ko'p sotilgan tovarlar":
                queryset = queryset.order_by("-sold_amount")
            else:
                queryset = queryset.filter(tag__id=int(filter_by))
        return queryset

    def get_context_data(self,**kwargs):
        session_key = self.request.session.session_key
        wishlist = WishList.objects.get_or_create(session_key=session_key)
        if 'billur_products' in self.request.GET:
            title = 'Billur tovarlar'
        elif 'extra_products' in self.request.GET:
            title = "Boshqalar"
        else:
            title = " "
        print(title)
        try:
            cart_items = CartItems.objects.filter(session_key=session_key).select_related('product__category')
        except CartItems.DoesNotExist:
            return HttpResponse('<h1>Savatcha Mahsuotlari topilmadi!!! oldin Savatchaga mahsulot qo\'shing</h1>')
        try:
            user = User.objects.get(id=self.request.user.id)
        except User.DoesNotExist:
            user = None
        context = super().get_context_data(**kwargs)
        context.update({
            'user': user,
            'cart_items_number':len(cart_items),
            'title':title,
            'wishlist':wishlist,
            "tags": ProductTag.objects.all().prefetch_related("products"),
            'aksiya': Aksiyalar_qoshish.objects.last()
        })
        return context
    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        if request.is_ajax() and 'product_id' in request.POST:
            product_id = request.POST['product_id']
            product = get_object_or_404(Product, id=product_id)
            wishlist, created = WishList.objects.get_or_create(session_key=request.session.session_key)
            wishlist.add_product(product)
            return JsonResponse({'success': True})
        return render(request, self.template_name, self.get_context_data())


class CardView(View):
    template_name ='products/client-cart.html'
    def get_context_data(self, request,**kwargs):
        referring_url = request.META.get('HTTP_REFERER')
        session_key = request.session.session_key
        
        try:
            cart_items = CartItems.objects.filter(session_key=session_key).select_related('product__category')
        except CartItems.DoesNotExist:
            messages.warning(request,"Mahsulot topilmadi...")
            return redirect(referring_url)
        kwargs['cart_items'] = cart_items
        kwargs['cart_items_number'] = len(cart_items)
        kwargs['cart_sum'] = sum([i.overall_price() for i in cart_items])
        return kwargs

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(request))


    def post(self, request, *args, **kwargs):
        ctxt = {}

        if 'add_quantity' in request.POST:
            product = CartItems.objects.get(session_key=request.session.session_key,product_id=request.POST.get('product'))
            quantity = request.POST.get('quantity')
            products = Product.objects.get(id=product.product.id)
            if products.amount < int(quantity):
                messages.warning(request, 'Kechirasiz mahsulot yetarli emas!! Boshqa Mahsulotlarni ham qarap ko\'ring')
            else:
                product.quantity = int(quantity)
                product.save()

        elif 'delete' in request.POST:
            product = CartItems.objects.get(session_key=request.session.session_key,product_id=request.POST.get('product_delete'))
            product.delete()
        elif 'order' in request.POST:
            session_key = request.session.session_key
            cart_items = CartItems.objects.filter(session_key=session_key).select_related('product')
            order_amount = sum([i.overall_price() for i in cart_items])
            # print(cart_items)
            if order_amount > 100000:
                order_instance = Orders.objects.create(
                customer_full_name=request.POST.get('customer_full_name'),
                address=request.POST.get('address'),
                target=request.POST.get('target'),
                phone_number=request.POST.get('phone_number'),
                session_key=session_key,
                )
                print(cart_items)
                for i in cart_items:
                    print(i.product)
                    order_items = OrderItems.objects.create(
                        quantity = i.quantity,
                        sessionkey = session_key,
                        order = order_instance,
                        products = i.product
                        )
                    # print()
                cart_items.delete()
                messages.warning(request,"Buyurtmangiz qabul qilindi")
            else: 
                messages.warning(request, 'Umumiy qiymat 100.000 so\'mni tashkil etganda buyurtma berish mumkin!!!')           
        return render(request, self.template_name, self.get_context_data(request,**ctxt))


class WishListView(View):
    template_name = 'trendi-wishlist.html'
    

    def get_context_data(self, **kwargs):
        session_key = self.request.session.session_key
        print(self.request.session.session_key)
        wishlist = WishList.objects.get(session_key=session_key)
        products = wishlist.products.select_related('category').all()
        status = False
        if products:
            status = True
        else:
            pass
        kwargs['wishlist'] = wishlist
        kwargs['wishlist_status'] = status
        return kwargs


    def get(self,reqeust, *args, **kwargs):
        return render(reqeust, self.template_name, self.get_context_data())
    

    def post(self,request, *args, **kwargs):
        ctxt = {}
        if 'add_to_cart' in request.POST:
            request = request
            product_id = request.POST.get('product')
            print(product_id)
            add_to_cart(request,product_id)
        elif 'delete' in request.POST:
            wishlist = WishList.objects.get(session_key=request.session.session_key)
            product_id = request.POST.get('product')
            print(product_id)
            product = get_object_or_404(Product, id=product_id)
            wishlist.products.remove(product)
        return render(request, self.template_name, self.get_context_data(**ctxt))

@require_POST
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    session_key = request.session.session_key

    if not session_key:
        request.session.save()
        session_key = request.session.session_key

    wishlist, created = WishList.objects.get_or_create(session_key=session_key)
    
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        is_added = False
    else:
        wishlist.products.add(product)
        is_added = True

    return JsonResponse({'is_added': is_added})


def add_to_card(request, product_id):
    referring_url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=product_id)
    session_key = request.session.session_key
    if 'quantity' in request.POST:
        quantity = request.POST.get('quantity')
    

    if not session_key:
        request.session.save()
        session_key = request.session.session_key

    
    try:
        cart_item = CartItems.objects.get(session_key=session_key, product_id=product.id)
        quantity = request.POST.get('quantity')
        if quantity != None:
            if product.amount == 0 or product.amount < int(quantity):
               messages.warning(request, f"Mahsulot omborda yetarli emas!!!")
               
            messages.warning(request, f"Mahsulot omborga qo'shildi!!!")
            cart_item.quantity += int(quantity)
            cart_item.save()
            
    except CartItems.DoesNotExist:
        quantity = request.POST.get('quantity')
        if quantity:
            quantity = int(quantity)
            CartItems.objects.create(
                product_id=product_id,
                session_key=session_key,
            )
            cart_item = CartItems.objects.get(session_key=session_key, product_id = product_id)
            cart_item.quantity += quantity
            cart_item.save()
            messages.warning(request, f"Mahsulot  omborga qo'shildi")
        else:
            cart_item = CartItems.objects.create(
                product_id=product_id,
                session_key=session_key,
            )
            cart_item.quantity += 1
            cart_item.save()
            messages.warning(request, f"Mahsulot  omborga qo'shildi")
    return redirect(referring_url)
