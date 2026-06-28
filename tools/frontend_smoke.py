import requests
import json

URL = "http://import.meta.env.VITE_API_URL/recommend/40beb0b49193159063a6f6135e02b4f42d96de02234afea9a002b8e193195431"


def main():
    try:
        r = requests.get(URL, timeout=10)
    except Exception as e:
        print("ERROR: could not reach recommendation API:", e)
        return

    print("STATUS", r.status_code)
    try:
        data = r.json()
    except Exception as e:
        print("ERROR parsing JSON:", e)
        return

    print("KEYS:", list(data.keys()))
    recs = data.get("recommendations") or []
    print("RECS_COUNT", len(recs))
    if recs:
        print("FIRST:", json.dumps(recs[0], indent=2))


if __name__ == '__main__':
    main()
