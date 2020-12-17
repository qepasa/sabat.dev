import datetime
import random
import itertools

import requests
import flask
import flask.blueprints
import flask_caching

from api.__vars import *

api = flask.blueprints.Blueprint('tta', __name__, url_prefix='/api')
cache = flask_caching.Cache(config=CONFIG)


@cache.cached()
@api.route('/tta', methods=['GET'])
def tta():
	try:
		if 'c' in flask.request.args.keys():
			klass = flask.request.args['c'].upper()
		else:
			return flask.jsonify({"success":False,"error":"No class url parameter."}), 406

		if klass not in DB["VLO"]["CLASS"]["IDR"].keys():
			return flask.jsonify({"success":False,"error":f"{klass} not in class list"}), 406

		if 'o' not in flask.request.args.keys():
			offset = 0
		else:
			offset = int(flask.request.args['o'])

		today = datetime.date.today()
		year = today.year

		last_monday = today + datetime.timedelta(days=-today.weekday())
		next_friday = last_monday + datetime.timedelta(days=4)

		last_monday += datetime.timedelta(weeks=offset)
		next_friday += datetime.timedelta(weeks=offset)

		resp = requests.post(
			url="https://v-lo-krakow.edupage.org/timetable/server/currenttt.js?__func=curentttGetData",
			headers={
				'User-Agent': random.choice(DB["AGENTS"]),
				'Origin': 'https://v-lo-krakow.edupage.org',
				'Referer': 'https://v-lo-krakow.edupage.org/substitution/'
			},
			json={
				'__args': [
					None,
					{
						'year': str(year),
						'datefrom': str(last_monday),
						'dateto': str(next_friday),
						'table': 'classes',
						'id': DB["VLO"]["CLASS"]["IDR"][klass],
						'showColors': True,
						'showIgroupsInClasses': True,
						'showOrig': True
					},
				],
				'__gsh': '00000000',
			}
		)
		resp_json = resp.json()['r']['ttitems']

		for i,obj in enumerate(resp_json):
			year_curr, month_curr, day_curr = [int(x) for x in obj['date'].split('-')]
			day_index = datetime.date(year_curr, month_curr, day_curr) - last_monday
			day_index = day_index.days

			if int(obj['starttime'].split(':')[0]) < 7 and int(obj['endtime'].split(':')[0]) > 18:
				#eg. "6:15" -> ["6","15"] -> "6" -> 6 < 7
				#eg. "21:10" -> ["21","10"] -> "21" -> 21 > 18
				obj['starttime'] = "7:10"
				obj['endtime'] = "17:15"
				obj['durationperiods'] = 11

			hours_start, minutes_start = [int(x) for x in obj['starttime'].split(':')]
			hours_stop, minutes_stop = [int(x) for x in obj['endtime'].split(':')]

			a = datetime.timedelta(hours=hours_start, minutes=minutes_start)
			b = datetime.timedelta(hours=hours_stop, minutes=minutes_stop)

			time_index = DB["VLO"]["TIME"]["MAP"][obj['starttime']]

			try:
				color_ = obj['colors'][0]
			except:
				color_ = "#D0FFD0"

			try:
				duration = int(obj['durationperiods'])
			except:
				duration = 1

			try:
				subj_  = DB["VLO"]["SUBJECTS"]["ID"]["LONG"][obj['subjectid']]
				subj_s = DB["VLO"]["SUBJECTS"]["ID"]["SHORT"][obj['subjectid']]
			except:
				subj_  = None
				subj_s = None

			try:
				teach_ = DB["VLO"]["TEACHERS"]["ID"]["SHORT"][obj['teacherids'][0]]
			except:
				teach_ = None

			try:
				class_ = DB["VLO"]["CLASS"]["ROOM"]["ID"][obj['classroomids'][0]]
			except:
				class_ = None

			try:
				group_ = obj['groupnames'][0]
			except:
				group_ = None
			
			if obj['type'] == 'event':
				try:
					subj_ = obj['name']
				except KeyError:
					subj_ = None
				
				

			resp_json[i] = {
				'subject': subj_,
				#'subject_short': subj_s,
				'teacher': teach_,
				'classroom': class_,
				'color': color_,
				'time_index': time_index,
				'duration': duration,
				'date': obj['date'],
				'day_index': day_index,
				'group': group_
			}

		days = []
		for _,y in itertools.groupby(resp_json, lambda x: x['day_index']):
			days.append(list(y))

		buff = {'0':{},'1':{},'2':{},'3':{},'4':{},}

		for i,day in enumerate(days):
			for x,y in itertools.groupby(day, lambda x: x['time_index']):
				out = list(y)
				buff[str(i)][str(x)] = out
		
		resp = [[x for _,x in x.items()] for _,x in buff.items()]

		return flask.jsonify({"success":True,'resp': resp}), 200

	except Exception as error:
		return flask.jsonify({"success":False,"error":str(error)}), 406

	