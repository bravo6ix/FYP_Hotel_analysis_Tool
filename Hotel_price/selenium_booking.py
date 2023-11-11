from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time

# define the website to scrape and path where the chromediver is located
website = 'https://www.booking.com/searchresults.en-gb.html?ss=Hong%20Kong&ssne=Hong%20Kong&ssne_untouched=Hong%20Kong&label=gog235jc-1DCAEoggI46AdIM1gDaGKIAQGYAQm4AQfIAQzYAQPoAQGIAgGoAgO4ApiJ-6UGwAIB0gIkYzI2N2E0ZjAtYmFhOS00YjUzLTliYTUtZjk1NDBlYmMzN2Fj2AIE4AIB&sid=bc9a4cbfda9728a8ab892f66ceaa1a79&aid=397617&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-1353149&dest_type=city&checkin=2023-08-01&checkout=2023-08-05&group_adults=2&no_rooms=1&group_children=0'
path = '/Users/kamingau/Downloads/chromedriver_mac_arm64/chromedriver'  # write your path here
service = Service(executable_path=path)  # selenium 4
driver = webdriver.Chrome(service=service)  # define 'driver' variable
# open Google Chrome with chromedriver
driver.get(website)

# time.sleep(10)

# # locate and click on a button
# all_matches_button = driver.find_element(by='xpath', value='//label[@analytics-event="All matches"]')
# all_matches_button.click()

# select elements in the table
hotels = driver.find_elements(by='xpath', value='//div[@data-testid="property-card"]')
print(f'There are: {len(hotels)} hotels.')


hotel_list = []
# looping through the matches list
for hotel in hotels:
    hotel_dict = {}
    hotel_dict['hotel'] = hotel.find_element(by='xpath', value='//div[@data-testid="title"]').text
    hotel_dict['price'] = hotel.find_element(by='xpath', value='//span[@data-testid="price-and-discounted-price"]').text
    hotel_dict['score'] = hotel.find_element(by='xpath', value='//div[@data-testid="review-score"]/div[1]').text
    hotel_dict['avg review'] = hotel.find_element(by='xpath', value='//div[@data-testid="review-score"]/div[2]/div[1]').text
    hotel_dict['reviews count'] = hotel.find_element(by='xpath', value='//div[@data-testid="review-score"]/div[2]/div[2]').text
    hotel_list.append(hotel_dict)
    df = pd.DataFrame(hotel_list)
    df.to_csv('hotels_list.csv', index=False)
# quit drive we opened at the beginning
driver.quit()

