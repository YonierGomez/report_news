import requests
from bs4 import BeautifulSoup


def news(URL, DOMAIN):
    """Funcion para obtener noticias de Google News"""
    r = requests.get(URL)

    if r.ok:
        r_content = r.text
        leer = r.text
        
        soup = BeautifulSoup(leer, 'html.parser')

        get_news = []
        for r_title in soup.find_all('article', {'jsmodel': 'hT8rr'}, limit=15):
            url = DOMAIN + r_title.a["href"]
            url = url.replace("./articles/", "")
            get_news.append(f'*{r_title.text}: {url}')
            # get_news.append(f'*{r_title.h4.text}: {url}')
        
        return get_news
        
if __name__ == '__main__':
    print('='*130)
    print('Google News - Principales noticias Sr Yonier')
    print('='*130)
    
    # news('https://news.google.com/topics/CAAqLQgKIidDQkFTRndvSkwyMHZNR1ptZHpWbUVnWmxjeTAwTVRrYUFrTlBLQUFQAQ?hl=es-419&gl=CO&ceid=CO%3Aes-419', 'https://news.google.com/')
    for new in news('https://news.google.com/topics/CAAqLQgKIidDQkFTRndvSkwyMHZNR1ptZHpWbUVnWmxjeTAwTVRrYUFrTlBLQUFQAQ?hl=es-419&gl=CO&ceid=CO%3Aes-419', 'https://news.google.com/articles/'):
        print(new, '\n')
        print('='*130)