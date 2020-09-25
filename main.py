import flask
import requests

app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False

import collections
import json
import pprint
import random
import re
import datetime
import itertools

import requests
import xmltodict
from bs4 import BeautifulSoup

AGENTS = ["Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1","Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",]
CLASS_ID = {"-1":"3A","-2":"3B","-3":"3C","-4":"3D","-5":"3E","-6":"3F","-7":"3G","-8":"3H","-29":"2A","-30":"2B","-31":"2C","-32":"2D","-33":"2E","-34":"2F","-35":"2G","-36":"2H","-37":"2AG","-38":"2BG","-39":"2CG","-40":"2DG","-41":"2EG","-42":"2FG","-43":"2GG","-44":"2HG","-45":"1A","-46":"1B","-47":"1C","-48":"1D","-49":"1E","-50":"1F","-51":"1G","-52":"1H"}
CLASS_KEY = {"1A":"-45","1B":"-46","1C":"-47","1D":"-48","1E":"-49","1F":"-50","1G":"-51","1H":"-52","2A":"-29","2Ag":"-37","2B":"-30","2Bg":"-38","2C":"-31","2Cg":"-39","2D":"-32","2Dg":"-40","2E":"-33","2Eg":"-41","2F":"-34","2Fg":"-42","2G":"-35","2Gg":"-43","2H":"-36","2Hg":"-44","3A":"-1","3B":"-2","3C":"-3","3D":"-4","3E":"-5","3F":"-6","3G":"-7","3H":"-8"}
TEACHER_ID = {"-1":"Chruściel","-3":"Jantos","-4":"Kos","-6":"Ostachowska-Kos","-7":"Pasieka","-9":"Adamska","-10":"Dudek","-11":"Kandyba","-14":"Olszewska","-15":"Oniszczuk","-16":"Ostrowska","-17":"Płaneta","-18":"Sowińska","-20":"Zagórny","-21":"Rabiega","-22":"Pabian","-24":"SM","-25":"Wojtasiewicz","-26":"Zborczyńska","-27":"Bajer","-28":"Kotula","-29":"Kapłon","-30":"Szewczyk","-31":"Wadowska","-32":"Rojewska","-33":"Kurzawińska","-34":"Pach","-35":"Sokólska","-36":"Szklarska","-37":"Boroń","-38":"Garlicki","-39":"Jaworski","-40":"Kobylec","-42":"Drabczyk","-43":"Borcz","-44":"Dymel","-45":"Gunia","-46":"Kaszuba","-47":"Kielar","-48":"Kraszewski","-49":"Niedźwiedź","-52":"Pietras","-53":"Zając","-54":"Fryt","-55":"Król","-56":"Przybylski","-58":"Gełdon","-59":"Kręgiel","-60":"Zuchmańska","-61":"Osuch","-62":"Słowiak","-64":"Brezdeń","-67":"Duraj","-68":"Gś","-70":"Kabłak","-71":"Piekarska","-72":"Kosiński","-73":"Stolarski","-74":"Studnicki","-75":"Berkowicz","-76":"Gł","-77":"Dziedzic","-79":"Kieres","-81":"Ptak-Grzesik","-82":"Zawadzki","-83":"Sokołowska","-84":"Marcinek","-85":"Kulczycki","-86":"Burek","-87":"Kobos","-88":"Herman","-91":"PU","-92":"Ciepielowska","-94":"UA","-95":"Kaniecka","-96":"An","-98":"Gorczyca","-101":"Faryna","-102":"Bałucka","-103":"Bednarek","-104":"Micygała","-105":"cV","-106":"Chodacka","-108":"Koszałka","-109":"Niemczyk","-111":"Kamińska","-112":"Maruszczak","-133":"Kopiec","-114":"Pieniążek","-115":"Pezarski","-116":"Kołdras","-118":"MS","-120":"Mach","-121":"Wy","-122":"V1","-123":"AV","-124":"3V","-125":"Słowikowska","-126":"Malcharek","-127":"Andryka","-128":"Jachowicz","-129":"Kmiecik","-130":"Stokłosa","-131":"Stypuła","-132":"Stańczyk","-134":"ZV","-135":"pV","-136":"Szarek","-137":"SzymlakE","-138":"Gluszko","-139":"Czyrnecka","-140":"Marcińska","-141":"Gluszko"}
CLASSROOM_ID = {"-1":"1","-2":"2","-3":"3","-4":"5","-6":"13","-7":"13A","-8":"13B","-9":"13C","-10":"14","-11":"15","-12":"16","-13":"17","-14":"18","-15":"19","-16":"20","-17":"21","-18":"22","-19":"23","-20":"24","-21":"25","-22":"26","-23":"27","-24":"28","-25":"29","-26":"31","-27":"32","-28":"35","-29":"36","-30":"37","-31":"33","-32":"aula","-33":"01","-34":"02","-35":"03","-36":"04","-37":"inf1","-38":"inf2","-39":"siłownia","-42":"dH1","-43":"DH2","-44":"DH3","-48":"CUJ 1","-49":"piw_prawa","-50":"piw_lewa","-51":"par_lewy","-52":"par_prawy","-53":"I lewy","-54":"I prawy","-55":"II lewy","-56":"II prawy","-57":"CUJ2","-58":"CUJ3","-59":"CUJ4","-60":"Biblio","-61":"mpn","-63":"DPN","-64":"g_mala","-65":"g_duza","-66":"A1","-67":"A2","-68":"A3","-69":"A4","-70":"A5","-71":"A6","-72":"A7","-73":"A8","-74":"A9","-75":"A10","-76":"A11","-77":"13B","-78":"PN","-79":"IP"}
SUBJECT_ID = {"-1":"Język polski o","-2":"Język polski","-3":"Język polski - R","-4":"Język obcy I","-5":"Konwersatorium","-6":"Język obcy II","-7":"Język niemiecki","-8":"Język angielski","-9":"Język francuski","-10":"Język rosyjski","-11":"Język hiszpański","-12":"Język włoski","-13":"j.chiński","-14":"Historia","-15":"Historia - R","-16":"Historia i społeczeństwo o","-17":"Historia i społeczeństwo","-18":"Wiedza o społeczeństwie","-19":"Wiedza o społeczeństwie - R","-20":"Wiedza o kulturze","-21":"Matematyka o","-22":"Matematyka","-23":"Matematyka - R","-24":"Fizyka z astronomią","-25":"Fizyka z astronomią - R","-27":"Fizyka stosowana","-28":"Chemia","-29":"Chemia - R o","-30":"Chemia - R","-31":"Biologia","-32":"Biologia - R o","-33":"Biologia - R","-34":"Biologia dla chemików","-35":"Geografia","-37":"Przyroda","-38":"Podstawy przedsiębiorczości","-39":"Informatyka","-40":"Informatyka o","-41":"Informatyka - R","-42":"Informatyka - S","-43":"Wychowanie fizyczne","-44":"Edukacja dla bezpieczeństwa","-45":"Godzina z wychowawc ą  o","-46":"Godzina z wychowawcą","-47":"Etyka","-48":"Religia o","-49":"Religia","-50":"Podstawy historii sztuki","-51":"Wychowanie do życia w rodzinie","-52":"Zniżka - dyrektor","-53":"Zniżka - wicedyrektor","-54":"Obowiązki bibliotekarza","-55":"Obowiązki pedagoga","-56":"Obowiązki psychologa","-57":"Zajęcia laboratoryjne UJ","-58":"Zajęcia laboratoryjne UJ 1","-59":"Zajęcia międzyoddziałowe - chemia","-60":"Nauczanie indywidualne","-61":"algorytmika o","-62":"algorytmika","-63":"Zajęcia pozalekcyjne artystyczne","-64":"Doradztwo zawodowe","-65":"Kultura Chin","-66":"Urlop dla poratowania zdrowia","-67":"rewalidacja","-71":"Filozofia","-72":"Fizyka UJ","-73":"zaj. wyrównawcze","-74":"szcz. uzdolnieni","-75":"Fakultet matematyczny","-76":"UJ Polski","-77":"Chmura","-78":"Konwersatorium z jęyka angielskiego","-79":"Filozofia z elementami psychologii","-80":"Konwersatorium z języka niemieckiego","-81":"Konwersatorium z języka francuskiego","-82":"Konwersatorium z języka hizpańskiego"}
TIME_MAP = {'07:10':0,'7:10':0,'08:00':1,'8:00':1,'09:00':2,'9:00':2,'10:00':3,'11:00':4,'12:00':5,'13:00':6,'14:00':7,'14:50':8,'15:40':9,'16:30':10}
URL_TT = "https://v-lo-krakow.edupage.org/timetable/server/currenttt.js?__func=curentttGetData"
URL_RP = "https://v-lo-krakow.edupage.org/substitution/server/viewer.js?__func=getSubstViewerDayDataHtml"

@app.route('/')
def home():
	return flask.render_template('home.html')


@app.route('/projects')
def projects():
	return flask.render_template('projects.html')


@app.route('/contact')
def contact():
	return flask.render_template('contact.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
	return flask.render_template('login.html')


@app.route('/api/replacements', methods=['GET'])
def replacements():
	try:
		klass = flask.request.args.get('class')
		if str(klass).upper() not in CLASS_KEY.keys():
			raise ValueError(flask.request.url)
		klass = klass.upper()

		if not flask.request.args.get('offset'):
			offset = 0
		else:
			offset = int(flask.request.args.get('offset'))
			
		date_today = datetime.datetime.now() - datetime.timedelta(days=offset)
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

		if klass in resp.keys():
			return flask.jsonify({
				"resp": resp[klass],
				"success":True
				}), 200
		else:
			return flask.jsonify({
				"resp": [],
				"success":True
				}), 200	
	except Exception as error:
		return flask.jsonify({
			"error":str(error),
			"success":False
			}), 406
	

@app.route('/api/timetable', methods=['GET'])
def timetable():
	try:
		klass = flask.request.args.get('class')
		if str(klass).upper() not in CLASS_KEY.keys():
			raise ValueError(flask.request.url)

		klass = klass.upper()

		today = datetime.date.today()
		last_monday = today + datetime.timedelta(days=-today.weekday(), weeks=0)
		next_friday = last_monday + datetime.timedelta(days=4)

		resp = requests.post(
			URL_TT,
			headers={
				"User-Agent": random.choice(AGENTS),
				"Origin": "https://v-lo-krakow.edupage.org",
				"Referer": "https://v-lo-krakow.edupage.org/substitution/",
			},
			json={
				"__args": [
					None,
					{
						"year": 2020,
						"datefrom": str(last_monday),
						"dateto": str(next_friday),
						"table": "classes",
						"id": CLASS_KEY[klass],
						"showColors": True,
						"showIgroupsInClasses": True,
						"showOrig": True,
					},
				],
				"__gsh": "00000000",
			},
		)
		resp_json = resp.json()['r']['ttitems']

		for i,obj in enumerate(resp_json):
			year_curr, month_curr, day_curr = [int(x) for x in obj['date'].split('-')]
			day_index = datetime.date(year_curr, month_curr, day_curr) - last_monday
			day_index = day_index.days

			hours_start, minutes_start = [int(x) for x in obj['starttime'].split(':')]
			hours_stop, minutes_stop = [int(x) for x in obj['endtime'].split(':')]
			a = datetime.timedelta(hours=hours_start, minutes=minutes_start)
			b = datetime.timedelta(hours=hours_stop, minutes=minutes_stop)
			total_duration = b-a
			total_duration = total_duration.seconds//60//45

			time_index = TIME_MAP[obj['starttime']]

			try: duration = int(obj['durationperiods'])
			except KeyError:
				duration = 1

			resp_json[i] = {
				'subject': SUBJECT_ID[obj['subjectid']],
				'teacher': TEACHER_ID[obj['teacherids'][0]],
				'classroom': CLASSROOM_ID[obj['classroomids'][0]],
				'color': obj['colors'][0],
				'time_index': time_index,
				'duration': duration,
				'date': obj['date'],
				'day_index': day_index
			}

		#days = []
		#i,j = 0,1
		#prev_date = resp_json[0]['date']
		
		#for obj in resp_json:
		#	if obj['date'] != prev_date or j==len(resp_json):
		#		days.append(resp_json[i:j-1])
		#		prev_date = obj['date']
		#		i = j
		#	j += 1
		days = []
		for _,y in itertools.groupby(resp_json, lambda x: x['day_index']):
			days.append(list(y))

		buff = {
			'0':{},
			'1':{},
			'2':{},
			'3':{},
			'4':{},
		}

		for i,day in enumerate(days):
			for x,y in itertools.groupby(day, lambda x: x['time_index']):
				out = list(y)
				#print(f'[{i}][{x}]={out}')
				buff[str(i)][str(x)] = out
		
		resp = [[x for _,x in x.items()] for _,x in buff.items()]

		return flask.jsonify({
			"resp": resp,
			"success": True
			}), 200

	except Exception as error:
		return flask.jsonify({
			"error":str(error),
			"success":False
			}), 406


'''

	if day_index - prev_date:
		days.append(resp_json[i:j])
		i = j
		j += 1

	j+=1
	
	prev_time = 0
	subj = [[None]*11]*5
	print(subj)
	pprint.pprint(days[0])

	for i,day in enumerate(days):
		for lesson in day:
			time_idx = TIME_MAP[lesson['starttime']]
			if time_idx - prev_time:
				subj[i][time_idx] = lesson
			elif isinstance(subj[i][time_idx], (type(None),dict)):
				subj[i][time_idx] = [subj[i][time_idx]]
				subj[i][time_idx].append(lesson)
			else:
				subj[i][time_idx].append(lesson)

	pprint.pprint(subj[0])

	for day in days:
		for lesson in day:
			year_curr, month_curr, day_curr = [int(x) for x in lesson['date'].split('-')]
			day_index = datetime.date(year_curr, month_curr, day_curr) - last_monday
			day_index = day_index.days

			hours_start, minutes_start = [int(x) for x in lesson['starttime'].split(':')]
			hours_stop, minutes_stop = [int(x) for x in lesson['endtime'].split(':')]
			a = datetime.timedelta(hours=hours_start, minutes=minutes_start)
			b = datetime.timedelta(hours=hours_stop, minutes=minutes_stop)
			total_duration = b-a
			total_duration = total_duration.seconds//60//45

			time_index = TIME_MAP[lesson['starttime']]

			try: duration = int(lesson['durationperiods'])
			except KeyError:
				duration = 1
	
			node = {
				'subject': SUBJECT_ID[lesson['subjectid']],
				'teacher': TEACHER_ID[lesson['teacherids'][0]],
				'classroom': CLASSROOM_ID[lesson['classroomids'][0]],
				'color': lesson['colors'][0],
				'time_index': time_index,
				'duration': duration
			}
	
			if isinstance(sub[day_index][time_index], dict):
				sub[day_index][time_index] = [sub[day_index][time_index]]
				sub[day_index][time_index].append(node)
			else:
				sub[day_index][time_index] = node


			#print(day_index, time_index)
			#print(obj['date'], end='  ')
			#print(obj['starttime'], end='  ')
			#print(obj['endtime'], end='  ')
			#print(day_index, time_index)
			#print(total_duration)
			#obj['subjectid'] = SUBJECT_ID[obj['subjectid']]
			#obj['classids'] = CLASS_ID[obj['classids'][0]]
			#obj['teacherids'] = TEACHER_ID[obj['teacherids'][0]]
			#obj['classroomids'] = CLASSROOM_ID[obj['classroomids'][0]]
			#obj['colors'] = obj['colors'][0]
		#for obj in resp_json:
		#    datetime.timedelta()
		#print(sub[0][0])
		#print(sub[1][0])
		#print(sub[2][0])
	'''


if __name__ == '__main__':
	app.run(debug=True)
