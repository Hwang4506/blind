from django.contrib import admin
from .models import Product_info,Review, Rinfo

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['Product_Name']

admin.site.register(Product_info, ProductAdmin)

class ReviewAdmin(admin.ModelAdmin):
    search_fields = ['Author']

admin.site.register(Review, ReviewAdmin)

class RinfoAdmin(admin.ModelAdmin):
    search_fields = ['Author']

admin.site.register(Rinfo, RinfoAdmin)