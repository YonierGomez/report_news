import requests
from bs4 import BeautifulSoup


def news(URL):
    """Funcion para obtener noticias de Computer hoy"""
    r = requests.get(URL)

    if r.ok:
        soup = BeautifulSoup(r.text, 'html.parser')

        get_news = []
        for article in soup.find_all('article', class_='c-article', limit=10):
            heading = article.find(['h2', 'h3'])
            link = article.find('a', href=True)
            if heading and link:
                href = link['href']
                if not href.startswith('http'):
                    href = 'https://computerhoy.20minutos.es' + href
                get_news.append((heading.text.strip(), href))

        return get_news

if __name__ == '__main__':
    print('='*130)
    print('Computer hoy - Principales noticias Sr Yonier')
    print('='*130)
    for new in news('https://computerhoy.20minutos.es/'):
        print(new, '\n')
        print('='*130)
