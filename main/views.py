from django.http import Http404, HttpResponse,FileResponse
from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.views import View
from .models import Orders, OrderItems, Deliver, Expenses, Staffs, PackageItems, Packages
from products.models import Storage
from products.models import Product
from .forms import DriverForm, StaffsForm, PackagesForm

import io
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from django.http import FileResponse
from reportlab.lib.units import inch


import io
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from django.http import FileResponse
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet

import io
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from django.http import FileResponse
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from django.contrib import messages
def generate_pdf_for_orders(order):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter, bottomup=0)
    elements = []

   
    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]

    text_lines = [
        f"<b>Zakaz qilingan sana:</b> {order.date_added}",
        f"<b>Zakaz qilgan shaxs:</b> {order.customer_full_name}",
        f"<b>Mijozning Raqami:</b> {order.phone_number}",
        f"<b>Manzil:</b> {order.address}",
        f"<b>Mo'ljal:</b> {order.target}",
        f"<b>Sotuvchi:</b> {order.received_admin}",
        f"<b>Yetkazib beruvchi:</b> {order.deliver}",
        f"",
        f"",
    ]


    for line in text_lines:
        line_paragraph = Paragraph(line, style_normal)
        line_paragraph.alignment = 0 
        elements.append(line_paragraph)
      
    page_width, _ = letter

    table_data = [
        ["Mahsulot", "Narxi", "Soni","Umumiy qiymati"],
    ]

    for item in order.order_items.all():
        table_data.append([item.products.name, item.products.price, item.quantity,item.get_overall()])

      
    column_widths = [page_width / len(table_data[0])] * len(table_data[0])

    table = Table(table_data, colWidths=column_widths)

      
    style_table = TableStyle([
        ('LEFTPADDING', (0, 0), (10, 10), inch),
        ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    table.setStyle(style_table)

        
    elements.append(table)

    
    doc.build(elements)

    buf.seek(0)
    return buf




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
                context['orders'] =Orders.objects.all()
        return render(request, self.template_name,context)
    

    def post(self, request, *args, **kwargs):
        context = {}
        if 'received' in request.POST:
            order = Orders.objects.get(id=request.POST.get('order'))
            for i in order.order_items.all():
                if i.products.amount < i.quantity:
                    messages.warning(request, f"Omborda { i.products.name } yetarli emas")
                else:
                    order.status = request.POST.get('received')
                    order.received_admin = request.user
                    order.deliver_id = request.POST.get('driver_select')
            # print(order_items)
            for i in order.order_items.all():
                products = Product.objects.get(id=i.products.id)
                if products.amount < i.quantity:
                    messages.warning(request, f'Mahsulot {products.name} omborda yetarli emas')
                else:
                    products.amount -= i.quantity
                    products.sold_amount += i.quantity
                    products.save()
                    print(products.amount)
                    print(i.products)
                    print(i)
                    order.save()
        if 'send' in request.POST:
            print("Id--------",request.POST.get('order'))
            order = Orders.objects.get(id=request.POST.get('order'))
            deliver_obj = Deliver.objects.get(id=request.POST.get('driver_select'))
            order.deliver = deliver_obj
            order.status = request.POST.get('send')
            order.save()
        if 'payment_type_add' in request.POST:
            order = Orders.objects.get(id=request.POST.get('order'))
            order.payment_type = request.POST.get('payment_type')
            order.save()
        if 'cancel' in request.POST:
            order = Orders.objects.get(id=request.POST.get('order'))
            order.status = request.POST.get('cancel')
            order.save()
        if 'add_direction' in request.POST:
            order = Orders.objects.get(id=request.POST.get('order'))
            order.direction = request.POST.get('direction')
            order.save()
        if 'driver' in request.POST:
            form = DriverForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                return render(request,self.template_name, self.get_context_data(**context))
        if 'print' in request.POST:
            try:
                order = Orders.objects.get(id=request.POST.get('print'))
            except Orders.DoesNotExist:
                raise Http404("Order does not exist")
            pdf_buffer = generate_pdf_for_orders(order)
            return FileResponse(pdf_buffer, as_attachment=True, filename='orders_report.pdf')
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
    

class PackageView(View):
    template_name = "naborlar.html"


    def get_context_data(self,*args,**kwargs):
        kwargs['nabor'] = Packages.objects.all()
        kwargs['form'] = PackagesForm()
        return kwargs
    
    def get(self, request,*args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request,*args,**kwargs):
        context = {}
        if 'package_add' in request.POST:
            form = PackagesForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                form = PackagesForm()
        return render(request, self.template_name, self.get_context_data(**context))


class PackageDetailView(View):
    template_name = 'nabor_detail.html'

    def get_object(self):
        try:
            object = Packages.objects.get(pk=self.kwargs['pk'])
            print(object.get_overall_price())
        except Packages.DoesNotExist:
            raise Http404('Package not found!')
        return object


    def get_context_data(self, **kwargs):
        kwargs['object'] = self.get_object()
        return kwargs
    
    def get(self,request,*args,**kwargs):
        return render(request, self.template_name,self.get_context_data())


    def post(self,request,*args,**kwargs):
        ctxt = {}
        if 'add_quantity' in request.POST:
            item = PackageItems.objects.get(id=request.POST.get('product'))
            product = Product.objects.get(id=item.product.id)
            quantity = request.POST.get('quantity')
            if product.amount < int(quantity):
                messages.warning(request, 'Kechirasiz mahsulot yetarli emas!! Boshqa Mahsulotlarni ham qarap ko\'ring')
            else:
                item.quantity = int(quantity)
                item.save()
        elif 'delete' in request.POST:
            item = PackageItems.objects.get(id=request.POST.get('product_delete'))
            item.delete()
        elif 'order' in request.POST:
            session_key = request.session.session_key
            package_items = PackageItems.objects.filter(package=self.get_object())
            order_instance = Orders.objects.create(
                customer_full_name=request.POST.get('customer_full_name'),
                address=request.POST.get('address'),
                target=request.POST.get('target'),
                phone_number=request.POST.get('phone_number'),
                session_key=session_key,
                )
            for i in range(len(package_items)):
                print(package_items[i].product)
                order_items = OrderItems.objects.create(
                    quantity = package_items[i].quantity,
                    sessionkey = session_key,
                    order = order_instance,
                    products = package_items[i].product
                    )
                # order_instance.items.set(cart_items)
        return render(request, self.template_name, self.get_context_data(**ctxt))