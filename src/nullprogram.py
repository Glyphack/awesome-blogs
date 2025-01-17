from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from save import save


def fetch():
    url = "https://nullprogram.com"
    response = requests.get(url + "/index/")
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    posts = []
    post_list = soup.find("ul", class_="post-list")

    if not post_list:
        raise ValueError("No post list found")

    for link in post_list.find_all("a"):
        post_url = urljoin(url, link["href"])
        title = link.text.strip()
        # The date is part of the URL in the format /blog/YYYY/MM/DD/
        # We can extract it from the href
        href = link["href"]
        date = None
        if "/blog/" in href:
            parts = href.split("/")
            if len(parts) >= 5:  # Ensure we have enough parts
                date = f"{parts[2]}-{parts[3]}-{parts[4]}"

        posts.append({"url": post_url, "title": title, "date": date})

    save("nullprogram", posts)


if __name__ == "__main__":
    fetch()
