from django.contrib import admin
from .models import Product, ProductCategory, ProductTag,Storage, Aksiyalar_qoshish

admin.site.register(Product)
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug':('name', )}


@admin.register(ProductTag)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug':('name', )}

admin.site.register(Storage)
admin.site.register(Aksiyalar_qoshish)