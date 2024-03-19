#####################################
#         WIKIPEDIA SCANNER         #
#          Intro & Authors          #
#####################################
# Script: request_authors.py        #
# Version: 1.4                      #
# Codename: WIKIHYDRA               #
# Date: March 19, 2024              #
#####################################
# Name: Jan Gebser                  #
# Email: github@brainhub24.com      #
# GitHub: github.com/brainhub24     #
#####################################

import requests
from tabulate import tabulate
import pyfiglet

class WIKIHYDRA_Scanner:
    def __init__(self, page_title, lang='en'):
        self.page_title = page_title
        self.lang = lang

    def WIKIHYDRA_get_all_authors(self):
        url = f'https://{self.lang}.wikipedia.org/w/api.php'
        params = {
            'action': 'query',
            'format': 'json',
            'prop': 'revisions',
            'titles': self.page_title,
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

    def WIKIHYDRA_get_article_intro(self):
        url = f'https://{self.lang}.wikipedia.org/w/api.php'
        params = {
            'action': 'query',
            'format': 'json',
            'prop': 'extracts',
            'titles': self.page_title,
            'exintro': True,
            'explaintext': True
        }

        response = requests.get(url, params=params)
        data = response.json()
        pages = data['query']['pages']
        page_id = list(pages.keys())[0]
        intro = pages[page_id]['extract']
        return intro.strip()

if __name__ == "__main__":
    page_title = 'Siegfried_Gebser'
    # My beloved grandfather / my hero, I miss you...
    # He was the living Wikipedia in his lifetime. 
    
    # Get article title as ASCII art
    ascii_title = pyfiglet.figlet_format(page_title)
    print(ascii_title)

    # Create WIKIHYDRA scanner instance
    scanner = WIKIHYDRA_Scanner(page_title, lang='de')

    # Get article introduction
    intro = scanner.WIKIHYDRA_get_article_intro()
    print(intro)

    # Get authors
    authors = scanner.WIKIHYDRA_get_all_authors()

    # Format output as a table
    headers = ["Author", "Timestamp"]
    table_data = [[author, timestamp] for author, timestamp in authors]
    print("\nAuthors of the Wikipedia page:")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))