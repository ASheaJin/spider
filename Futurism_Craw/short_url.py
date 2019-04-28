# 1437d14095c53d1c9e7258c1094047eb
# 828375184

# !/usr/bin/python
# -*- coding: utf-8 -*-
import requests

def Convert_SINA_Short_Url(source,long_url):
    data = {
        'source':source,
        'url_long':long_url
    }
    address = 'http://api.t.sina.com.cn/short_url/shorten.json'

    r = requests.get(address,params=data)
    short_url = r.json()[0].get('url_short')
    print(short_url)
    return short_url