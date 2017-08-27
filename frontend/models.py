from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)
    sub_name = models.CharField(max_length=200)
    description = models.CharField(max_length=600)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    size = models.CharField(max_length=600)
    category = models.CharField(max_length=200)
    price = models.FloatField()

class Extras(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    price = models.FloatField()

class ProductExtras(models.Model):
    product_id = models.IntegerField(max_length=50)
    extra_id = models.IntegerField(max_length=50)

class UtilityData(models.Model):
    name = models.CharField(max_length=200)
    info = models.CharField(max_length=200)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.CharField(max_length=3000)
    total = models.FloatField()
    paymentType = models.CharField(max_length=200)
    deliveryType = models.CharField(max_length=200)
    address = models.CharField(max_length=1000)
    name = models.CharField(max_length=200)
