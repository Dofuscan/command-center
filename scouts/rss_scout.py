# scouts/rss_scout.py

import feedparser
import requests
import time
import os
import json
import hashlib
from datetime import datetime

# --- CONFIGURATION ---
# The script will now get the API Key from an environment variable for security
BUNKER_API_KEY = os.environ.get('BUNKER_API_KEY')
BUNKER_API_URL = "http://bunker.271triliun.xyz/api/submit_scraped_data.php"

# Because the GitHub Action runner is temporary, we define the feeds directly here.
# For a more advanced setup, this could read from a JSON file in the repository.
FEEDS_TO_SCRAPE = [
    {"url": "http://feeds.reuters.com/reuters/businessNews", "narrative_tag": "GLOBAL_MACRO"},
    {"url": "https://www.coindesk.com/arc/outboundfeeds/rss/", "narrative_tag": "CRYPTO_REGULATION"},
    {"url": "https://decrypt.co/feed", "narrative_tag": "CRYPTO_DEGEN"}
]

def post_to_bunker(data):
    headers = { 'Content-Type': 'application/json', 'X-API-KEY': BUNKER_API_KEY }
    try:
        response = requests.post(BUNKER_API_URL, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        print(f"Success: Posted '{data.get('headline')}' to Bunker.")
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to post to Bunker. {e}")

def main():
    if not BUNKER_API_KEY:
        print("FATAL ERROR: BUNKER_API_KEY secret not found. Cannot proceed.")
        return

    print("RSS Scout starting cycle...")
    # NOTE: Since this is a stateless environment, we don't save a state file.
    # It will re-process recent articles each time. Your Bunker PHP script's logic
    # should ideally prevent duplicate *file* creation, but for our intel
    # purposes, getting the same headline twice is not a critical failure.

    for feed_info in FEEDS_TO_SCRAPE:
        url = feed_info.get('url')
        narrative_tag = feed_info.get('narrative_tag', 'GENERAL_NEWS')
        print(f"Processing feed: {url}")
        
        feed = feedparser.parse(url)
        for entry in feed.entries:
            # We will post the last few articles each run.
            data_to_send = {
                "source_type": "RSS_FEED",
                "source_link": entry.get('link', ''),
                "headline": entry.title,
                "content": entry.get('summary', 'No summary.'),
                "published_at": entry.get('published', datetime.now().isoformat()),
                "macro_thesis_tag": narrative_tag
            }
            post_to_bunker(data_to_send)
            time.sleep(1) 
    print("RSS Scout cycle complete.")

if __name__ == "__main__":
    main()