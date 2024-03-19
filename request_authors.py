import requests

def get_authors(page_title, lang='en'):
    url = f'https://{lang}.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'revisions',
        'titles': page_title,
        'rvprop': 'user'
    }
    response = requests.get(url, params=params)
    data = response.json()
    pages = data['query']['pages']
    page_id = list(pages.keys())[0]
    revisions = pages[page_id]['revisions']
    authors = [rev['user'] for rev in revisions]
    return authors

if __name__ == "__main__":
    page_title = 'Siegfried_Gebser'
    authors = get_authors(page_title, lang='de')
    print("Authors of the Wikipedia page:")
    for author in authors:
        print(author)
