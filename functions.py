import datetime
import requests
from bs4 import BeautifulSoup
import re
import csv
import os
import json

today = str(datetime.datetime.today())[:-7]


def get_data_from_web(next_page: str, scrapping_dictionary: dict, proxy_url: str, api_key: str) -> list[dict, ..., dict]:  # scraps websites and returns a list of dictionaries with wanted elements,
    # scrapping dictionary provides names of html elements that we want to scrap
    results = []

    if re.search(r'allegro\.pl', next_page):
        page = requests.get(url='https://proxy.scrapeops.io/v1/', params={'api_key': 'd6ff2897-f7d1-40c0-8859-15dcb1d0d177', 'url': next_page})
    else:
        page = requests.get(next_page)

    print(page.status_code, next_page)
    soup = BeautifulSoup(page.content, 'html.parser')

    for position in scrapping_dictionary:
        data = scrapping_dictionary[position]

        if position == 'urls_allegro':
            results.append([re.split('" href="|" title="', str(a))[1] for a in soup.find_all(data[0], class_=data[1])])
        elif position == 'max_page_all_lok':
            results.append(json.loads(soup.find(scrapping_dictionary[position][0],
                                                {scrapping_dictionary[position][1]: True})[scrapping_dictionary[position][1]])[scrapping_dictionary[position][2]])
        elif position != 'urls':
            results.append([a.get_text() for a in soup.find_all(data[0], class_=data[1])])
        else:
            results.append([a['href'] for a in soup.find_all(data[0], class_=data[1])])

    return results


def remove_duplicates(dictionary_list: list[dict, ..., dict]) -> list[dict, ..., dict]:  # remove duplicates from the list, checks only urls
    no_duplicates_list = []
    temp = []
    for dictionary in dictionary_list:
        if dictionary['LINK'] not in temp:
            no_duplicates_list.append(dictionary)
            temp.append(dictionary['LINK'])

    return no_duplicates_list


def csv_to_dict_list(file_path: str) -> list:  # returns a list of links from an existing file which are later comparing with a new list in order to avoid duplicates
    csv_input = open(file_path, 'r', newline='', encoding='utf-8')
    reader = csv.DictReader(csv_input)

    return [row["LINK"] for row in reader]


def write_data(data_file_path: str, data_list_with_duplicates: list, fieldnames: list) -> None:  # append new lines to an existing file or create a new one
    # uses functions: csv_to_dict_list, remove_duplicates
    data_list = remove_duplicates(data_list_with_duplicates)
    output_list = []
    exists = False

    if os.path.exists(data_file_path):
        reader_list = csv_to_dict_list(data_file_path)
        exists = True

    with open(data_file_path, 'a', newline='', encoding='utf-8') as data_file_csv_write:
        writer = csv.DictWriter(data_file_csv_write, fieldnames=fieldnames, lineterminator='\n')

        if not exists:
            writer.writeheader()
        writer.writerow({'DATA': today})

        for data_list_row in data_list:
            if exists:
                if data_list_row['LINK'] not in reader_list:
                    output_list.append(data_list_row)
            else:
                output_list.append(data_list_row)

        for output_list_row in output_list:
            writer.writerow(output_list_row)


def get_laptops_occasions(url: list[str, int, str], scrapping_dictionary: dict, searching_dictionary: dict, base_url: str,
                          headers: list, proxy_url: str, api_key: str, restricted_max_page: bool or int) -> list[dict, ..., dict]:
    # prepares arguments for the get_data_from_web function, checks if scraped data includes searched contain, creates a list with possibly duplicates
    # uses functions: get_data_from_web
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

        if re.search(r'allegro\.pl', next_page) and page_num == 10:  # scrap only pages 0-10 and 55-70
            page_num = 55
            max_page = 70

        for n in range(len(titles)):
            if not re.search('3050U', titles[n].upper()):
                for position in searching_dictionary:
                    if re.search(searching_dictionary[position][0].lower(), titles[n].lower()):
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
