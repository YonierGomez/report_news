import requests
from bs4 import BeautifulSoup


def news(URL):
    """Obtiene noticias de Krebs on Security."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    }
    r = requests.get(URL, headers=headers, timeout=15)

    if r.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
        get_news = []
        for article in soup.find_all('article', limit=10):
            h2 = article.find('h2')
            if h2:
                link = h2.find('a', href=True)
                if link:
                    get_news.append((link.text.strip(), link['href']))
        return get_news
    return []


if __name__ == '__main__':
    for item in news('https://krebsonsecurity.com/'):
        print(item)
