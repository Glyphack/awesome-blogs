import datetime

import requests
from bs4 import BeautifulSoup

from save import save


def extract_blog_posts(year):
    url = f"https://commandcenter.blogspot.com/{year}/"
    response = requests.get(url)
    if response.status_code == 404:
        return []
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    posts = []
    for ul in soup.find_all("ul", class_="posts"):
        for li in ul.find_all("li"):
            link = li.find("a", href=True)
            if link:
                post_url = link["href"]
                title = link.text.strip()
                posts.append({"url": post_url, "title": title})
    return posts


def fetch():
    current_year = datetime.datetime.now().year
    years = list(range(2004, current_year + 1))
    posts = []
    for year in years:
        print(f"Processing year: {year}")
        posts.extend(extract_blog_posts(year))
    save("robpike", posts)


if __name__ == "__main__":
    fetch()
