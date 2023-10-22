import requests
from bs4 import BeautifulSoup

def news(URL):
    """Funcion para obtener noticias de Distrowatch"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    r = requests.get(URL, headers=headers)

    get_news = []
    if r.ok:
        r_content = r.text
        leer = r.text
        
        soup = BeautifulSoup(leer, 'html.parser')
        for title in soup.find_all('td', class_='NewsHeadline'):
            link = title.find('a', href=True)
            if link is not None:
                get_news.append(f'*{title.text.strip()}: {URL + link["href"]}')
        
    else:
        print('No fue posible hacer la solicitud', r.text)
        
    return get_news

if __name__ == '__main__':
    print('='*130)
    print('Distrowatch - Principales noticias Sr Yonier')
    print('='*130)
    
    # news('https://distrowatch.com/')
    
    for new in news('https://distrowatch.com/'):
        print(new, '\n')
        print('='*130)
