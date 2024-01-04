from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests
import pandas as pd


# MongoDB连接信息
MONGO_CONNECTION_URL = "mongodb+srv://qq1027784227:qq1027784227@hotel.0a4is7r.mongodb.net/"
MONGO_DB_NAME = "hotels"
MONGO_COLLECTION_NAME = "booking_price"

# CSV文件路径
CSV_FILE_PATH = "booking_data.csv"

offset = 0
page = 1
max_pages = 10

url = f"https://www.booking.com/searchresults.en-gb.html?label=gog235jc-1DCAEoggI46AdIM1gDaGKIAQGYAQm4AQfIAQzYAQPoAQGIAgGoAgO4ApiJ-6UGwAIB0gIkYzI2N2E0ZjAtYmFhOS00YjUzLTliYTUtZjk1NDBlYmMzN2Fj2AIE4AIB&sid=bc9a4cbfda9728a8ab892f66ceaa1a79&aid=397617&ss=Hong+Kong&ssne=Hong+Kong&ssne_untouched=Hong+Kong&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-1353149&dest_type=city&checkin=2024-01-05&checkout=2024-01-06&ltfd=6%3A2%3A1-2024_2-2024_3-2024%3A1%3A1&group_adults=2&no_rooms=1&group_children=0&offset={offset}"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# 使用BeautifulSoup解析页面并提取数据
hotels = soup.find_all('div', {'data-testid': 'property-card'})

# 从booking.com获取数据的函数
def scrape_booking_data():
    offset = 0
    page = 1
    max_pages = 10  # 需要捞取的最大页数

    while page <= max_pages:
        url = f"https://www.booking.com/searchresults.en-gb.html?label=gog235jc-1DCAEoggI46AdIM1gDaGKIAQGYAQm4AQfIAQzYAQPoAQGIAgGoAgO4ApiJ-6UGwAIB0gIkYzI2N2E0ZjAtYmFhOS00YjUzLTliYTUtZjk1NDBlYmMzN2Fj2AIE4AIB&sid=bc9a4cbfda9728a8ab892f66ceaa1a79&aid=397617&ss=Hong+Kong&ssne=Hong+Kong&ssne_untouched=Hong+Kong&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-1353149&dest_type=city&checkin=2024-01-05&checkout=2024-01-06&ltfd=6%3A2%3A1-2024_2-2024_3-2024%3A1%3A1&group_adults=2&no_rooms=1&group_children=0&offset={offset}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # 使用BeautifulSoup解析页面并提取数据
        hotels = soup.find_all('div', {'data-testid': 'property-card'})

        # 如果没有找到数据，则停止循环
        if not hotels:
            break

        # 处理每个酒店
        for hotel in hotels:
            # 提取所需的数据
            # Extract the hotel name
            name_element = hotel.find('div', {'data-testid': 'title'})
            name = name_element.text.strip()

            # Extract the hotel location
            location_element = hotel.find('span', {'data-testid': 'address'})
            location = location_element.text.strip()

            # Extract the hotel price
            price_element = hotel.find('span', {'data-testid': 'price-and-discounted-price'})
            price = price_element.text.strip().replace(u'\xa0', u' ')

            # Extract the hotel rating
            rating_element = hotel.find('div', {'class': 'a3b8729ab1 d86cee9b25'})
            rating = rating_element.text.strip()

            # Time period
            time_element = hotel.find('div', {'class': 'c1bae49f17'})
            time = time_element.text.strip()

            # 写入CSV文件
            write_to_csv(name, location, price, rating, time)

            # 写入MongoDB数据库
            write_to_mongodb(name, location, price, rating, time)

        # 偏移量增加25
        offset += 25
        page += 1

# 将数据写入CSV文件（使用pandas）
def write_to_csv(name, location, price, rating, time):
    data = {"Name": [name], "Address": [location], "Price": [price], "Rating": [rating], "Time": [time]}
    df = pd.DataFrame(data)
    df.to_csv(CSV_FILE_PATH, mode="a", index=False, header=not pd.read_csv(CSV_FILE_PATH).empty)

# 将数据写入MongoDB数据库
def write_to_mongodb(name, location, price, rating, time):
    client = MongoClient(MONGO_CONNECTION_URL)
    db = client[MONGO_DB_NAME]
    collection = db[MONGO_COLLECTION_NAME]
    data = {"Name": name, "Address": location, "Price": price, "Rating": rating, "Time": time}
    collection.insert_one(data)
    client.close()

# 运行爬虫脚本
scrape_booking_data()