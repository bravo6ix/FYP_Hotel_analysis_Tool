from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import re
import time

#url = 'https://www.booking.com/searchresults.en-gb.html?label=gog235jc-1DCAEoggI46AdIM1gDaGKIAQGYAQm4AQfIAQzYAQPoAQGIAgGoAgO4ApiJ-6UGwAIB0gIkYzI2N2E0ZjAtYmFhOS00YjUzLTliYTUtZjk1NDBlYmMzN2Fj2AIE4AIB&sid=bc9a4cbfda9728a8ab892f66ceaa1a79&aid=397617&ss=Hong%20Kong&ssne=Hong%20Kong&ssne_untouched=Hong%20Kong&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-1353149&dest_type=city&checkin=2023-08-01&checkout=2023-08-05&group_adults=2&no_rooms=1&group_children=0&offset=1'
url = 'https://www.booking.com/searchresults.en-gb.html?ss=Hong+Kong&ssne=Hong+Kong&ssne_untouched=Hong+Kong&label=gog235jc-1DCAEoggI46AdIM1gDaGKIAQGYAQm4AQfIAQzYAQPoAQGIAgGoAgO4ApiJ-6UGwAIB0gIkYzI2N2E0ZjAtYmFhOS00YjUzLTliYTUtZjk1NDBlYmMzN2Fj2AIE4AIB&sid=bc9a4cbfda9728a8ab892f66ceaa1a79&aid=397617&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-1353149&dest_type=city&checkin=2024-01-05&checkout=2024-01-06&ltfd=6%3A2%3A1-2024_2-2024_3-2024%3A1%3A1&group_adults=2&no_rooms=1&group_children=0'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

response = requests.get(url, headers=headers)
time.sleep(5)
soup = BeautifulSoup(response.text, 'html.parser')


# Find all the hotel elements in the HTML document
hotels = soup.findAll('div', {'data-testid': 'property-card'})

hotels_data = []
# Loop over the hotel elements and extract the desired data
for hotel in hotels:
    # Extract the hotel name
    name_element = hotel.find('div', {'data-testid': 'title'})
    if name_element is not None:
        name = name_element.text.strip()
    else:
        name = 'N/A'

    # Extract the hotel location
    location_element = hotel.find('span', {'data-testid': 'address'})
    if location_element is not None:
        location = location_element.text.strip().split(',')[0]
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

    # Append hotes_data with info about hotel
    hotels_data.append({
        'hotel_name': name,
        'district': location,
        'price': price,
        'rating': ratings,
        'month': month2,
    })

hotels = pd.DataFrame(hotels_data)
hotels.head()

# hotels.to_csv('bs_hotels.csv', header=True, index=False)
hotels.to_json('Hotel_price/bs_hotels.json', orient='records')