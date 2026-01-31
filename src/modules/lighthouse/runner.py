from .http import fetch_lighthouse
from ...services.reports import write_report


def run_lighthouse_report(
    url: str,
    api_key: str,
    strategy: str = "Desktop",
    round_timestamp: str = "",
) -> str:
    print(f"Running Lighthouse for {url}...")
    body = fetch_lighthouse(url, api_key=api_key, strategy=strategy)

    if body is None:
        raise RuntimeError("Lighthouse run failed.")

    key = strategy.lower() + "-" + round_timestamp

    out_path = write_report(url, key, body)

    print(f"Report saved to: {out_path}")
    return out_path
