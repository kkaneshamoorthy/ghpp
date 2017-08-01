from django.contrib import admin
from frontend.models import Product
from frontend.models import Extras
from frontend.models import Category
from frontend.models import ProductExtras
from frontend.models import UtilityData


# Register your models here.
admin.site.register(Product)
admin.site.register(Extras)
admin.site.register(Category)
admin.site.register(ProductExtras)
admin.site.register(UtilityData)