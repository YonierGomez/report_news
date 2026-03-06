import requests
from bs4 import BeautifulSoup


def news(URL):
    """Obtiene noticias de Hacker News."""
    r = requests.get(URL, timeout=15)

    if r.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
        get_news = []
        for item in soup.find_all('tr', class_='athing', limit=10):
            title_span = item.find('span', class_='titleline')
            if title_span:
                link = title_span.find('a', href=True)
                if link and link.text.strip():
                    url = link['href']
                    if url.startswith('item?'):
                        url = 'https://news.ycombinator.com/' + url
                    get_news.append((link.text.strip(), url))
        return get_news
    return []


if __name__ == '__main__':
    for item in news('https://news.ycombinator.com/'):
        print(item)
