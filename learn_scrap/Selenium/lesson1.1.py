from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

website = 'https://www.adamchoi.co.uk/overs/detailed'
path = '/Users/kamingau/Downloads/chromedriver_mac_arm64/chromedriver'
# already inject in local bin
driver = webdriver.Chrome()
driver.get(website)

all_matches_button = driver.find_element(by='xpath', value='//label[@analytics-event="All matches"]')
all_matches_button.click()
matches = driver.find_elements(by='xpath', value='//tr')

date = []
home_team = []
score = []
away_team = []

for match in matches:
    date.append(match.find_element(by='xpath', value='./td[1]').text)
    home = match.find_element(by='xpath', value='./td[2]').text
    home_team.append(home)
    print(home)
    score.append(match.find_element(by='xpath', value='./td[3]').text)
    away_team.append(match.find_element(by='xpath', value='./td[4]').text)


# Create Dataframe in Pandas and export to CSV (Excel)
df = pd.DataFrame({'date': date, 'home_team': home_team, 'score': score, 'away_team': away_team})
df.to_csv('football_data.csv', index=False)
print(df)

# quit drive we opened at the beginning
driver.quit()