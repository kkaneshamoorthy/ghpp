from django.shortcuts import render
from frontend.models import Product
from frontend.models import Category
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest
from .serializers import ProductSerializer
from .serializers import CategorySerializer
import json

# Create your views here.
def index(request):
    return render(request, 'website/index.html')

# Create your views here.
def menu(request):
    try:
        category = Category.objects.all()
        product = Product.objects.all()
        context = {
            'category_list': category,
            'product' : product,
        }

        return render(request, 'website/menu.html', context)
    except Product.DoesNotExist:
        raise Http404
    # return render(request, 'website/menu.html')

def get_product_given_category(request, category):
    try:
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return HttpResponse(json.dumps(serializer.data), content_type="application/json")
    except Product.DoesNotExist:
        raise Http404

def product(request, id):
    try:
        product = Product.objects.get(product_id=id)
        context = {'product_name': id, 'product': product}
        return render(request, 'website/menu.html', context)
    except Product.DoesNotExist:
        raise Http404