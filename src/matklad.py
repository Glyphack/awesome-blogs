import json
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def extract_blog_posts(url, output_file):
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

    with open(output_file, "w") as json_file:
        json.dump(posts, json_file, indent=4)
    print(f"Saved {len(posts)} posts to {output_file}")


if __name__ == "__main__":
    blog_url = "https://matklad.github.io/"
    output_file = "blog_posts.json"
    extract_blog_posts(blog_url, output_file)
