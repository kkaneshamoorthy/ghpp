import datetime

from django.shortcuts import render
from frontend.models import Product
from frontend.models import Category
from frontend.models import ProductExtras
from frontend.models import Extras
from frontend.models import UtilityData
from frontend.models import User
from frontend.models import OptionCategory
from frontend.models import Options
from frontend.models import ProductOption
from frontend.models import Order
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest
from .serializers import ProductSerializer, UserSerializer
from .serializers import CategorySerializer
from .serializers import ProductExtrasSerializer
from .serializers import OrderSerializer
from .serializers import UtilitySerializer
from .serializers import ExtraSerializer
from .serializers import OptionCategorySerializer
from .serializers import OptionsSerializer
from .serializers import ProductOptionSerializer
from .serializers import ExtraSerializer
from .serializers import ExtraSerializer
from frontend.models import Order
import json
from paypalrestsdk import Payment
from rest_framework.renderers import JSONRenderer
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser

# Create your views here.
def index(request):
    category = Category.objects.all()

    products = []

    for cat in category:
        catProduct = Product.objects.filter(category=cat.name)
        productSerializer = ProductSerializer(catProduct, many=True)
        products.append({cat: catProduct})

    # product = Product.objects.all()
    context = {
        'category_list': category,
        # 'product' : product,
        'products': products
    }

    if 'basket' not in request.session:
        request.session['basket'] = {}
        # request.session['basket']['totalItem'] = 0

    return render(request, 'website/index.html', context)

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
        selectedOption = request.POST.get("selectedOption")

        extraArr = []
        quantity = 1

        if "extras_id" in request.POST:
            extras_id = request.POST.get("extras_id").split(",")
            for value in extras_id:
                extraArr.append(value)

        basket = request.session['basket']

        if product_id in basket:
            quantity = basket[product_id]["quantity"]+1

        basket[product_id] = {"extras" : extraArr, "quantity" : quantity, "selectedOption" : selectedOption}
        # basket["totalItem"] = basket['totalItem']+1

        request.session['basket'] = basket
        return HttpResponse("product added:"+selectedOption)
    raise Http404


def reset_basket(request):
    request.session['basket'] = {}
    return HttpResponse("basket resetted")

def view_basket(request):
    if 'basket' in request.session:
        basket = request.session['basket']
    else:
        basket = {}

    return HttpResponse(json.dumps(basket))

def basket(request):
    products = []
    total = 0

    if 'basket' in request.session:
        basket = request.session['basket']
    else:
        basket = {}

    for key,value in basket.items():
        productData = key.split(":")
        product_id = int(productData[0])
        product_subname = productData[1]
        product_price = productData[2]
        extraIds = value['extras']
        quantity = value['quantity']
        selectedOption = value['selectedOption']
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
        products.append({'product': product, 'product_subname' : product_subname, 'price':productTotal, 'extras' : extraData, 'product_id' : key, 'quantity' : quantity, 'selectedOption' : selectedOption})
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
        selectedOption = value['selectedOption']
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
        total += productTotal * quantity

        products.append({'product': product.name, 'product_subname' : product_subname, 'price':productTotal, 'extras' : extraData, 'product_id' : key, 'quantity' : quantity, 'selectedOption' : selectedOption})

    card_charge = UtilityData.objects.filter(name="card_charge")[0].info
    delivery_charge = UtilityData.objects.filter(name="delivery_charge")[0].info

    if deliveryType != "collection":
        total = total + float(delivery_charge)
    if payment_type != "cash":
        total = total + float(card_charge)

    total = round(total, 2)

    checkout = {'product' : ordered_products, "selectedOption" : selectedOption}

    request.session['checkout'] = checkout
    request.session['basket_total'] = total
    request.session['products'] = {'products': products}
    request.session['ordered_products'] = {'ordered_products': ordered_products, 'selected_option': selectedOption}
    request.session['order_info'] = {'payment_title': paymentTitle, 'delivery_title': deliveryTitle, 'payment_type' : payment_type, 'delivery_type' : deliveryType, 'card_charge' : card_charge, 'delivery_charge' : delivery_charge}


    return render(request, 'website/checkout-delivery.html', request.session['order_info'])

def checkout_payment(request):
    if (request.method == 'POST'):
        name = request.POST.get("name")
        street = request.POST.get("street")
        postcode = request.POST.get("postcode")
        city = request.POST.get("city")
        country = request.POST.get("country")
        phone = request.POST.get("phone")

        delivery = {'name' : name, 'street' : street, 'postcode' : postcode, 'city' : city, 'country' : country, 'phone' : phone}

        request.session['delivery'] = delivery

        return HttpResponse("delivery data saved")
    raise Http404

def save_payment(request):
    if (request.method == 'POST'):
        card_type = request.POST.get("card_type")
        card_number = request.POST.get("card_number")
        expiry_month = request.POST.get("expiry_month")
        expiry_year = request.POST.get("expiry_year")
        cvv = request.POST.get("cvv")
        card_holdername = request.POST.get("card_holdername")
        comment = request.POST.get("comment")

        payment = {'card_type': card_type, 'card_number': card_number, 'expiry_month': expiry_month, 'expiry_year': expiry_year,
         'cvv': cvv, 'card_holdername': card_holdername}

        request.session['payment'] = payment
        request.session['comment'] = comment

        return HttpResponse("payment data saved")
    raise Http404

def view_checkout(request):
    return HttpResponse(json.dumps(request.session['checkout']))

def payment(request): #card payment
    context = {}
    if (request.method == 'POST'):
        paymentData = request.session['payment']
        deliveryData = request.session['delivery']
        comment = request.session['comment']
        total = request.session.get('basket_total')

        first_name, second_name = paymentData['card_holdername'].split(" ")

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
                        "first_name": first_name, #"Joe",
                        "last_name": second_name, #"Shopper",
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
                    "total": total, #"7.47",
                    "currency": "GBP"
                },
                "description": "This is the payment transaction description."
            }]
        })

        # Create payment
        if payment.create():
            order = Order(
                product= request.session['ordered_products'],
                total = float(total),
                paymentType = "Card",
                deliveryType = request.session['order_info'],
                address = deliveryData['street']+", "+deliveryData['city']+", "+deliveryData['postcode'],
                name = deliveryData['name'],
                status = "Order Received",
                email = request.session['account']['email'],
                date=datetime.datetime.now(),
                comment = comment,
                option = deliveryData['total']['selectedOption']
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

def order(request): #cash payment
    context = {}
    if (request.method == 'POST'):
        checkout = request.session['checkout']
        email = request.session['account']['email']
        paymentData = request.session['payment']
        deliveryData = request.session['delivery']
        # selectedOption = checkout['selectedOption']
        comment = request.session['comment']
        total = request.session['basket_total']

        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute

        # if (hour >= 23 & minute >= 1):
        #     return render(request, 'website/ordered.html', {'status' : 'failed', 'orderStatus' : 'Order failed', 'message' : 'Shop is now closed. Order must be made before 11PM.'})

        order = Order(
            product= request.session['ordered_products'].get('ordered_products'),
            total = float(total),
            paymentType = "Cash",
            deliveryType = request.session['context']['delivery_type'],
            address = deliveryData['street']+", "+deliveryData['city']+", "+deliveryData['postcode'],
            name = deliveryData['name'],
            status = "Order Received",
            email = email,
            date = datetime.datetime.now(),
            comment = comment,
            option = request.session['ordered_products'].get('selected_option')
        )
        order.save()

        context = {"status": "success", "orderStatus": "Order Received", "message": "Order created successfully", 'data': "", "orderId" : order.id}
        request.session['basket'] = {}
        request.session['checkout'] = {}

    return render(request, 'website/ordered.html', context)

def admin(request):
    if (request.method == "POST"):
        serializer = None
        toggle = None
        if ('open-orders-bt' in request.POST):
            orders = Order.objects.filter(status = "Order Received")
            serializer = OrderSerializer(orders, many=True)
            toggle = "openOrders"
        elif ('past-orders-bt' in request.POST):
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            toggle = "pastOrders"
        elif ('today-orders-bt' in request.POST):
            today = datetime.date.today()
            orders = Order.objects.filter(date__gte=datetime.date(today.year, today.month, today.day))
            serializer = OrderSerializer(orders, many=True)
            toggle = "todayOrders"

        context = {
            'orders' : serializer.data,
            'page' : toggle
        }

        return render(request, 'website/admin.html', context)
        # return HttpResponse(json.dumps(serializer.data), content_type="application/json")
    else:
        today = datetime.date.today()
        # orders = Order.objects.filter(date__gte=datetime.date(today.year, today.month, today.day))
        # serializer = OrderSerializer(orders, many=True)
        orders = Order.objects.filter(status="Order Received")
        serializer = OrderSerializer(orders, many=True)

        context = {
            'orders': serializer.data,
            'page' : 'openOrders'
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

def account(request):
    context = {'orders' : None}

    if 'account' in request.session:
        isAdmin = request.session['account']['type'] == "admin"

        if isAdmin == True:
            userOrders = Order.objects.all()
            orderSerializer = OrderSerializer(userOrders, many=True)
        else:
            email = request.session['account']['email']
            userOrders = Order.objects.filter(email=email)
            orderSerializer = OrderSerializer(userOrders, many=True)

        context = {'orders' : orderSerializer.data}

    return render(request, 'website/account.html', context)

def login(request):
    if (request.method == 'POST'):
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email, password = password)
            serializer = UserSerializer(user, many=False)
            request.session['account'] = serializer.data

            return HttpResponseRedirect('/')
        except User.DoesNotExist:
            context = {'status': "failed", 'message': "Username or password is incorrect"}
            return render(request, 'website/account.html/', context)
    raise Http404

def logout(request):
    if (request.method == 'GET'):
        del request.session['account']
    return HttpResponseRedirect("/")

def register(request):
    if (request.method == "POST"):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        street = request.POST.get('street')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = User(
            first_name = first_name,
            last_name = last_name,
            phone = phone,
            street = street,
            city = city,
            postcode = postcode,
            password = password,
            email = email,
            type = "user"
        )

        user.save()

        return render(request, 'website/account.html', context={'status' : "", 'message' : 'Account is created successfully'})
    raise Http404

def checkEmailAvailable(request):
    if (request.method == "POST"):
        emailAddress = request.POST.get("email")

        userCount = User.objects.filter(email=emailAddress).count()

        if userCount == 0:
            return HttpResponse("available")
        else:
            return HttpResponse("unavailable")
    raise Http404

def loggedInUserdata(request):
    return HttpResponse(json.dumps(request.session['account']), content_type="application/json")

def editPersonalDetails(request):
    if (request.method == "POST"):
        first_name = request.POST.get('edited-first-name')
        last_name = request.POST.get('edited-last-name')
        phone = request.POST.get('edited-phone')
        street = request.POST.get('edited-street')
        city = request.POST.get('edited-city')
        postcode = request.POST.get('edited-postcode')
        emailAddress = request.POST.get('edited-email')

        user = User.objects.get(email=emailAddress)

        user.phone = phone
        user.street = street
        user.city = city
        user.postcode = postcode
        user.first_name = first_name
        user.last_name = last_name

        user.save()

        userSerializer = UserSerializer(user, many=False)
        request.session['account'] = userSerializer.data

        return HttpResponseRedirect("/account/")
    raise Http404

def checkDeliveryRadius(request):
    if (request.method == "POST"):
        userPostcode = request.POST.get('postcode').upper()

        validPostcode = ['MK1', 'MK2', 'MK3', 'MK4', 'MK5', 'MK6', 'MK7', 'MK8',
                         'MK9', 'MK10', 'MK11', 'MK12', 'MK13', 'MK14', 'MK15',
                         'MK16', 'MK19']

        for postcode in validPostcode:
            if (userPostcode.startswith(postcode)):
                return HttpResponse("valid")
        return HttpResponse("invalid")
    raise Http404

def hasNewOrders(request):
    if (request.method == "POST"):
        count = request.POST.get('numberOfOrder')
        currentlyDisplayedPage = request.POST.get('currentlyDisplayedPage')

        if (currentlyDisplayedPage == "pastOrders" or currentlyDisplayedPage == "todayOrders"):
            return HttpResponse("false")

        # today = datetime.date.today()
        # orders = Order.objects.filter(date__gte=datetime.date(today.year, today.month, today.day)).count()

        orders = Order.objects.filter(status="Order Received").count()

        if int(count) == orders:
            return HttpResponse("false")
        return HttpResponse("true")
    raise Http404

def getNumberOfOptions(request):
    if (request.method == "POST"):
        productId = request.POST.get('productId')

        numberOfOptions = ProductOption.objects.filter(product=productId).count()

        return HttpResponse(numberOfOptions)
    raise Http404

def getCategoryOptions(request):
    if (request.method == 'POST'):
        productId = request.POST.get('productId')

        productObj = Product.objects.filter(id=productId)
        po = ProductOption.objects.filter(product=productObj)
        poSerializer = ProductOptionSerializer(po, many=True)

        return HttpResponse(json.dumps(poSerializer.data))
    raise Http404

def getOptions(request):
    if (request.method == 'POST'):
        optionCategoryName = request.POST.get('optionCategoryNameArr').split(",")

        context = ""
        for category in optionCategoryName:
            categoryObj = OptionCategory.objects.filter(name=category)
            optionObj = Options.objects.filter(category=categoryObj)
            optionSerializer = OptionsSerializer(optionObj, many=True)
            context += json.dumps(optionSerializer.data)

        return HttpResponse(context)
    raise Http404