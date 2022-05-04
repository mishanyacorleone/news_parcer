import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import csv


agent = UserAgent()

with open('news.csv', 'w') as F:
    writer = csv.writer(F)
    writer.writerow(['Date', 'Title', 'Full-text', 'img1', 'img2', 'img3', 'img4', 'img5', 'img6', 'img7', 'img8', 'img9', 'img10'])


def scrap_news(links, agent):
    for link in links:
        response = requests.get(url=link, params={
            'user-agent': f'{agent.random}'
        }).text
        soup = BeautifulSoup(response, 'lxml')
        date = soup.find_all('div', class_='news-item__date')[0].text
        title = soup.find_all('div', class_='news-item__title')[0].text
        try:
            full_text = soup.find_all('div', class_='news-item__full-text')[0]
            html_text = '\n'.join(str(text) for text in full_text.find_all('p'))
            images = soup.find_all('li', role='presentation')
            final_data = [date, title, html_text]
            for image in images:
                final_data.append(image.find_all('a')[0].find_all('img')[0].get('src'))
            with open('news.csv', 'a', encoding='utf-8') as F:
                writer = csv.writer(F)
                writer.writerow(final_data)
        except Exception as ex:
            html_text = ''
            for full_text in soup.find_all('p'):
                if '© 2015, Комитет по образованию города Барнаула' in full_text.text:
                    break
                else:
                    html_text += str(full_text)
            images = soup.find_all('li', role='presentation')
            final_data = [date, title, html_text]
            for image in images:
                final_data.append(image.find_all('a')[0].find_all('img')[0].get('src'))
            with open('news.csv', 'a', encoding='utf-8') as F:
                writer = csv.writer(F)
                writer.writerow(final_data)



def num_pages(agent):
    links = list()

    for i in range(1, 33):
        links.append('https://barnaul-obr.ru/news?News_page=' + f'{i}')
    news_links = list()

    for link in links:
        response = requests.get(url=link, params={
            'user-agent': f'{agent.random}'
        }).text
        soup = BeautifulSoup(response, 'lxml').find_all('a', class_='full-link')

        for href in soup:
            news_links.append('https://barnaul-obr.ru' + href.get('href'))
    scrap_news(news_links, agent)


def main():
    num_pages(agent=agent)


if __name__ == '__main__':
    main()