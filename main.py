import os
import time
from apify_client import ApifyClient
from sheets import add_row
from discord_sender import send_message

# ---------------------------
# APIFY CLIENT
# ---------------------------
client = ApifyClient(os.getenv("APIFY_TOKEN"))

# ---------------------------
# LOAD SEEN POSTS
# ---------------------------
seen = set()

if os.path.exists("seen_posts.txt"):
    with open("seen_posts.txt", "r", encoding="utf-8") as f:
        seen = set(line.strip() for line in f)

# ---------------------------
# READ KEYWORDS
# ---------------------------
with open("keywords.txt", "r", encoding="utf-8") as f:
    keywords = [line.strip() for line in f if line.strip()]

# ---------------------------
# LOOP THROUGH KEYWORDS
# ---------------------------
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

    posts_processed = 0

    for post in dataset.iterate_items():

        # ---------------------------
        # GET FIELDS
        # ---------------------------
        post_url = post.get("post_url", "")
        text = post.get("text", "")
        search_input = post.get("search_input", keyword)

        author = "Unknown"
        if post.get("author"):
            author = post["author"].get("name", "Unknown")

        posted = post.get("posted_at", {})
        date_str = str(posted.get("date", "")).lower()

        # ---------------------------
        # SKIP IF NO URL
        # ---------------------------
        if not post_url:
            continue

        # ---------------------------
        # SKIP DUPLICATES
        # ---------------------------
        if post_url in seen:
            continue

        # ---------------------------
        # KEEP ONLY 0–3 HOUR POSTS
        # ---------------------------

        if not date_str:
            continue

        # Skip days, weeks, months, years
        if (
            "d" in date_str
            or "w" in date_str
            or "mo" in date_str
            or "y" in date_str
        ):
            continue

        # Allow minutes
        if "m" in date_str:
            pass

        # Allow only <=3 hours
        elif "h" in date_str:
            digits = ''.join(filter(str.isdigit, date_str))

            if digits:
                hours = int(digits)

                if hours > 3:
                    continue
        else:
            continue

        # ---------------------------
        # LIMIT POSTS PER KEYWORD
        # ---------------------------
        if posts_processed >= 5:
            break

        # ---------------------------
        # SAVE TO GOOGLE SHEETS
        # ---------------------------
        add_row([
            date_str,
            author,
            search_input,
            text[:500],
            post_url
        ])

        # Avoid Google rate limit
        time.sleep(1)

        # ---------------------------
        # SEND TO DISCORD
        # ---------------------------
        message = f"""
🚨 New LinkedIn Post

Keyword: {search_input}
Author: {author}
Posted: {date_str}

{text[:700]}

{post_url}
"""

        send_message(message)

        # Avoid Discord rate limit
        time.sleep(2)

        # ---------------------------
        # SAVE TO seen_posts.txt
        # ---------------------------
        with open(
            "seen_posts.txt",
            "a",
            encoding="utf-8"
        ) as sf:
            sf.write(post_url + "\n")

        seen.add(post_url)
        posts_processed += 1

print("Automation Completed Successfully")
