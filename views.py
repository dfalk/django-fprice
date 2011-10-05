#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fprice.models import Section, Product, Shop, Trade
from fprice.forms import TradeForm

from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic import list_detail
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q

from django.core import serializers
import simplejson
import datetime, time
from decimal import Decimal


def price_list(request, page=0, template_name='fprice/price_list.html', **kwargs):
    return list_detail.object_list(
        request,
        queryset = Trade.objects.all(),
        paginate_by = 30,
        page = page,
        template_name = template_name,
        **kwargs)

@login_required
def price_add(request, **kwargs):
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            # CHECK EXISTING PRICE OR ADD NEW
            if form.cleaned_data['shop']:
                shop = Shop.objects.get(id=int(form.cleaned_data['shop']))
            else:
                shop = Shop()
                shop.title = form.cleaned_data['shop_visual']
                shop.save()
            if form.cleaned_data['product']:
                product = Product.objects.get(id=int(form.cleaned_data['product']))
            else:
                product = Product()
                product.title = form.cleaned_data['product_visual']
                product.unit = form.cleaned_data['product_visual']
                product.save()
            price = "%.2f" % ( float(form.cleaned_data['cost']) / float(form.cleaned_data['amount']) )

            # SAVE RESULT
            new_trade = form.save(commit=False)
            new_trade.customer = request.user
            new_trade.shop = shop
            new_trade.product = product
            new_trade.price = price
            new_trade.save()
            form.save_m2m()

            return HttpResponseRedirect(reverse('price_index'))
    else:
        form = TradeForm()

    return direct_to_template(request, 'fprice/price_add.html',{'form':form})


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
