from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Product_info(models.Model):
    BEVERAGE = '음료'
    MEDICINE = '의약품'
    COSMETICS = '화장품'
    DAILYNECESSITY = '생필품'
    FIRST_CLASS_CHOICES = [
        (BEVERAGE, '음료'),
        (MEDICINE, '의약품'),
        (COSMETICS, '화장품'),
        (DAILYNECESSITY, '생필품'),
    ]
    First_Class = models.CharField(max_length=5, choices=FIRST_CLASS_CHOICES, null=True, blank=True)
    Second_Class = models.CharField(max_length=50, null=True, blank=True)
    Product_Name = models.CharField(max_length=50, null=True, blank=True)
    Price = models.IntegerField(default=0, null=True, blank=True)
    Expiration_Date = models.DateField(null=True, blank=True)
    Basic_Information = models.CharField(max_length=200, null=True, blank=True)
    Notice = models.CharField(max_length=200, null=True, blank=True)
    Additional_Information = models.CharField(max_length=200, null=True, blank=True)
    barcode_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.Product_Name

class Review(models.Model):
    Product = models.ForeignKey(Product_info, on_delete=models.CASCADE)
    User_Review = models.CharField(max_length=200)
    Author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='author_review')
    create_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_review')

class Rinfo(models.Model):
    Product = models.ForeignKey(Product_info, on_delete=models.CASCADE)
    Realtime_Information = models.CharField(max_length=200)
    Author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    create_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    modify_date = models.DateTimeField(null=True, blank=True)

class Blind_User(models.Model):
    Permission_check = models.CharField(max_length=2, null=True, blank=True)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    review = models.ForeignKey(Review, null=True, blank=True, on_delete=models.CASCADE)
    rinfo = models.ForeignKey(Rinfo, null=True, blank=True, on_delete=models.CASCADE)

