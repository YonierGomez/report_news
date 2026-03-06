import requests
from bs4 import BeautifulSoup


def news(URL):
    """Obtiene noticias de TechCrunch."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    }
    r = requests.get(URL, headers=headers, timeout=15)

    if r.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
        get_news = []
        for h in soup.find_all(['h2', 'h3'], limit=20):
            link = h.find('a', href=True)
            if link and len(h.text.strip()) > 10:
                get_news.append((h.text.strip(), link['href']))
        return get_news[:10]
    return []


if __name__ == '__main__':
    for item in news('https://techcrunch.com/'):
        print(item)
