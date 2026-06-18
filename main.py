import os
from apify_client import ApifyClient

token = os.getenv("APIFY_TOKEN")

client = ApifyClient(token)

print("Apify Connected Successfully")
