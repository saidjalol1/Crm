import datetime
from datetime import datetime
from datetime import timedelta
from django.shortcuts import render, redirect
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth
from django.views import View
from django.shortcuts import render
from products.models import Product
from main.models import OrderItems, Orders, Expenses
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.db.models import Count
from .forms import ExpensesForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Max
from django.db.models import Subquery, OuterRef
current_month = datetime.now()


class StatisticsView(View):
    template_name = 'index.html'


    def get_context_data(self,*args,**kwargs):
        try:
            data = Orders.objects.filter(status="Jo'natildi").annotate(
                 month=TruncMonth('date_added')
                        ).values('month').annotate(
                                    total_quantity=Sum(F('order_items__products__price') * F('order_items__quantity')),
                                        order_count=Count('id')
                                                ).order_by('month')
            data_list = [
            {'month': entry['month'].strftime('%Y-%m-%d'), 'total_quantity': entry['total_quantity']}
            for entry in data
            ]
        except Orders.DoesNotExist:
            data = "Ma'lumot mavjud emas"
        try:
            expenses = Expenses.objects.annotate(
                                month=TruncMonth('date_added')
                                            ).values('month').annotate(
                                                    total_amount=Sum('amount')
                                                            ).order_by('month')
            expenses_list = [
                {'month': entry['month'].strftime('%Y-%m-%d'), 'total_amount': entry['total_amount']}
                for entry in expenses
            ]
        except Expenses.DoesNotExist:
            expenses = "Ma'lumot mavjud emas"
        try:
            per_worker = Orders.objects.filter(status="Jo'natildi").annotate(
                 month=TruncMonth('date_added')
                        ).values('month', 'received_admin').annotate(
                                    total_quantity=Sum(F('order_items__products__price') * F('order_items__quantity')),
                                        order_count=Count('id')
                                                ).order_by('month')
            per_worker_list = [
            {'month': entry['month'].strftime('%Y-%m-%d'), 'seller': entry['received_admin'], 'total_quantity': entry['total_quantity']}
            for entry in per_worker
            ]
        except Orders.DoesNotExist:
            per_worker = "Ma'lumot mavjud emas"
        try:
            most_sold_products_current_month = Orders.objects.filter(
                                         
                status="Jo'natildi",
                date_added__month=current_month.month,
                date_added__year=current_month.year
                ).annotate(
                month=TruncMonth('date_added'),
                        product_quantity=Sum('order_items__quantity')
                            ).values('order_items__products__name').order_by('-product_quantity').first()
            
        except Orders.DoesNotExist:
            print("error")

        try:
            most_sold_admin_current_month = Orders.objects.filter(
                                            status="Jo'natildi",
                                            date_added__month=current_month.month,
                                            date_added__year=current_month.year
                                            ).values('received_admin').annotate(
                                            total_quantity=Sum(F('order_items__products__price') * F('order_items__quantity')),
                                            order_count=Count('id')
                                            ).order_by('-total_quantity').first()
        except Orders.DoesNotExist:
            most_sold_admin_current_month = "Ma'lumot mavjud emas"

        try:
            card_sale = Orders.objects.filter(
                                            status="Jo'natildi",
                                            payment_type='plastik',
                                            date_added__month=current_month.month,
                                            date_added__year=current_month.year
                                            ).values('received_admin').annotate(
                                            total_quantity=Sum(F('order_items__products__price') * F('order_items__quantity')),
                                            order_count=Count('id')
                                            ).order_by('-total_quantity').first()
        except Orders.DoesNotExist:
            print("error")

        try:
            money_sale = Orders.objects.filter(
                                            status="Jo'natildi",
                                            payment_type='naxt',
                                            date_added__month=current_month.month,
                                            date_added__year=current_month.year
                                            ).values('received_admin').annotate(
                                            total_quantity=Sum(F('order_items__products__price') * F('order_items__quantity')),
                                            order_count=Count('id')
                                            ).order_by('-total_quantity').first()
        except Orders.DoesNotExist:
            money_sale = "Ma'lumot mavjud emas"
        # print(calculate_profits)
        # print(most_sold_products_current_month)
        # most_sold = sum([i.quantity for i in OrderItems.objects.filter(product__name = most_sold_products_current_month.order_items__products__name)])
        # print(most_sold)
        print
        data_json = json.dumps(data_list, cls=DjangoJSONEncoder)
        expenses_json = json.dumps(expenses_list, cls=DjangoJSONEncoder)
        per_worker_lists_json = json.dumps(per_worker_list, cls=DjangoJSONEncoder)
        kwargs['data'] = data_json
        kwargs['expenses'] = expenses_json
        kwargs['workers'] = per_worker_lists_json
        kwargs['expensesForm'] = ExpensesForm()
        kwargs['sellerForm'] = UserCreationForm()
        kwargs['users'] = User.objects.filter()
        kwargs['current_month_sale'] = sum(i.get_overall() for i in Orders.objects.filter(date_added__month=current_month.month))
        kwargs['current_month_expense'] = sum(i.amount for i in Expenses.objects.filter(date_added__month=current_month.month))
        kwargs['most_sold_current_month'] = most_sold_products_current_month
        if most_sold_admin_current_month:
            kwargs['admin_best'] =  User.objects.get(id=most_sold_admin_current_month['received_admin'])
        else:
            kwargs['admin_best'] = "Ma'lumot mavjud emas"
        kwargs['card_sale'] = card_sale
        kwargs['money_sale'] = money_sale
        # kwargs['profit_calculations'] = int(sum(i.get_overall_net_profit_orders() for i in calculate_profits ))
        # kwargs['body_price'] = int(sum(i.get_overall_net_profit_orders() for i in calculate_profits ))
        # print(kwargs['profit_calculations'])
        # print(kwargs['most_sold'])
        # print(current_month.month)

        return kwargs


    def get(self,request,*args,**kwargs):
        return render(request,self.template_name, self.get_context_data())
    

    def post(self,request,*args,**kwargs):
        ctxt = {}
        if 'add_expense' in request.POST:
            form = ExpensesForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                print(form.errors)
                return render('/')
        if 'add_seller' in request.POST:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                seller =  form.save(commit=False)
                print(seller)
                seller.is_staff = True
                print(dir(seller))
                seller.save()
            else:
                return redirect('/')
        return render(request,self.template_name,self.get_context_data(**ctxt))