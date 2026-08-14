import os
import re
import requests

SHOW_ID = os.getenv("SHOW_ID", "116360")

URL = (
    "https://in.bookmyshow.com/movies/hyderabad/"
    f"seat-layout/ET00439318/AMBH/{SHOW_ID}/20260814"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Linux; Android 10) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Mobile Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

print("Checking:", URL)

try:
    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=30,
        allow_redirects=True,
    )

    print("HTTP status:", response.status_code)
    print("Final URL:", response.url)
    print("Response size:", len(response.text))

    text = re.sub(r"\s+", " ", response.text).lower()

    keywords = [
        "sold out",
        "soldout",
        "available",
        "seat",
        "blocked",
        "booking",
    ]

    print("\nKeyword diagnostics:")

    for keyword in keywords:
        print(f"{keyword}: {text.count(keyword)}")

    if response.status_code != 200:
        raise SystemExit(
            f"BookMyShow returned HTTP {response.status_code}"
        )

    print("\nTEST PASSED")
    print("BookMyShow response was received.")
    print("Next step: identify the actual seat-status data.")

except requests.RequestException as error:
    print("REQUEST ERROR:", error)
    raise SystemExit(1)
