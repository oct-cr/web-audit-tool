import argparse
import os
import sys
from datetime import datetime

from dotenv import load_dotenv

from ..modules.lighthouse import run_lighthouse_report
from ..services.workspaces import find_site, load_sites


def run_lighthouse(argv) -> int:
    load_dotenv()

    parser = argparse.ArgumentParser(prog="webaudit lighthouse")
    parser.add_argument("site_key", help="Site key or name from sites.yaml")
    parser.add_argument("--sites", default="sites.yaml", help="Path to sites config")
    parser.add_argument("--dry", action="store_true", help="Show URLs without running audits")

    args = parser.parse_args(argv)

    sites = load_sites(args.sites)
    site = find_site(sites, args.site_key)

    if not site:
        print(f"Site not found for key/name: {args.site_key}", file=sys.stderr)
        return 2

    pages_conf = site.get("pages", {})
    api_key = os.environ.get("PAGESPEED_API_KEY")
    if not api_key:
        print("PAGESPEED_API_KEY must be set", file=sys.stderr)
        return 1

    round_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for page in pages_conf.values():
        url = page.get("url")
        if not url:
            continue

        if args.dry:
            print(f"[DRY RUN] {url}")
            continue

        run_lighthouse_report(url, api_key=api_key, round_timestamp=round_timestamp)

    return 0
