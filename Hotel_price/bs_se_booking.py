import csv
import time
from selenium import webdriver
from bs4 import BeautifulSoup



# set up webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # run Chrome in headless mode
driver = webdriver.Chrome(options=options)

# navigate to page
url = 'https://www.booking.com/searchresults.en-gb.html?ss=Hong+Kong&ssne=Hong+Kong&ssne_untouched=Hong+Kong&label=gen173nr-1FCAMoYjjpAkgJWARoYogBAZgBCbgBB8gBDNgBAegBAfgBAogCAagCA7gChPz9pQbAAgHSAiQzODZkOGE5MS0xMGVhLTQxZjQtYjNlMC02NGM0YmUxOGYzM2HYAgXgAgE&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=city&dest_id=-1353149&dest_type=city&checkin=2023-08-01&checkout=2023-08-05&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure'
driver.get(url)

# loop through all pages
page = 1
while True:
    # wait for page to load
    time.sleep(2)

    # parse HTML with BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # find all hotel names and ratings
    hotel_names = soup.find_all('div', {'data-testid': 'title'})
    hotel_ratings = soup.find_all('div', {'class': 'b5cd09854e d10a6220b4'})

    # write data to CSV file
    with open('booking.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        if page == 1:
            writer.writerow(['Hotel Name', 'Rating'])

        for i in range(len(hotel_names)):
            hotel_name = hotel_names[i].text.strip()
            hotel_rating = hotel_ratings[i].text.strip()
            writer.writerow([hotel_name, hotel_rating])

    # check if there is a next page
    # next_button = driver.find_elements_by_xpath('//button[@aria-label="Next page"]')
    next_button = driver.find_element(by='xpath', value='//span[@class="b6dc9a9e69 e25355d3ee"]')
    if not next_button:
        break

    # go to next page
    next_button.click()
    page += 1

# close webdriver
driver.quit()