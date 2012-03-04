#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
import mptt
from datetime import datetime


class City(models.Model):
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return u"%s" % (self.title)

    class Meta:
        ordering = ["title"]


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    city = models.ForeignKey(City, blank=True, null=True)

    def __unicode__(self):
        return u"%s" % (self.user)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
User.get_profile = lambda u: UserProfile.objects.get_or_create(user=u)[0]


class Shop(models.Model):
    title = models.CharField(max_length=200)
    city = models.ForeignKey(City, blank=True, null=True)

    def __unicode__(self):
        return u"%s" % (self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('fprice.views.shop_detail',[unicode(self.id)])

    class Meta:
        ordering = ["title"]


class ProductCategory(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, max_length=50)
    description = models.TextField(blank=True)
    position = models.PositiveIntegerField(default=0)

    parent = models.ForeignKey('self', null=True, blank=True,
                               related_name='children')

    def __unicode__(self):
        return u"%s" % (self.title)

    @property
    def tree_path(self):
        """Return category's tree path, by his ancestors"""
        #if self.parent:
        #    return '%s/%s' % (self.parent.tree_path, self.slug)
        return self.slug

    @models.permalink
    def get_absolute_url(self):
        """Return category's URL"""
        return ('price_product_category', (self.tree_path,))

    class Meta:
        ordering = ["title"]

mptt.register(ProductCategory, order_insertion_by=['title'])


UNIT_CHOICES = (
    ('sh', 'шт'),
    ('kg', 'кг'),
    ('l', 'л'),
    ('m', 'м'),
    ('gr', 'гр'),
)

class Product(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(ProductCategory, null=True, blank=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return u"%s" % (self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('fprice.views.product_detail',[unicode(self.id)])

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


class Summary(models.Model):
    user = models.ForeignKey(User)
    time = models.DateTimeField(default=datetime.now)
    time_added = models.DateTimeField(default=datetime.now,editable=False) # actual time

    shop = models.ForeignKey(Shop, blank=True, null=True)
    summary = models.DecimalField(max_digits=19, decimal_places=2)
    currency = models.CharField(max_length=3,choices=CURR_CHOICES,default='rur')

    def __unicode__(self):
        return u"%s %s - %s" % (self.summary, self.currency, self.time)

    @models.permalink
    def get_absolute_url(self):
        return ('fprice.views.summary_detail',[unicode(self.id)])

    def get_abs_summary(self):
        return u"%.2f" % (abs(self.summary))
    get_abs_summary.short_description = "Absolute summary"

    class Meta:
        ordering = ["-time"]


class Trade(models.Model):
    customer = models.ForeignKey(User)
    time = models.DateTimeField(default=datetime.now) #(auto_now_add=True)
    time_added = models.DateTimeField(default=datetime.now,editable=False)

    price = models.ForeignKey(Price)
    amount = models.FloatField()
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    summary = models.ForeignKey(Summary, blank=True, null=True)

    def __unicode__(self):
        return u"%s - %s" % (self.price.product, self.amount)

    def get_price(self):
        return u"%s %s" % (self.price.price, self.price.currency)
    get_price.short_description = "Price"

    class Meta:
        ordering = ["-time"]

