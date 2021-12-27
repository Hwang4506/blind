from rest_framework import serializers
from .models import Product_info

class ProductinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_info
        fields = ['First_Class', 'Second_Class', 'Product_Name', 'Manufacturer', 'Price',
                  'Expiration_Date', 'Basic_Information',
                  'Notice', 'Additional_Information', 'barcode_number'
                  ]