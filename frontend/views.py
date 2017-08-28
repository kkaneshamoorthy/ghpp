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
from .serializers import OrderSerializer
from .serializers import UtilitySerializer
from .serializers import ExtraSerializer
from frontend.models import Order
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

        products = []

        for cat in category:
            catProduct = Product.objects.filter(category=cat.name)
            productSerializer = ProductSerializer(catProduct, many=True)
            products.append({cat : catProduct})

        # product = Product.objects.all()
        context = {
            'category_list': category,
            # 'product' : product,
            'products' : products
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
        allowableSelection = 0

        if (product_id == 14):
            allowableSelection = 3

        if extraIds == '':
            extraData = []
        else:
            for extraId in extraIds:
                extra = Extras.objects.get(id=extraId)
                extraData.append(extra)
                if (allowableSelection == 0):
                    extraTotal += extra.price
                else:
                    allowableSelection -= 1

        price = float(product.price)
        productTotal = price + extraTotal+float(product_price)
        products.append({'product': product, 'product_subname' : product_subname, 'price':productTotal, 'extras' : extraData, 'product_id' : key, 'quantity' : quantity})
        total += productTotal * quantity

        total = round(total, 3)

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

    ordered_products = ""

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

        ordered_products += product.name+" "+product_subname+ "; "

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

    card_charge = UtilityData.objects.filter(name="card_charge")[0].info
    delivery_charge = UtilityData.objects.filter(name="delivery_charge")[0].info

    if deliveryType != "collection":
        total = total + float(delivery_charge)
    if payment_type != "cash":
        total = total + float(card_charge)

    total = round(total, 2)

    checkout = {'total' : total, 'product' : ordered_products}

    request.session['checkout'] = checkout
    request.session['basket_total'] = total

    context = {'products': products, 'total': total, 'payment_title': paymentTitle, 'delivery_title': deliveryTitle, 'payment_type' : payment_type, 'delivery_type' : deliveryType,
               'card_charge' : card_charge, 'delivery_charge' : delivery_charge}

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
        paymentData = checkout['payment']
        deliveryData = checkout['delivery']
        total = deliveryData['total']

        payment = Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "credit_card",
                "funding_instruments": [{
                    "credit_card": {
                        "type": paymentData['card_type'], #"visa",
                        "number":  paymentData['card_number'], #"4601044104515989",
                        "expire_month": paymentData['expiry_month'], #"11",
                        "expire_year": paymentData['expiry_year'], #"2018",
                        "cvv2": paymentData['cvv'], #"874",
                        "first_name": "Joe",
                        "last_name": "Shopper",
                        "billing_address": {
                            "line1": deliveryData['street'],#"52 N Main ST",
                            "city": deliveryData['city'], #"Johnstown",
                            #"state": "OH",
                            "postal_code": deliveryData['postcode'], #"43210",
                            "country_code": "GB"
                        }
                    }
                }]
            },
            "transactions": [{
                "amount": {
                    "total": total['total'], #"7.47",
                    "currency": "GBP"
                },
                "description": "This is the payment transaction description."
            }]
        })

        # Create payment
        if payment.create():
            order = Order(
                product= deliveryData['total']['product'],
                total = float(total['total']),
                paymentType = "Card",
                deliveryType = "Collection",
                address = deliveryData['street']+", "+deliveryData['city']+", "+deliveryData['postcode'],
                name = "Kowrishankar",
                status = "Order Received"
            )
            order.save()

            context = {"orderStatus": "Order Received", "status": "success", "message": "Payment created successfully",
                       'data': payment.id, "orderId" : order.id}
            request.session['basket'] = {}
            request.session['checkout'] = {}

        else:
            # Display Error message
            context = {"status" : "failed", "message" : "Error while creating payment:", "data" : payment.error}
    return render(request, 'website/ordered.html', context)


def order(request):
    context = {}
    if (request.method == 'POST'):
        checkout = request.session['checkout']
        paymentData = checkout['payment']
        deliveryData = checkout['delivery']
        total = deliveryData['total']

        order = Order(
            product= deliveryData['total']['product'],
            total = float(total['total']),
            paymentType = "Card",
            deliveryType = "Collection",
            address = deliveryData['street']+", "+deliveryData['city']+", "+deliveryData['postcode'],
            name = "Kowrishankar",
            status = "Order Received"
        )
        order.save()

        context = {"status": "success", "orderStatus": "Order Received", "message": "Order created successfully", 'data': "", "orderId" : order.id}
        request.session['basket'] = {}
        request.session['checkout'] = {}

    return render(request, 'website/ordered.html', context)

def admin(request):
    order = Order.objects.all()
    serializer = OrderSerializer(order, many=True)

    context = {
        'orders' : serializer.data
    }

    return render(request, 'website/admin.html', context)
    # return HttpResponse(json.dumps(serializer.data), content_type="application/json")

def changeOrderStatus(request):
    if (request.method == "POST"):
        newStatus = request.POST.get("status")
        orderId = request.POST.get("orderId")

        order = Order.objects.get(id=orderId)
        order.status = newStatus
        order.save()

        return HttpResponse("status changed")
    raise Http404
