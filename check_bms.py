import os
import json
import requests

SHOW_ID = os.getenv("SHOW_ID", "116360")
VENUE = "AMBH"

URL = (
    "https://in.bookmyshow.com/serv/getData"
    "?cmd=GETSHOWINFOJSON"
    f"&vid={VENUE}"
    f"&ssid={SHOW_ID}"
    "&format=json"
)

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json,text/plain,*/*",
    "Referer": (
        f"https://in.bookmyshow.com/movies/hyderabad/"
        f"seat-layout/ET00439318/AMBH/{SHOW_ID}/20260814"
    ),
    "Origin": "https://in.bookmyshow.com",
}

print("Testing BookMyShow API")
print("Show ID:", SHOW_ID)
print("URL:", URL)

session = requests.Session()

try:
    response = session.get(
        URL,
        headers=headers,
        timeout=30
    )

    print("HTTP status:", response.status_code)
    print("Response size:", len(response.text))
    print("Final URL:", response.url)

    print("\n--- RESPONSE START ---")
    print(response.text[:10000])
    print("--- RESPONSE END ---")

    if response.status_code != 200:
        raise SystemExit(
            f"BookMyShow API returned HTTP {response.status_code}"
        )

    try:
        data = response.json()
        print("\nJSON received successfully.")

        # Save a readable copy in the Actions log
        print(json.dumps(data, indent=2)[:10000])

    except ValueError:
        print("\nResponse was not JSON.")
        raise SystemExit(1)

except requests.RequestException as error:
    print("REQUEST ERROR:", error)
    raise SystemExit(1)
