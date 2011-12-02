#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import url, patterns
from fprice.app_settings import USE_ROOT_URL

urlpatterns = patterns('fprice.views',

    url(r'^search/$', view='search', name='price_search'),

    url(r'^shops/$', view='shop_list', name='price_shop_list'),
    url(r'^shops/(?P<shop_id>\d+)/$', view='shop_detail', name='price_shop_detail'),

    url(r'^products/$', view='product_list', name='price_product_list'),
    url(r'^products/(?P<product_id>\d+)/$', view='product_detail', name='price_product_detail'),

    url(r'^products/(?P<product_id>\d+)/shop/(?P<shop_id>\d+)/$', view='product_and_shop', name='price_prodshop_detail'),
    url(r'^products/category/(?P<slug>\w+)/$', view='product_category', name='price_product_category'),

    url(r'^prices/$', view='price_list', name='price_list'),
    url(r'^prices/admin/$', view='price_admin', name='price_admin'),
    url(r'^prices/(?P<price_id>\d+)/up/$', view='price_up', name='price_up'),

    url(r'^trades/$', view='trade_list', name='price_trade_list'),
    url(r'^trades/admin/$', view='trade_admin', name='price_trade_admin'),
    url(r'^trades/add/$', view='trade_add', name='price_trade_add'),
    url(r'^lookup/(shop|product)/$', view='lookup', name='json_lookup'),

    url(r'^summary/$', view='summary_list', name='price_summary_list'),
    url(r'^summary/(?P<summary_id>\d+)/$', view='summary_detail', name='price_summary_detail'),

)

if USE_ROOT_URL:
    urlpatterns += patterns('fprice.views',
        url(r'^$', view='product_list', name='price_index'),
    )
else:
    urlpatterns += patterns('fprice.views',
        url(r'^products/$', view='product_list', name='price_index'),
    )
