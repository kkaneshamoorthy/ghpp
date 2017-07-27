from django.shortcuts import render
from frontend.models import Product
from frontend.models import Category
from frontend.models import ProductExtras
from frontend.models import Extras
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest
from .serializers import ProductSerializer
from .serializers import CategorySerializer
from .serializers import ProductExtrasSerializer
from .serializers import ExtraSerializer
import json

# Create your views here.
def index(request):
    if 'basket' not in request.session:
        request.session['basket'] = {}

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

def get_product_extra(request, productId):
    try:
        productExtras = ProductExtras.objects.filter(product_id=productId)
        extraResult = []
        for product in productExtras:
            extras = Extras.objects.filter(id=product.extra_id)
            extraSerializer = ExtraSerializer(extras, many=True)
            extraResult += json.dumps(extraSerializer.data)

        return HttpResponse(extraResult, content_type="application/json")
    except ProductExtras.DoesNotExist:
        raise Http404

def product(request, id):
    try:
        product = Product.objects.get(product_id=id)
        context = {'product_name': id, 'product': product}
        return render(request, 'website/menu.html', context)
    except Product.DoesNotExist:
        raise Http404

def add_product(request):
    if (request.method == 'POST'):
        product_id = request.POST.get("product_id")
        extras_id = request.POST.get("extras_id").split(",")
        extraArr = []

        for value in extras_id:
            extraArr.append(value)

        basket = request.session['basket']
        basket[product_id] = extraArr

        request.session['basket'] = basket
        return HttpResponse(json.dumps(basket))
    raise Http404


def reset_basket(request):
    request.session['basket'] = {}
    return HttpResponse("basket resetted")

def basket(request):
    products = []
    total = 0
    basket = request.session['basket']

    for key,value in basket.items():
        productData = key.split(":")
        product_id = int(productData[0])
        product_subname = productData[1]
        product_price = productData[2]
        extraIds = value
        extraTotal = 0
        extraData = []
        product = Product.objects.get(id=product_id) #get product

        if extraIds[0] == '':
            extraData = []
        else:
            for extraId in extraIds:
                extra = Extras.objects.get(id=extraId)
                extraData.append(extra)
                extraTotal += extra.price

        price = float(product.price)
        productTotal = price + extraTotal+float(product_price)
        products.append({'product': product, 'product_subname' : product_subname, 'price':productTotal, 'extras' : extraData})
        total += productTotal

    request.session['basket_total'] = total
    context = {'products':products, 'total' : total}
    return render(request, 'website/basket.html',context)