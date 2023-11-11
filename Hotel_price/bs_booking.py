from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://www.booking.com/searchresults.en-gb.html?label=gog235jc-1DCAEoggI46AdIM1gDaGKIAQGYAQm4AQfIAQzYAQPoAQGIAgGoAgO4ApiJ-6UGwAIB0gIkYzI2N2E0ZjAtYmFhOS00YjUzLTliYTUtZjk1NDBlYmMzN2Fj2AIE4AIB&sid=bc9a4cbfda9728a8ab892f66ceaa1a79&aid=397617&ss=Hong%20Kong&ssne=Hong%20Kong&ssne_untouched=Hong%20Kong&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-1353149&dest_type=city&checkin=2023-08-01&checkout=2023-08-05&group_adults=2&no_rooms=1&group_children=0&offset=1'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'lxml')

#Pagination
pagination = soup.find('ol', class_='a8b500abde')
pages = pagination.find_all('li', class_='f32a99c8d1')
last_page = pages[-2].text

# for page in range(1, int(last_page)+1):

# Find all the hotel elements in the HTML document
hotels = soup.findAll('div', {'data-testid': 'property-card'})

hotels_data = []
# Loop over the hotel elements and extract the desired data
for hotel in hotels:
    # Extract the hotel name
    name_element = hotel.find('div', {'data-testid': 'title'})
    name = name_element.text.strip()

    # Extract the hotel location
    location_element = hotel.find('span', {'data-testid': 'address'})
    location = location_element.text.strip()

    # Extract the hotel price
    price_element = hotel.find('span', {'data-testid': 'price-and-discounted-price'})
    price = price_element.text.strip()

    # Extract the hotel rating
    rating_element = hotel.find('div', {'class': 'b5cd09854e d10a6220b4'})
    rating = rating_element.text.strip()

    # Append hotes_data with info about hotel
    hotels_data.append({
        'name': name,
        'location': location,
        'price': price,
        'rating': rating
    })

hotels = pd.DataFrame(hotels_data)
hotels.head()

hotels.to_csv('bs_hotels.csv', header=True, index=False)