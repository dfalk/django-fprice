#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings

SHOW_PRICE_BREADCRUMB = getattr(settings, 'FPRICE_SHOW_PRICE_BREADCRUMB', 'True')
SHOW_PRICE_TITLE = getattr(settings, 'FPRICE_SHOW_PRICE_TITLE', 'True')
USE_ROOT_URL = getattr(settings, 'FPRICE_USE_ROOT_URL', 'True')
