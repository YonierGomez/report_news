import requests
from bs4 import BeautifulSoup


def news(URL, DOMAIN):
    """Funcion para obtener noticias de Google News"""
    r = requests.get(URL)

    if r.ok:
        r_content = r.text
        leer = r.text
        
        soup = BeautifulSoup(leer, 'html.parser')

        title = soup.find('div', {'class': 'c4Stqc'})

        get_news = []
        for r_title in title.find_all('article', class_='IFHyqb DeXSAc'):

            get_news.append(f'*{r_title.div.h4.text}: { DOMAIN + r_title.div.a["href"]}')

        return get_news
        
if __name__ == '__main__':
    print('='*130)
    print('Google News - Principales noticias Sr Yonier')
    print('='*130)
    
    for new in news('https://news.google.com/topics/CAAqLQgKIidDQkFTRndvSkwyMHZNR1ptZHpWbUVnWmxjeTAwTVRrYUFrTlBLQUFQAQ?hl=es-419&gl=CO&ceid=CO%3Aes-419', 'https://news.google.com/topics'):
        print(new, '\n')
        print('='*130)
