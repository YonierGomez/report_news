import requests
from bs4 import BeautifulSoup


# def news():
def news(URL):
    """Funcion para obtener noticias de Apple Esfera"""
    # r = requests.get(URL)

    get_news = []
    # if r.ok:
    #     r_content = r.text
    #     leer = r.text
    with open("/home/neytor/web-scraper/project/news/distro.html", "rb") as leeme:
        leer = leeme.read()
        soup = BeautifulSoup(leer, 'html.parser')
        # title = soup.find('table', {'style': 'width: 60%; vertical-align: top; border: none'})
        title = soup.find('td', {'style': 'width: 60%; vertical-align: top; border: none'})
        # title = soup.find('tr')
        # title = soup.find('table', class_='Logo')
        # title = soup.find('table', {'class': 'News'})
        # title = title.find

        # print(title.prettify())
        # print(title.prettify())
        for r_title in title.find_all('td', {'class', 'NewsHeadline'}, limit=10):
        # for r_title in title.find_all('td', class_='NewsHeadline', limit=10):
        # for r_title in title.find_all('table', class_='News', limit=10):
            # print(r_title)
        # for r_title in title.find_all('td', class_='NewsHeadline', limit=10):
            # get_news.append( f'* {r_title.tbody}:')
            a_tag = soup.find('td', class_='NewsHeadline').find('a')
            ver = a_tag.get('href')
            get_news.append( f"*{ver}")
            # get_news.append( f"* {r_title.text}: {ver}")
            # get_news.append( f'* {r_title.text}: {r_title["href"]}')
            # get_news.append( f'* {r_title.td.td.a.text}: {r_title["href"]}')

        return get_news
    # else:
        # print(leer)
        # print(r.text)

if __name__ == '__main__':
    print('='*130)
    print('Distros Linux - Principales noticias Sr Yonier')
    print('='*130)
    # print(news(), '\n')
    # news('https://distrowatch.com/')
    for new in news('https://distrowatch.com/'):
        print(new, '\n')
        print('='*130)
