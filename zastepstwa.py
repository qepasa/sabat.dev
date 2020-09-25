import collections
import pprint
import random
import re
from datetime import datetime

import requests
import xmltodict
from bs4 import BeautifulSoup

AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
]

date_today = datetime.now()
date_today = f"{date_today.year}-{str(date_today.month).rjust(2,'0')}-{str(date_today.day-16).rjust(2,'0')}"

url = "https://v-lo-krakow.edupage.org/substitution/server/viewer.js?__func=getSubstViewerDayDataHtml"
resp = requests.post(
    url,
    headers={
        "User-Agent": random.choice(AGENTS),
        "Origin": "https://v-lo-krakow.edupage.org",
        "Referer": "https://v-lo-krakow.edupage.org/substitution/",
    },
    json={
        "__args": [None, {"date": date_today, "mode": "classes"}],
        "__gsh": "00000000",
    },
)
print(date_today)

classes = {}
resp_html = BeautifulSoup(resp.json()["r"], features="lxml")

for cls in resp_html.find_all("div", class_="section print-nobreak"):
    cls_name = cls.find("span", class_="print-font-resizable").text
    rm_list = []

    for removed in cls.find_all("div", class_="row remove"):
        div_idx = removed.find("div", class_="period")
        span_idx = div_idx.find("span", class_="print-font-resizable")
        span_idx = span_idx.text

        div_info = removed.find("div", class_="info")
        span_info = div_info.find("span", class_="print-font-resizable")
        span_info = span_info.text

        rm_list.append((span_idx, span_info))

    classes[cls_name] = rm_list
resp = {}
for key, value in classes.items():
    resp[key.upper()] = value

pprint.pprint(resp)
