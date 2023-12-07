from django.db import models
from products.models import Product
from django.contrib.auth.models import User


    
class Deliver(models.Model):
    name = models.CharField(max_length=200,verbose_name="Ismi")
    surname = models.CharField(max_length=250,verbose_name="Familiyasi")
    car_type = models.CharField(max_length=250,verbose_name="Moshina nomi")
    car_color = models.CharField(max_length=250,verbose_name="Moshina rangi")
    car_number = models.CharField(max_length=250,verbose_name="Moshina raqami")
    phone_number = models.CharField(max_length=250,verbose_name="Telefon raqami")


    def __str__(self):
        return    'Haydovchi' + " " + str(self.name + " " + self.surname)

    

class CartItems(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    

    def overall_price(self):
        if self.product.discount != 0:
            return self.product.price - ((self.product.price / 100) * self.product.discount)
        else:
            return int(self.product.price * self.quantity)
        

class Orders(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    customer_full_name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    target = models.CharField(max_length=250)
    direction = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=250)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    status = models.CharField(max_length=250,null=True,blank=True,default='active')
    received_admin = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sold_products',blank=True,null=True)
    deliver = models.ForeignKey(Deliver, on_delete=models.CASCADE, related_name='deliver_products', blank=True, null=True)
    payment_type = models.CharField(max_length=7,blank=True,null=True)
    class Meta:
        ordering = ['-date_added']


    def get_overall(self):
        return int(sum([i.get_overall() for i in self.order_items.all()]))
    

    def get_overall_body_price_orders(self):
        return int(sum(i.get_overall_body_price() for i in self.order_items.all()))



class OrderItems(models.Model):
    quantity = models.PositiveBigIntegerField(default=0)
    products = models.ForeignKey(Product,on_delete=models.CASCADE, blank=True, null=True)
    sessionkey = models.CharField(max_length=40, blank=True, null=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name = 'order_items',blank=True, null=True)


    def get_overall(self):
        return int(self.products.price * self.quantity)
    
    
    def get_overall_body_price_items(self):
        return int(self.products.body_price * self.quantity)
    
    def __str__(self):
        return str(self.order.customer_full_name)


class WishList(models.Model):
    products = models.ManyToManyField(Product,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40,blank=True, null=True)


    def __str__(self):
        return str(self.date_added)
    

class Expenses(models.Model):
    name = models.CharField(max_length=250)
    amount = models.BigIntegerField(default=0)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.name) + " " + str(self.amount)
    

class UserTrack(models.Model):
    order = models.ForeignKey(Orders,on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.seller.first_name


class Staffs(models.Model):
    name = models.CharField(max_length=250,verbose_name="Ismi")
    phone_number = models.CharField(max_length=250,verbose_name="Telefon raqami")
    address = models.CharField(max_length=250,blank=True, null=True,verbose_name="Manzili")
    salary = models.BigIntegerField(default=0,verbose_name="Oyligi")
    position = models.CharField(max_length=250,verbose_name="Lavozimi")
    date_added = models.DateTimeField(auto_now_add=True,verbose_name="Qo'shilgan")


    def __str__(self):
        return self.name


class Packages(models.Model):
    name = models.CharField(max_length=250,verbose_name='Nabor nomi')
    date_added = models.DateField(auto_now_add=True)
    order = models.ForeignKey(Orders,on_delete=models.CASCADE,blank=True,null=True)


    def get_overall_price(self):
        try:
            return int(sum([i.get_overall() for i in self.package_items.all()]))
        except AttributeError:
            return str("0 so'm")


    def __str__(self):
        return self.name
    

class PackageItems(models.Model):
    quantity = models.PositiveBigIntegerField(default=0)
    product = models.ForeignKey(Product,on_delete=models.CASCADE, blank=True, null=True)
    package = models.ForeignKey(Packages, on_delete=models.CASCADE, related_name = 'package_items',blank=True, null=True)


    def get_overall(self):
        return int(self.product.price * self.quantity)


    def __str__(self):
        return str(self.package.name) + " product " + str(self.id)