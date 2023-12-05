from django.db import models
from django_resized import ResizedImageField


class Storage(models.Model):
    name = models.CharField(max_length=250)
    last_updated = models.DateTimeField(auto_now_add=True)
    

    def overall_products_number(self):
        count = 0
        for i in self.products.all():
            count += i.amount
        return count
    


    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)


    def __str__(self):
        return str(self.name)


class ProductTag(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)


    def __str__(self):
        return str(self.name)

class Product(models.Model):
    name = models.CharField(max_length=250,verbose_name = "Tovar nomi")
    price = models.IntegerField(default=0,verbose_name='Narxi')
    body_price = models.IntegerField(default=0,verbose_name='Tan Narxi')
    old_price = models.IntegerField(default=0,verbose_name='Eski narxi')
    amount = models.PositiveIntegerField(default=0,verbose_name='Soni')
    discount = models.PositiveIntegerField(default=0,verbose_name='Chegirma')
    image = ResizedImageField(size=[570,650],upload_to='movie_posters/')
    description = models.TextField(blank=True,verbose_name="Tovar haqida ma'lumot")
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    tag = models.ForeignKey(ProductTag, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    sold_amount = models.PositiveIntegerField(default=0)
   

    class Meta:
        ordering = ['id']


    def products_status_in_storage(self):
        overall_products = self.storage.overall_products_number()
        if overall_products > 0:
            percentage = (self.amount / overall_products) * 100
            return round(percentage, 2)
        else:
            return 0


    def __str__(self):
        return str(self.name)
    



