import requests
from bs4 import BeautifulSoup


# En news_fayer.py
def news(URL, DOMAIN):
    """Funcion para obtener noticias de Fayer Wayer News"""
    r = requests.get(URL)

    if r.ok:
        r_content = r.text
        leer = r.text

        soup = BeautifulSoup(leer, 'html.parser')

        title = soup.find('div', {'class': 'container layout-section'})

        get_news = []
        for r_title in title.find_all('div', class_='list-item'):
            # Formatea y agrega cada noticia a la lista de get_news
            get_news.append(f"* {r_title.h2.text}: {DOMAIN + r_title.a['href']}")

    return get_news  # Devuelve la lista de get_news

if __name__ == '__main__':
    print('='*130)
    print('Fayer Wayer - Principales noticias Sr Yonier')
    print('='*130)
    for new in news('https://www.fayerwayer.com/internet/', 'https://www.fayerwayer.com'):
        print(new, '\n')
        print('='*130)
