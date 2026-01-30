import argparse
import os
import sys

from rich.console import Console

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from sections.urlsummary.dataprovider import get_url_summary
from sections.urlsummary.view import get_url_summary_view
from services.workspaces import load_sites, find_site


def main(argv=None):
    p = argparse.ArgumentParser(description="List report files for a site key")
    p.add_argument("site_key", help="Site key to look up")
    args = p.parse_args(argv)

    sites = load_sites("sites.yaml")
    site = find_site(sites, args.site_key)

    if site is None:
        raise ValueError(f"Site not found: {args.site_key}")

    print(f"{site.get('name')} ({args.site_key})")

    console = Console()

    for page in site.get("pages", {}).values():
        url = page.get("url")

        if not url:
            continue

        url_summary = get_url_summary(url)
        if not url_summary:
            continue

        console.print(get_url_summary_view(url_summary))


if __name__ == "__main__":
    sys.exit(main())
