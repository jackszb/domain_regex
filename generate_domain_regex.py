#!/usr/bin/env python3
import json
import re
import urllib.request
from pathlib import Path
from typing import Optional

WILDCARD_URL = "https://raw.githubusercontent.com/jackszb/DnsFilter/main/wildcard.txt"
OUTPUT_FILE = Path("domain_regex.json")

# 允许域名字符：字母、数字、点、- 和 *
VALID_DOMAIN_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-*")

def wildcard_to_regex(domain: str) -> Optional[str]:
    domain = domain.strip()
    if not domain or domain.startswith("#"):
        return None

    # 去掉末尾不完整的点
    domain = domain.rstrip(".")

    # 检查是否包含非法字符
    if not set(domain) <= VALID_DOMAIN_CHARS:
        return None

    # 如果剩下的只有 * 或 - 或 .，跳过
    if not any(c.isalnum() for c in domain):
        return None

    # 转义正则特殊字符，保留 *
    domain_regex = re.escape(domain).replace(r"\*", ".*")

    return f"^{domain_regex}$"

def main():
    response = urllib.request.urlopen(WILDCARD_URL)
    content = response.read().decode("utf-8")

    regex_list = []
    skipped_count = 0

    for line in content.splitlines():
        regex = wildcard_to_regex(line)
        if regex:
            regex_list.append(regex)
        else:
            skipped_count += 1

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

    print(f"生成完成：{OUTPUT_FILE}")
    print(f"有效规则数量：{len(regex_list)}，跳过非法条目：{skipped_count}")

if __name__ == "__main__":
    main()
