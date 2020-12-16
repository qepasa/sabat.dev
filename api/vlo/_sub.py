import datetime
import random
import math

import requests
import flask
import flask.blueprints
from bs4 import BeautifulSoup
import flask_caching

from api.__vars import *

api = flask.blueprints.Blueprint('sub', __name__, url_prefix='/api')
cache = flask_caching.Cache(config=CONFIG)

@cache.cached()
@api.route('/sub', methods=['GET'])
def sub():
	try:
		if 'c' in flask.request.args.keys():
			klass = flask.request.args['c'].upper()
		else:
			return flask.jsonify({"success":False,"error":""}), 406

		if klass not in CLASS_KEY.keys():
			return flask.jsonify({"success":False,"error":""}), 406

		if 'o' not in flask.request.args.keys():
			offset = 0
		else:
			offset = int(flask.request.args['o'])
		
		date_today = datetime.datetime.now() + offset*datetime.timedelta(days=1)
		date_today = f"{date_today.year}-{str(date_today.month).rjust(2,'0')}-{str(date_today.day).rjust(2,'0')}"

		resp = requests.post(
			URL_RP,
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

		for key, val in classes.items():
			resp[key.upper()] = val
		for key, val in resp.items():
			resp[key.upper()] = val

		if klass in resp.keys():
			return flask.jsonify({"success":True,"resp": resp[klass.upper()]}), 200
		else:
			return flask.jsonify({"success":True,"resp": []}), 200

	except Exception as error:
		return flask.jsonify({"success":False,"error":str(error)}), 406
