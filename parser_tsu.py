import requests
from bs4 import BeautifulSoup
import time
import asyncio
import aiohttp
import lxml
import json
import csv
from find_dates_in_string import find_date_in_string, normalise_str
import hashlib
import datetime
from datetime import date


def get_data_tsu():
    headers = {
        'authority': 'mc.yandex.ru',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'origin': 'https://news.tsu.ru',
        'referer': 'https://news.tsu.ru/',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    url = "https://news.tsu.ru/calendar-of-events/?"

    un_id = "tsu"
    un_name = "Томский государственный университет"

    result = []

    response = requests.get(url, headers)

    soup = BeautifulSoup(response.text, "lxml")
    confs_data_tsu = soup.find_all("div", class_="news-calendar__content")
    # print(confs_data_tsu)

    confs_urls_tsu = []
    for conf_tsu in confs_data_tsu:
        conf_url_tsu = "https://news.tsu.ru/" + conf_tsu.find("div", class_="news-calendar__text").find("a", class_="news-calendar__title").get("href")
        # print(conf_url_tsu)
        confs_urls_tsu.append(conf_url_tsu)


# II'm not sure about the doable of this hypothesis.
# But I'll try, as in the conference card I didn't find any link to create a unique number for hash_
# If this not work, I'll move this try-except down, after the line: for conf_url_tsu in confs_urls_tsu:
        try:
            conf_id = conf_tsu.find("div", class_="news-calendar__text").find("a", class_="news-calendar__title").get("href").strip().split("/")[-2]
        except:
            conf_id = "Id конференции отсутствует"
        # print(conf_id)


    for conf_url_tsu in confs_urls_tsu[0:3]:
        response = requests.get(conf_url_tsu, headers)
        soup = BeautifulSoup(response.text, "lxml")

        conf_data_tsu = soup.find("div", class_="main__content")


        try:
            conf_name = conf_data_tsu.find("h1", class_="event-hero__title").text.strip()
        except:
            conf_name = "Название конференции неизвестно"
        # print(conf_name)


        try:
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
        except:
            hash_ = "Хэш конференции отстутсвует"
        # print(hash_)


        try:
            conf_address = conf_data_tsu.find("div", class_="address").find_next("span").find_next("span").text
        except:
            conf_address = "Место проведения конференции неизвестно"
        # print(conf_address)


        try:
            conf_date_begin = conf_data_tsu.find("div", class_="address").find("span").text.split(",")[0]
        except:
            conf_date_begin = "Дата начала проведения конференции неизвестна"
        # print(conf_date_begin)

        try:
            conf_s_desc = conf_data_tsu.find("div", class_="text-content").find("b").text
        except:
            conf_s_desc = "Краткое описание конеференции отсутствует"
        # print(conf_s_desc)

        try:
            conf_href = conf_data_tsu.find("p", class_="external-link").find("a").get("href")
        except:
            conf_href = "Ссылка на регистрацию отсутсвует"
        # print(conf_href)

        reg_date_begin = ""
        reg_date_end = ""
        conf_date_end = ""
        conf_card_href = ""
        reg_href = ""
        conf_desc = ""
        org_name = ""
        themes = ""
        local = ""
        online = ""
        offline = ""
        rinc = ""
        contacts = ""





        result.append(
            {'conf_id': conf_id,
             'hash': hash_,
             'un_name': un_name,
             'local': local,
             'reg_date_begin': reg_date_begin,
             'reg_date_end': reg_date_end,
             'conf_date_begin': conf_date_begin,
             'conf_date_end': conf_date_end,
             'conf_card_href': conf_card_href,
             'reg_href': reg_href,
             'conf_name': conf_name,
             'conf_s_desc': conf_s_desc,
             'conf_desc': conf_desc,
             'org_name': org_name,
             'themes': themes,
             'online': online,
             'conf_href': conf_href,
             'offline': offline,
             'conf_address': conf_address,
             'contacts': contacts,
             'rinc': rinc,
             }
        )

    # print(result)

    try:
        with open(f"TSU/{un_id}_{date.today()}.json", "w", encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


def main():
    get_data_tsu()


if __name__ == '__main__':
    main()


