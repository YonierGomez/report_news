import requests
from bs4 import BeautifulSoup


def news(URL):
    """Funcion para obtener noticias de Hipertextual"""
    r = requests.get(URL)

    if r.ok:
        r_content = r.text
        leer = r.text
        
        soup = BeautifulSoup(leer, 'html.parser')

        get_news = []
        for r_title in soup.find_all(class_='hentry', limit=10):
            get_news.append((r_title.h2.text.strip(), r_title.a["href"]))

        return get_news

if __name__ == '__main__':
    print('='*130)
    print('Hipertextual - Principales noticias Sr Yonier')
    print('='*130)
    for new in news('https://hipertextual.com/tecnologia'):
        print(new, '\n')
        print('='*130)
