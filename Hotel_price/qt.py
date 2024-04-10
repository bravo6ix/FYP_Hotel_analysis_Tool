from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import Qt
from pymongo import MongoClient
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient
import requests
import pandas as pd
import re
import time

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.mongo_label = QLabel("MongoDB connect string")
        self.mongo_input = QLineEdit()

        self.address_label = QLabel("Booking target address")
        self.address_input = QLineEdit()

        self.collection_label = QLabel("MongoDB collection")
        self.collection_input = QLineEdit()

        self.scrape_button = QPushButton("Scrape")
        self.scrape_button.clicked.connect(self.scrape)

        layout = QVBoxLayout()
        layout.addWidget(self.mongo_label)
        layout.addWidget(self.mongo_input)
        layout.addWidget(self.address_label)
        layout.addWidget(self.address_input)
        layout.addWidget(self.collection_label)
        layout.addWidget(self.collection_input)
        layout.addWidget(self.scrape_button)

        self.setLayout(layout)

    def scrape(self):
        mongo_connect_string = self.mongo_input.text()
        target_address = self.address_input.text()
        collection_name = self.collection_input.text()

        client = MongoClient(mongo_connect_string)
        db = client['hotels']
        collection = db[collection_name]

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'
        }

        response = requests.get(target_address, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        hotels = soup.findAll('div', {'data-testid': 'property-card'})

        hotels_data = []
        for hotel in hotels:
            # Here you can call your scrape function
            # hotel_data = scrape_hotel_data(hotel)
            # hotels_data.append(hotel_data)
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
        all_hotels_data = scrape_all_hotels(address_input)
        hotels = pd.DataFrame(all_hotels_data)
        hotelss = hotels.drop_duplicates()
        data_dict = hotelss.to_dict("records")
        collection.insert_many(hotels_data)

    # Current time
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    hotelss.to_csv(f'Hotel_price/sraped_folder/{current_time}_bs_hotels.csv', header=True, index=False)
    hotelss.to_json(f'Hotel_price/sraped_folder/{current_time}_bs_hotels.json', orient='records')
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()