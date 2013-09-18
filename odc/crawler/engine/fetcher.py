# -*- coding: utf-8 -*-

import requests

from ..models import URL, url_pre_fetch, url_post_fetch


def fetch_url(url):
    """ 
    Coleta dados de uma `url`. 
    """
    url_pre_fetch.send(sender=URL, instance=url)

    request = requests.get(url)
    
    url.is_rawdata_fetched = True
    url.rawdata = request.text
    url.save()

    url_post_fetch.send(sender=URL, instance=url)