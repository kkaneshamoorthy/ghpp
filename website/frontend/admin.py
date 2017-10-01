from django.contrib import admin
from frontend.models import Product
from frontend.models import Extras
from frontend.models import Category
from frontend.models import ProductExtras
from frontend.models import UtilityData
from frontend.models import User
from frontend.models import Order
from frontend.models import Options
from frontend.models import OptionCategory
from frontend.models import ProductOption

# Register your models here.
admin.site.register(Product)
admin.site.register(Extras)
admin.site.register(Category)
admin.site.register(ProductExtras)
admin.site.register(UtilityData)
admin.site.register(User)
admin.site.register(Order)
admin.site.register(Options)
admin.site.register(OptionCategory)
admin.site.register(ProductOption)