#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from django.forms.formsets import formset_factory
from fprice.models import Trade, Shop, CURR_CHOICES
import datetime

class TitleForm(forms.ModelForm):
    shop_visual = forms.CharField(max_length=200, label="Shop")
    shop = forms.CharField(widget=forms.HiddenInput, max_length=200, required=False)
    currency = forms.ChoiceField(choices=CURR_CHOICES, initial='rur')
    spytrade = forms.BooleanField(initial=False, required=False) # if true it makes only price instance without trade
    summary = forms.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        model = Trade
        fields = ('spytrade', 'time', 'shop_visual')

    def __init__(self, *args, **kwargs):
        super(TitleForm, self).__init__(*args, **kwargs)
        self.fields['shop_visual'].widget.attrs['size'] = 50
        self.fields['shop_visual'].widget.attrs['autofocus'] = 'autofocus'
        self.fields['time'].widget.attrs['size'] = 16
        self.fields['time'].widget.format = '%d.%m.%Y %H:%M'
        self.fields['summary'].widget.attrs['size'] = 10

class TradeForm(forms.ModelForm):
    product_visual = forms.CharField(max_length=200, label="Product", required=True)
    product = forms.CharField(widget=forms.HiddenInput, max_length=200, required=False)
    price_visual = forms.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        model = Trade
        fields = ('product_visual', 'price_visual', 'amount')
        #exclude = ('customer', 'price')

    def __init__(self, *args, **kwargs):
        super(TradeForm, self).__init__(*args, **kwargs)
        self.fields['product_visual'].widget.attrs['size'] = 50
        self.fields['price_visual'].widget.attrs['size'] = 10
        self.fields['amount'].widget.attrs['size'] = 9

TradeFormSet = formset_factory(TradeForm)
