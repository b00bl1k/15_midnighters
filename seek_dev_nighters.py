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
        users_list = requests.get(DEVMAN_API_URL, {"page": page}).json()
        pages = users_list["number_of_pages"]
        page += 1
        for user in users_list["records"]:
            yield user


def get_midnighters():
    midnighters = Counter()
    for user in load_attempts():
        tz = pytz.timezone(user["timezone"])
        time = datetime.fromtimestamp(user["timestamp"], tz)
        hour = time.hour
        if NIGHT_START <= hour < NIGHT_END:
            midnighters.update([user["username"]])
    return midnighters


def main():
    midnighters = get_midnighters()
    print("Top midnighters:")
    for midnighter, attempts in midnighters.most_common():
        print("- {} made {} attempts".format(midnighter, attempts))


if __name__ == "__main__":
    main()
