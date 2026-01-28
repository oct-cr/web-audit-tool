import argparse

from modules.lighthouse.http import fetch_lighthouse
from services.reports import write_report


def run_lighthouse_report(url, api_key, strategy=None):
    print(f"Running Lighthouse for {url}...")
    body = fetch_lighthouse(url, api_key=api_key, strategy=strategy)

    if body is None:
        raise RuntimeError("Lighthouse run failed.")

    out_path = write_report(url, body)

    print(f"Report saved to: {out_path}")


def main():
    p = argparse.ArgumentParser(
        description="Run Lighthouse (PageSpeed API) for a URL and produce a JSON report"
    )
    p.add_argument("url", help="URL to audit")
    p.add_argument(
        "--folder",
        default=".",
        help="Target report folder where JSON will be saved",
    )
    p.add_argument("--key", required=True, help="Google API key")
    p.add_argument(
        "--strategy",
        choices=["mobile", "desktop"],
        help="Run strategy (mobile or desktop)",
    )

    args = p.parse_args()
    api_key = args.key

    run_lighthouse_report(args.url, api_key=api_key, strategy=args.strategy)


if __name__ == "__main__":
    main()
