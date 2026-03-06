import requests
from bs4 import BeautifulSoup


def news(URL):
    """Obtiene noticias de The Hacker News (seguridad informática)."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    }
    r = requests.get(URL, headers=headers, timeout=15)

    if r.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
        get_news = []
        for story in soup.find_all('div', class_='body-post', limit=10):
            title_tag = story.find('h2', class_='home-title')
            link_tag = story.find('a', class_='story-link', href=True)
            if title_tag and link_tag:
                get_news.append((title_tag.text.strip(), link_tag['href']))
        return get_news
    return []


if __name__ == '__main__':
    for item in news('https://thehackernews.com/'):
        print(item)
