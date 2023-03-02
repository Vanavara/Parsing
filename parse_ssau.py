from bs4 import BeautifulSoup
import requests
import lxml
import time
import datetime
import csv
import json
import hashlib


def parse_ssau():
    headers = {
        'authority': 'ssau.ru',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }

    url = "https://ssau.ru/science/rnid/conferences"


    cur_date = datetime.datetime.now().strftime("%d-%m_%Y_%H_%M")
    un_name = "Самарский университет"
    un_id = "ssau"

    result = []

    response = requests.get(url = url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    confs_data_ssau = soup.find_all("div", class_="mb-5")
    # print(confs_data_ssau)

    for conf_data_ssau in confs_data_ssau:


        try:
            conf_name = conf_data_ssau.find("a").text
        except:
            conf_name = "Информация по названию конференции отсутсвует"

        try:
            conf_id = un_id + "-" + conf_data_ssau.find("a").get("href").split('/')[-1]
        except:
            conf_id = "Id конференции отсутствует"

        try:
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
        except:
            hash_ = "Хэш конференции отсутствует"

        try:
            conf_href = conf_data_ssau.find("a").get("href")
        except:
            conf_href = "Ссылка на конференцию отсутствует"

        try:
            conf_address = conf_data_ssau.find("div", class_="card-body").find_next("p", class_="card-text mb-0").find_next("p", class_="card-text mb-0").text
        except:
            conf_address = "Информация по адресу конференции отсутсвует"

        try:
            conf_date_begin = conf_data_ssau.find_next("p", class_="card-text").find_next("p", class_="card-text").find_next("p", class_="card-text").text.split("-")[0].split(":")[1].strip()
        except:
            conf_date_begin = "Информация по дате начала конференции неизвестна"

        try:
            conf_date_end = conf_data_ssau.find_next("p", class_="card-text").find_next("p", class_="card-text").find_next("p", class_="card-text").text.split("-")[1].strip()
        except:
            conf_date_end = "Информация по дате начала конференции неизвестна"

        local = ""
        reg_date_begin = ""
        reg_date_end = ""
        conf_card_href = ""
        reg_href = ""
        conf_s_desc = ""
        conf_desc = ""
        org_name = ""
        themes = ""
        online = ""
        offline = ""
        contacts = ""
        rinc = ""


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


    with open(f"data/{un_id}_{cur_date}.json", "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)



def main():
    parse_ssau()


if __name__ == "__main__":
    main()