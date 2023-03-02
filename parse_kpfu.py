from bs4 import BeautifulSoup
import requests
import lxml
import pd
import time
import datetime
import csv
import json
import aiohttp
import asyncio
import hashlib


def get_data_kpfu(url):
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    headers = {
        'authority': 'mc.yandex.ru',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'text/plain',
        'origin': 'https://kpfu.ru',
        'referer': 'https://kpfu.ru/',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    url = "https://kpfu.ru/portal_new.main_page?p_sub=6308&p_group_name=&p_meropriatie_vid_type=2&p_kon_kfu=1&p_mounth_date=&p_year_start=2023&status=&p_office=&p_date_start=01.01.2023&p_date_end=&p_page=1"

    response = requests.post(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    # print(response.text)

    un_name = "Казанский (Приволжский) федеральный университет"
    un_id = "kpfu"
    result = []

    page_count_kpfu = int(soup.find("div", class_="pagination").find_all("a")[-2].text)

    for page in range(1, page_count_kpfu +1):
        url_pages = f"https://kpfu.ru/portal_new.main_page?p_sub=6308&p_group_name=&p_meropriatie_vid_type=2&p_kon_kfu=1&p_mounth_date=&p_year_start=2023&status=&p_office=&p_date_start=01.01.2023&p_date_end=&p_page={page}"

        response = requests.get(url=url_pages, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        conf_item_kpfu = soup.find_all("tr", class_="konf_tr")
  
        for conf in conf_item_kpfu:
            conf_data_kpfu = conf.find_all("td")

            try:
                conf_name = conf_data_kpfu[1].text.strip()
            except:
                conf_name = "Информация по названию конференции отсутствует"

            try:
                conf_id = un_id + "-" + conf_data_kpfu[1].text.strip()
            except:
                conf_id = "Id конференции отсутствует"

            try:
                hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
            except:
                hash = "Хэш конференции отсутствует"

            try:
                conf_date_begin = conf_data_kpfu[2].text.strip()
            except:
                conf_date_begin = "Информация по датам проведения конференции отсутствует"

            try:
                org_name = conf_data_kpfu[3].text.strip()
            except:
                org_name = "Информация по организаторам проведения конференции отсутствует"

            local = ""
            reg_date_begin = ""
            reg_date_end = ""
            conf_date_end = ""
            conf_card_href = ""
            reg_href = ""
            conf_s_desc = ""
            conf_desc = ""
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


    with open(f"KPFU/kpfu_{cur_time}.json", "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)



def main():
    get_data_kpfu("https://kpfu.ru/portal_new.main_page?p_sub=6308&p_group_name=&p_meropriatie_vid_type=2&p_kon_kfu=1&p_mounth_date=&p_year_start=2023&status=&p_office=&p_date_start=01.01.2023&p_date_end=&p_page=1")

if __name__ == '__main__':
    main()