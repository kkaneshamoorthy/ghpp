from django.shortcuts import render
from frontend.models import Product
from frontend.models import Category
from frontend.models import ProductExtras
from frontend.models import Extras
from frontend.models import UtilityData
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest
from .serializers import ProductSerializer
from .serializers import CategorySerializer
from .serializers import ProductExtrasSerializer
from .serializers import UtilitySerializer
from .serializers import ExtraSerializer
import json
from paypalrestsdk import Payment

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
        extraArr = []
        quantity = 1

        if "extras_id" in request.POST:
            extras_id = request.POST.get("extras_id").split(",")
            for value in extras_id:
                extraArr.append(value)

        basket = request.session['basket']

        if product_id in basket:
            quantity = basket[product_id]["quantity"]+1

        basket[product_id] = {"extras" : extraArr, "quantity" : quantity}

        request.session['basket'] = basket
        return HttpResponse("product added")
    raise Http404


def reset_basket(request):
    request.session['basket'] = {}
    return HttpResponse("basket resetted")

def view_basket(request):
    return HttpResponse(json.dumps(request.session['basket']))

def basket(request):
    products = []
    total = 0
    basket = request.session['basket']

    for key,value in basket.items():
        productData = key.split(":")
        product_id = int(productData[0])
        product_subname = productData[1]
        product_price = productData[2]
        extraIds = value['extras']
        quantity = value['quantity']
        extraTotal = 0
        extraData = []
        product = Product.objects.get(id=product_id) #get product

        if extraIds == '':
            extraData = []
        else:
            for extraId in extraIds:
                extra = Extras.objects.get(id=extraId)
                extraData.append(extra)
                extraTotal += extra.price

        price = float(product.price)
        productTotal = price + extraTotal+float(product_price)
        products.append({'product': product, 'product_subname' : product_subname, 'price':productTotal, 'extras' : extraData, 'product_id' : key, 'quantity' : quantity})
        total += productTotal * quantity

    request.session['basket_total'] = total
    context = {'products':products, 'total' : total}
    return render(request, 'website/basket.html',context)

def remove(request):
    if (request.method == 'POST'):
        product_id = request.POST.get("product_id")
        basket = request.session['basket']

        basket[product_id]['quantity'] -= 1

        try:
            if basket[product_id]['quantity'] <= 0:
                del basket[product_id]
        except IndexError:
            return HttpResponse("No such a product id")

        request.session['basket'] = basket

        return HttpResponse("product removed")
    raise Http404

def checkout(request):
    if (request.method == "POST"):
        context = {}
        paymentTitle = ""
        deliveryTitle = ""
        payment_type = request.POST.get("payment_type")
        delivery_type = request.POST.get("delivery_type")

        if (payment_type == "cash"):
            paymentTitle = "CASH PAYMENT"
        else:
            paymentTitle = "CARD PAYMENT"

        if (delivery_type == "collection"):
            deliveryTitle = "YOUR ADDRESS"
        else:
            deliveryTitle = "DELIVERY ADDRESS"

        context = {'payment_title' : paymentTitle, 'delivery_title' : deliveryTitle, 'payment_type' : payment_type, 'delivery_type' : delivery_type}

        request.session['context'] = context

    request.session['checkout'] = {}
    return HttpResponseRedirect("/checkout/1")

def checkout_delivery(request):
    context = {}
    paymentTitle = request.session['context']['payment_title']
    payment_type = request.session['context']['payment_type']
    deliveryTitle = request.session['context']['delivery_title']
    deliveryType = request.session['context']['delivery_type']

    products = []
    total = 0
    request.session['checkout'] = {}
    checkout = request.session['checkout']
    delivery_and_payment_info = request.session['context']

    basket = request.session['basket']

    for key,value in basket.items():
        productData = key.split(":")
        product_id = int(productData[0])
        product_subname = productData[1]
        product_price = productData[2]
        extraIds = value['extras']
        quantity = value['quantity']
        extraTotal = 0
        extraData = []
        product = Product.objects.get(id=product_id) #get product

        if extraIds == '':
            extraData = []
        else:
            for extraId in extraIds:
                extra = Extras.objects.get(id=extraId)
                extraData.append(extra)
                extraTotal += extra.price

        price = float(product.price)
        productTotal = price + extraTotal+float(product_price)
        products.append({'product': product, 'product_subname' : product_subname, 'price':productTotal, 'extras' : extraData, 'product_id' : key, 'quantity' : quantity})
        total += productTotal * quantity

    checkout = {'total' : total}

    request.session['checkout'] = checkout
    request.session['basket_total'] = total

    card_charge = UtilitySerializer(UtilityData.objects.filter(name="card_charge"), many=True)
    delivery_charge = UtilitySerializer(UtilityData.objects.filter(name="delivery_charge"), many=True)

    context = {'products': products, 'total': total, 'payment_title': paymentTitle, 'delivery_title': deliveryTitle, 'payment_type' : payment_type, 'delivery_type' : deliveryType,
               'card_charge' : json.dumps(card_charge.data), 'delivery_charge' : json.dumps(delivery_charge.data)}

    return render(request, 'website/checkout-delivery.html', context)

def checkout_payment(request):
    if (request.method == 'POST'):
        name = request.POST.get("name")
        street = request.POST.get("street")
        postcode = request.POST.get("postcode")
        city = request.POST.get("city")
        country = request.POST.get("country")
        phone = request.POST.get("phone")

        checkout = request.session['checkout']

        checkout = {'name' : name, 'street' : street, 'postcode' : postcode, 'city' : city, 'country' : country, 'phone' : phone, 'total': checkout}

        request.session['checkout'] = checkout

        return HttpResponse("saved")
    raise Http404

def save_payment(request):
    if (request.method == 'POST'):
        card_type = request.POST.get("card_type")
        card_number = request.POST.get("card_number")
        expiry_month = request.POST.get("expiry_month")
        expiry_year = request.POST.get("expiry_year")
        cvv = request.POST.get("cvv")
        card_holdername = request.POST.get("card_holdername")

        checkout = request.session['checkout']

        payment = {'card_type': card_type, 'card_number': card_number, 'expiry_month': expiry_month, 'expiry_year': expiry_year,
         'cvv': cvv, 'card_holdername': card_holdername}

        checkout = {'payment' : payment, 'delivery' : checkout}

        request.session['checkout'] = checkout

        return HttpResponse("saved")
    raise Http404

def view_checkout(request):
    return HttpResponse(json.dumps(request.session['checkout']))

def payment(request):
    context = {}
    if (request.method == 'POST'):
        checkout = request.session['checkout']
        payment = checkout['payment']
        delivery = checkout['delivery']
        total = delivery['total']
        #
        # payment = Payment({
        #   "intent": "sale",
        #   "payer": {
        #     "payment_method": "credit_card",
        #     "funding_instruments": [{
        #       "credit_card": {
        #         "type": payment['card_type'],
        #         "number": payment['card_number'],
        #         "expire_month": payment['expiry_month'],
        #         "expire_year": payment['expiry_year'],
        #         "cvv2": payment['cvv'],
        #         "first_name": "Joe",
        #         "last_name": "Shopper",
        #         "billing_address": {
        #           "line1": "52 N Main ST",
        #           "city": "Johnstown",
        #           "state": "OH",
        #           "postal_code": "43210",
        #           "country_code": "US"
        #         }
        #       }
        #     }]
        #   },
        #   "transactions": [{
        #     "amount": {
        #       "total": total,
        #       "currency": "GBP"
        #     },
        #     "description": "This is the payment transaction description."
        #   }]
        # })

        payment = Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "credit_card",
                "funding_instruments": [{
                    "credit_card": {
                        "type": payment['card_type'],
                        "number": payment['card_number'],
                        "expire_month": payment['expiry_month'],
                        "expire_year": payment['expiry_year'],
                        "cvv2": payment['cvv'],
                        "first_name": "Joe",
                        "last_name": "Shopper",
                        "billing_address": {
                            "line1": delivery['street'],#"52 N Main ST",
                            "city": delivery['city'], #"Johnstown",
                            "state": "OH",
                            "postal_code": delivery['postcode'], #"43210",
                            "country_code": "GB"
                        }
                    }
                }]
            },
            "transactions": [{
                "amount": {
                    "total": total['total'],
                    "currency": "GBP"
                },
                "description": "This is the payment transaction description."
            }]
        })

        # Create payment
        if payment.create():
            context = {"status" : "success", "message" : "Payment created successfully", 'data' : payment.id}
            request.session['basket'] = {}
            request.session['checkout'] = {}
        else:
            # Display Error message
            context = {"status" : "failed", "message" : "Error while creating payment:", "data" : payment.error}
    return render(request, 'website/ordered.html', context)