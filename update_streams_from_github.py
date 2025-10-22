#!/usr/bin/env python3
"""
update_streams_from_github.py

Fetches an .m3u playlist from a GitHub repository,
extracts all .m3u8 links, and updates a JSON file with them.
Always creates streams.json even if no links are found.
"""

import json
import re
import requests
import os

M3U_URL = "https://raw.githubusercontent.com/Srivyaa/News_Channels/main/news_channels.m3u"
DATA_FOLDER = "data"
JSON_FILE = os.path.join(DATA_FOLDER, "streams.json")

# Ensure the data folder exists
os.makedirs(DATA_FOLDER, exist_ok=True)

def fetch_m3u(url):
    response = requests.get(url, timeout=15)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch M3U file (HTTP {response.status_code})")
    return response.text

def extract_m3u8_links(m3u_content):
    pattern = re.compile(r'https?://[^\s"\']+?\.m3u8(?:\?[^\s"\']*)?', re.IGNORECASE)
    links = pattern.findall(m3u_content)
    return sorted(set(links))

def update_json(links, json_path):
    data = {"m3u8_links": links}
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return len(links)

def main():
    try:
        # Try to fetch the M3U file
        m3u_content = fetch_m3u(M3U_URL)
        links = extract_m3u8_links(m3u_content)
    except Exception as e:
        print(f"❌ Error fetching M3U file: {e}")
        links = []

    # Always update/create JSON file, even if links is empty
    count = update_json(links, JSON_FILE)
    print(f"✅ Updated {JSON_FILE} with {count} links.")
    print(f"link_count={count}")  # GitHub Actions output

if __name__ == "__main__":
    main()
