import requests
from bs4 import BeautifulSoup
import json
import time
import schedule
import thefuzz.fuzz

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0 (Edition Yx GX 03)"
}

def get_bus(headers):
    url = "https://ru.busti.me/krasnoyarsk/"
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    button_ui = soup.find_all("a", class_='ui')

    count = 0
    bus_dict = {}

    for article in button_ui:
        count += 1
        article_title = article.get("title")
        article_desc = article.find('div', class_='bheader')
        text = article_desc.find_next_sibling(string=True).strip()
        article_url = f'https://ru.busti.me/krasnoyarsk/{article.get("href")}'
        article_bus = article.find("span", class_="busamount").text.strip()
        article_id = article_url.split('/')[-1]

        bus_dict[article_id] = {
            "article_title": article_title,
            "Number": text,
            "BusLine": article_bus
        }

        if count == 64:
            break

    with open("Bus_Time.json", "w", encoding="utf-8") as file:
        json.dump(bus_dict, file, indent=4, ensure_ascii=False)




def main():
    get_bus(headers)







def get_bus_route(headers, kayBus):
    url = f"https://ru.busti.me/krasnoyarsk/{kayBus}/"
    r = requests.get(url=url, headers=headers)
    print(kayBus, url)
    soup = BeautifulSoup(r.text, "lxml")


    Bus_Stop = soup.find_all("td") #<-------------


    with open("Bus_Time.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        user_data = data.get(kayBus, {})
        startstop = str(user_data.get("article_title")).split('↔')[1].strip()

    busstoplist = []
    wherebuslist = []


    for art in Bus_Stop:

        busstop = art.find("a")
        busstop = str(busstop).split('"')

        WhereBus = art.find_all("img")

        if len(WhereBus) != 0 and busstop != 'None':
            wherebuslist.append(1)
        else:
            wherebuslist.append(0)


        try:
            if busstop[-1] != 'None':
                busstoplist.append(busstop[-1][1:-4].strip())
            else:
                pass
        except:
            pass

    busstoplist.insert(0, startstop)
    wherebuslist = wherebuslist[2:]


    with open("Bus_Time.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        user_data = data.get(kayBus, {})

        The_final = str(user_data.get("article_title")).split('↔')[0].strip()


        bus_down = []
        bus_up = []
        c = 0
        for e in range(len(busstoplist)):
            i = busstoplist[e]

            if i != The_final:
                if wherebuslist[e] == 1:
                    txt = f'🚍 {i}'
                else:
                    txt = f'{i}'
                bus_down.append(txt)
                c += 1

            else:
                if wherebuslist[e] == 1:
                    txt = f'🚍 {i}'
                else:
                    txt = f'{i}'
                bus_down.append(txt)
                c += 1
                break


        wherebuslist = wherebuslist[c+1:]
        for e in range(len(busstoplist[c-1:])):
            i = busstoplist[c-1:][e]

            if wherebuslist[e-1] == 1:
                txt = f'🚍 {i}'
            else:
                txt = f'{i}'

            bus_up.append(txt)


        itog = [bus_up, bus_down]
        return itog










def Nearest_bus(NameStop):
    NameStop = str(NameStop).lower()
    url = 'https://ru.busti.me/krasnoyarsk/stop/'
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    Name = soup.find_all("div", class_='ui four column stackable grid')  # <-------------

    for N in Name:
        Title = N.find_all("a", class_='item')



    result = []
    for i in range(len(Title)):
        tmp = Title[i]
        tmp = str(tmp).split('"')[4]
        # if NameStop in tmp.lower():
        tmp = tmp.split(">")
        if tmp[1] == "<b":
            tmp = tmp[2][:-3]
        else:
            tmp = tmp[1][:-3]

        if thefuzz.fuzz.WRatio(NameStop, tmp.lower()) > 80 or NameStop in tmp.lower(): result.append(tmp)
        # if NameStop in tmp.lower(): result.append(tmp)

    return result




def get_url_busstop(NameStop):
    NameStop = str(NameStop).lower()

    url = 'https://ru.busti.me/krasnoyarsk/stop/'
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    Name = soup.find_all("div", class_='ui four column stackable grid')  # <-------------

    for N in Name:
        Title = N.find_all("a", class_='item')

    list1 = []
    UrlS = ''
    for i in range(len(Title)):
        tmp = Title[i]
        tmp2 = str(tmp).split('"')[4]
        if NameStop in tmp2.lower():
            UrlS += str(tmp).split('"')[3]

    UrlS = 'https://ru.busti.me/'+UrlS


    return UrlS



def get_bus_url(url):
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    TimeBus = soup.find_all("tbody")  # <-------------



    TimeAndBus = []
    for art in TimeBus:
        all = art.find_all("tr")


        Time = []
        Bus = []
        for e in all:
            tmp1 = str(e).split('class="ui basic blue button" href="/krasnoyarsk/')
            tmp2 = str(e).split('target="_blank">')

            TB = tmp1[0][11:16]
            for i in range(1, len(tmp2)):
                NB = str(tmp2[i]).split('<')[0]
                Time.append(TB)
                Bus.append(NB)



        TimeAndBus.append(Time)
        TimeAndBus.append(Bus)

    return TimeAndBus




def get_side(url):
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    side = soup.find_all("h3")  # <-------------
    print(side)

    s = []
    for art in side:
        print(art)
        s.append(str(art).split('i')[-1][2:-5])

    print(s)
    s.pop(0)

    if len(s) < 0:
        return 0
    else:
        return s


