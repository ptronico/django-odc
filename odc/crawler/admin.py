# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import URL


class URLAdmin(admin.ModelAdmin):
    list_display = ['url', 'updated', 'is_rawdata_fetched', 'is_rawdata_parsed']
    list_filter = ['is_rawdata_fetched', 'is_rawdata_parsed']
    search_fields = ['url']

admin.site.register(URL, URLAdmin)