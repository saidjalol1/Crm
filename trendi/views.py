from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from products.models import Product, ProductCategory, ProductTag
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
# class TrendiView(TemplateView):
#     template_name = "trendi.html"

class TrendiView(ListView):
    model = Product
    template_name = "trendi.html"
    paginate_by = 6
    success_url = reverse_lazy('/')

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'billur_products' in self.request.GET:
            queryset = queryset.filter(category__name='Billur')
        elif 'extra_products' in self.request.GET:
            queryset = queryset.filter(category__name='Boshqalar')
        elif 'search' in self.request.GET:
            queryset = queryset.filter(name__icontains=self.request.GET.get('product'))
        return queryset

    def get_context_data(self, **kwargs):
        wishlist = WishList.objects.get_or_create(session_key=self.request.session.session_key),
        title = None
        if 'billur_products' in self.request.path:
            title = 'Billur tovarlar'
        elif 'extra-products' in self.request.path:
            title = "Boshqalar"
        else:
            title = " "
        print(title)
        try:
            user = User.objects.get(id=self.request.user.id)
        except User.DoesNotExist:
            user = None
        context = super().get_context_data(**kwargs)
        context.update({
            'title': title,
            'wishlist_products':wishlist,
            'user': user,
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
        session_key = request.session.session_key
        try:
            cart_items = CartItems.objects.filter(session_key=session_key)
        except CartItems.DoesNotExist:
            return HttpResponse('<h1>Savatcha Mahsuotlari topilmadi!!! oldin Savatchaga mahsulot qo\'shing</h1>')
        kwargs['cart_items'] = cart_items
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
            cart_items = CartItems.objects.filter(session_key=session_key)
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
                # order_instance.items.set(cart_items)
            else: 
                messages.warning(request, 'Umumiy qiymat 100.000 so\'mni tashkil etganda buyurtma berish mumkin!!!')           
        return render(request, self.template_name, self.get_context_data(request,**ctxt))