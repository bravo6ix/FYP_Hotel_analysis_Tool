from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient
import requests
import pandas as pd
import re
import time

base_url = 'https://www.booking.com/searchresults.en-gb.html?ss=Hong+Kong&ssne=Hong+Kong&ssne_untouched=Hong+Kong&efdco=1&label=gog235jc-1BCAEoggI46AdIM1gDaGKIAQGYAQm4AQfIAQzYAQHoAQGIAgGoAgO4ApiJ-6UGwAIB0gIkYzI2N2E0ZjAtYmFhOS00YjUzLTliYTUtZjk1NDBlYmMzN2Fj2AIF4AIB&sid=bc9a4cbfda9728a8ab892f66ceaa1a79&aid=397617&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-1353149&dest_type=city&checkin=2024-05-01&checkout=2024-05-04&ltfd=6%3A2%3A%3A%3A1&group_adults=2&no_rooms=1&group_children=0'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

response = requests.get(base_url, headers=headers)
#time.sleep(5)
# soup = BeautifulSoup(response.text, 'html.parser')
soup = BeautifulSoup(response.text, "lxml")

# Find all the hotel elements in the HTML document
hotels = soup.findAll('div', {'data-testid': 'property-card'})

hotels_data = []

def scrape_hotel_data(hotel):
    #Extract the hotel name
    name_element = hotel.find('div', {'data-testid': 'title'})
    if name_element is not None:
        name = name_element.text.strip()
    else:
        name = 'N/A'

    # Extract the hotel location
    location_element = hotel.find('span', {'data-testid': 'address'})
    if location_element is not None:
        location = location_element.text.strip().split(',')[0]
        location = location.split(' District')[0]
    else:
        location = 'N/A'


    # Extract the hotel price
    price_element = hotel.find('span', {'data-testid': 'price-and-discounted-price'})
    if price_element is not None:
        price = price_element.text.strip().replace(u'\xa0', u' ')
        price = int(''.join(re.findall(r'\d+', price.replace(',', ''))))
    else:
        price = 0


    # Extract the hotel rating
    rating_element = hotel.find('div', {'class': 'a3b8729ab1 d86cee9b25'})
    if rating_element is not None:
        rating = rating_element.text.strip()
        ratings = float(rating.split('Scored')[0].strip())
    else:
        ratings = 0

    # Time for scraping
    month2 = datetime.now().strftime('%b')

    # Extract the target start and end dates
    startweek_element = hotel.find('div', {'class': 'a8887b152e'})
    if startweek_element is not None:
        startweek = startweek_element.text.strip()
        startweek = startweek[:3]
    else:
        startweek = 'N/A'

    startday_element = hotel.find('div', {'class': 'a8887b152e'})
    if startday_element is not None:
        start_month_day = startday_element.text.strip()
        start_month_day = ''.join(re.findall(r'\d+', start_month_day))
    else:
        start_month_day = 'N/A'

    startmonth_element = hotel.find('div', {'class': 'a8887b152e'})
    if startmonth_element is not None:
        start_month = startmonth_element.text.strip()
        start_month = start_month[-3:]
    else:
        start_month = 'N/A'

    # End
    endweek_element = hotel.find('div', {'class': 'a8887b152e'})
    if endweek_element is not None:
        end_week = endweek_element.text.strip()
        end_week = end_week[:3]
    else:
        end_week = 'N/A'

    endday_element = hotel.find('div', {'class': 'a8887b152e'})
    if endday_element is not None:
        end_month_day = endday_element.text.strip()
        end_month_day = ''.join(re.findall(r'\d+', end_month_day))
    else:
        end_month_day = 'N/A'

    endmonth_element = hotel.find('div', {'class': 'a8887b152e'})
    if endmonth_element is not None:
        end_month = endmonth_element.text.strip()
    else:
        end_month = 'N/A'

    # Extract the number of views
    platform_views_element = hotel.find('div', {'class': 'abf093bdfe f45d8e4c32 d935416c47'})
    if platform_views_element is not None:
        platform_views = platform_views_element.text.strip()
        platform_views = int(''.join(re.findall(r'\d+', platform_views.replace(',', ''))))
    else:
        platform_views = 0

    # Append hotes_data with info about hotel
    hotel_data = {
        'hotel_name': name,
        'district': location,
        'price': price,
        'rating': ratings,
        'scraped_month': month2,
        'views': platform_views,
        'target_start_week' : startweek,
        'target_start_month': start_month,
        'target_start_month_day': start_month_day,
        'target_end_week' : end_week,
        'target_end_month': end_month,
        'target_end_month_day': end_month_day,
    }

    return hotel_data

def scrape_all_hotels(base_url):
    offset = 0
    all_hotels_data = []

    while offset <= 100:
        url = f"{base_url}?offset={offset}"
        response = requests.get(url, headers=headers)
        time.sleep(2)
        soup = BeautifulSoup(response.text, 'html.parser')
        hotels = soup.findAll('div', {'data-testid': 'property-card'})

        for hotel in hotels:
            hotel_data = scrape_hotel_data(hotel)
            all_hotels_data.append(hotel_data)

        offset += 25

    return all_hotels_data

all_hotels_data = scrape_all_hotels(base_url)
hotels = pd.DataFrame(all_hotels_data)
hotelss = hotels.drop_duplicates()
# MongoDB connection
client = MongoClient("mongodb+srv://qq1027784227:qq1027784227@hotel.0a4is7r.mongodb.net/")
db = client['hotels']
collection = db['booking_price']

## handle transform dataframe to dict
data_dict = hotelss.to_dict("records")
collection.insert_many(data_dict)

# Current time
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
hotelss.to_csv(f'Hotel_price/sraped_folder/{current_time}_bs_hotels.csv', header=True, index=False)
hotelss.to_json(f'Hotel_price/sraped_folder/{current_time}_bs_hotels.json', orient='records')