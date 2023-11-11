from bs4 import BeautifulSoup
import requests

root = 'https://subslikescript.com'
website = f'{root}/movies_letter-A'
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')
# print(soup.prettify())

#Pagination
pagination = soup.find('ul', class_='pagination')
pages = pagination.find_all('li', class_='page-item')
last_page = pages[-2].text

links = []
for page in range(1, int(last_page)+1)[:2]: # rage(1, 92+1)
    # https://subslikescript.com/movies_letter-A?page=1
    website = f'{website}?page={page}'
    result = requests.get(website)
    content = result.text
    soup = BeautifulSoup(content, 'lxml')

    box = soup.find('article', class_='main-article')


    for link in box.find_all('a', href=True):
        links.append(link['href'])

    print(links)

    for links in link:
        try:
            print(link)
            website = f'{root}/{link}'
            result = requests.get(website)
            content = result.text
            soup = BeautifulSoup(content, 'lxml')

            box = soup.find('article', class_='main-article')

            title = box.find('h1').get_text()
            transcript = box.find('div', class_='full-script').get_text(strip=True, separator=' ')

            with open(f'{title}.txt', 'w') as file:
                file.write(transcript)
        except:
            print(' ---- Link not work ---- ')
            print(link)

