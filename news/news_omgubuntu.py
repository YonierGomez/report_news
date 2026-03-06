import requests
from bs4 import BeautifulSoup


def news(URL):
    """Funcion para obtener noticias de OMG! Ubuntu"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    }
    r = requests.get(URL, headers=headers)

    if r.ok:
        soup = BeautifulSoup(r.text, 'html.parser')

        get_news = []
        for h3 in soup.find_all('h3', class_='layout__title', limit=10):
            link = h3.find('a', href=True)
            if link:
                get_news.append((h3.text.strip(), link['href']))

        return get_news

if __name__ == '__main__':
    for item in news('https://www.omgubuntu.co.uk/'):
        print(item)
