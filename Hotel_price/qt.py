import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit
from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
from datetime import datetime
import json

class ScraperApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.url_input = QLineEdit()
        self.layout.addWidget(self.url_input)

        self.start_button = QPushButton('Start Scrapy')
        self.start_button.clicked.connect(self.start_scrapy)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

    def start_scrapy(self):
        base_url = "https://www.booking.com/searchresults.en-gb.html?label=gog235jc-1DCAEoggI46AdIM1gDaGKIAQGYAQm4AQfIAQzYAQPoAQGIAgGoAgO4ApiJ-6UGwAIB0gIkYzI2N2E0ZjAtYmFhOS00YjUzLTliYTUtZjk1NDBlYmMzN2Fj2AIE4AIB&sid=bc9a4cbfda9728a8ab892f66ceaa1a79&aid=397617&ss=Hong+Kong&ssne=Hong+Kong&ssne_untouched=Hong+Kong&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-1353149&dest_type=city&checkin=2024-01-05&checkout=2024-01-06&ltfd=6%3A2%3A1-2024_2-2024_3-2024%3A1%3A1&group_adults=2&no_rooms=1&group_children=0"
        data = []

        for offset in range(0, 501, 25):
            url = f"{base_url}&offset={offset}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            hotels = soup.find_all('div', {'data-testid': 'property-card'})

            for hotel in hotels:
                name = hotel.find('div', {'data-testid': 'title'}).text.strip()
                location = hotel.find('span', {'data-testid': 'address'}).text.strip()
                price = float(hotel.find('span', {'data-testid': 'price-and-discounted-price'}).text.strip().replace(u'\xa0', u' '))
                rating = float(hotel.find('div', {'class': 'a3b8729ab1 d86cee9b25'}).text.strip())
                time = datetime.now().strftime('%Y-%m')
                month = datetime.now().strftime('%b')
                district = location.split(',')[1] if ',' in location else location

                data.append({
                    'hotel_name': name,
                    'location': location,
                    'price': price,
                    'rating': rating,
                    'time': time,
                    'month': month,
                    'district': district
                })

        client = MongoClient('mongodb+srv://qq1027784227:qq1027784227@hotel.0a4is7r.mongodb.net/')
        db = client['hotels']
        collection = db['booking_price']
        collection.insert_many(data)

        print(f'Successfully scraped and saved data from {base_url}')

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = ScraperApp()

    ex.show()

    sys.exit(app.exec_())