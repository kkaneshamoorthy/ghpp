from rest_framework import serializers
from .models import Product
from .models import Category
from .models import Extras
from .models import ProductExtras
from .models import ProductOption
from .models import UtilityData
from .models import Order
from .models import User
from .models import OptionCategory

class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    sub_name = serializers.CharField()
    description = serializers.CharField()

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField(read_only=True)
    description = serializers.CharField()
    category = serializers.CharField()
    size = serializers.CharField()
    price = serializers.FloatField()

class ExtraSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField(read_only=True)
    price = serializers.FloatField()

class ProductExtrasSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    extra_id = serializers.CharField()

class UtilitySerializer(serializers.Serializer):
    info = serializers.CharField()

class OrderSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField(read_only=True)
    total = serializers.FloatField()
    product = serializers.CharField()
    address = serializers.CharField()
    deliveryType = serializers.CharField()
    paymentType = serializers.CharField()
    status = serializers.CharField()
    email = serializers.CharField()
    date = serializers.DateTimeField()
    comment = serializers.CharField()
    option = serializers.CharField()

class UserSerializer(serializers.Serializer):
    id = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField()
    street = serializers.CharField()
    city = serializers.CharField()
    postcode = serializers.CharField()
    email = serializers.CharField()
    type = serializers.CharField()

class OptionCategorySerializer(serializers.Serializer):
    name = serializers.CharField()

class OptionsSerializer(serializers.Serializer):
    name = serializers.CharField()
    category = OptionCategorySerializer()

class ProductOptionSerializer(serializers.Serializer):
    product = ProductSerializer()
    optionCategory = OptionCategorySerializer()