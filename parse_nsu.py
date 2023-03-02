import requests
import lxml
from bs4 import BeautifulSoup
import json
import csv
import time
import datetime
import hashlib
from find_dates_in_string import find_date_in_string
from find_dates_in_string import normalise_str
from dateutil.parser import parse
from datetime import datetime
from datetime import date


def parsing_nsu():
    headers = {
        'authority': 'mc.yandex.ru',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'origin': 'https://conf.nsu.ru',
        'referer': 'https://conf.nsu.ru/',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',
    }

    url = "https://conf.nsu.ru/"

    cur_time = datetime.now().strftime("%d_%m_%Y_%H_%M")

    response = requests.get(url = url, headers=headers)

    result = []
    un_name = "НГУ"

    soup = BeautifulSoup(response.text, "lxml")
    # print(response.text)
    confs_data_nsu = soup.find_all("div", class_="col-12 col-sm-6 col-md-4")
    # print(confs_data_nsu)
    # time.sleep(1)

    confs_urls_nsu = []
    for conf_data_nsu in confs_data_nsu:
        conf_url_nsu = "https://conf.nsu.ru" + conf_data_nsu.find("a").get("href")
        # print(conf_url_nsu)
        confs_urls_nsu.append(conf_url_nsu)
    # print(confs_urls_nsu)

    for conf_url_nsu in confs_urls_nsu:
        response = requests.get(conf_url_nsu, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        conf_data_nsu = soup.find("div", class_="main-container")
        # print(conf_data_nsu)


        try:
            reg_href = "https://conf.nsu.ru" + conf_data_nsu.find("a", class_="btn btn-blue mt-1 mb-1").get("href")
        except:
            reg_href = "Ссылка на регистрацию отсутствует"
        # print(reg_href)

        try:
            conf_id = un_name + "-" + conf_data_nsu.find("a", class_="btn btn-blue mt-1 mb-1").get("href").split('/')[-2]
        except:
            conf_id = "Id конференции отсутствует"

        try:
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
        except:
            hash_ = "Хэш конференции отсутствует"

        try:
            conf_name = conf_data_nsu.find("div", class_="col-12 col-md-9").text.strip()
        except:
            conf_name = "Название конференции отсутствует"
        # print(conf_name)

        try:
            reg_date_end = conf_data_nsu.find("div", class_="text-secondary").text.strip()
        except:
            reg_date_end = "Информация по дате окончания регистрации отсутствует"
        # print(reg_date_end)

        try:
            contacts = normalise_str(conf_data_nsu.find("div", class_="alert alert-info pl-5 pr-5 pb-5 mt-4").text.strip())
        except:
            contacts = "Контактные данные отсутствуют"
        # print(contacts)

        try:
            conf_date_begin_r = normalise_str(conf_data_nsu.find("div", class_="text color-blue").text.strip())
            conf_date_begin_r = conf_date_begin_r.split(" - ")
            conf_date_begin = conf_date_begin_r[0].replace("г.", "").strip()
            # date1 = datetime.strptime(date1_string, '%d %B %Y')
        except:
            conf_date_begin = "Информация по дате проведения конференции отсутствует"
        # print(conf_date_begin)

        try:
            conf_date_end_r = normalise_str(conf_data_nsu.find("div", class_="text color-blue").text.strip())
            conf_date_end_r = conf_date_end_r.split(" - ")
            conf_date_end = conf_date_end_r[1].replace("г.", "").strip()
        except:
            conf_date_end = "Информация по дате проведения конференции отсутствует"
        # print(conf_date_end)

        local = ""
        reg_date_begin = ""
        conf_card_href = ""
        conf_s_desc = ""
        conf_desc = ""
        org_name = ""
        themes = ""
        online = ""
        conf_href = ""
        offline = ""
        conf_address = ""
        rinc = ""



        result.append(
            {
                'conf_id': conf_id,
                'hash': hash_,
                'un_name': un_name,
                'local': local,
                'reg_date_begin': reg_date_begin,
                'reg_date_end': reg_date_end,
                'conf_date_begin': conf_date_begin.strip(),
                'conf_date_end': conf_date_end.strip(),
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


    try:
        with open(f"NSU/{un_name}_{cur_time}.json", "w", encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        # return result
    except Exception as e:
        print(e)




def main():
    pass

if __name__ == "__main__":
    parsing_nsu()