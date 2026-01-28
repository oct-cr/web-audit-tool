import argparse
import os
import sys

from rich.console import Console

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from modules.lighthouse.insights import get_summary, get_summary_columns
from modules.lighthouse.categories import get_relevant_category_audits
from modules.lighthouse.terminal import print_audit, print_summary_table
from services.workspaces import load_sites, find_site
from services.reports import get_url_reports, read_report


def main(argv=None):
    p = argparse.ArgumentParser(description="List report files for a site key")
    p.add_argument("site_key", help="Site key to look up")
    args = p.parse_args(argv)

    sites = load_sites("sites.yaml")
    site = find_site(sites, args.site_key)

    if site is None:
        raise ValueError(f"Site not found: {args.site_key}")

    print(f"{site.get('name')} ({args.site_key})")

    for page in site.get("pages", {}).values():
        url = page.get("url")

        if not url:
            continue

        reports = get_url_reports(url)
        if not reports:
            continue

        report = read_report(reports[0])

        print_insights(report)


def print_insights(data):
    lr = data.get("lighthouseResult", {})
    audits = lr.get("audits", {})
    categories = lr.get("categories", {})

    initial_url = lr.get("requestedUrl")
    if initial_url:
        print(f"Report for: {initial_url}")

    fetch_time = lr.get("fetchTime")
    if fetch_time:
        print(f"Fetched at: {fetch_time}")

    columns = get_summary_columns()
    del columns["url"]

    print_summary_table([get_summary(data)], columns=columns)

    print()

    console = Console()
    for category in categories.values():
        relevant_audits = get_relevant_category_audits(audits, category)

        if len(relevant_audits) == 0:
            continue

        console.rule(
            f"{category.get('title')} {len(relevant_audits)}",
            align="left",
            style="dim",
        )

        for audit in relevant_audits:
            print_audit(audit)

        print()


if __name__ == "__main__":
    sys.exit(main())
