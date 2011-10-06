#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.db import models
from fprice.models import Trade, Shop

class TradeForm(forms.ModelForm):
    shop_visual = forms.CharField(max_length=200, label="Shop")
    product_visual = forms.CharField(max_length=200, label="Product")
    shop = forms.CharField(widget=forms.HiddenInput, max_length=200, required=False)
    product = forms.CharField(widget=forms.HiddenInput, max_length=200, required=False)

    class Meta:
        model = Trade
        fields = ('spytrade', 'time', 'shop_visual', 'product_visual', 'amount', 'cost', 'currency')
        exclude = ('customer', 'price')

    def __init__(self, *args, **kwargs):
        super(TradeForm, self).__init__(*args, **kwargs)
        self.fields['shop_visual'].widget.attrs['size'] = 50
        self.fields['product_visual'].widget.attrs['size'] = 50
