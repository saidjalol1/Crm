from django.http import Http404, HttpResponse
from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.views import View
from .models import Orders, OrderItems, Deliver, Expenses, Staffs
from products.models import Storage
from products.models import Product
from .forms import DriverForm, StaffsForm






class OrdersView(View):
    template_name = 'products/ecom-product-order.html'


    def get_context_data(self, *args, **kwargs):
        kwargs['orders'] = Orders.objects.all()
        kwargs['driver_add_form'] = DriverForm()
        kwargs['delivers'] = Deliver.objects.all()
        return kwargs
    

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        if 'filter' in request.GET:
            print('ishlayapti')
            date = request.GET.get('by_date')
            status = request.GET.get('by_status')
            if date and status:
                context['orders'] = Orders.objects.filter(date_added__date=date, status=status)
            elif date and not status:
                context['orders'] = Orders.objects.filter(date_added__date=date)
            elif status and not date:
                context['orders'] = Orders.objects.filter(status=status)
            else:
                context['orders'] = Orders.objects.all()
            return render(request, self.template_name, context)
        return render(request, self.template_name,context)
    

    def post(self, request, *args, **kwargs):
        context = {}
        if 'ready' in request.POST:
            order = Orders.objects.get(id=request.POST.get('order'))
            order.status = request.POST.get('ready')
            order.save()
        if 'send' in request.POST:
            order = Orders.objects.get(id=request.POST.get('order'))
            order.status = request.POST.get('send')
            order_items = order.order_items.all()
            order.received_admin = request.user
            order.deliver_id = request.POST.get('driver_select')
            # print(order_items)
            for i in order_items:
                products = Product.objects.get(id=i.products.id)
                if products.amount < i.quantity:
                    return HttpResponse(f"<h1>Mahsulot {products.name} omborda yetarli emas</h1>")
                else:
                    products.amount -= i.quantity
                    products.save()
                    print(products.amount)
                    print(i.products)
                    print(i)
            order.save()
        if 'is_being' in request.POST:
            order = Orders.objects.get(id=request.POST.get('order'))
            order.status = request.POST.get('is_being')
            order.save()
        if 'received' in request.POST:
            order = Orders.objects.get(id=request.POST.get('order'))
            order.status = request.POST.get('received')
            order.save()
        if 'cancel' in request.POST:
            order = Orders.objects.get(id=request.POST.get('order'))
            order.status = request.POST.get('cancel')
            order.save()
        if 'delete' in request.POST:
            order_instance = Orders.objects.get(pk=request.POST.get('order'))
            order_instance.delete()
        if 'driver' in request.POST:
            form = DriverForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                return render(request,self.template_name, self.get_context_data(**context))
        return render(request, self.template_name, self.get_context_data(**context))



class OrdersStatusView(View):
    template_name = 'products/orders_status.html'

    def get_context_data(self,*args,**kwargs):
        kwargs['orders'] = Orders.objects.all()
        return kwargs

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        if 'filter' in request.GET:
            print('ishlayapti')
            date = request.GET.get('by_date')
            status = request.GET.get('by_status')
            if date and status:
                context['orders'] = Orders.objects.filter(date_added__date=date, status=status)
            elif date and not status:
                context['orders'] = Orders.objects.filter(date_added__date=date)
            elif status and not date:
                context['orders'] = Orders.objects.filter(status=status)
            else:
                context['orders'] = Orders.objects.all()
            return render(request, self.template_name, context)
        return render(request, self.template_name, context)
    

    def post(self,request,*args,**kwargs):
        context = {}
        return render(request,self.template_name, self.get_context_data(**context))
    

class OrderDetail(View):
    template_name = 'order_detail.html'

    def get_object(self):
        try:
            object = Orders.objects.get(pk=self.kwargs['pk'])
        except Orders.DoesNotExist:
            raise Http404('Order not found!')
        return object


    def get_context_data(self, **kwargs):
        kwargs['object'] = self.get_object()
        return kwargs
    
    def get(self,request,*args,**kwargs):
        return render(request, self.template_name,self.get_context_data())


    def post(self,request,*args,**kwargs):
        ctxt = {}
        if 'delete' in request.POST:
            print(request.POST.get('product_delete'))
            product_id = request.POST.get('product_delete')
            order_instance = Orders.objects.get(pk=self.get_object().id)
            item = order_instance.order_items.get(id=product_id)
            item.delete()
        return render(request, self.template_name, self.get_context_data(**ctxt))


class StorageView(View):
    template_name = 'ombor.html'


    def get_context_data(self,**kwargs):
        kwargs['products'] = Storage.objects.get(id=1)
        print(kwargs['products'].overall_products_number())
        return kwargs
    

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,self.get_context_data())


    def post(self, request,*args,**kwargs):
        ctxt = {}
        return render(request, self.template_name, self.get_context_data(**ctxt))


class StaffsView(View):
    template_name = 'staffs.html'

    def get_context_data(self,*args,**kwargs):
        kwargs['objects'] = Staffs.objects.all()
        kwargs['add_staff'] = StaffsForm()
        return kwargs
    
    def get(self, request,*args,**kwargs):
        context = self.get_context_data()
        return render(request,self.template_name, context)
    
    def post(self,request,*args,**kwargs):
        context = {}
        if 'add_staff' in request.POST:
            form = StaffsForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                return redirect('/')
        return render(request, self.template_name, self.get_context_data(**context))
    

class ExpensesView(View):
    template_name = 'expenses.html'

    def get_context_data(self,*args,**kwargs):
        kwargs['objects'] = Expenses.objects.all()
        return kwargs
    
    def get(self, request,*args,**kwargs):
        context = self.get_context_data()
        if 'filter' in request.GET:
            date = request.GET.get('by_date')
            status = request.GET.get('by_status')
            if date and status:
                context['objects'] = Expenses.objects.filter(date_added__date=date, name__icontains=status)
            elif date and not status:
                context['objects'] = Expenses.objects.filter(date_added__date=date)
            elif status and not date:
                context['objects'] = Expenses.objects.filter(name__icontains=status)
            else:
                context['objects'] = Expenses.objects.all()
            return render(request, self.template_name, context)
        return render(request,self.template_name, context)
    
    def post(self,request,*args,**kwargs):
        context = {}
        return render(request, self.template_name, self.get_context_data(**context))
    

