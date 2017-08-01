from rest_framework import serializers
from .models import Product
from .models import Category
from .models import Extras
from .models import ProductExtras
from .models import UtilityData

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