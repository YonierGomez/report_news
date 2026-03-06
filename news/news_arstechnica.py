import requests
from bs4 import BeautifulSoup


def news(URL):
    """Funcion para obtener noticias de Ars Technica AI"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    }
    r = requests.get(URL, headers=headers)

    if r.ok:
        soup = BeautifulSoup(r.text, 'html.parser')

        get_news = []
        for h2 in soup.find_all('h2', limit=10):
            link = h2.find('a', href=True)
            if link and len(h2.text.strip()) > 10:
                get_news.append((h2.text.strip(), link['href']))

        return get_news

if __name__ == '__main__':
    for item in news('https://arstechnica.com/ai/'):
        print(item)
