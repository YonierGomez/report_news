import requests
from bs4 import BeautifulSoup

def news(URL):
    """Funcion para obtener noticias de muy linux"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    r = requests.get(URL, headers=headers)

    get_news = []
    if r.ok:
        r_content = r.text
        leer = r.text
        
        soup = BeautifulSoup(leer, 'html.parser')
        title = soup.find('div', class_='zoxrel zox100')
        
        for r_title in title.find_all('div', class_='zox-art-title', limit=10):
            get_news.append(f'*{r_title.a.h2.text}: {r_title.a["href"]}')
        
    else:
        print('No fue posible hacer la solicitud', r.text)
        
    return get_news

if __name__ == '__main__':
    print('='*130)
    print('Muy Linux - Principales noticias Sr Yonier')
    print('='*130)
    for new in news('https://www.muylinux.com/'):
        print(new, '\n')
        print('='*130)
