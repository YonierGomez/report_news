import requests
from bs4 import BeautifulSoup


def news(URL):
    """Funcion para obtener noticias de muy linux"""
    r = requests.get(URL)

    if r.ok:
        r_content = r.text
        leer = r.text
        
        soup = BeautifulSoup(leer, 'html.parser')
        title = soup.find('div', class_='zoxrel zox100')
        

        get_news = []
            
        for r_title in title.find_all('div', class_='zox-art-title'):
            get_news.append(f'*{r_title.a.h2.text}: {r_title.a["href"]}')
        
        # print(get_news)
        # return get_news

if __name__ == '__main__':
    print('='*130)
    print('Muy Linux - Principales noticias Sr Yonier')
    print('='*130)
    news('https://www.muylinux.com/')
    # for new in news('https://www.muylinux.com/'):
    #     print(new, '\n')
    #     print('='*130)
