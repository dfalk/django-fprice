#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import connections
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

from fprice.models import Shop, ProductCategory, Product, Price, Trade, Summary
from fprice.forms import TradeForm, TradeFormSet, TitleForm


def search(request):
    query = request.GET.get('q', '')
    if query:
        results = Product.objects.filter(title__icontains=query).distinct()
    else:
        results = []
    return list_detail.object_list(request, queryset=results, paginate_by=30)

def product_list(request, page=0, template_name='fprice/product_list.html', **kwargs):
    children = ProductCategory.objects.filter(parent__isnull=True)
    return list_detail.object_list(
        request,
        queryset = Product.objects.all(),
        paginate_by = 30,
        page = page,
        template_name = template_name,
        extra_context = {'children':children},
        **kwargs)

def product_category(request, slug, page=0, template_name='fprice/product_list.html', **kwargs):
    category = ProductCategory.objects.get(slug=slug)
    subcategories = category.get_descendants(include_self=True)
    categories = category.get_ancestors()
    children = category.get_children()
    return list_detail.object_list(
        request,
        queryset = Product.objects.filter(category__in=subcategories),
        paginate_by = 30,
        page = page,
        template_name = template_name,
        extra_context = {'category':category,'categories':categories,'children':children},
        **kwargs)

def product_detail(request, product_id, page=0, template_name='fprice/product_detail.html', **kwargs):
    product = Product.objects.get(id=product_id)
    try:
        categories = product.category.get_ancestors()
    except:
        categories = None
    price_param = product_id
    price_list = Price.objects.raw('SELECT * FROM (SELECT * FROM (SELECT product_id AS pid, shop_id AS sid, MAX(last_time_update) as maxtime FROM fprice_price GROUP BY product_id, shop_id HAVING product_id = %s) as fmax LEFT JOIN fprice_price as fp ON fmax.pid = fp.product_id AND fmax.sid = fp.shop_id AND fmax.maxtime = fp.last_time_update) as ffull LEFT JOIN fprice_shop AS fs ON ffull.shop_id = fs.id', [price_param])
    return list_detail.object_list(
        request,
        queryset = Price.objects.filter(product__id=product_id),
        paginate_by = 30,
        page = page,
        template_name = template_name,
        extra_context = {'product':product, 'price_list':price_list, 'categories':categories},
        **kwargs)

def shop_list(request, page=0, template_name='fprice/shop_list.html', **kwargs):
    return list_detail.object_list(
        request,
        queryset = Shop.objects.all(),
        paginate_by = 30,
        page = page,
        template_name = template_name,
        **kwargs)

def shop_detail(request, shop_id, page=0, template_name='fprice/shop_detail.html', **kwargs):
    shop = Shop.objects.get(id=shop_id)
    price_param = shop_id
    price_list = Price.objects.raw('SELECT * FROM (SELECT * FROM (SELECT shop_id AS sid, product_id AS pid, MAX(last_time_update) as maxtime FROM fprice_price GROUP BY product_id, shop_id HAVING shop_id = %s) as fmax LEFT JOIN fprice_price as fp ON fmax.sid = fp.shop_id AND fmax.pid = fp.product_id AND fmax.maxtime = fp.last_time_update) as ffull LEFT JOIN fprice_product AS fs ON ffull.product_id = fs.id', [price_param])
    return list_detail.object_list(
        request,
        queryset = Price.objects.filter(shop__id=shop_id),
        paginate_by = 30,
        page = page,
        template_name = template_name,
        extra_context = {'shop':shop, 'price_list':price_list},
        **kwargs)

def product_and_shop(request, product_id, shop_id, page=0, template_name='fprice/prodshop_detail.html', **kwargs):
    product = Product.objects.get(id=product_id)
    try:
        categories = product.category.get_ancestors()
    except:
        categories = None
    shop = Shop.objects.get(id=shop_id)
    shop_list = Shop.objects.filter(pk=shop_id)
    return list_detail.object_list(
        request,
        queryset = Price.objects.filter(product__id=product_id, shop__id=shop_id),
        paginate_by = 30,
        page = page,
        template_name = template_name,
        extra_context = {'shop':shop, 'product':product, 'shop_list':shop_list, 'categories':categories},
        **kwargs)

@staff_member_required
def price_up(request, price_id, **kwargs):
    """ Hijax ajax principle """
    price = Price.objects.get(id=price_id)
    price.last_time_update = datetime.datetime.now()
    price.last_user_update = request.user
    price.update_counter += 1
    price.save()
    if request.is_ajax():
        data = "counted"
        return HttpResponse(data)
    else:
        return HttpResponseRedirect(reverse(request.path))

@login_required
def summary_list(request, page=0, template_name='fprice/summary_list.html', **kwargs):
    queryset = Summary.objects.filter(user=request.user).filter(time__gt=datetime.datetime.now()-datetime.timedelta(days=30))
    summary_sum = queryset.aggregate(Sum('summary'))
    #month_list = Summary.objects.filter(time__gt=datetime.datetime.now()-datetime.timedelta(days=365)).dates('time','month',order='DESC')
    month_list = Summary.objects.filter(time__gt=datetime.datetime.now()-datetime.timedelta(days=365)).extra(select={'year': connections[Summary.objects.db].ops.date_extract_sql('year', 'time'), 'month': connections[Summary.objects.db].ops.date_extract_sql('month', 'time')}).values('year','month').annotate(sum=Sum('summary')).order_by('-year','-month')
    return list_detail.object_list(
        request,
        queryset = queryset,
        paginate_by = 30,
        page = page,
        template_name = template_name,
        extra_context = {'sum':summary_sum, 'month_list': month_list},
        **kwargs)

@login_required
def summary_archive_year(request, year, page=0, template_name='fprice/summary_archive_year.html', **kwargs):
    queryset = Summary.objects.filter(user=request.user).filter(time__year=year)
    summary_sum = queryset.aggregate(Sum('summary'))
    return list_detail.object_list(
        request,
        queryset = queryset,
        paginate_by = 10,
        page = page,
        template_name = template_name,
        extra_context = {'sum':summary_sum, 'year':year},
        **kwargs)

@login_required
def summary_archive_month(request, year, month, page=0, template_name='fprice/summary_archive_month.html', **kwargs):
    queryset = Summary.objects.filter(user=request.user).filter(time__year=year, time__month=month)
    summary_sum = queryset.aggregate(Sum('summary'))
    return list_detail.object_list(
        request,
        queryset = queryset,
        paginate_by = 10,
        page = page,
        template_name = template_name,
        extra_context = {'sum':summary_sum, 'month':datetime.date(int(year),int(month),1)},
        **kwargs)



@login_required
def summary_detail(request, summary_id, page=0, template_name='fprice/summary_detail.html', **kwargs):
    summary = Summary.objects.get(id=summary_id)
    # TODO: check user
    return list_detail.object_list(
        request,
        queryset = Trade.objects.filter(summary=summary),
        paginate_by = 30,
        page = page,
        template_name = template_name,
        extra_context = {'summary':summary},
        **kwargs)

@login_required
def price_list(request, page=0, template_name='fprice/price_list.html', **kwargs):
    return list_detail.object_list(
        request,
        queryset = Price.objects.filter(user=request.user),
        paginate_by = 30,
        page = page,
        template_name = template_name,
        **kwargs)

@staff_member_required
def price_admin(request, page=0, template_name='fprice/price_list.html', **kwargs):
    return list_detail.object_list(
        request,
        queryset = Price.objects.all(),
        paginate_by = 30,
        page = page,
        template_name = template_name,
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

            if not forma.cleaned_data['spytrade']:
                new_summ = Summary()
                new_summ.time = forma.cleaned_data['time']
                new_summ.user = request.user
                new_summ.shop = shop
                new_summ.currency = forma.cleaned_data['currency']
                new_summ.summary = 0 - forma.cleaned_data['summary']
                new_summ.save()

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
                        if forma.cleaned_data['time'] < new_price.time:
                            new_price.time = forma.cleaned_data['time']
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
                        new_trade.summary = new_summ
                        new_trade.save()
                        form.save_m2m()

            return HttpResponseRedirect(reverse('price_summary_list'))
    else:
        forma = TitleForm()
        formset = TradeFormSet()

    return direct_to_template(request, 'fprice/trade_add.html',{'formset':formset, 'forma':forma})

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
