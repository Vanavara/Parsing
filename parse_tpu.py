import datetime
import hashlib

from bs4 import BeautifulSoup
import requests
import lxml
import aiohttp
import asyncio
import time
import json
import csv
import html
from find_dates_in_string import find_date_in_string, normalise_str

def get_data_tpu():
    cur_time = datetime.datetime.now().strftime("%d-%m_%Y_%H_%M")

    with open(f"tpu_{cur_time}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Название конференции",
                "Дата проведения",
                "Место проведения",
                "Срок подачи заявок",
                "Ссылка на мероприятие"
            )
        )

    headers = {
        'authority': 'mc.yandex.ru',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'origin': 'https://portal.tpu.ru',
        'referer': 'https://portal.tpu.ru/',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    url = "https://portal.tpu.ru/science/foreign-konf"

    un_id = "tpu"
    un_name = "Томский политехнический университет"
    cur_date = datetime.datetime.now().strftime("%d-%m_%Y_%H_%M")


    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    page_count_tpu = int(soup.find("span", class_="normal c-pages").find_all("a")[-2].text)
    # print(page_count_tpu)

    result = []

    for page_tpu in range(1, page_count_tpu + 1):
        url = f"https://portal.tpu.ru/science/foreign-konf?p={page_tpu}&y=2023&m=02"
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        conf_item_tpu = soup.find_all("tr", valign="top")
        # print(conf_item_tpu)

        for conf_tpu in conf_item_tpu:
            conf_data_tpu = conf_tpu.find_all("td")

            try:
                conf_name = conf_data_tpu[0].text.strip()
            except:
                conf_name = "У этой конференции отсутсвует название"

            try:
                conf_id = un_id + "-" + conf_data_tpu[4].find('a').get("href")
            except:
                conf_id = "Id конференции отсутствует"

            try:
                hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
            except:
                hash_ = "Хэш конференции отсутствует"

            try:
                conf_date_begin = normalise_str(conf_data_tpu[1].text.split("-")[0].strip())
                # conf_date_begin = html.unescape(json.loads(conf_data_tpu)['text'])
            except:
                conf_date_begin = "Информация по срокам проведения конференции отсутсвует"

            try:
                conf_date_end = normalise_str(conf_data_tpu[1].text.split("-")[1].strip())
                # conf_date_begin = html.unescape(json.loads(conf_data_tpu)['text'])
            except:
                conf_date_end = "Информация по срокам проведения конференции отсутсвует"

            try:
                conf_address = conf_data_tpu[2].text.strip()
            except:
                conf_address = "Информация по месту проведения конференции отсутсвует"

            try:
                reg_date_end = normalise_str(conf_data_tpu[3].text.strip())
            except:
                reg_date_end = "Информация по срокам проведения регистрации на конференцию отсутсвует"

            try:
                conf_card_href = conf_data_tpu[4].find('a').get("href")
            except:
                conf_card_href = "Ссылка на конференцию отсутсвует"


            local = ""
            reg_date_begin = ""
            reg_href = ""
            conf_s_desc = ""
            conf_desc = ""
            org_name = ""
            themes = ""
            online = ""
            offline = ""
            contacts = ""
            rinc = ""
            conf_href = ""


            result.append(
                {
                     'conf_id': conf_id,
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
                     'contacts': contacts.strip(),
                     'rinc': rinc,
                }
            )


    with open(f"data/tpu_{cur_time}.json", "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)


def maim_tpu():
    get_data_tpu()

if __name__ == '__main__':
    maim_tpu()


