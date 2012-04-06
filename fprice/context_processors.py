#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fprice.app_settings import SHOW_PRICE_BREADCRUMB, SHOW_PRICE_TITLE


def settings(request):

    context_dict = {
        'FPRICE_SHOW_PRICE_BREADCRUMB': SHOW_PRICE_BREADCRUMB,
        'FPRICE_SHOW_PRICE_TITLE': SHOW_PRICE_TITLE,
    }

    return context_dict
