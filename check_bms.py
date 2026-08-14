import requests

url = "https://in.bookmyshow.com/api/movies-data/v4/showtimes-by-event/primary-dynamic"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "x-app-code": "WEB",
    "x-region-code": "HYD",
    "x-region-slug": "hyderabad",
    "x-latitude": "17.385",
    "x-longitude": "78.487",
    "x-location-selection": "manual",
}

params = {
    "eventCode": "ET00439318",
    "dateCode": "20260814",
    "isDesktop": "true",
    "regionCode": "HYD",
    "xLocationShared": "false",
    "memberId": "",
    "lsId": "",
    "subCode": "",
    "lat": "17.385",
    "lon": "78.487",
}

print("Checking BookMyShow API...")

r = requests.get(
    url,
    headers=headers,
    params=params,
    timeout=30
)

print("HTTP:", r.status_code)
print("Response length:", len(r.text))
print(r.text[:5000])
