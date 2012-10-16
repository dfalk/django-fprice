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
from django.forms.formsets import formset_factory

from django.core import serializers
import datetime, time
from decimal import Decimal

from fprice.models import Shop, ProductCategory, Product, Price, Trade, Summary, ShopProduct, ShopCategory, ShopNet
from fprice.forms import TradeForm, TradeFormSet, TitleForm, PriceFormSet, PriceForm


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
    price_list = Price.objects.filter(shop_product__product=product).select_related()
    return list_detail.object_list(
        request,
        queryset = ShopProduct.objects.filter(product=product),
        paginate_by = 30,
        page = page,
        template_name = template_name,
        extra_context = {'product':product, 'categories':categories, 'price_list':price_list},
        **kwargs)

def shop_list(request, page=0, template_name='fprice/shop_list.html', **kwargs):
    children = ShopCategory.objects.filter(parent__isnull=True)
    return list_detail.object_list(
        request,
        queryset = Shop.objects.all(),
        paginate_by = 30,
        page = page,
        template_name = template_name,
        extra_context = {'children':children},
        **kwargs)

def shopnet_list(request, page=0, template_name='fprice/shopnet_list.html', **kwargs):
    return list_detail.object_list(
        request,
        queryset = ShopNet.objects.all(),
        paginate_by = 30,
        page = page,
        template_name = template_name,
        **kwargs)

def shopnet_detail(request, slug, page=0, template_name='fprice/shopnet_list.html', **kwargs):
    shopnet = ShopNet.objects.get(slug=slug)
    return list_detail.object_list(
        request,
        queryset = Shop.objects.filter(net=shopnet),
        paginate_by = 30,
        page = page,
        template_name = template_name,
        extra_context = {'shopnet':shopnet},
        **kwargs)

def shop_category(request, slug, page=0, template_name='fprice/shop_list.html', **kwargs):
    category = ShopCategory.objects.get(slug=slug)
    subcategories = category.get_descendants(include_self=True)
    categories = category.get_ancestors()
    children = category.get_children()
    return list_detail.object_list(
        request,
        queryset = Shop.objects.filter(category__in=subcategories),
        paginate_by = 30,
        page = page,
        template_name = template_name,
        extra_context = {'category':category,'categories':categories,'children':children},
        **kwargs)

def shop_detail(request, shop_id, page=0, template_name='fprice/shop_detail.html', **kwargs):
    shop = Shop.objects.get(id=shop_id)
    queryset = ShopProduct.objects.filter(shop=shop).select_related('shop','product','last_price')
    subcategories = ProductCategory.objects.filter(id__in=queryset.values('product__category'))
    return list_detail.object_list(
        request,
        queryset = queryset,
        paginate_by = 30,
        page = page,
        template_name = template_name,
        extra_context = {'shop':shop, 'subcategories':subcategories},
        **kwargs)

def shop_detail_category(request, shop_id, cat_slug, page=0, template_name='fprice/shop_detail_category.html', **kwargs):
    shop = Shop.objects.get(id=shop_id)
    category = ProductCategory.objects.get(slug=cat_slug)
    queryset = ShopProduct.objects.filter(shop=shop).filter(product__category=category).select_related('shop','product','last_price')
    return list_detail.object_list(
        request,
        queryset = queryset,
        paginate_by = 30,
        page = page,
        template_name = template_name,
        extra_context = {'shop':shop, 'category':category},
        **kwargs)

def product_and_shop(request, product_id, shop_id, page=0, template_name='fprice/prodshop_detail.html', **kwargs):
    product = Product.objects.get(id=product_id)
    try:
        categories = product.category.get_ancestors()
    except:
        categories = None
    shop = Shop.objects.get(id=shop_id)
    shopprod = ShopProduct.objects.get(product=product,shop=shop)
    shop_list = Shop.objects.filter(pk=shop_id)
    return list_detail.object_list(
        request,
        queryset = Price.objects.filter(shop_product=shopprod).select_related(),
        paginate_by = 30,
        page = page,
        template_name = template_name,
        extra_context = {'shop':shop, 'product':product, 'shop_list':shop_list, 'categories':categories},
        **kwargs)

@login_required
def summary_list(request, page=0, template_name='fprice/summary_list.html', **kwargs):
    queryset = Summary.objects.filter(user=request.user).filter(time__gt=datetime.datetime.now()-datetime.timedelta(days=30)).select_related('shop','user')
    summary_sum = queryset.aggregate(Sum('summary'))
    shop_list = Summary.objects.filter(user=request.user).order_by('shop').values('shop','shop__title').annotate(count=Count('shop')).order_by('-count')[:20]
    #month_list = Summary.objects.filter(time__gt=datetime.datetime.now()-datetime.timedelta(days=365)).dates('time','month',order='DESC')
    month_list = Summary.objects.filter(user=request.user).filter(time__gt=datetime.datetime.now()-datetime.timedelta(days=365)).extra(select={'year': connections[Summary.objects.db].ops.date_extract_sql('year', 'time'), 'month': connections[Summary.objects.db].ops.date_extract_sql('month', 'time')}).values('year','month').annotate(sum=Sum('summary')).order_by('-year','-month')
    return list_detail.object_list(
        request,
        queryset = queryset,
        paginate_by = 30,
        page = page,
        template_name = template_name,
        extra_context = {'sum':summary_sum, 'month_list': month_list, 'shop_list': shop_list},
        **kwargs)

@login_required
def summary_archive_year(request, year, page=0, template_name='fprice/summary_archive_year.html', **kwargs):
    queryset = Summary.objects.filter(user=request.user).filter(time__year=year).select_related('shop','user')
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
    queryset = Summary.objects.filter(user=request.user).filter(time__year=year, time__month=month).select_related('shop','user')
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
        queryset = Trade.objects.filter(summary=summary).select_related(),
        paginate_by = 30,
        page = page,
        template_name = template_name,
        extra_context = {'summary':summary},
        **kwargs)

@login_required
def price_list(request, page=0, template_name='fprice/price_list.html', **kwargs):
    return list_detail.object_list(
        request,
        queryset = Price.objects.filter(user=request.user).select_related(),
        paginate_by = 30,
        page = page,
        template_name = template_name,
        **kwargs)

@staff_member_required
def price_admin(request, page=0, template_name='fprice/price_list.html', **kwargs):
    return list_detail.object_list(
        request,
        queryset = Price.objects.all().select_related(),
        paginate_by = 30,
        page = page,
        template_name = template_name,
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

                    # check existing shop_product or add new
                    try:
                        new_shopprod = ShopProduct.objects.get(shop=shop,product=product)
                    except ShopProduct.DoesNotExist:
                        new_shopprod = None
                    if new_shopprod == None:
                        new_shopprod = ShopProduct()
                        new_shopprod.shop = shop
                        new_shopprod.product = product
                        new_shopprod.save()

                    # check existing price or add new
                    newer_price = None
                    new_price = None

                    try:
                        older_price = Price.objects.filter(shop_product=new_shopprod, time__lt=forma.cleaned_data['time'], currency=forma.cleaned_data['currency'])[0]
                    except IndexError:
                        older_price = None
                        try:
                            newer_price = Price.objects.order_by('last_time_update').filter(shop_product=new_shopprod, last_time_update__gt=forma.cleaned_data['time'], currency=forma.cleaned_data['currency'])[0]
                        except IndexError:
                            newer_price = None

                    if older_price:
                        if older_price.price == form.cleaned_data['price_visual']:
                            older_price.last_user_update = request.user
                            if forma.cleaned_data['time'] > older_price.last_time_update:
                                older_price.last_time_update = forma.cleaned_data['time']
                            older_price.update_counter += 1
                            older_price.save()
                            new_price = older_price
                        elif forma.cleaned_data['time'] < older_price.last_time_update:
                            # split price
                            new_newer_price = Price()
                            new_newer_price.user = older_price.last_user_update
                            new_newer_price.last_user_update = older_price.last_user_update
                            new_newer_price.time = older_price.last_time_update
                            new_newer_price.last_time_update = older_price.last_time_update
                            new_newer_price.shop_product = new_shopprod
                            new_newer_price.price = older_price.price
                            new_newer_price.currency = older_price.currency
                            new_newer_price.save()
                            older_price.last_user_update = older_price.user
                            older_price.last_time_update = older_price.time
                            older_price.update_counter = 0
                            older_price.save()
                    elif newer_price and newer_price.price == form.cleaned_data['price_visual']:
                        newer_price.last_user_update = request.user
                        newer_price.time = forma.cleaned_data['time']
                        newer_price.update_counter += 1
                        newer_price.save()
                        new_price = newer_price

                    if not new_price:
                        new_price = Price()
                        new_price.user = request.user
                        new_price.last_user_update = request.user
                        new_price.time = forma.cleaned_data['time']
                        new_price.last_time_update = forma.cleaned_data['time']
                        new_price.shop_product = new_shopprod
                        new_price.price = form.cleaned_data['price_visual']
                        new_price.currency = forma.cleaned_data['currency']
                        new_price.save()
                        
                    # update shop_product last_price
                    if new_shopprod.last_price:
                        if new_shopprod.last_price.last_time_update < new_price.last_time_update:
                            new_shopprod.last_price = new_price
                            new_shopprod.save()
                    else:
                            new_shopprod.last_price = new_price
                            new_shopprod.save()

                    # save trade if it is not spy
                    if not forma.cleaned_data['spytrade']:
                        new_trade = form.save(commit=False)
                        #new_trade.customer = request.user
                        #new_trade.time = forma.cleaned_data['time']
                        new_trade.price = new_price
                        new_trade.amount = form.cleaned_data['amount']
                        new_trade.cost = cost
                        new_trade.summary = new_summ
                        new_trade.save()
                        form.save_m2m()

            return HttpResponseRedirect(reverse('price_summary_list'))
    else:
        forma = TitleForm()
        formset = TradeFormSet()

    return direct_to_template(request, 'fprice/trade_add.html',{'formset':formset, 'forma':forma})

@login_required
def shop_edit_featured(request, shop_id, page=0, template_name='fprice/shop_edit_featured.html', **kwargs):
    shop = Shop.objects.get(id=shop_id)
    products = Product.objects.filter(is_featured=True)
    PriceFormSetA = formset_factory(PriceForm, extra=0)

    if request.method == 'POST':
        formset = PriceFormSetA(request.POST)

        if formset.is_valid():
            for form in formset.forms:
                if form.has_changed() and form.cleaned_data['price_visual']:
                    # check shop_product
                    product = Product.objects.get(id=form.cleaned_data['product'])

                    # check existing shop_product or add new
                    try:
                        new_shopprod = ShopProduct.objects.get(shop=shop,product=product)
                    except ShopProduct.DoesNotExist:
                        new_shopprod = None
                    if new_shopprod == None:
                        new_shopprod = ShopProduct()
                        new_shopprod.shop = shop
                        new_shopprod.product = product
                        new_shopprod.save()

                    # check existing price or add new
                    try:
                        new_price = Price.objects.get(shop_product=new_shopprod, price=form.cleaned_data['price_visual'])
                    except Price.DoesNotExist:
                        new_price = None
                    if (new_price == None):
                        # TODO form has changed not working
                        new_price = Price()
                        new_price.user = request.user
                        new_price.last_user_update = request.user
                        new_price.time = datetime.datetime.now()#forma.cleaned_data['time']
                        new_price.last_time_update = datetime.datetime.now()#forma.cleaned_data['time']
                        new_price.shop_product = new_shopprod
                        new_price.price = form.cleaned_data['price_visual']
                        new_price.currency = 'rur'#forma.cleaned_data['currency']
                        new_price.save()
                    else:
                        if datetime.datetime.now() > new_price.last_time_update:
                            new_price.last_user_update = request.user
                            new_price.last_time_update = datetime.datetime.now()#forma.cleaned_data['time']
                        if datetime.datetime.now() < new_price.time:
                            new_price.time = datetime.datetime.now()#forma.cleaned_data['time']
                        new_price.update_counter += 1
                        new_price.save()

                    # update shop_product last_price
                    # TODO check if not last_price
                    if new_shopprod.last_price:
                        if new_shopprod.last_price.last_time_update < new_price.last_time_update:
                            new_shopprod.last_price = new_price
                            new_shopprod.save()
                    else:
                            new_shopprod.last_price = new_price
                            new_shopprod.save()

            return HttpResponseRedirect(reverse('price_shop_detail', args=[shop_id]))
    else:
        initial_data_list = []
        for item in products:
            initial_data_list.append({'product':item.id, 'product_visual':item.title})
        formset = PriceFormSetA(initial=initial_data_list)

    return direct_to_template(request, 'fprice/shop_edit_featured.html',{'shop':shop, 'formset':formset})

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
