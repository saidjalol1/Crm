from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from .models import Product, ProductCategory, ProductTag
from django.http import HttpResponse
from main.models import Orders, CartItems, OrderItems, WishList, Packages, PackageItems
from django.views import View
from .forms import ProductAddForm
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









class ProductsList(FormView,ListView):
    model = Product
    form_class = ProductAddForm
    template_name = 'products/ecom-product-grid.html'
    paginate_by = 8
    success_url = reverse_lazy('/')

   
    def get_queryset(self):
        queryset = super().get_queryset()
        if 'billur_products' in self.request.GET:
            queryset = queryset.filter(category__name='Billur').select_related('category')
        elif 'extra_products' in self.request.GET:
            queryset = queryset.filter(category__name='Boshqalar').select_related('category')
        elif 'search' in self.request.GET:
            queryset = queryset.filter(name__icontains=self.request.GET.get('product')).select_related('category')
        return queryset



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wishlist = WishList.objects.get_or_create(session_key=self.request.session.session_key)
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
        # print(user)
        context.update({
            'wishlist_products':wishlist,
            'login_form': AuthenticationForm(),
            'product_form': ProductAddForm(),
            'user': user,
            'title':title,
            'naborlar':Packages.objects.all()
        })  
        return context
    

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        if 'new_product_add' in request.POST:
            form = ProductAddForm(request.POST,request.FILES)
            if form.is_valid():
                try:
                    product = Product.objects.get(name=form.cleaned_data['name'])
                    product.name = form.cleaned_data['name']
                    product.amount = form.cleaned_data['amount']
                    product.discount = form.cleaned_data['discount']
                    product.price = form.cleaned_data['price']
                    product.image = form.cleaned_data['image']
                    product.description = form.cleaned_data['description']
                    product.category = form.cleaned_data['category']
                    product.save()
                except Product.DoesNotExist:
                    form.save()
            else:
                print(form.errors)
                print('form is not valid -----------------')
            # return self.form_invalid(form)
        if 'login' in request.POST:
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                user = authenticate(
                    username=login_form.cleaned_data['username'],
                    password=login_form.cleaned_data['password'],
                )
                if user is not None:
                    login(request, user)
                    print('logged in')
                    return redirect('products:product_list')
                else:
                    print('wrong')
                    return redirect('products:product_list')
        if 'add_to_package' in request.POST:
            product = Product.objects.get(id=request.POST.get('product'))
            quantity = request.POST.get('quantity')
            package = Packages.objects.get(id=request.POST.get('package'))
            package_item = PackageItems.objects.create(
                product = product,
                quantity = quantity,
                package = package
            )
        return render(request, self.template_name, self.get_context_data())

    
class ProductDetail(DetailView):
    model = Product
    template_name = 'products/ecom-product-detail.html'


def add_to_cart(request, product_id):
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
                return HttpResponse('<h1>Omborda Mahsulot yetrali emas</h1>')

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
        else:
            cart_item = CartItems.objects.create(
                product_id=product_id,
                session_key=session_key,
            )
            cart_item.quantity += 1
            cart_item.save()
    return redirect(referring_url)


class CardView(View):
    template_name ='card_page.html'

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
            return redirect("/cart_page/")
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


class CustomerOrdersView(View):
    template_name = 'customers/customer_orders.html'


    def get_context_data(self, *args, **kwargs):
        return kwargs
    

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        session_key = request.session.session_key
        context['orders'] = Orders.objects.filter(session_key=session_key)
        return render(request, self.template_name, context)
    

    def post(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, self.get_context_data(**context))


class CustomerOrderDetail(DetailView):
    model = Orders
    template_name = 'order_detail.html'


class WishListView(View):
    template_name = 'wishlist.html'
    

    def get_context_data(self, **kwargs):
        session_key = self.request.session.session_key
        print(self.request.session.session_key)
        wishlist = WishList.objects.get(session_key=session_key)
        products = wishlist.products.all()
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
        if 'add_to_card' in request.POST:
            request = request
            product_id = request.POST.get('product')
            print(product_id)
            add_to_cart(request,product_id)
        elif 'delete' in request.POST:
            wishlist = WishList.objects.get(session_key=request.session.session_key)
            product_id = request.POST.get('product_delete')
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

    wishlist =  WishList.objects.get(
        session_key=session_key,
        )
    wishlist.products.set(wishlist.products.all())


    if product in wishlist.products.all():
        wishlist.products.remove(product)
        is_added = False
    else:
        wishlist.products.add(product)
        is_added = True

    return JsonResponse({'is_added': is_added})

