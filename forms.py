#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from fprice.models import Trade

class TradeForm(forms.ModelForm):

    class Meta:
        model = Trade

