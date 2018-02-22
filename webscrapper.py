import requests
from bs4 import BeautifulSoup
import datetime
import time
from dateutil import parser


class boss:
    boss_name = ""
    dt_first = None
    dt_last = None
    dt_est = None
    time_to_window = None
    in_window = None
    def __init__(self,name):
        self.boss_name = name
    # def change_spawn_window(self,):



def refresh_bosses(bosses):

    quote_page = "http://urzasarchives.com/bdo/wbtbdo/wbtna/"
    page = requests.get(quote_page)

    soup = BeautifulSoup(page.content, "html.parser")

    tmp_name = ""
    for tr in soup.find_all('tr')[:]:
        tds = tr.find_all('td')
        if "(World Boss)" in tds[0].text or "(Field Boss)" in tds[0].text:
            bosses[tds[0].text.strip()] = boss(tds[0].text.strip())
            tmp_name = tds[0].text.strip()
        elif "Next Spawn:" in tds[0].text:
            txt = tds[1].text.strip().split()
            first = txt[0] + " " + txt[1]
            last = txt[4] + " " + txt[5]
            dt_first = parser.parse(first)
            dt_last = parser.parse(last)
            bosses[tmp_name].dt_first = dt_first
            bosses[tmp_name].dt_last = dt_last

            if datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M") > dt_first and \
                datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"%Y-%m-%d %H:%M") < dt_last:
                bosses[tmp_name].in_window = True
                bosses[tmp_name].time_to_window = None
            elif datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"%Y-%m-%d %H:%M") > dt_last:
                bosses[tmp_name].in_window = False
                bosses[tmp_name].time_to_window = "FM"
            else:
                bosses[tmp_name].in_window = False
                bosses[tmp_name].time_to_window = dt_first - datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                           "%Y-%m-%d %H:%M")
        elif "Est. Spawn:" in tds[0].text:
            txt = tds[1].text.strip().split()
            est = txt[0] + " " + txt[1]
            dt_est = parser.parse(est)
            bosses[tmp_name].dt_est = dt_est


def start():
    bosses = {}
    print("Refreshing Boss")
    refresh_bosses(bosses)
    return bosses
