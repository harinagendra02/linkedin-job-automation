Read keywords.txt
       ↓
For each keyword:
       ↓
Run Apify Actor
       ↓
Get JSON results
       ↓
For each post:
       ↓
post_url already seen?
      / \
    Yes  No
     |     |
 Ignore   Save to Sheet
           Send to Discord
           Add URL to seen_posts.txt
