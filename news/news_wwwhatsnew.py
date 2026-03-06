import requests
from bs4 import BeautifulSoup


def news(URL):
    """Funcion para obtener noticias de Wwwhat's new"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    }
    r = requests.get(URL, headers=headers)

    if r.ok:
        soup = BeautifulSoup(r.text, 'html.parser')

        get_news = []
        for article in soup.find_all('article', limit=10):
            h = article.find(['h2', 'h3'])
            link = article.find('a', href=True)
            if h and link:
                get_news.append((h.text.strip(), link['href']))

        return get_news

if __name__ == '__main__':
    for item in news('https://wwwhatsnew.com/'):
        print(item)
