import json
import toml

with open('./config.toml', 'r', encoding='utf-8') as f:
	CONFIG = toml.load(f)

with open('./api/db.json', 'r', encoding='utf-8') as f:
	DB = json.load(f) 

def update():
	with open('./api/db.json', 'r', encoding='utf-8') as f:
		DB = json.load(f)

URL_DB = "https://v-lo-krakow.edupage.org/rpr/server/maindbi.js?__func=mainDBIAccessor"
URL_TT = "https://v-lo-krakow.edupage.org/timetable/server/currenttt.js?__func=curentttGetData"
URL_RP = "https://v-lo-krakow.edupage.org/substitution/server/viewer.js?__func=getSubstViewerDayDataHtml"

