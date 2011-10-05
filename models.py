#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Shop(models.Model):
    title = models.CharField(max_length=200)

    def __unicode__(self):
        return u"%s" % (self.title)

    class Meta:
        ordering = ["title"]


class Section(models.Model):
    title = models.CharField(max_length=50)

    def __unicode__(self):
        return u"%s" % (self.title)

    class Meta:
        ordering = ["title"]


UNIT_CHOICES = (
    ('sh', 'шт'),
    ('kg', 'кг'),
    ('l', 'л'),
    ('m', 'м'),
    ('gr', 'гр'),
)

class Product(models.Model):
    title = models.CharField(max_length=200)
    unit = models.CharField(max_length=5, choices=UNIT_CHOICES)
    section = models.ForeignKey(Section, null=True, blank=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return u"%s" % (self.title)

    class Meta:
        ordering = ["title"]


CURR_CHOICES = (
    ('rur','руб'),
    ('usd','usd'),
    ('eur','eur'),
)

"""
class Price(models.Model):
    user = models.ForeignKey(User)
    shop = models.ForeignKey(Shop)
    product = models.ForeignKey(Product)
    time_added = models.DateTimeField(default=datetime.now,editable=False) #auto
    time_first = models.DateTimeField(default=datetime.now) #(auto_now_add=True)
    time = models.DateTimeField(default=datetime.now) #(auto_now_add=True)
    count_up = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    currency = models.CharField(max_length=3,choices=CURR_CHOICES)

    def __unicode__(self):
        return u"%s %s (%s)" % (self.product, self.price, self.shop)

    class Meta:
        ordering = ["-time"]
"""


class Trade(models.Model):
    customer = models.ForeignKey(User)
    time = models.DateTimeField(default=datetime.now) #(auto_now_add=True)
    time_added = models.DateTimeField(default=datetime.now,editable=False)
    #price = models.ForeignKey(Price)
    shop = models.ForeignKey(Shop)
    product = models.ForeignKey(Product)
    amount = models.FloatField()
    price = models.DecimalField(max_digits=19, decimal_places=2)
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3,choices=CURR_CHOICES,default='rur')
    spytrade = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s %s" % (self.product, self.amount)

    class Meta:
        ordering = ["-time"]

