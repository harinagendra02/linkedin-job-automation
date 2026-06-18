import os
from apify_client import ApifyClient
from sheets import add_row
from discord_sender import send_message

client = ApifyClient(os.getenv("APIFY_TOKEN"))

# Load seen posts
seen = set()
if os.path.exists("seen_posts.txt"):
    with open("seen_posts.txt", "r", encoding="utf-8") as f:
        seen = set(line.strip() for line in f)

# Read keywords
with open("keywords.txt", "r", encoding="utf-8") as f:
    keywords = [line.strip() for line in f if line.strip()]

for keyword in keywords:
    print(f"Searching: {keyword}")

    run_input = {
        "keywords": keyword,
        "maximumPosts": 5
    }

    run = client.actor(
        "benjarapi/linkedin-post-search"
    ).call(run_input=run_input)

    dataset = client.dataset(run.default_dataset_id)

    for post in dataset.iterate_items():

        post_url = post.get("post_url", "")
        text = post.get("text", "")
        search_input = post.get("search_input", keyword)

        author = "Unknown"
        if post.get("author"):
            author = post["author"].get("name", "Unknown")

        date = ""
        if post.get("posted_at"):
            date = post["posted_at"].get("date", "")

        if not post_url:
            continue

        if post_url in seen:
            continue

        # Google Sheets
        add_row([
            date,
            author,
            search_input,
            text[:500],
            post_url
        ])

        # Discord
        msg = f"""
🚨 New LinkedIn Post

Keyword: {search_input}
Author: {author}

{text[:800]}

{post_url}
"""

        send_message(msg)

        # Save duplicate
        with open(
            "seen_posts.txt",
            "a",
            encoding="utf-8"
        ) as sf:
            sf.write(post_url + "\n")

        seen.add(post_url)

print("Automation Completed")
