import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"


def fetch_lighthouse(url, api_key=None, strategy=None):
    params = [
        ("url", url),
        ("category", "performance"),
        ("category", "accessibility"),
        ("category", "best-practices"),
        ("category", "seo"),
    ]

    if api_key:
        params.append(("key", api_key))
    if strategy:
        params.append(("strategy", strategy))

    qs = urllib.parse.urlencode(params)
    full_url = f"{API_BASE}?{qs}"

    try:
        resp = urllib.request.urlopen(full_url)

    except urllib.error.HTTPError as e:
        try:
            msg = e.read().decode("utf-8", errors="ignore")
        except Exception:
            msg = ""

        raise Exception(f"HTTPError {e.code}: {e.reason}\n{msg}") from e

    except Exception as e:
        raise Exception(f"Error calling PageSpeed API: {e}") from e

    body = resp.read()
    return body
