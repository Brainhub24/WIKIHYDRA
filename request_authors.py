import requests

def get_all_authors(page_title, lang='en'):
    url = f'https://{lang}.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'revisions',
        'titles': page_title,
        'rvprop': 'user|timestamp',
        'rvlimit': 'max'  # Retrieve all revisions
    }
    authors = []
    continue_flag = True

    while continue_flag:
        response = requests.get(url, params=params)
        data = response.json()
        pages = data['query']['pages']
        page_id = list(pages.keys())[0]
        revisions = pages[page_id]['revisions']
        
        for rev in revisions:
            # Append author and timestamp as a tuple
            authors.append((rev['user'], rev['timestamp']))

        if 'continue' in data:
            params['rvcontinue'] = data['continue']['rvcontinue']
        else:
            continue_flag = False

    return authors

if __name__ == "__main__":
    page_title = 'Siegfried_Gebser'
    # My beloved grandfather / my hero, I miss you...
    # He was the living Wikipedia in his lifetime. 
    authors = get_all_authors(page_title, lang='de')
    print("Authors of the Wikipedia page:")
    for author, timestamp in authors:
        print(f"{author} - {timestamp}")
