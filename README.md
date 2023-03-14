This program scraps offer data from allegro.pl, allegrolokalnie.pl, olx.pl and if some offer is interesting 
(it's an offer of a product we're looking for and the price of that product is acceptable) stores received data in a csv file.
Data scraping is legal but allegro.pl is blocking it, so to make it works this scraper uses https://scrapeops.io/
to constantly changing IP address while getting data from allegro.pl. 
The whole occasions data are stored in laptop_occasions.csv and the newest occasions are stored in new_laptop_occasions.xlsx


Variables in main.py:

<br />HEADERS - columns headers in the csv file and dictionary keys
<br />SHEET_NAME - name of sheet in our data_file
<br />unwanted_expressions_in_titles - contains expressions which we dont want in our data occasions
<br />searching_data_dict - contains expressions which we are searching in data
<br />data_file - a file to store scraped data
<br />base_url_... - the base of url address, using to create new urls
<br />urls_... - url address which we want to scrap for data
<br />scrapping_data_html_dict_... - contains names of html elements that we want to scrap
