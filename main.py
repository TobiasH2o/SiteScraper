import os

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_all_pages(url):
    """Returns a list of all pages in the given site.

  Args:
    url: The URL of the site to crawl.

  Returns:
    A list of all pages in the site.
  """
    parent = urlparse(url)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/99.0.4844.84 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip,deflate,br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
    }

    # Get the HTML of the homepage.
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    while url[-1] == "/":
        url = url[:-1]

    # Find all the links on the homepage.
    links = soup.find_all('a')

    # Create a list to store the pages.
    pages = []
    # Iterate over the links and add them to the list of pages.
    for link in links:
        try:
            href = link['href']
        except KeyError:
            continue
        if href.startswith('/'):
            href = parent.scheme + "://" + parent.netloc + href
            if href not in pages:
                pages.append(href)
        else:
            if urlparse(href).netloc == parent.netloc and href not in pages:
                pages.append(href)

    # Return the list of pages.
    return pages

def print_spirte(id):


if __name__ == '__main__':
    # Get the URL from the user.
    url = input('Enter the URL of the site to crawl: ')

    os.system('cls')

    # Get all of the pages in the site.
    pages = get_all_pages(url)

    page_count = 1
    # Keep checking each subdirectory until it is complete.
    while page_count < len(pages):
        # Get the next page.
        page = pages[page_count]
        page_count += 1
        # Get all of the links on the page.
        links = get_all_pages(page)

        new_links = [x for x in links if x not in pages]

        # Add the links to the list of pages.
        pages.extend(new_links)

        print("\033[%d;%dH" % (0, 0))
        print(f"Scanning\nPage {page_count} of {len(pages)}")
        print_spirte(page_count)

    # Print the list of pages.
    for page in pages:
        print(page)
