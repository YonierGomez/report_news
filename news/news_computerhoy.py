import requests
from bs4 import BeautifulSoup


def news(URL):
    """Funcion para obtener noticias de Computer hoy"""
    r = requests.get(URL)

    if r.ok:
        r_content = r.text
        leer = r.text
        
        soup = BeautifulSoup(leer, 'html.parser')

        get_news = []
        for r_title in soup.find_all(class_='teaser_teaser__gSQCt', limit=10):
            get_news.append(f'* {r_title.h3.text}: {r_title.a["href"]}')

        return get_news

if __name__ == '__main__':
    print('='*130)
    print('Computer hoy - Principales noticias Sr Yonier')
    print('='*130)
    for new in news('https://computerhoy.20minutos.es/'):
        print(new, '\n')
        print('='*130)
