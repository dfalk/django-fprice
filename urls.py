#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('fprice.views',

    # List views
    url(r'^$', view='price_list', name='price_index'),
    url(r'^trade/all/$', view='trade_admin', name='price_trade_admin'),
    url(r'^trade/$', view='trade_list', name='price_trade_list'),
    url(r'^product/(?P<product_id>\d+)/$', view='product_detail', name='price_product_detail'),

    url(r'^trade/add/$', view='trade_add', name='price_trade_add'),
    url(r'^lookup/(shop|product)/$', view='lookup', name='json_lookup'),

)

