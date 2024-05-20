import requests
from bs4 import  BeautifulSoup

def news(URL):
    """Funcion para obtener noticias de Xataka"""
    r = requests.get(URL)

    if r.ok:
        leer = r.text
        
        soup = BeautifulSoup(leer, 'html.parser')
            
        get_news = []
        for r_title in soup.find_all('h2', class_='abstract-title'):
            get_news.append(f'* {r_title.a.text}: {r_title.a["href"]}')

        return get_news
        

if __name__ == '__main__':
    print('='*130)
    print('Genbeta actualidad - Principales noticias Sr Yonier')
    print('='*130)
    for new in news('https://www.genbeta.com/categoria/actualidad'):
        print(new, '\n')
        print('='*130)
    
