from datetime import datetime
from collections import Counter
import requests
import pytz


NIGHT_START = 0
NIGHT_END = 4
DEVMAN_API_URL = "https://devman.org/api/challenges/solution_attempts/"


def load_attempts():
    pages = 1
    page = 1
    while page <= pages:
        attempts = requests.get(DEVMAN_API_URL, {"page": page}).json()
        pages = attempts["number_of_pages"]
        page += 1
        yield from attempts["records"]


def get_midnighters():
    for attempt in load_attempts():
        tz = pytz.timezone(attempt["timezone"])
        time = datetime.fromtimestamp(attempt["timestamp"], tz)
        hour = time.hour
        if NIGHT_START <= hour < NIGHT_END:
            yield attempt["username"]


def main():
    midnighters_counter = Counter(get_midnighters())
    print("Top midnighters:")
    for midnighter, attempts in midnighters_counter.most_common():
        print("- {} made {} attempts".format(midnighter, attempts))


if __name__ == "__main__":
    main()
