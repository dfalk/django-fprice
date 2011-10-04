#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fprice.models import Section, Product, Price, Trade, Shop
from fprice.forms import TradeForm

from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic import list_detail
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q

import simplejson
import datetime, time
from decimal import Decimal


def price_list(request, page=0, template_name='fprice/price_list.html', **kwargs):
    return list_detail.object_list(
        request,
        queryset = Price.objects.all(),
        paginate_by = 30,
        page = page,
        template_name = template_name,
        **kwargs)

@login_required
def price_add(request, **kwargs):
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            new_trade = form.save(commit=False)
            new_trade.author = request.user
            new_trade.save()
            return HttpResponseRedirect(reverse('price_index'))
    else:
        form = TradeForm()

    return direct_to_template(request, 'fprice/price_add.html',{'form':form})
