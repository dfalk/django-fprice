#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db.models import get_model
from django.template import Library, Node
from django.template import TemplateSyntaxError
import datetime

register = Library()

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

class LatestCountNode(Node):
    def __init__(self, model, num, varname):
        self.num, self.varname = num, varname
        self.model = get_model(*model.split('.'))
        
    def render(self, context):
        context[self.varname] = self.model._default_manager.filter(time_added__gt=datetime.datetime.now()-datetime.timedelta(days=self.num))
        return ''

def get_count(parser, token):
    """
    Usage: {% get_count <app.model> <days> as <var> %}
    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_count tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_latest tag must be 'as'"
    return LatestContentNode(bits[1], bits[2], bits[4])
get_count = register.tag(get_count)
