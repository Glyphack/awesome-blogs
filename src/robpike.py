import datetime
import json

import requests
from bs4 import BeautifulSoup


def extract_blog_posts(year, output_file):
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


if __name__ == "__main__":
    current_year = datetime.datetime.now().year
    years = list(range(2004, current_year + 1))
    blog_url = "https://commandcenter.blogspot.com/"
    output_file = "commandcenter_posts.json"
    posts = []
    for year in years:
        print(f"Processing year: {year}")
        posts.extend(extract_blog_posts(year, output_file))
    with open(output_file, "w") as json_file:
        json.dump(posts, json_file, indent=4)
    print(f"Sved {len(posts)} posts to {output_file}")
