# -*- coding: utf-8 -*
import time
import json
import requests

def to_local_time(epoch):
    if not epoch or epoch == 0:
        return ''
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(epoch))

def get_json_data(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        r = requests.get(url, headers=headers)
        assert r.status_code == 200
        return json.loads(r.text)
    except requests.exceptions.ConnectionError:
        print('ConnectionError. Please make sure your network is ok')
        exit()
    except AssertionError:
        print(f'Some problem occur when request {url}. Please make sure your api key is valid.')
        exit()