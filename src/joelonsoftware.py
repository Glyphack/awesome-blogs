import json
import re

import requests
from bs4 import BeautifulSoup

archive_url = "https://www.joelonsoftware.com/archives/"
response = requests.get(archive_url)
soup = BeautifulSoup(response.text, "html.parser")

archive_links = [
    link["href"]
    for link in soup.find_all("a", href=True)
    if re.search(r"https://www\.joelonsoftware\.com/\d{4}/\d{2}/", link["href"])
]

articles_data = []

for index, link in enumerate(archive_links, start=1):
    print(f"Processing archive {index}/{len(archive_links)}: {link}")
    archive_response = requests.get(link)
    archive_soup = BeautifulSoup(archive_response.text, "html.parser")
    articles = archive_soup.find_all("h1", class_="entry-title")
    for article in articles:
        article_link = article.find("a", href=True)
        if article_link:
            article_url = article_link["href"]
            date_match = re.search(r"/(\d{4}/\d{2}/\d{2})/", article_url)
            date = date_match.group(1) if date_match else "Unknown"
            articles_data.append(
                {"title": article_link.text.strip(), "link": article_url, "date": date}
            )

print("Saving articles to JSON file...")
with open("articles.json", "w") as json_file:
    json.dump(articles_data, json_file, indent=4)
print("Done.")
