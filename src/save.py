import json


def deduplicate_posts(posts):
    unique_links = set()
    deduplicated_posts = []
    for post in posts:
        link = post.get("url")
        if link is None:
            raise ValueError("Post is missing a url")
        if link not in unique_links:
            unique_links.add(link)
            deduplicated_posts.append(post)
    return deduplicated_posts


def save(name, posts):
    posts = deduplicate_posts(posts)
    print(f"Saving {name} articles to JSON...")
    with open(f"{name}.json", "w") as json_file:
        json.dump(posts, json_file, indent=4)
    print("Done.")
