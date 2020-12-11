import json

with open('./api/timetable.json','r', encoding='utf-8') as f:
	ttconf = json.load(f)
	CLASS_KEY 	 = ttconf['CLASS_KEY']
	TIME_MAP  	 = ttconf['TIME_MAP']
	CLASSROOM_ID = ttconf['CLASSROOM_ID']
	TEACHER_ID	 = ttconf['TEACHER_ID']
	SUBJECT_ID	 = ttconf['SUBJECT_ID']

with open('./api/agents.json','r', encoding='utf-8') as f:
	agconf = json.load(f)
	AGENTS = agconf['AGENTS']

URL_TT = "https://v-lo-krakow.edupage.org/timetable/server/currenttt.js?__func=curentttGetData"
URL_RP = "https://v-lo-krakow.edupage.org/substitution/server/viewer.js?__func=getSubstViewerDayDataHtml"
