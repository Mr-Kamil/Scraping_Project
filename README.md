This program is a scrapper, it scraps offers data from allegro.pl, allegrolokalnie.pl, olx.pl and if some offer is interesting 
(it's an offer of a product we're looking for and the price of the product is acceptable) stores received data in a csv file.
Data scraping is legal but allegro.pl is blocking it, so to make it works this scrapper uses https://scrapeops.io/
to constantly changing IP address while getting data from allegro.pl

HEADERS - headers columns in the csv file and dictionary keys
searching_data_dict - it contain expressions which we are searching in data
data_file - file to store scraped data
base_url_... - the base of url address, using to create new urls
urls_... - url address which we want to scrap for data
scrapping_data_html_dict_... - contains names of html elements that we want to scrap
