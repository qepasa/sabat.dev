import collections
import json
import pprint
import random
import re
import datetime

import requests
import xmltodict
from bs4 import BeautifulSoup

AGENTS = ["Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1","Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",]
CLASS_ID = {"-1":"3A","-2":"3B","-3":"3C","-4":"3D","-5":"3E","-6":"3F","-7":"3G","-8":"3H","-29":"2A","-30":"2B","-31":"2C","-32":"2D","-33":"2E","-34":"2F","-35":"2G","-36":"2H","-37":"2Ag","-38":"2Bg","-39":"2Cg","-40":"2Dg","-41":"2Eg","-42":"2Fg","-43":"2Gg","-44":"2Hg","-45":"1A","-46":"1B","-47":"1C","-48":"1D","-49":"1E","-50":"1F","-51":"1G","-52":"1H"}
CLASS_KEY = {"1A":"-45","1B":"-46","1C":"-47","1D":"-48","1E":"-49","1F":"-50","1G":"-51","1H":"-52","2A":"-29","2Ag":"-37","2B":"-30","2Bg":"-38","2C":"-31","2Cg":"-39","2D":"-32","2Dg":"-40","2E":"-33","2Eg":"-41","2F":"-34","2Fg":"-42","2G":"-35","2Gg":"-43","2H":"-36","2Hg":"-44","3A":"-1","3B":"-2","3C":"-3","3D":"-4","3E":"-5","3F":"-6","3G":"-7","3H":"-8"}
TEACHER_ID = {"-1":"Chruściel","-3":"Jantos","-4":"Kos","-6":"Ostachowska-Kos","-7":"Pasieka","-9":"Adamska","-10":"Dudek","-11":"Kandyba","-14":"Olszewska","-15":"Oniszczuk","-16":"Ostrowska","-17":"Płaneta","-18":"Sowińska","-20":"Zagórny","-21":"Rabiega","-22":"Pabian","-24":"SM","-25":"Wojtasiewicz","-26":"Zborczyńska","-27":"Bajer","-28":"Kotula","-29":"Kapłon","-30":"Szewczyk","-31":"Wadowska","-32":"Rojewska","-33":"Kurzawińska","-34":"Pach","-35":"Sokólska","-36":"Szklarska","-37":"Boroń","-38":"Garlicki","-39":"Jaworski","-40":"Kobylec","-42":"Drabczyk","-43":"Borcz","-44":"Dymel","-45":"Gunia","-46":"Kaszuba","-47":"Kielar","-48":"Kraszewski","-49":"Niedźwiedź","-52":"Pietras","-53":"Zając","-54":"Fryt","-55":"Król","-56":"Przybylski","-58":"Gełdon","-59":"Kręgiel","-60":"Zuchmańska","-61":"Osuch","-62":"Słowiak","-64":"Brezdeń","-67":"Duraj","-68":"Gś","-70":"Kabłak","-71":"Piekarska","-72":"Kosiński","-73":"Stolarski","-74":"Studnicki","-75":"Berkowicz","-76":"Gł","-77":"Dziedzic","-79":"Kieres","-81":"Ptak-Grzesik","-82":"Zawadzki","-83":"Sokołowska","-84":"Marcinek","-85":"Kulczycki","-86":"Burek","-87":"Kobos","-88":"Herman","-91":"PU","-92":"Ciepielowska","-94":"UA","-95":"Kaniecka","-96":"An","-98":"Gorczyca","-101":"Faryna","-102":"Bałucka","-103":"Bednarek","-104":"Micygała","-105":"cV","-106":"Chodacka","-108":"Koszałka","-109":"Niemczyk","-111":"Kamińska","-112":"Maruszczak","-133":"Kopiec","-114":"Pieniążek","-115":"Pezarski","-116":"Kołdras","-118":"MS","-120":"Mach","-121":"Wy","-122":"V1","-123":"AV","-124":"3V","-125":"Słowikowska","-126":"Malcharek","-127":"Andryka","-128":"Jachowicz","-129":"Kmiecik","-130":"Stokłosa","-131":"Stypuła","-132":"Stańczyk","-134":"ZV","-135":"pV","-136":"Szarek","-137":"SzymlakE","-138":"Gluszko","-139":"Czyrnecka","-140":"Marcińska","-141":"Gluszko"}
CLASSROOM_ID = {"-1":"1","-2":"2","-3":"3","-4":"5","-6":"13","-7":"13A","-8":"13B","-9":"13C","-10":"14","-11":"15","-12":"16","-13":"17","-14":"18","-15":"19","-16":"20","-17":"21","-18":"22","-19":"23","-20":"24","-21":"25","-22":"26","-23":"27","-24":"28","-25":"29","-26":"31","-27":"32","-28":"35","-29":"36","-30":"37","-31":"33","-32":"aula","-33":"01","-34":"02","-35":"03","-36":"04","-37":"inf1","-38":"inf2","-39":"siłownia","-42":"dH1","-43":"DH2","-44":"DH3","-48":"CUJ 1","-49":"piw_prawa","-50":"piw_lewa","-51":"par_lewy","-52":"par_prawy","-53":"I lewy","-54":"I prawy","-55":"II lewy","-56":"II prawy","-57":"CUJ2","-58":"CUJ3","-59":"CUJ4","-60":"Biblio","-61":"mpn","-63":"DPN","-64":"g_mala","-65":"g_duza","-66":"A1","-67":"A2","-68":"A3","-69":"A4","-70":"A5","-71":"A6","-72":"A7","-73":"A8","-74":"A9","-75":"A10","-76":"A11","-77":"13B","-78":"PN","-79":"IP"}
SUBJECT_ID = {"-1":"Język polski o","-2":"Język polski","-3":"Język polski - R","-4":"Język obcy I","-5":"Konwersatorium","-6":"Język obcy II","-7":"Język niemiecki","-8":"Język angielski","-9":"Język francuski","-10":"Język rosyjski","-11":"Język hiszpański","-12":"Język włoski","-13":"j.chiński","-14":"Historia","-15":"Historia - R","-16":"Historia i społeczeństwo o","-17":"Historia i społeczeństwo","-18":"Wiedza o społeczeństwie","-19":"Wiedza o społeczeństwie - R","-20":"Wiedza o kulturze","-21":"Matematyka o","-22":"Matematyka","-23":"Matematyka - R","-24":"Fizyka z astronomią","-25":"Fizyka z astronomią - R","-27":"Fizyka stosowana","-28":"Chemia","-29":"Chemia - R o","-30":"Chemia - R","-31":"Biologia","-32":"Biologia - R o","-33":"Biologia - R","-34":"Biologia dla chemików","-35":"Geografia","-37":"Przyroda","-38":"Podstawy przedsiębiorczości","-39":"Informatyka","-40":"Informatyka o","-41":"Informatyka - R","-42":"Informatyka - S","-43":"Wychowanie fizyczne","-44":"Edukacja dla bezpieczeństwa","-45":"Godzina z wychowawc ą  o","-46":"Godzina z wychowawcą","-47":"Etyka","-48":"Religia o","-49":"Religia","-50":"Podstawy historii sztuki","-51":"Wychowanie do życia w rodzinie","-52":"Zniżka - dyrektor","-53":"Zniżka - wicedyrektor","-54":"Obowiązki bibliotekarza","-55":"Obowiązki pedagoga","-56":"Obowiązki psychologa","-57":"Zajęcia laboratoryjne UJ","-58":"Zajęcia laboratoryjne UJ 1","-59":"Zajęcia międzyoddziałowe - chemia","-60":"Nauczanie indywidualne","-61":"algorytmika o","-62":"algorytmika","-63":"Zajęcia pozalekcyjne artystyczne","-64":"Doradztwo zawodowe","-65":"Kultura Chin","-66":"Urlop dla poratowania zdrowia","-67":"rewalidacja","-71":"Filozofia","-72":"Fizyka UJ","-73":"zaj. wyrównawcze","-74":"szcz. uzdolnieni","-75":"Fakultet matematyczny","-76":"UJ Polski","-77":"Chmura","-78":"Konwersatorium z jęyka angielskiego","-79":"Filozofia z elementami psychologii","-80":"Konwersatorium z języka niemieckiego","-81":"Konwersatorium z języka francuskiego","-82":"Konwersatorium z języka hizpańskiego"}

today = datetime.date.today()
last_monday = today + datetime.timedelta(days=-today.weekday(), weeks=0)
next_friday = last_monday + datetime.timedelta(days=4)

url = "https://v-lo-krakow.edupage.org/timetable/server/currenttt.js?__func=curentttGetData"

resp = requests.post(
    url,
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
                "id": CLASS_KEY['2E'],
                "showColors": True,
                "showIgroupsInClasses": True,
                "showOrig": True,
            },
        ],
        "__gsh": "00000000",
    },
)
resp_json = resp.json()['r']['ttitems']

for obj in resp_json:
    print(obj['date'], end='  ')
    print(obj['starttime'], end='  ')
    print(obj['endtime'], end='  ')
    print(SUBJECT_ID[obj['subjectid']], end='  ')
    #print([CLASS_ID[x] for x in obj['classids']], end='  ')
    print(TEACHER_ID[obj['teacherids'][0]], end='  ')
    print(CLASSROOM_ID[obj['classroomids'][0]], end='  ')
    print(obj['colors'][0], end='\n')
    

#open("test.json", "w", encoding="utf-8", errors="replace").write(json.dumps(resp.json()["r"], indent=2))
