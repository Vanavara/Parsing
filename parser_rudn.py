from datetime import date
from bs4 import BeautifulSoup
import json
import requests
import hashlib
from find_dates_in_string import find_date_in_string, normalise_str
from datetime import datetime
import time
import hashlib




def make_parse_rudn():
    headers = {
        'authority': 'www.rudn.ru',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.rudn.ru',
        'referer': 'https://www.rudn.ru/media/events?direction=501',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    url = "https://www.rudn.ru/media/events?direction=501&format=968"

    result = []
    un_id = "rudn"
    un_name = "РУДН"
    year = date.today().year


    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    confs_data_rudn = soup.find_all("div", class_="col-md-4 col-sm-6")
    # print(response.text)
    # time.sleep(1)

    # confs_urls_rudn = []
    # for conf in confs_data_rudn:
    #     conf_url_rudn = "https://www.rudn.ru/" + conf.find("div", class_="events__item new-dis__events_item").find("a").get("href")
    #     # print(conf_url_rudn)
    #     confs_urls_rudn.append(conf_url_rudn)

    # for conf_url_rudn in confs_urls_rudn[0:1]:
    #     response = requests.get(conf_url_rudn, headers)
    #     soup = BeautifulSoup(response.text, "lxml")
    #     conf_data_rudn = soup.find("div", class_="article__one-top ")
    #     print(conf_data_rudn)
    #     time.sleep(1)

    for conf in confs_data_rudn:

        try:
            conf_name = conf.find("div", class_="events__item-h").text.strip()
        except:
            conf_name = "Информация по названию конференции отсутствует"

        try:
            conf_href = "https://www.rudn.ru/" + conf.find("div", class_="events__item new-dis__events_item").find("a").get("href")
        except:
            conf_href = "Ссылка на конференцию отсутствует"
        # print(conf_href)

        try:
            conf_id = un_id + "-" + conf.find("div", class_="events__item new-dis__events_item").find("a").get("href").split('/')[-1]
        except:
            conf_id = "Id конференции отсутствует"
        print(conf_id)

        try:
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
        except:
            hash = "Хэш конференции отсутствует"

        try:
            conf_year_rudn = normalise_str(conf.find("div", class_="events__year").text)
        except:
            conf_year_rudn = "Информация по году проведения конференции отсутсвует"

        try:
            conf_date_begin = normalise_str(conf.find("div", class_="header__date").text.strip()[5:])
        except:
            conf_date_begin = "Информация по дате проведения конференции отсутсвует"

        try:
            themes = normalise_str(conf.find("div", class_="events__item-text").text)
        except:
            themes = "Информация по теме конференции отсутсвует"


        conf_s_desc = ''
        reg_date_begin = ''
        reg_date_end = ''
        conf_date_end = ''
        conf_desc = ''
        org_name = ''
        online = False
        offline = False
        conf_address = ''
        reg_href = ''
        contacts = ''
        conf_card_href = ''
        rinc = False


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


    try:
        with open(f'RUDN/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


def main():
    make_parse_rudn()


if __name__ == '__main__':
    main()