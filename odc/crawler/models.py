# -*- coding: utf-8 -*-

from django.utils import timezone
from django.db import models, connection, transaction
from django.dispatch import Signal, receiver


class URLManager(models.Manager):

    def bulk_create_url(self, url_list):

        now = timezone.now().astimezone(timezone.get_default_timezone())

        query = """
            INSERT IGNORE INTO crawler_url (url, rawdata, updated, 
                created, is_rawdata_parsed, is_rawdata_fetched) 
            VALUES (%s, '', %s, %s, 0, 0); 
        """

        params = []
        for url in url_list:
            params.append((url, now.strftime('%Y-%m-%d %H:%M:%S'), 
                now.strftime('%Y-%m-%d %H:%M:%S')))

        cursor = connection.cursor()            
        affected = cursor.executemany(query, params)
        transaction.commit_unless_managed()
        cursor.close()

        return affected

    def get_unparsed_urls(self):
        return self.filter(is_rawdata_fetched=True, 
            is_rawdata_parsed=False).order_by('id')

    def get_unfetched_urls(self):
        return self.filter(is_rawdata_fetched=False).order_by('id')


class URL(models.Model):

    url = models.URLField(unique=True)
    rawdata = models.TextField(blank=True)        
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    is_rawdata_parsed = models.BooleanField(
        verbose_name='Parsed', default=False)
    is_rawdata_fetched = models.BooleanField(
        verbose_name='Fetched', default=False)
    
    objects = URLManager()

    class Meta:
        ordering = ['url', ]

    def __unicode__(self):
        return '%s' % self.url

# Sinais

url_pre_fetch = Signal(providing_args=['instance'])
url_post_fetch = Signal(providing_args=['instance'])

url_pre_parse = Signal(providing_args=['instance'])
url_post_parse = Signal(providing_args=['instance'])