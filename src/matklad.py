from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from save import save


def fetch():
    url = "https://matklad.github.io/"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    posts = []
    for link in soup.select(".post-list a"):
        post_url = urljoin(url, link["href"])
        title = link.text.strip()
        date_element = link.find_previous("time")
        date = date_element["datetime"] if date_element else None
        posts.append({"url": post_url, "title": title, "date": date})

    save("matklad", posts)


if __name__ == "__main__":
    fetch()
