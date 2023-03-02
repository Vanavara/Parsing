from bs4 import BeautifulSoup
import requests
import lxml
import time
import datetime
import csv
import json
import aiohttp
import asyncio
import hashlib
from find_dates_in_string import normalise_str


def parse_urfu():
    headers = {
        'authority': 'urfu.ru',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',
    }

    url = "https://urfu.ru/ru/science/konferencii/"

    un_name = "Уральский федеральный университет"
    un_id = "urfu"

    result = []

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    # print(response.text)

    confs_items_urfu = soup.find("table", class_="ce-table").find_all("tr")[1:]
    # print(confs_items_urfu)

    for conf in confs_items_urfu:
        conf_data = conf.find_all("td")
        # print(conf_data)

        try:
            conf_id = normalise_str(un_id + "-" + conf_data[0].text.strip())
        except:
            conf_id = "Id конференции отсутствует"

        try:
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
        except:
            hash_ = " - "

        try:
            conf_name = normalise_str(conf_data[0].text.strip())
        except:
            conf_name = "Информация по названию конференции отсутствует"

        try:
            conf_date_begin = conf_data[1].text.strip()
        except:
            conf_date_begin = "Информация по названию конференции отсутствует"

        try:
            conf_card_href = conf_data[2].find("a").get("href")
        except:
            conf_card_href = "Информация по названию конференции отсутствует"

        local = ""
        reg_date_begin = ""
        reg_date_end = ""
        conf_date_end = ""
        reg_href = ""
        conf_s_desc = ""
        conf_desc = ""
        org_name = ""
        themes = ""
        online = ""
        conf_href = ""
        offline = ""
        conf_address = ""
        contacts = ""
        rinc = ""


        result.append(
            {
                'conf_id': conf_id,
                'hash': hash_,
                'un_name': un_name,
                'local': " ",
                'reg_date_begin': reg_date_begin,
                'reg_date_end': reg_date_end,
                'conf_date_begin': conf_date_begin,
                'conf_date_end': conf_date_end,
                'conf_card_href': conf_card_href,
                'reg_href': reg_href,
                'conf_name': conf_name.replace("/", " "),
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


    # print(result)
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    with open(f"URFU/{un_name}_{cur_time}.json", "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

def main():
    parse_urfu()


if __name__ == "__main__":
    main()