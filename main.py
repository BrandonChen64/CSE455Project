import pandas as pd
import requests
from bs4 import BeautifulSoup
# from requests_html import HTMLSession

original = pd.read_csv('news_summary.csv', encoding='ISO-8859-1') #Both ISO-8859-1 and cp1252 seem to work

# df.describe()

print(original.info()) #The info is consistent with the website
print(original.isnull().sum()) #Number of missing is also consistent with the website

# df.isna().mean()

#Try to fill in missing data

missing_ctext = original[original['ctext'].isnull()]
#All missing ctext seems to come from the same website
for i, row in missing_ctext.iterrows():

    string = ''
    url = row['read_more']
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')

    #https://www.indiatoday.in/ format
    container = soup.find('div', class_='jsx-ace90f4eca22afc7 Story_description__fq_4S description paywall')
    if container:
        content = container.find_all('p')
        # string = ''.join([text.text.strip() for text in content if text.text.strip()])
        for text in content: string = string + text.text
        string = string.strip()
        print("Row: ", i)
        if not string:
            print('Story has expired\n\n')
        else:
            print(string, '\n\n')
    else:
        print("Row: ", i, "might have a different soup logic")





    #Use 136 as an example
    # if i == 136:
    #     print(row['read_more'])

    #Use 1140 as a bad example?
    #501 story has expired
    #510 story as a ad div in the middle
    # print(i)
    # if i == 1167:
    #     print(row['read_more'])
    #     print(row['text'])