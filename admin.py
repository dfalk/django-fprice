#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from fprice.models import Section, Product, Trade, Shop, Price
from fprice.forms import TradeForm

class TradeAdmin(admin.ModelAdmin):
    #form = TradeForm
    actions = ['make_spy']
    exclude = ('customer',)
    list_display = ['__unicode__', 'get_price', 'cost', 'time', 'customer']

    def make_spy(self, request, queryset):
        rows_updated = queryset.update(spytrade=True)
        #if rows_updated == 1:
        # message_bit = "1 покупка была"
        #else:
        # message_bit = "%s покупок было" % rows_updated
        #self.message_user(request, "%s отмечено как подсмотренные." % message_bit)
    make_spy.short_description = 'Mark as spy'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.customer = request.user
            # TODO update price
            #obj.price = "%.2f" % ( float(obj.cost) / float(obj.amount) )
        obj.save()

class PriceAdmin(admin.ModelAdmin):
    #form = TradeForm
    exclude = ('user','last_user_update','time','last_time_update', 'update_counter',)
    list_display = ['__unicode__', 'last_time_update', 'last_user_update']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.customer = request.user
        obj.save()

admin.site.register(Section)
admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(Trade, TradeAdmin)
admin.site.register(Price, PriceAdmin)
