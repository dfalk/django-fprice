#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings

USE_ROOT_URL = getattr(settings, 'FPRICE_USE_ROOT_URL', 'True')
