from functions import write_data, get_laptops_occasions
from proxy_data import proxy_url, api_key
import os

"""
common variables
"""
HEADERS = ['TYTUŁ', 'CENA', 'LINK', 'DATA']
SHEET_NAME = 'Laptopy'

unwanted_expressions_in_titles = ['3050u', 'komputer', 'karta graficzna', 'stacjonarny', 'N3060', '6500U']

# first argument: a search word, second argument: the maximum acceptable price
searching_data_dict = {'RTX 3070': ['3070', 4000],
                       'RTX 4050': ['4050', 4000],
                       'RTX 3060': ['3060', 3200],
                       'RTX 3050': ['3050', 2400],
                       'RTX 2080': ['2080', 3800],
                       'RTX 2070': ['2070', 3200],
                       'RTX 2050': ['2050', 2600],
                       'MSI GS65': ['GS65', 2800],
                       'MSI GP66': ['GP66', 4000],
                       'MSI GE66': ['GE66', 4200],
                       'MSI GS66': ['GS66', 4200],
                       'Laptop OLED': ['OLED', 3000],
                       'MSI Stealth': ['Stealth', 3500],
                       'Radeon 6600M': ['6600M', 3800],
                       'Radeon 6700M': ['6700M', 4200],
                       'Radeon 6550': ['6550', 3300],
                       'Radeon 6550': ['6500', 3300],
                       'Radeon 6800M': ['6800M', 4600],
                       'RTX 2050': ['2050', 2500],
                       'Bravo': ['Bravo', 4000],
                    }

data_file = 'laptop_occasions.csv'

"""
allegro lokalnie variables
"""

base_url_all_lok = 'https://allegrolokalnie.pl'

urls_all_lok = [['https://allegrolokalnie.pl/oferty/komputery/laptopy-491?price_from=1000&price_to=5000&page=', 2, '']]

scrapping_data_html_dict_all_lok = {'titles': ['h3', 'mlc-itembox__title'],
                                    'prices': ['span', 'ml-offer-price__dollars'],
                                    'urls': ['a', 'mlc-card mlc-itembox'],
                                    'max_page_all_lok': ['div', 'data-mlc-listing-bottom-pagination', 'pages_count']}

"""
allegro variables
"""

base_url_allegro = ''

urls_allegro = [['https://allegro.pl/kategoria/laptopy-491?price_from=1400&price_to=5000&order=n&p=', 2, '']]

scrapping_data_html_dict_allegro = {'titles': ['h2', "mgn2_14 m9qz_yp meqh_en mpof_z0 mqu1_16 m6ax_n4 mp4t_0 m3h2_0 mryx_0 munh_0 mj7a_4"],
                                    'prices': ['span', "mli8_k4 msa3_z4 mqu1_1 mgmw_qw mp0t_ji m9qz_yo mgn2_27 mgn2_30_s"],
                                    'urls_allegro': ['h2', "mgn2_14 m9qz_yp meqh_en mpof_z0 mqu1_16 m6ax_n4 mp4t_0 m3h2_0 mryx_0 munh_0 mj7a_4"],
                                    'max_page': ['span', "_1h7wt mgmw_wo mh36_8 mvrt_8"]}

"""
olx variables
"""

base_url_olx = 'https://www.olx.pl/'

urls_olx = [['https://www.olx.pl/elektronika/komputery/laptopy/warszawa/?page=', 2,
             '&search%5Bdist%5D=30&search%5Bfilter_float_price%3Afrom%5D=1400&search%5Bfilter_float_price%3Ato%5D=5000&search%5Border%5D=created_at%3Adesc'],
            ['https://www.olx.pl/elektronika/komputery/laptopy/q-msi/?page=', 2,
             '&search%5Bfilter_float_price%3Afrom%5D=1000&search%5Bfilter_float_price%3Ato%5D=5000&search%5Border%5D=created_at%3Adesc']]

scrapping_data_html_dict_olx = {'titles': ['h6', 'css-16v5mdi er34gjf0'],
                                'prices': ['p', 'css-10b0gli er34gjf0'],
                                'urls': ['a', 'css-rc5s2u'],
                                'max_page': ['a', "css-1mi714g"]}


arguments_list = [[urls_olx, (scrapping_data_html_dict_olx, searching_data_dict, base_url_olx, HEADERS,
                              proxy_url, api_key, unwanted_expressions_in_titles, 15)],
                  [urls_all_lok, [scrapping_data_html_dict_all_lok, searching_data_dict, base_url_all_lok, HEADERS,
                                  proxy_url, api_key, unwanted_expressions_in_titles, 15]],
                  [urls_allegro, [scrapping_data_html_dict_allegro, searching_data_dict, base_url_allegro, HEADERS,
                                  proxy_url, api_key, unwanted_expressions_in_titles, False]]]


arguments_list2 = [[urls_allegro, [scrapping_data_html_dict_allegro, searching_data_dict, base_url_allegro, HEADERS,
                                  proxy_url, api_key, unwanted_expressions_in_titles, False]]]


arguments_list1 = [[urls_olx, (scrapping_data_html_dict_olx, searching_data_dict, base_url_olx, HEADERS,
                              proxy_url, api_key, unwanted_expressions_in_titles, 20)],
                  [urls_all_lok, [scrapping_data_html_dict_all_lok, searching_data_dict, base_url_all_lok, HEADERS,
                                  proxy_url, api_key, unwanted_expressions_in_titles, 15]]]


def main():
    occasion_list = []

    for arguments in arguments_list:
        for url in arguments[0]:
            laptops_occasions = get_laptops_occasions(url, *arguments[1])
            for occasion in laptops_occasions:
                occasion_list.append(occasion)

    write_data(data_file, occasion_list, HEADERS, SHEET_NAME)
    os.system(r'start ' + r"C:\Users\Dom\Desktop\new_laptop_occasions.xlsx.lnk")
    print('ALL DONE')


if __name__ == '__main__':
    main()
