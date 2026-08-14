import os
import requests
from datetime import datetime

# ==============================
# WATCH CONFIG
# ==============================

EVENT_CODE = "ET00439318"
DATE_CODE = "20260814"

THEATRE = "AMB"
TARGET_TIME = "11:05 PM"

NTFY_TOPIC = os.getenv(
    "NTFY_TOPIC",
    "awarapan2-amb-847291"
)

# ==============================
# BOOKMYSHOW API
# ==============================

API_URL = (
    "https://in.bookmyshow.com/api/movies-data/v4/"
    "showtimes-by-event/primary-dynamic"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/145.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",

    "Referer": (
        "https://in.bookmyshow.com/movies/"
        "hyderabad/buytickets/ET00439318"
    ),

    "sec-ch-ua":
        '"Chromium";v="145", "Not:A-Brand";v="99"',

    "sec-ch-ua-mobile": "?0",

    "sec-ch-ua-platform": '"macOS"',

    "x-app-code": "WEB",
    "x-region-code": "HYD",
    "x-region-slug": "hyderabad",
    "x-geohash": "tep",
    "x-latitude": "17.385",
    "x-longitude": "78.487",
    "x-location-selection": "manual",
    "x-lsid": "",
}

PARAMS = {
    "eventCode": EVENT_CODE,
    "dateCode": DATE_CODE,
    "isDesktop": "true",
    "regionCode": "HYD",
    "xLocationShared": "false",
    "memberId": "",
    "lsId": "",
    "subCode": "",
    "lat": "17.385",
    "lon": "78.487",
}


# ==============================
# NTFY
# ==============================

def send_ntfy(message):

    url = f"https://ntfy.sh/{NTFY_TOPIC}"

    response = requests.post(
        url,
        data=message.encode("utf-8"),
        headers={
            "Title": "BookMyShow — AMB 11:05 PM",
            "Priority": "high",
            "Tags": "movie,ticket",
        },
        timeout=15,
    )

    print("ntfy HTTP:", response.status_code)

    if response.status_code >= 300:
        print(response.text)


# ==============================
# FETCH BMS
# ==============================

def get_bms():

    print("Checking BookMyShow...")
    print("Event:", EVENT_CODE)
    print("Date:", DATE_CODE)

    response = requests.get(
        API_URL,
        headers=HEADERS,
        params=PARAMS,
        timeout=30,
    )

    print("HTTP:", response.status_code)
    print("Response length:", len(response.text))

    if response.status_code != 200:

        print("BookMyShow did not return JSON.")
        print(response.text[:1000])

        return None

    return response.json()


# ==============================
# FIND AMB 11:05
# ==============================

def find_target(data):

    widgets = (
        data
        .get("data", {})
        .get("showtimeWidgets", [])
    )

    for widget in widgets:

        if widget.get("type") != "groupList":
            continue

        for group in widget.get("data", []):

            if group.get("type") != "venueGroup":
                continue

            for card in group.get("data", []):

                if card.get("type") != "venue-card":
                    continue

                additional = card.get(
                    "additionalData", {}
                )

                venue_name = additional.get(
                    "venueName", ""
                )

                venue_code = additional.get(
                    "venueCode", ""
                )

                if (
                    THEATRE.lower()
                    not in venue_name.lower()
                    and venue_code != "AMBH"
                ):
                    continue

                print("Found theatre:", venue_name)

                for show in card.get(
                    "showtimes", []
                ):

                    time = show.get(
                        "title", ""
                    ).strip()

                    if time != TARGET_TIME:
                        continue

                    print(
                        "TARGET FOUND:",
                        venue_name,
                        time
                    )

                    show_data = show.get(
                        "additionalData", {}
                    )

                    categories = show_data.get(
                        "categories", []
                    )

                    available = []

                    for category in categories:

                        name = category.get(
                            "priceDesc", ""
                        )

                        price = category.get(
                            "curPrice", ""
                        )

                        status = str(
                            category.get(
                                "availStatus", ""
                            )
                        )

                        print(
                            name,
                            "| ₹" + str(price),
                            "| status =", status
                        )

                        # 0 = SOLD OUT
                        # 1 = ALMOST FULL
                        # 2 = FILLING FAST
                        # 3 = AVAILABLE

                        if status in (
                            "1",
                            "2",
                            "3",
                        ):
                            available.append(
                                f"{name} ₹{price}"
                            )

                    if available:

                        message = (
                            "🎟️ SEATS AVAILABLE!\n\n"
                            "Awarapan 2\n"
                            "AMB Cinemas, Hyderabad\n"
                            "11:05 PM\n\n"
                            + "\n".join(
                                "• " + x
                                for x in available
                            )
                            + "\n\n"
                            "Book now!"
                        )

                        print(message)

                        send_ntfy(message)

                        return True

                    print(
                        "11:05 PM is currently SOLD OUT."
                    )

                    return False

    print(
        "AMB 11:05 PM show was not found."
    )

    return False


# ==============================
# MAIN
# ==============================

print("=" * 50)
print("AMB 11:05 PM BMS CHECKER")
print(datetime.now())
print("=" * 50)

data = get_bms()

if data is not None:
    find_target(data)
