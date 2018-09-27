# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Records, Leaves, CalcSalary, Documents, CompanyInfo

# Register your models here.
admin.site.register(Records)
admin.site.register(Leaves)
admin.site.register(CalcSalary)
admin.site.register(Documents)
admin.site.register(CompanyInfo)