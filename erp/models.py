from django.db import models
from django.shortcuts import redirect
from django.urls import reverse


class Maincategory(models.Model):
    name=models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name=models.CharField(max_length=50)
    category=models.ForeignKey('Maincategory',on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='items/%Y/%m/%d', blank=True)
    price=models.IntegerField(null=True)
    item_category=models.ForeignKey('Subcategory',on_delete=models.CASCADE)
    stock=models.IntegerField()
    created_at=models.DateTimeField(auto_now=True)
    available=models.BooleanField(default=True)


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('erp:item_detail',args=[self.id])


class Company(models.Model):
    name=models.CharField(max_length=50)
    representative=models.CharField(max_length=50,null=True)
    call=models.CharField(max_length=50,null=True)
    inout = (
        ('in', '입고처'),
        ('out', '발주처'),
    )
    inout=models.CharField(max_length=50,choices=inout,default='in')
    available=models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Input_order(models.Model):
    item=models.ForeignKey('Item',on_delete=models.PROTECT,null=True)
    company=models.ForeignKey('Company',on_delete=models.PROTECT,null=True)
    quantity=models.IntegerField()
    input_stock=models.IntegerField( null=True)
    created_at=models.DateTimeField(auto_now_add=True)


class Output_order(models.Model):
    item=models.ForeignKey('Item',on_delete=models.PROTECT)
    company = models.ForeignKey('Company',on_delete=models.PROTECT)
    quantity = models.IntegerField()
    output_stock=models.IntegerField(null=True)
    created_at=models.DateTimeField(auto_now_add=True)









