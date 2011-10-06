#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from django.forms.formsets import formset_factory
from fprice.models import Trade, Shop
import datetime

class TitleForm(forms.ModelForm):
    shop_visual = forms.CharField(max_length=200, label="Shop")
    shop = forms.CharField(widget=forms.HiddenInput, max_length=200, required=False)

    class Meta:
        model = Trade
        fields = ('spytrade', 'time', 'shop_visual', 'currency')

    def __init__(self, *args, **kwargs):
        super(TitleForm, self).__init__(*args, **kwargs)
        self.fields['shop_visual'].widget.attrs['size'] = 50

class TradeForm(forms.ModelForm):
    product_visual = forms.CharField(max_length=200, label="Product", required=True)
    product = forms.CharField(widget=forms.HiddenInput, max_length=200, required=False)

    class Meta:
        model = Trade
        fields = ('product_visual', 'amount', 'cost')
        #exclude = ('customer', 'price')

    def __init__(self, *args, **kwargs):
        super(TradeForm, self).__init__(*args, **kwargs)
        self.fields['product_visual'].widget.attrs['size'] = 50
        self.fields['amount'].widget.attrs['size'] = 8
        self.fields['cost'].widget.attrs['size'] = 9

TradeFormSet = formset_factory(TradeForm)
