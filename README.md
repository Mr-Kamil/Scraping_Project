This program scrapes offer data from allegro.pl, allegrolokalnie.pl and olx.pl .If an offer is interesting (it's an offer for a product the user is looking for and the price is acceptable) the program stores received data in a csv file.
<br />Data scraping is legal but allegro.pl is blocking it, so to get around this, this scraper uses https://scrapeops.io/
to constantly changing IP address while getting data from allegro.pl. 
<br />
<br />The whole scraped data is stored in laptop_occasions.csv and the newest data (the last search) is stored in new_laptop_occasions.xlsx
<br />
<br />
<br />Variables in main.py are as follows:
<br />
<br />HEADERS - columns headers in the csv file and dictionary keys
<br />SHEET_NAME - the name of sheet in the data_file
<br />unwanted_expressions_in_titles - expressions that should not appear in the scraped data occasions
<br />searching_data_dict - expressions that the program is searching for in the  data
<br />base_url_... - the base url address, using to create new urls
<br />urls_... - urls to scrape for data
<br />scrapping_data_html_dict_... - names of HTML elements that the program is scraping
