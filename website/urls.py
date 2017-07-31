"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from frontend import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^menu$', views.menu),
    url(r'^product/([^/]+)/$', views.get_product_given_category),
    url(r'^productExtra/([0-9]+)/$', views.get_product_extra),
    url(r'^addproduct/$', views.add_product),
    url(r'^basket/$', views.basket),
    url(r'^resetBasket/$', views.reset_basket),
    url(r'^remove/$', views.remove),
    url(r'^view/$', views.view_basket),
    url(r'^checkout/$', views.checkout),
    url(r'^viewcheckout/$', views.view_checkout),
    url(r'^checkout/1/$', views.checkout_delivery),
    url(r'^checkout/2/$', views.checkout_payment),
    url(r'^checkout/3/$', views.save_payment),
    url(r'^payment/$', views.payment),
]
