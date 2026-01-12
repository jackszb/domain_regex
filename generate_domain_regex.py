#!/usr/bin/env python3
import json
import re
import urllib.request
from pathlib import Path

WILDCARD_URL = "https://raw.githubusercontent.com/jackszb/DnsFilter/main/wildcard.txt"
OUTPUT_FILE = Path("domain_regex.json")

def wildcard_to_regex(domain: str) -> str | None:
    domain = domain.strip()
    if not domain or domain.startswith("#"):
        return None

    domain = re.escape(domain)
    domain = domain.replace(r"\*", ".*")
    return f"^{domain}$"

def main():
    response = urllib.request.urlopen(WILDCARD_URL)
    content = response.read().decode("utf-8")

    regex_list = []

    for line in content.splitlines():
        regex = wildcard_to_regex(line)
        if regex:
            regex_list.append(regex)

    output = {
        "version": 3,
        "rules": [
            {
                "domain_regex": regex_list
            }
        ]
    }

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
