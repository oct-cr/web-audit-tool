import argparse
import os
from datetime import datetime

from dotenv import load_dotenv

from ..modules.lighthouse import run_lighthouse_report
from ..services.workspaces import get_node_by_path, get_site_pages


def run_lighthouse(workspace, route, argv) -> int:
    load_dotenv()

    parser = argparse.ArgumentParser(prog="dashkit lighthouse")
    parser.add_argument("--dry", action="store_true", help="Show URLs without running audits")
    parser.add_argument(
        "--strategy", action="store", help="Audit strategy (Desktop or Mobile)", default="Mobile"
    )

    args = parser.parse_args(argv)

    is_dry_run = args.dry

    api_key = os.environ.get("PAGESPEED_API_KEY")
    if not is_dry_run and not api_key:
        raise RuntimeError("PAGESPEED_API_KEY must be set. Use --dry to run without API key.")

    site = get_node_by_path(workspace, route)
    if site.get("node_type") != "site":
        raise ValueError(
            "Lighthouse audits can only be run on site nodes. Please specify a site route."
        )

    pages = get_site_pages(site)

    round_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    strategy = args.strategy.lower()

    for page in pages:
        url = page.get("url")
        if not url:
            continue

        if args.dry:
            print(f"[DRY RUN] {url}")
            continue

        key_parts = ["lhr", site.get("key"), page.get("key"), strategy, round_timestamp]
        key = "-".join(key_parts)

        assert api_key is not None  # checked above. Type checker line

        run_lighthouse_report(
            url, api_key=api_key, workspace_key=workspace.get("key"), snapshot_key=key
        )

    return 0
