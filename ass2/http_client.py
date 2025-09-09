#!/usr/bin/env python3
"""
http_client.py
- GET and POST example using requests
- Displays status code, headers, and body
- Logs errors to http_client.log
"""

import requests
import logging
import sys
import json

LOGFILE = "http_client.log"
logging.basicConfig(filename=LOGFILE, level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s", filemode="w")


def do_get(url, params=None):
    try:
        r = requests.get(url, params=params, timeout=10)
        print(f"GET {r.url} -> {r.status_code}")
        print("Headers:")
        for k, v in r.headers.items():
            print(f"  {k}: {v}")
        print("\nResponse body (truncated 1000 chars):")
        print(r.text[:1000])
        logging.info("GET %s %s", url, r.status_code)
        return r
    except Exception as e:
        logging.exception("GET request failed: %s", e)
        print("GET request failed:", e)
        return None


def do_post(url, payload=None):
    try:
        r = requests.post(url, json=payload, timeout=10)
        print(f"POST {r.url} -> {r.status_code}")
        print("Headers:")
        for k, v in r.headers.items():
            print(f"  {k}: {v}")
        print("\nResponse body (truncated 1000 chars):")
        print(r.text[:1000])
        logging.info("POST %s %s", url, r.status_code)
        return r
    except Exception as e:
        logging.exception("POST request failed: %s", e)
        print("POST request failed:", e)
        return None


def main():
    # Default test endpoints (httpbin.org)
    get_url = "https://httpbin.org/get"
    post_url = "https://httpbin.org/post"

    print("HTTP Client Demo")
    print("================")

    print("\nPerforming GET request...")
    do_get(get_url, params={"student": "sumit", "task": "http-get"})

    print("\nPerforming POST request...")
    payload = {"name": "sumit", "roll": "2301MC29", "task": "http-post"}
    do_post(post_url, payload=payload)


if __name__ == "__main__":
    main()
