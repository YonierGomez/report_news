import requests
from bs4 import BeautifulSoup


# def news():
def news(URL):
    """Funcion para obtener noticias de Apple Esfera"""
    r = requests.get(URL)

    get_news = []
    if r.ok:
        r_content = r.text
        leer = r.text
    # with open("/home/neytor/web-scraper/project/news/distro.html", "rb") as leeme:
        # leer = leeme.read()
        soup = BeautifulSoup(leer, 'html.parser')
        title = soup.find('table', {'class': 'Logo'})

        
        for r_title in title.find_all('td', {'class', 'NewsHeadline'}, limit=30):
            get_news.append( f"* {r_title.text}")

        return get_news
    else:
        print(leer)
        print(r.text)

if __name__ == '__main__':
    print('='*130)
    print('Distros Linux - Principales noticias Sr Yonier')
    print('='*130)
    # print(news(), '\n')
    # news('https://distrowatch.com/')
    for new in news('https://distrowatch.com/'):
        print(new, '\n')
        print('='*130)