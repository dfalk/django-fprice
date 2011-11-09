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

class Price(models.Model):
    user = models.ForeignKey(User)
    time = models.DateTimeField(default=datetime.now)
    time_added = models.DateTimeField(default=datetime.now,editable=False) # actual time

    last_user_update = models.ForeignKey(User, related_name="last_user_update")
    last_time_update = models.DateTimeField(default=datetime.now)
    update_counter = models.IntegerField(default=0)

    shop = models.ForeignKey(Shop)
    product = models.ForeignKey(Product)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    currency = models.CharField(max_length=3,choices=CURR_CHOICES,default='rur')

    def __unicode__(self):
        return u"%s - %s %s (%s)" % (self.product, self.price, self.currency, self.shop)

    class Meta:
        ordering = ["-last_time_update"]


class Trade(models.Model):
    customer = models.ForeignKey(User)
    time = models.DateTimeField(default=datetime.now) #(auto_now_add=True)
    time_added = models.DateTimeField(default=datetime.now,editable=False)

    # FIXME clear code, it has moved to price model
    price = models.ForeignKey(Price)
    #shop = models.ForeignKey(Shop)
    #product = models.ForeignKey(Product)
    #price = models.DecimalField(max_digits=19, decimal_places=2)
    #currency = models.CharField(max_length=3,choices=CURR_CHOICES,default='rur')

    amount = models.FloatField()
    cost = models.DecimalField(max_digits=12, decimal_places=2)

    def __unicode__(self):
        return u"%s - %s" % (self.price.product, self.amount)

    def get_price(self):
        return u"%s %s" % (self.price.price, self.price.currency)
    get_price.short_description = "Price"

    class Meta:
        ordering = ["-time"]

