import requests
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient

def scrape_booking_data(offset):
    # 设置请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

    # 构造URL，根据不同的offset获取不同的页面数据
    url = f'https://www.booking.com/xxx?offset={offset}'

    # 发送GET请求，获取页面内容
    response = requests.get(url, headers=headers)

    # 解析HTML内容
    soup = BeautifulSoup(response.content, 'html.parser')

    # 找到需要的数据，如名字、位置、评级和价格
    # Extract the hotel name
    name_element = soup.find('div', {'data-testid': 'title'})
    names = name_element.text.strip()

    # Extract the hotel location
    location_element = soup.find('span', {'data-testid': 'address'})
    locations = location_element.text.strip()

    # Extract the hotel price
    price_element = soup.find('span', {'data-testid': 'price-and-discounted-price'})
    prices = price_element.text.strip().replace(u'\xa0', u' ')

    # Extract the hotel rating
    rating_element = soup.find('div', {'class': 'a3b8729ab1 d86cee9b25'})
    ratings = rating_element.text.strip()

    # Time period
    time_element = soup.find('div', {'class': 'c1bae49f17'})
    times = time_element.text.strip()

    # 存储数据到CSV文件
    data = {
        'Name': names,
        'Location': locations,
        'Rating': ratings,
        'Price': prices,
        'Time': times,
    }
    df = pd.DataFrame(data)
    df.to_csv('booking_data.csv', mode='a', header=False, index=False)

    # 存储数据到MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['booking']
    collection = db['data']
    for i in range(len(names)):
        entry = {
            'Name': names[i].text.strip(),
            'Location': locations[i].text.strip(),
            'Rating': ratings[i].text.strip(),
            'Price': prices[i].text.strip(),
        }
        collection.insert_one(entry)

# 设置初始offset和每页的偏移量
initial_offset = 0
offset_increment = 25

# 爬取首十页的数据
for page in range(10):
    offset = initial_offset + page * offset_increment
    scrape_booking_data(offset)