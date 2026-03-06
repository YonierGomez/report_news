import requests
from bs4 import BeautifulSoup


def news(URL):
    """Obtiene noticias de The Verge."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    }
    r = requests.get(URL, headers=headers, timeout=15)

    if r.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
        get_news = []
        seen = set()

        # Buscar h2 con links
        for h2 in soup.find_all('h2', limit=20):
            link = h2.find('a', href=True)
            if link and len(h2.text.strip()) > 10:
                url = link['href']
                if not url.startswith('http'):
                    url = 'https://www.theverge.com' + url
                if url not in seen:
                    seen.add(url)
                    get_news.append((h2.text.strip(), url))

        # Buscar links a artículos con año en la URL
        if len(get_news) < 5:
            for a in soup.find_all('a', href=True):
                href = a.get('href', '')
                if '/202' in href and len(a.text.strip()) > 20:
                    url = href if href.startswith('http') else 'https://www.theverge.com' + href
                    if url not in seen:
                        seen.add(url)
                        get_news.append((a.text.strip(), url))

        return get_news[:10]
    return []


if __name__ == '__main__':
    for item in news('https://www.theverge.com/tech'):
        print(item)
