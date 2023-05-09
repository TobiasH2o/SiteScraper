import subprocess

print("Importing required modules")
try:
    import requests
except ImportError:
    print("Error importing requests module. Confirm downloading requests module.")
    input("Confirm?")
    subprocess.call(["pip", "install", "requests"])
    import requests
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error importing BeautifulSoup module. Confirm downloading BeautifulSoup Module.")
    input("Confirm?")
    subprocess.call(["pip", "install", "bs4"])
    from bs4 import BeautifulSoup

import os
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


def loading_sprite(frame_id, percent_bar):
    length = 50

    image1 = "      ~ ~ ~ ###    "
    image2 = "┍━━━━┑       ╭┅╮   "
    image3 = "│ ╭╮ └─┰─┰─┰─┘ ╞╕  "
    image4 = "│ ╰╯   ┇ ┇ ┇   ╞╛  "
    image5 = "└⍽⍽⍽⍽⍽┄┄┄┄┄⍽┄┄⍽╯   "
    image6 = " 0↻0↻0     0↻↻0    "

    completed_number = int((length + len(image1)) * percent_bar / 100)
    to_do_number = int(length + len(image1)) - completed_number
    edge_up = "╭" + "╥" * completed_number + "─" * to_do_number + "╮"
    edge_centre = "╞" + "╩" * completed_number + "═" * to_do_number + "╡"
    edge_down = "└" + "─" * int(length + len(image1)) + "┘"
    print(edge_up)
    print(edge_centre)
    left_length = frame_id % length
    right_length = length - left_length

    padding = "│" + " " * left_length
    padding2 = " " * right_length + "│"

    print(padding + image1 + padding2 + "\n" \
          + padding + image2 + padding2 + "\n" \
          + padding + image3 + padding2 + "\n" \
          + padding + image4 + padding2 + "\n" \
          + padding + image5 + padding2 + "\n" \
          + padding + image6 + padding2)

    print(edge_down)


def update_dictionary(url, dictionary):
    # Get the HTML of the website.
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

    # Find the text of the website.
    text = soup.get_text()
    text = str.lower(text)

    if not any(item.find(" ") != -1 for item in dictionary.keys()):
        text = text.split()

    for phrase in dictionary.keys():
        count = text.count(phrase)
        dictionary[phrase] += count

    return dictionary


if __name__ == '__main__':
    os.system('cls')
    partial = False
    # Get the URL from the user.
    url = input('Enter the URL of the site to crawl: ')
    url = url.replace("\\", "/")
    phrases = []
    while True:
        os.system('cls')
        if any(item.find(" ") != -1 for item in phrases):
            partial = True

        if partial:
            print("    ----    Partial matching enabled    ----    ")

        print(f"Searching {url}")
        print("Search phrases:")
        for x in range(len(phrases)):
            print(f"{x}> {phrases[x]}")
        print("To remove a phrase, add the phrase a second time")
        print("To allow partial matches add a multi-word search phrase")
        print("To confirm enter nothing")
        opt = input("> ")
        if opt == "":
            break
        if opt in phrases:
            phrases.remove(str.lower(opt))

        else:
            phrases.append(str.lower(opt))
    os.system('cls')
    # Get all the pages in the site.
    pages = get_all_pages(url)

    page_count = 1
    # Keep checking each subdirectory until it is complete.
    while page_count < len(pages):
        # Get the next page.
        page = pages[page_count]
        # Get all the links on the page.
        links = get_all_pages(page)

        new_links = [x for x in links if x not in pages]

        # Add the links to the list of pages.
        pages.extend(new_links)

        print("\033[%d;%dH" % (0, 0))
        print(f"Indexing\nPage {page_count} of {len(pages)} - ({round(100 * page_count / len(pages), 4)}%)")
        loading_sprite(page_count, 100 * page_count / len(pages))
        page_count += 1

    page_count = 0

    phrase_dictionary = dict.fromkeys(phrases)
    for key in phrase_dictionary.keys():
        phrase_dictionary[key] = 0

    while page_count <= len(pages):
        print("\033[%d;%dH" % (0, 0))
        print(f"Scanning\nPage {page_count} of {len(pages)} - ({round(100 * page_count / len(pages), 6)}% )"
              f"                                                              ")
        loading_sprite(page_count, 100 * page_count / len(pages))
        if page_count != len(pages):
            phrase_dictionary = update_dictionary(pages[page_count], phrase_dictionary)
        for key in phrase_dictionary.keys():
            print(f"{key}: {phrase_dictionary[key]}")
        page_count += 1
    print("Complete")
    print("SAFETY LINE. IF YOU SEE ME THEN SOMETHING HAS GONE WRONG. DONT WORRY THOUGH I AM SURE IT IS OKAY")
