import os
from apify_client import ApifyClient

client = ApifyClient(os.getenv("APIFY_TOKEN"))

run_input = {
    "keywords": "java developer tx gc",
    "maximumPosts": 5
}

run = client.actor("benjarapi/linkedin-post-search").call(
    run_input=run_input
)

print("Run ID:", run.id)
print("Dataset ID:", run.default_dataset_id)
