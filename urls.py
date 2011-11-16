#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('fprice.views',

    #url(r'^$', view='price_list', name='price_index'),
    url(r'^products/$', view='price_list', name='price_index'),
    url(r'^products/(?P<product_id>\d+)/$', view='product_detail', name='price_product_detail'),

    url(r'^search/$', view='search', name='price_search'),

    url(r'^shops/$', view='shop_list', name='price_shop_list'),
    url(r'^shops/(?P<shop_id>\d+)/$', view='shop_detail', name='price_shop_detail'),

    url(r'^products/(?P<product_id>\d+)/shop/(?P<shop_id>\d+)/$', view='product_and_shop', name='price_prodshop_detail'),

    url(r'^prices/(?P<price_id>\d+)/up/$', view='price_up', name='price_up'),

    url(r'^trade/$', view='trade_list', name='price_trade_list'),
    url(r'^trade/admin/$', view='trade_admin', name='price_trade_admin'),
    url(r'^trade/add/$', view='trade_add', name='price_trade_add'),
    url(r'^lookup/(shop|product)/$', view='lookup', name='json_lookup'),

)
