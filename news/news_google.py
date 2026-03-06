import requests
from bs4 import BeautifulSoup
from googlenewsdecoder import new_decoderv1


def _decode_url(google_url):
    """Decodifica una URL de Google News a la URL real del artículo."""
    try:
        result = new_decoderv1(google_url, interval=1)
        if result.get('status'):
            return result['decoded_url']
    except Exception:
        pass
    return google_url


def news(URL, DOMAIN):
    """Obtiene noticias de Google News con títulos limpios y URLs reales."""
    r = requests.get(URL)
    if not r.ok:
        return []

    soup = BeautifulSoup(r.text, 'html.parser')
    get_news = []

    for a in soup.find_all('a', class_='gPFEn', limit=10):
        title = a.text.strip()
        href = a.get('href', '')

        # Construir URL completa de Google News
        if href.startswith('./'):
            full_url = DOMAIN + href[2:]
        else:
            full_url = DOMAIN + href

        # Decodificar a URL real del artículo
        real_url = _decode_url(full_url)
        get_news.append((title, real_url))

    return get_news


if __name__ == '__main__':
    print('=' * 130)
    print('Google News - Principales noticias')
    print('=' * 130)

    results = news(
        'https://news.google.com/topics/CAAqLQgKIidDQkFTRndvSkwyMHZNR1ptZHpWbUVnWmxjeTAwTVRrYUFrTlBLQUFQAQ?hl=es-419&gl=CO&ceid=CO%3Aes-419',
        'https://news.google.com/'
    )
    for title, url in results:
        print(f'{title}\n{url}\n')
        print('=' * 130)
