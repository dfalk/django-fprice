#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('fprice.views',

    # List views
    url(r'^$', view='price_list', name='price_index'),

    url(r'^add/$', view='price_add', name='price_add'),

)

