#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.db import models
from fprice.models import Trade, Shop

class TradeForm(forms.ModelForm):
    shop_pk = forms.IntegerField(widget=forms.HiddenInput, required=False)
    product_pk = forms.IntegerField(widget=forms.HiddenInput, required=False)
    shop = forms.CharField(max_length=200)
    product = forms.CharField(max_length=200)

    class Meta:
        model = Trade
        fields = ('spytrade', 'time', 'shop', 'product', 'amount', 'cost', 'currency')
        exclude = ('customer', 'price')

    def __init__(self, *args, **kwargs):
        super(TradeForm, self).__init__(*args, **kwargs)
        self.fields['shop'].widget.attrs['size'] = 40
        self.fields['product'].widget.attrs['size'] = 40
