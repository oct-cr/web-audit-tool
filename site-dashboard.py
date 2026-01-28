import argparse
import os
import sys

from rich.console import Console

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from modules.lighthouse.insights import get_summary
from modules.lighthouse.terminal import print_summary_table

from services.reports import get_url_reports, read_report
from services.workspaces import load_sites, find_site, get_site_urls


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("site_key", help="Site key to look up")
    args = p.parse_args(argv)

    sites = load_sites("sites.yaml")
    site = find_site(sites, args.site_key)

    if site is None:
        raise ValueError(f"Site not found: {args.site_key}")

    rows = []

    for url in get_site_urls(site):
        report_urls = get_url_reports(url)
        if not report_urls:
            continue

        report = read_report(report_urls[0])
        rows.append(get_summary(report))

    console = Console()

    if not rows:
        console.print("[yellow]No reports found for this site.[/]")
        return

    print_summary_table(rows)


if __name__ == "__main__":
    sys.exit(main())
