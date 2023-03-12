from functions import write_data, get_laptops_occasions
from proxy_data import proxy_url, api_key

"""
this program is a scrapper, it scraps offers data from allegro.pl, allegrolokalnie.pl, olx.pl and if some offer is interesting 
(it,s an offer of a product we're looking for and the price of the product is acceptable) stores received data in a csv file
data scraping is legal but allegro.pl is blocking it, so to make it works this scrapper uses https://proxy.scrapeops.io/v1/ 
to constantly changing IP address while getting data from allegro.pl

HEADERS - headers columns in the csv file and dictionary keys
searching_data_dict - it contain expressions which we are searching in data
data_file - file to store scraped data
base_url_... - the base of url address, using to create new urls
urls_... - url address which we want to scrap for data
scrapping_data_html_dict_... - contains names of html elements that we want to scrap
"""

"""
common variables
"""
HEADERS = ['TYTUŁ', 'CENA', 'LINK', 'DATA']

searching_data_dict = {'RTX 3070': ['3070', 4600],
                       'RTX 3060': ['3060', 3600],
                       'RTX 3050': ['3050', 2900],
                       'RTX 2080': ['2080', 4800],
                       'RTX 2070': ['2070', 3700],
                       'RTX 2060': ['2060', 2500],
                       'GTX 1660': ['1660', 2200],
                       'GTX 1650': ['1650', 2000],
                       'MSI GS65': ['GS65', 2800],
                       'MSI GP66': ['GP66', 4000],
                       'MSI GE66': ['GE66', 4200],
                       'MSI GS66': ['GS66', 4200],
                       'Laptop OLED': ['OLED', 3000],
                       'MSI Stealth': ['Stealth', 3500],
                       'Radeon 6600M': ['6600M', 3800],
                       'Radeon 6700M': ['6700M', 4200],
                       'Radeon 6800M': ['6800M', 4600]
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
                                    'max_page': ['span', "_1h7wt mgmw_wo mh36_8 mvrt_8 _6d89c_wwgPl _6d89c_oLeFV"]}

"""
olx variables
"""

base_url_olx = 'https://www.olx.pl/'

urls_olx = [['https://www.olx.pl/elektronika/komputery/laptopy/warszawa/?page=', 2, '&search%5Bdist%5D=30&search%5Bfilter_float_price%3Afrom%5D=1400&search%5Bfilter_float_price%3Ato%5D=5000&search%5Border%5D=created_at%3Adesc'],
            ['https://www.olx.pl/elektronika/komputery/laptopy/q-msi/?page=', 2, '&search%5Bfilter_float_price%3Afrom%5D=1000&search%5Bfilter_float_price%3Ato%5D=5000&search%5Border%5D=created_at%3Adesc']]

scrapping_data_html_dict_olx = {'titles': ['h6', 'css-16v5mdi er34gjf0'],
                                'prices': ['p', 'css-10b0gli er34gjf0'],
                                'urls': ['a', 'css-rc5s2u'],
                                'max_page': ['a', "css-1mi714g"]}


def main():
    occasion_list = []

    for url in urls_olx:
        laptops_occasions = get_laptops_occasions(url, scrapping_data_html_dict_olx, searching_data_dict, base_url_olx, HEADERS, proxy_url, api_key,  restricted_max_page=False)
        for occasion in laptops_occasions:
            occasion_list.append(occasion)

    for url in urls_all_lok:
        laptops_occasions = get_laptops_occasions(url, scrapping_data_html_dict_all_lok, searching_data_dict, base_url_all_lok, HEADERS, proxy_url, api_key, restricted_max_page=20)
        for occasion in laptops_occasions:
            occasion_list.append(occasion)

    for url in urls_allegro:
        laptops_occasions = get_laptops_occasions(url, scrapping_data_html_dict_allegro, searching_data_dict, base_url_allegro, HEADERS, proxy_url, api_key, restricted_max_page=False)
        for occasion in laptops_occasions:
            occasion_list.append(occasion)

    write_data(data_file, occasion_list, HEADERS)
    print('ALL DONE')


if __name__ == '__main__':
    main()
