#!/usr/bin/env python3
"""
update_streams_json.py

Fetches an M3U playlist from GitHub, extracts .m3u8 links,
and writes them to a JSON file in the detailed structure.
"""

import json
import re
import requests
import os
import uuid
from datetime import datetime

# Input M3U URL
M3U_URL = "https://raw.githubusercontent.com/Srivyaa/News_Channels/main/news_channels.m3u"

# Output JSON path
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)
JSON_FILE = os.path.join(DATA_FOLDER, "streams.json")


def fetch_m3u(url):
    """Fetch M3U content from URL."""
    response = requests.get(url, timeout=15)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch M3U (HTTP {response.status_code})")
    return response.text


def extract_m3u8_links(m3u_content):
    """Return a list of all .m3u8 links."""
    pattern = re.compile(r'https?://[^\s"\']+?\.m3u8(?:\?[^\s"\']*)?', re.IGNORECASE)
    links = pattern.findall(m3u_content)
    return sorted(set(links))


def build_stream_entry(url):
    """Build a dictionary entry in the required JSON format."""
    now = datetime.utcnow()
    iso_now = now.isoformat() + "Z"
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")

    entry = {
        "changeuuid": str(uuid.uuid4()),
        "stationuuid": str(uuid.uuid4()),
        "serveruuid": str(uuid.uuid4()),
        "name": url.split("/")[-1],  # Use last part of URL as name
        "url": url,
        "url_resolved": url,
        "homepage": "",
        "favicon": "",
        "tags": "",
        "country": "",
        "countrycode": "",
        "iso_3166_2": "",
        "state": "",
        "language": "",
        "languagecodes": "",
        "votes": 0,
        "lastchangetime": timestamp_str,
        "lastchangetime_iso8601": iso_now,
        "codec": "MP3",
        "bitrate": 128,
        "hls": 1,
        "lastcheckok": 1,
        "lastchecktime": timestamp_str,
        "lastchecktime_iso8601": iso_now,
        "lastcheckoktime": timestamp_str,
        "lastcheckoktime_iso8601": iso_now,
        "lastlocalchecktime": timestamp_str,
        "lastlocalchecktime_iso8601": iso_now,
        "clicktimestamp": timestamp_str,
        "clicktimestamp_iso8601": iso_now,
        "clickcount": 0,
        "clicktrend": 0,
        "ssl_error": 0,
        "geo_lat": None,
        "geo_long": None,
        "geo_distance": None,
        "has_extended_info": False
    }
    return entry


def main():
    try:
        m3u_content = fetch_m3u(M3U_URL)
        links = extract_m3u8_links(m3u_content)
    except Exception as e:
        print(f"❌ Error fetching or parsing M3U: {e}")
        links = []

    entries = [build_stream_entry(url) for url in links]

    # Always write JSON, even if empty
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)

    print(f"✅ Written {len(entries)} entries to {JSON_FILE}")
    print(f"link_count={len(entries)}")  # For GitHub Actions output


if __name__ == "__main__":
    main()
