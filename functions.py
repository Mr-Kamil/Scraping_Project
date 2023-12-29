import datetime
import requests
from bs4 import BeautifulSoup
import re
import csv
import os
import json
import pandas as pd
from selenium import webdriver
import random

today = str(datetime.datetime.today())[:-7]


def get_data_from_web(next_page: str, scrapping_dictionary: dict, proxy_url: str, api_key: str) -> list[dict, ..., dict]:
    # scrapes websites and returns a list of dictionaries containing desired elements,
    # scrapping_dictionary provides names of html elements that we want to scrap
    results = []

    try:
        if re.search(r'allegro\.pl', next_page):
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("window-size=1920,1080")
            chrome_options.add_argument("--headless")

            driver = webdriver.Chrome(options=chrome_options)
            driver.get(next_page)
            # input()

            driver.implicitly_wait(random.randint(3, 5))
            page = driver.page_source
            driver.quit()
            print(next_page)
            soup = BeautifulSoup(page, 'html.parser')

            # page = requests.get(url=proxy_url, params={'api_key': api_key, 'url': next_page})

        else:
            page = requests.get(next_page)
            print(page.status_code, type(page.status_code), next_page)
            soup = BeautifulSoup(page.content, 'html.parser')


        for position in scrapping_dictionary:
            data = scrapping_dictionary[position]

            if position == 'urls_allegro':
                results.append([re.split('" href="|" title="', str(a))[1] for a in soup.find_all(data[0], class_=data[1])])
            elif position == 'max_page_all_lok':
                results.append('blabla')
                # results.append(json.loads(soup.find(scrapping_dictionary[position][0],
                #                                     {scrapping_dictionary[position][1]: True})[scrapping_dictionary[position][1]])[scrapping_dictionary[position][2]])
            elif position != 'urls':
                results.append([a.get_text() for a in soup.find_all(data[0], class_=data[1])])
            else:
                results.append([a['href'] for a in soup.find_all(data[0], class_=data[1])])

    except:
        print('ERROR')
        return ['', '', '', '']

    return results


def remove_duplicates(dictionary_list: list[dict, ..., dict], headers: list) -> list[dict, ..., dict]:
    # removes duplicates from the list, checks only urls
    no_duplicates_list = []
    temp = []
    for dictionary in dictionary_list:
        if dictionary[headers[2]] not in temp:
            no_duplicates_list.append(dictionary)
            temp.append(dictionary[headers[2]])

    return no_duplicates_list


def csv_to_dict_list(file_path: str, headers: list) -> list:
    # returns a list of occasion IDs (link + price) from an existing file. These IDs will be compared with a new list in order to avoid duplicates
    csv_input = open(file_path, 'r', newline='', encoding='utf-8')
    reader = csv.DictReader(csv_input)

    return [row[headers[2]] + row[headers[1]] for row in reader]


def write_data(data_file_path: str, data_list_with_duplicates: list, headers: list, sheet_name: str) -> None:
    # appends new lines to an existing file or creates a new one
    # uses functions: csv_to_dict_list, remove_duplicates
    data_list = remove_duplicates(data_list_with_duplicates, headers)
    output_list = []
    exists = False

    if os.path.exists(data_file_path):
        reader_list = csv_to_dict_list(data_file_path, headers)
        exists = True

    with open(data_file_path, 'a', newline='', encoding='utf-8') as data_file_csv_write:
        writer = csv.DictWriter(data_file_csv_write, fieldnames=headers, lineterminator='\n')

        if not exists:
            writer.writeheader()
        writer.writerow({headers[3]: today})

        for data_list_row in data_list:
            if exists:
                if data_list_row[headers[2]] + str(data_list_row[headers[1]]) not in reader_list:
                    output_list.append(data_list_row)
            else:
                output_list.append(data_list_row)

        make_xlsx_file(output_list, data_file_path, sheet_name)

        for output_list_row in output_list:
            writer.writerow(output_list_row)


def make_xlsx_file(input_data: list[dict, ..., dict], data_file_path: str, sheet_name: str) -> None:
    # creates xlsx file with only the newest occasions
    df = pd.DataFrame(input_data)
    writer = pd.ExcelWriter('new_' + data_file_path.split('.')[0] + '.xlsx', engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name=sheet_name)

    for i, column in enumerate(df.columns):
        column_width = max(df[column].astype(str).map(len).max(), len(column)) + 1
        writer.sheets[sheet_name].set_column(i, i, column_width)

    writer._save()


def check_titles_for_unwanted_expressions(title: str, unwanted_expressions: list) -> bool:
    for expression in unwanted_expressions:
        if re.search(expression, title, re.IGNORECASE):
            return False
    return True


def get_laptops_occasions(url: list[str, int, str], scrapping_dictionary: dict, searching_dictionary: dict, base_url: str, headers: list,
                          proxy_url: str, api_key: str, unwanted_expressions: list, restricted_max_page: bool or int) -> list[dict, ..., dict]:
    # prepares arguments for the get_data_from_web function, checks if the scraped data includes searched contents, creates a list with possibly duplicates
    # uses functions: get_data_from_web, check_titles_for_unwanted_expressions
    page_num = 0
    occasions_list = []

    while True:
        page_num += 1
        next_page = url[0] + str(page_num) + url[2]

        titles, prices, urls, max_pages = get_data_from_web(next_page, scrapping_dictionary, proxy_url, api_key)

        if page_num == 1:
            if restricted_max_page:
                max_page = restricted_max_page
            else:
                max_page = int(max_pages[-1]) if (type(max_pages) == list and len(max_pages) > 1) else max_pages

        if re.search(r'allegro\.pl', next_page) and page_num == 6:  # scrap allegro.pl only for pages 0-10 and 55-70
            page_num = 45
            max_page = 60

        for n in range(len(titles)):
            if check_titles_for_unwanted_expressions(titles[n], unwanted_expressions):
                for position in searching_dictionary:
                    if re.search(searching_dictionary[position][0], titles[n], re.IGNORECASE):
                        try:
                            price = int(re.match(r'\d+', prices[n].replace(' ', '')).group(0))
                        except:
                            pass

                        if searching_dictionary[position][1] >= price:
                            data = {headers[0]: titles[n], headers[1]: price, headers[2]: base_url + str(urls[n]), headers[3]: today}
                            print(data)
                            occasions_list.append(data)

        if page_num == max_page:
            return occasions_list
