import requests
from bs4 import BeautifulSoup


def news(URL):
    """Funcion para obtener noticias de Xataka"""
    r = requests.get(URL)

    if r.ok:
        r_content = r.text
        leer = r.text
        
        soup = BeautifulSoup(leer, 'html.parser')
        title = soup.find('div', {'class': 'content-container'})

        get_news = []
        for r_title in title.find_all('article', class_='recent-abstract abstract-article', limit=10):
            get_news.append(f'* {r_title.h2.text}: {r_title.a["href"]}')

        return get_news

if __name__ == '__main__':
    print('='*130)
    print('Xataka - Principales noticias Sr Yonier')
    print('='*130)
    for new in news('https://www.xataka.com/'):
        print(new, '\n')
        print('='*130)
    
