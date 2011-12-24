#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template
from django.http import HttpResponse, HttpResponseRedirect
from fprice.models import City, UserProfile, Shop, ProductCategory, Product, Price, Trade, Summary
from fprice.forms import TradeForm
from mptt.admin import MPTTModelAdmin


class ProductAdmin(admin.ModelAdmin):
    actions = ['change_category']
    list_display = ['__unicode__', 'category']

    class CategoryForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        category = forms.ModelChoiceField(ProductCategory.objects)

    def change_category(self, request, queryset):
        form = None
        if 'cancel' in request.POST:
            self.message_user(request, 'Canceled items categorization')
            return
        elif 'categorize' in request.POST:
            #do the categorization
            form = self.CategoryForm(request.POST)
            if form.is_valid():
                category = form.cleaned_data['category']
                count = 0
                for item in queryset:
                    item.category = category
                    item.save()
                    count += 1
                plural = ''
                if count != 1:
                    plural = 's'
                self.message_user(request, "Successfully added category %s to %d item%s." % (category, count, plural))
                return HttpResponseRedirect(request.get_full_path())
        if not form:
            form = self.CategoryForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        return direct_to_template(request, 'admin/set_category.html', {'items': queryset, 'form': form, 'path':request.get_full_path()})

    change_category.short_description = 'Set category'


class TradeAdmin(admin.ModelAdmin):
    #form = TradeForm
    actions = ['change_summary']
    list_display = ['__unicode__', 'get_price', 'cost', 'time', 'customer', 'summary']

    class SummaryForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        summary = forms.DecimalField(max_digits=12, decimal_places=2)

    def change_summary(self, request, queryset):
        form = None
        if 'cancel' in request.POST:
            self.message_user(request, 'Canceled items summarization')
            return
        elif 'summarize' in request.POST:
            #do the summarization
            form = self.SummaryForm(request.POST)
            if form.is_valid():
                summary = form.cleaned_data['summary']
                count = 0
                new_summ = Summary()
                new_summ.user = request.user
                new_summ.time = queryset[0].time
                new_summ.time_added = queryset[0].time_added
                new_summ.shop = queryset[0].price.shop
                new_summ.summary = 0 - summary
                new_summ.currency = queryset[0].price.currency
                new_summ.save()
                for item in queryset:
                    item.summary = new_summ
                    item.save()
                    count += 1
                plural = ''
                if count != 1:
                    plural = 's'
                self.message_user(request, "Successfully summarized %d item%s in %s." % (count, plural, summary))
                return HttpResponseRedirect(request.get_full_path())
        if not form:
            form = self.SummaryForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        return direct_to_template(request, 'admin/set_summary.html', {'items': queryset, 'form': form, 'path':request.get_full_path()})

    change_summary.short_description = 'Set summary'

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

class TradeInline(admin.TabularInline):
    model = Trade

class SummaryAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'time', 'user', 'shop']
    inlines = [
        TradeInline,
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()

class PriceAdmin(admin.ModelAdmin):
    #form = TradeForm
    #exclude = ('user','last_user_update','time','last_time_update', 'update_counter',)
    list_display = ['__unicode__', 'last_time_update', 'last_user_update']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()

admin.site.register(City)
admin.site.register(UserProfile)
admin.site.register(Shop)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, MPTTModelAdmin)
admin.site.register(Trade, TradeAdmin)
admin.site.register(Summary, SummaryAdmin)
admin.site.register(Price, PriceAdmin)
