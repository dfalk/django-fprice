#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db.models import get_model
from django.template import Library, Node
from django.template import TemplateSyntaxError
from django.utils.dates import MONTHS
import datetime

register = Library()

@register.filter
def month_name(month_number):
    return MONTHS[int(month_number)]

class LatestContentNode(Node):
    def __init__(self, model, num, varname):
        self.num, self.varname = num, varname
        self.model = get_model(*model.split('.'))
        
    def render(self, context):
        context[self.varname] = self.model._default_manager.all()[:self.num]
        return ''

def get_latest(parser, token):
    """
    Usage: {% get_latest <app.model> <count> as <var> %}
    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_latest tag must be 'as'"
    return LatestContentNode(bits[1], bits[2], bits[4])
get_latest = register.tag(get_latest)

class FeaturedContentNode(Node):
    def __init__(self, model, num, varname):
        self.num, self.varname = num, varname
        self.model = get_model(*model.split('.'))
        
    def render(self, context):
        context[self.varname] = self.model._default_manager.filter(is_featured=True)[:self.num]
        return ''

def get_featured(parser, token):
    """
    Usage: {% get_featured <app.model> <count> as <var> %}
    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_featured tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_latest tag must be 'as'"
    return FeaturedContentNode(bits[1], bits[2], bits[4])
get_featured = register.tag(get_featured)

class LatestCounterNode(Node):
    def __init__(self, model, num, varname):
        self.num, self.varname = int(num), varname
        self.model = get_model(*model.split('.'))
        
    def render(self, context):
        context[self.varname] = self.model._default_manager.filter(time_added__gt=datetime.datetime.now()-datetime.timedelta(days=self.num)).count()
        return ''

def get_counter(parser, token):
    """
    Usage: {% get_counter <app.model> <days> as <var> %}
    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_counter tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_counter tag must be 'as'"
    return LatestCounterNode(bits[1], bits[2], bits[4])
get_counter = register.tag(get_counter)
