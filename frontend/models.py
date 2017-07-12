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
    name = models.CharField(max_length=200)
    price = models.FloatField()

class ProductExtras(models.Model):
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    extra_name = models.ForeignKey(Extras, on_delete=models.CASCADE)