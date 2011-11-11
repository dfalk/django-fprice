#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import list_detail
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Q

from django.core import serializers
import datetime, time
from decimal import Decimal

from fprice.models import Section, Product, Shop, Trade, Price
from fprice.forms import TradeForm, TradeFormSet, TitleForm


def price_list(request, page=0, template_name='fprice/price_list.html', **kwargs):
    return list_detail.object_list(
        request,
        queryset = Price.objects.all(),
        paginate_by = 30,
        page = page,
        template_name = template_name,
        **kwargs)

def product_detail(request, product_id, page=0, template_name='fprice/product_detail.html', **kwargs):
    product = Product.objects.get(id=product_id)
    shop_list = Shop.objects.filter(pk__in=Price.objects.filter(product__id=product_id).values_list('shop', flat=True).order_by('shop').distinct())
    return list_detail.object_list(
        request,
        queryset = Price.objects.filter(product__id=product_id),
        paginate_by = 30,
        page = page,
        template_name = template_name,
        extra_context = {'product':product, 'shop_list':shop_list},
        **kwargs)

@login_required
def trade_list(request, page=0, template_name='fprice/trade_list.html', **kwargs):
    return list_detail.object_list(
        request,
        queryset = Trade.objects.filter(customer__id=request.user.id),
        paginate_by = 30,
        page = page,
        template_name = template_name,
        **kwargs)

@staff_member_required
def trade_admin(request, page=0, template_name='fprice/trade_list.html', **kwargs):
    return list_detail.object_list(
        request,
        queryset = Trade.objects.all(),
        paginate_by = 30,
        page = page,
        template_name = template_name,
        **kwargs)

@login_required
def trade_add(request, **kwargs):
    if request.method == 'POST':
        forma = TitleForm(request.POST)
        formset = TradeFormSet(request.POST)
        if forma.is_valid() and formset.is_valid():

            # check existing shop or add new
            shop = None
            if forma.cleaned_data['shop']:
                shop = Shop.objects.get(id=int(forma.cleaned_data['shop']))
                if shop.title != forma.cleaned_data['shop_visual']:
                    shop = None
            if shop == None:
                shop = Shop()
                shop.title = forma.cleaned_data['shop_visual']
                shop.save()

            for form in formset.forms:

                if form.has_changed():

                    # check existing product or add new
                    product = None
                    if form.cleaned_data['product']:
                        product = Product.objects.get(id=int(form.cleaned_data['product']))
                        if product.title != form.cleaned_data['product_visual']:
                            product = None
                    if product == None:
                        product = Product()
                        product.title = form.cleaned_data['product_visual']
                        product.save()

                    # count cost
                    cost = "%.2f" % ( float(form.cleaned_data['price_visual']) * float(form.cleaned_data['amount']) )

                    # check existing price or add new
                    try:
                        new_price = Price.objects.get(shop=shop, product=product, price=form.cleaned_data['price_visual'], currency=forma.cleaned_data['currency'])
                    except Price.DoesNotExist:
                        new_price = None
                    if new_price == None:
                        new_price = Price()
                        new_price.user = request.user
                        new_price.last_user_update = request.user
                        new_price.time = forma.cleaned_data['time']
                        new_price.last_time_update = forma.cleaned_data['time']
                        new_price.shop = shop
                        new_price.product = product
                        new_price.price = form.cleaned_data['price_visual']
                        new_price.currency = forma.cleaned_data['currency']
                        new_price.save()
                    else:
                        if forma.cleaned_data['time'] > new_price.last_time_update:
                            new_price.last_user_update = request.user
                            new_price.last_time_update = forma.cleaned_data['time']
                        new_price.update_counter += 1
                        new_price.save()

                    # save trade if it is not spy
                    if not forma.cleaned_data['spytrade']:
                        new_trade = form.save(commit=False)
                        new_trade.customer = request.user
                        new_trade.time = forma.cleaned_data['time']
                        new_trade.shop = shop
                        new_trade.product = product
                        new_trade.price = new_price
                        new_trade.cost = cost
                        new_trade.save()
                        form.save_m2m()

            return HttpResponseRedirect(reverse('price_index'))
    else:
        forma = TitleForm()
        formset = TradeFormSet()

    return direct_to_template(request, 'fprice/price_add.html',{'formset':formset, 'forma':forma})


def lookup(request, what):
    results = []
    if request.method == "GET":
        if request.GET.has_key(u'term'):
            value = request.GET[u'term']
            # Ignore queries shorter than length 2
            #if len(value) > 1:
            if what == 'shop':
                model_results = Shop.objects.filter(title__icontains=value)
            elif what == 'product':
                model_results = Product.objects.filter(title__icontains=value)
            results = serializers.serialize("json", model_results)

    return HttpResponse(results, mimetype='application/json')
