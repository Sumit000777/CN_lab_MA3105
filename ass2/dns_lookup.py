#!/usr/bin/env python3
"""
dns_lookup.py
- Resolve A, MX, CNAME records for a domain and log results to dns_lookup.log
"""

import dns.resolver
import logging

LOGFILE = "dns_lookup.log"
logging.basicConfig(filename=LOGFILE, level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s", filemode="w")


def query_records(domain):
    print(f"Querying DNS records for {domain}")
    logging.info("Querying DNS records for %s", domain)

    # A records
    try:
        answers = dns.resolver.resolve(domain, "A")
        addrs = [rdata.to_text() for rdata in answers]
        print("A records:", addrs)
        logging.info("A records: %s", addrs)
    except Exception as e:
        print("A lookup failed:", e)
        logging.warning("A lookup failed for %s: %s", domain, e)

    # MX records
    try:
        answers = dns.resolver.resolve(domain, "MX")
        mxs = [rdata.to_text() for rdata in answers]
        print("MX records:", mxs)
        logging.info("MX records: %s", mxs)
    except Exception as e:
        print("MX lookup failed:", e)
        logging.warning("MX lookup failed for %s: %s", domain, e)

    # CNAME (if any)
    try:
        answers = dns.resolver.resolve(domain, "CNAME")
        cnames = [rdata.to_text() for rdata in answers]
        print("CNAME records:", cnames)
        logging.info("CNAME records: %s", cnames)
    except Exception as e:
        # Not all domains have CNAMEs; treat it as informative
        logging.info("CNAME lookup for %s: %s", domain, e)

    print("-" * 40)


if __name__ == "__main__":
    domains = ["google.com", "iitp.ac.in", "mail.google.com", "nonexistent-example-abc-1234.com"]
    for d in domains:
        query_records(d)
