import requests
from bs4 import BeautifulSoup


def news(URL):
    """Funcion para obtener noticias de DistroWatch"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    r = requests.get(URL, headers=headers)

    if r.ok:
        soup = BeautifulSoup(r.text, 'html.parser')

        get_news = []
        for headline in soup.find_all('td', class_='NewsHeadline', limit=10):
            title = headline.get_text(strip=True)
            link = headline.find('a', href=True)
            if link:
                href = link['href']
                if not href.startswith('http'):
                    href = 'https://distrowatch.com/' + href
                get_news.append((title, href))

        return get_news

if __name__ == '__main__':
    print('='*130)
    print('DistroWatch - Principales noticias Sr Yonier')
    print('='*130)
    for new in news('https://distrowatch.com/'):
        print(new, '\n')
        print('='*130)
