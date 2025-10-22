#!/usr/bin/env python3
"""
update_streams_from_github.py

Fetches an .m3u playlist from a GitHub repository,
extracts all .m3u8 links, and updates a JSON file with them.
"""

import json
import re
import requests
import os

# GitHub raw URL of the M3U file
M3U_URL = "https://raw.githubusercontent.com/Srivyaa/News_Channels/main/news_channels.m3u"
JSON_FILE = "streams.json"

def fetch_m3u(url):
    """Fetch the M3U playlist content from a remote URL."""
    print(f"📥 Fetching M3U from: {url}")
    response = requests.get(url, timeout=15)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch M3U file (HTTP {response.status_code})")
    return response.text

def extract_m3u8_links(m3u_content):
    """Extract all .m3u8 URLs from the given text content."""
    pattern = re.compile(r'https?://[^\s"\']+?\.m3u8(?:\?[^\s"\']*)?', re.IGNORECASE)
    links = pattern.findall(m3u_content)
    return sorted(set(links))  # remove duplicates

def update_json(links, json_path):
    """Write links to JSON file."""
    data = {"m3u8_links": links}
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"✅ Updated {json_path} with {len(links)} links.")

def main():
    try:
        m3u_content = fetch_m3u(M3U_URL)
        links = extract_m3u8_links(m3u_content)
        if not links:
            print("⚠️ No .m3u8 links found.")
            return
        update_json(links, JSON_FILE)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
