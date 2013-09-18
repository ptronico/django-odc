# -*- coding: utf-8 -*-

import requests
import urlparse
import posixpath

from bs4 import BeautifulSoup

from django.core.validators import URLValidator
from ..models import URL, url_pre_parse, url_post_parse


BASE_DOMAIN = 'olavodecarvalho.org'
BASE_ADDRESS = 'http://www.olavodecarvalho.org'


def is_absolute_url_valid(absolute_url):
    """ 
    Retorna verdadeiro se `absolute_url` é uma URL absoluta e válida.
    """
    return True if URLValidator.regex.match(absolute_url) else False


def resolve_components(absolute_url):
    """
    Resolve eventuais caminhos erradoss na `absolute_url`.
    http://stackoverflow.com/questions/4317242/python-how-to-resolve-urls-containing
    """
    parsed = urlparse.urlparse(absolute_url)
    new_path = posixpath.normpath(parsed.path)
    if parsed.path.endswith('/'):
        new_path += '/'
    cleaned = parsed._replace(path=new_path)
    return cleaned.geturl()


def parse_url(url):
    """
    Analisa o conteúdo da URL e busca por outros links internos 
    (do mesmo site.)
    """
    url_pre_parse.send(sender=URL, instance=url)
    
    soup = BeautifulSoup(url.rawdata)    

    # Varrendo os links contidos na página
    absolute_url_set = set()
    for link in soup.find_all('a'):
        
        if link.get('href', None) is None:
            continue

        # Resolvendo links com caminhos relativos
        absolute_url = resolve_components(urlparse.urljoin(
            url.url, link.get('href', None)))
        
        # Evitando emails e URLs externas
        if is_absolute_url_valid(absolute_url) and \
            BASE_DOMAIN in absolute_url:
            absolute_url_set.add(absolute_url)    

    # Validando cada URL (pode levar alguns minutos)
    validated_absolute_url_set = set()
    for absolute_url in absolute_url_set:
        request = requests.get(absolute_url)
        validated_absolute_url_set.add(request.url)

    # Salvando novas URLs
    URL.objects.bulk_create_url(validated_absolute_url_set)

    # Atualizando a URL que sofreu parser
    url.is_rawdata_parsed = True
    url.save()

    url_post_parse.send(sender=URL, instance=url)

