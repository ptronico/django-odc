# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from ...models import URL
from ...engine.fetcher import fetch_url
from ...engine.parser import parse_url


class Command(BaseCommand):
    args = '<fetch parse>'
    help = 'Capta e analisa de URLs.'.decode('utf-8')

    def handle(self, *args, **options):

        if 'fetch' in args:
            for url in URL.objects.get_unfetched_urls():
                fetch_url(url)

        if 'parse' in args:
            for url in URL.objects.get_unparsed_urls():
                parse_url(url)