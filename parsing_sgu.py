from bs4 import BeautifulSoup
import requests
import lxml
import asyncio
import aiohttp
import time
import datetime
from selenium import webdriver
import modulefinder
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import hashlib
from find_dates_in_string import find_date_in_string, normalise_str
import json
from datetime import date

#  ########################################################################################################################
#  THIS CODE IS WRK ONLY WITH PAGE 1
# result = []
# def parser_pages_sgu():
#     headers = {
#         'authority': 'mc.yandex.ru',
#         'accept': '*/*',
#         'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
#         'origin': 'https://www.sgu.ru',
#         'referer': 'https://www.sgu.ru/',
#         'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
#         'sec-ch-ua-mobile': '?1',
#         'sec-ch-ua-platform': '"Android"',
#         'sec-fetch-dest': 'empty',
#         'sec-fetch-mode': 'cors',
#         'sec-fetch-site': 'cross-site',
#         'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',
#     }
#     url = "https://www.sgu.ru/conference"
#     un_name = "SGU"
#
#
#     response = requests.get(url=url, headers=headers)
#     soup = BeautifulSoup(response.text, "lxml")
#     confs_items_sgu = soup.find("table", class_="views-table cols-6").find_all("tr")
#
#     for conf in confs_items_sgu:
#         conf_data_sgu = conf.find_all("td")
#
#
#         try:
#             conf_name = normalise_str(conf_data_sgu[1].find("a").text)
#         except:
#             conf_name = "Название конференции неизвестно"
#         # print(conf_name)
#
#         try:
#             conf_href = "https://www.sgu.ru/" + normalise_str(conf_data_sgu[1].find("a").get("href"))
#         except:
#             conf_href = "Ссылка на конференцию отсуствует"
#         # print(conf_href)
#
#         try:
#             conf_id = un_name + "-" + normalise_str(conf_data_sgu[1].find("a").get("href").split('/')[-1])
#         except:
#             conf_id = "Название конференции отсуствует"
#         # print(conf_id)
#
#         try:
#             hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
#         except:
#             hash_ = "Хэш конференции отсутствует"
#         # print(hash_)
#
#         try:
#             conf_date_begin = normalise_str(conf_data_sgu[2].text)
#         except:
#             conf_date_begin = "Дата начала конференции отсуствует"
#         # print(conf_date_begin)
#
#
#         try:
#             conf_date_end = normalise_str(conf_data_sgu[3].text)
#         except:
#             conf_date_end = "Дата окончания конференции отсуствует"
#         # print(conf_date_end)
#
#
#         try:
#             org_name = normalise_str(conf_data_sgu[4].text)
#         except:
#             org_name = "Информация по организаторам конференции отсуствует"
#         # print(org_name)
#
#
#         try:
#             contacts = normalise_str(conf_data_sgu[5].text)
#         except:
#             contacts = "Информация по организаторам конференции отсуствует"
#         # print(contacts)
#
#
#         reg_href = ''
#         conf_s_desc = ''
#         reg_date_begin = ''
#         org_name = ''
#         online = False
#         offline = False
#         conf_address = ''
#         reg_href = ''
#         conf_card_href = ''
#         rinc = False
#         reg_date_end = ''
#         conf_desc = ''
#         themes = ''
#
#
#         # print(conf_name)
#         # # print(reg_href)
#         # # print(conf_id)
#         # # print(hash_)
#         # # print(conf_date_begin)
#         # # print(conf_date_end)
#         # # print(org_name)
#         # # print(contacts)
#         # print("#" * 15)
#         #
#         #
#         result.append(
#             {
#                 'conf_id': conf_id,
#                 'hash': hash_,
#                 'un_name': un_name,
#                 'local': " ",
#                 'reg_date_begin': reg_date_begin,
#                 'reg_date_end': reg_date_end,
#                 'conf_date_begin': conf_date_begin,
#                 'conf_date_end': conf_date_end,
#                 'conf_card_href': conf_card_href,
#                 'reg_href': reg_href,
#                 'conf_name': conf_name,
#                 'conf_s_desc': conf_s_desc,
#                 'conf_desc': conf_desc,
#                 'org_name': org_name,
#                 'themes': themes,
#                 'online': online,
#                 'conf_href': conf_href,
#                 'offline': offline,
#                 'conf_address': conf_address,
#                 'contacts': contacts.strip(),
#                 'rinc': rinc,
#             }
#         )
#
#
#         try:
#             with open(f"SGU/{un_name}_{date.today()}.json", "w", encoding="utf-8") as file:
#                 json.dump(result, file, indent=4, ensure_ascii=False)
#         except Exception as e:
#             print(e)
#  END OF CODE FOR PAGE 1
# #######################################################################################################################












def parser_pages_sgu():
    headers = {
        'authority': 'mc.yandex.ru',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'origin': 'https://www.sgu.ru',
        'referer': 'https://www.sgu.ru/',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',
    }

    url = "https://www.sgu.ru/conference"

    un_name = "SGU"

    result = []

    year = date.today().year

    options = webdriver.ChromeOptions()

    options.add_argument("'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',")
    driver = webdriver.Chrome("C:/Users/dell/Desktop/Проекты/ScratchingUniversities/Саратовский национальный исследовательский/chromedriver/chromedriver")



    try:


        #new line
        driver = webdriver.Chrome()

        driver.get(url=url)

        #  new lines
        # wait = WebDriverWait(driver, 35)

        # new location of this line
        next_button = driver.find_element(By.CLASS_NAME, "pager-next")

        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")


        # next_button = driver.find_element(By.CLASS_NAME, "pager-next").click()

        pages_count = int(soup.find("ul", class_="pager").find_all("a")[-3].text)

        for page in range(1, pages_count + 1):

            next_button = driver.find_element(By.CLASS_NAME, "pager-next").click()

            response = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(response.text, "lxml")

            confs_items_sgu = soup.find("table", class_="views-table cols-6").find_all("tr")
        #
        #     for conf in confs_items_sgu:
        #         conf_data_sgu = conf.find_all("td")
        #         print(conf_data_sgu)
        #         print("#" * 100)

    #             try:
    #                 conf_name = conf_data_sgu[1].find("a").text
    #                 print(conf_name)
    #             except:
    #                 conf_name = "Название конференции неизвестно"
    #
    #
    #             try:
    #                 conf_href = "https://www.sgu.ru/" + normalise_str(conf_data_sgu[1].find("a").get("href"))
    #             except:
    #                 conf_href = "Ссылка на конференцию отсуствует"
    #             # print(reg_href)
    #
    #             try:
    #                 conf_id = un_name + "-" + normalise_str(conf_data_sgu[1].find("a").get("href").split('/')[-1])
    #             except:
    #                 conf_id = "id конференции отсуствует"
    #
    #             try:
    #                 hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
    #             except:
    #                 hash_ = "Хэш конференции отсутствует"
    #
    #             try:
    #                 conf_name = conf_data_sgu[1].find("a").text[0]
    #             except:
    #                 conf_name = "Название конференции отсуствует"
    #
    #             try:
    #                 conf_date_begin = normalise_str(conf_data_sgu[2].text)
    #             except:
    #                 conf_date_begin = "Дата начала конференции отсуствует"
    #
    #             try:
    #                 conf_date_end = normalise_str(conf_data_sgu[3].text)
    #             except:
    #                 conf_date_end = "Дата окончания конференции отсуствует"
    #
    #             try:
    #                 org_name = normalise_str(conf_data_sgu[4].text)
    #             except:
    #                 org_name = "Информация по организаторам конференции отсуствует"
    #
    #             try:
    #                 contacts = normalise_str(conf_data_sgu[5].text)
    #             except:
    #                 contacts = "Контактные данные конференции отсуствуют"
    #
    #                 conf_s_desc = ''
    #                 reg_date_begin = ''
    #                 reg_date_end = ''
    #                 org_name = ''
    #                 online = False
    #                 offline = False
    #                 conf_address = ''
    #                 reg_href = ''
    #                 conf_card_href = ''
    #                 rinc = False
    #                 conf_desc = ''
    #                 themes = ''
    #
    #
    #                 result.append(
    #                     {
    #                         'conf_id': conf_id,
    #                         'hash': hash_,
    #                         'un_name': un_name,
    #                         'local': " ",
    #                         'reg_date_begin': reg_date_begin,
    #                         'reg_date_end': reg_date_end,
    #                         'conf_date_begin': conf_date_begin,
    #                         'conf_date_end': conf_date_end,
    #                         'conf_card_href': conf_card_href,
    #                         'reg_href': reg_href,
    #                         'conf_name': conf_name,
    #                         'conf_s_desc': conf_s_desc,
    #                         'conf_desc': conf_desc,
    #                         'org_name': org_name,
    #                         'themes': themes,
    #                         'online': online,
    #                         'conf_href': conf_href,
    #                         'offline': offline,
    #                         'conf_address': conf_address,
    #                         'contacts': contacts.strip(),
    #                         'rinc': rinc,
    #                     }
    #                 )
    #
    #
    #         try:
    #             with open(f'SGU/{un_name}_{date.today()}.json', 'w', encoding="utf-8") as file:
    #                 json.dump(result, file, indent=4, ensure_ascii = False)
    #                 return result
    #         except Exception as e:
    #             print(e)


    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def main():
    parser_pages_sgu()


if __name__ == "__main__":
    main()






#     pages_count = int(soup.find("ul", class_="pager").find_all("a")[-3].text)
#     for page in range(1, pages_count + 1):
#
#
#
#
#
#
#     options = webdriver.ChromeOptions()
#
#     options.add_argument("'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',")
#     driver = webdriver.Chrome("C:/Users/dell/Desktop/Проекты/ScratchingUniversities/Саратовский национальный исследовательский/chromedriver/chromedriver")
#
#     try:
#         driver.get(url=url)
#         time.sleep(1)
#
#         response = requests.get(url=url, headers=headers)
#         soup = BeautifulSoup(response.text, "lxml")
#
#
#
#         try:
#             element = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, "views-field views-field-name-field-et"))
#             )
#         except:
#             print("Timed out waiting for page to load")
#
#
#         for page in range(1, pages_count + 1):
#             next_button = driver.find_element(By.CLASS_NAME, "pager-next").click()
#             time.sleep(1)
#
#             response = requests.get(url = url, headers=headers)
#             soup = BeautifulSoup(response.text, "lxml")
#             confs_even_num_sgu = soup.find_all("tr", class_="even conforg")
#             confs_odd_num_sgu = soup.find_all("tr", class_="odd conforg")
#             print(confs_even_num_sgu)
#             # print(confs_odd_num_sgu)
#
#             projects_urls = []
#             for conf_even_num_sgu in confs_even_num_sgu:
#                 conf_even_url_sgu = confs_even_num_sgu.find("td", class_="views-field views-field-name-field-et").find("a").get("href")
#                 print(conf_even_url_sgu)
#                 projects_urls.append(conf_even_url)
#
#             for conf_odd_url in confs_even_num_sgu:
#                 conf_url = confs_odd_num_sgu.find_all("", class_="views-field views-field-name-field-et").find("a").get("href")
#                 print(conf_odd_url)
#                 projects_urls.append(conf_odd_url)
#
#             print(projects_urls)
#
#
#     except Exception as ex:Ф
#         print(ex)
#     finally:
#         driver.close()
#         driver.quit()
#
#     result = []
#     year = date.today().year
#
#     response = requests.get(url = url, headers=headers)
#     soup = BeautifulSoup(response.text, "lxml")
#     print(response.text)
#
#
# def main():
#     parser_pages_sgu()
#
#
# if __name__ == "__main__":
#     main()