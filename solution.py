import argparse
import requests


def download_timezones():
    url = "https://raw.githubusercontent.com/dmfilipenko/timezones.json/master/timezones.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to download time zone information.")


def get_timezones(match=None, offset=None):
    timezones = download_timezones()

    if match:
        timezones = [tz for tz in timezones if match.lower()==tz["value"].lower()]

    if offset:
        timezones = [tz for tz in timezones if tz["offset"] == offset]

    return timezones


def display_timezones(timezones):
    timezones_list = []
    if len(timezones) == 0:
        print("No time zones found matching the criteria.")
        return timezones_list
    else:
        for tz in timezones:
            data = {
                "Timezone Name": tz['value'],
                "Timezone Abbr": tz['abbr'],
                "Timezone Offset": tz['offset'],
                "Timezone isDST": tz['isdst'],
                "Timezone Description": tz['text'],
                "Timezone UTC": tz['utc']
            }
            timezones_list.append(data)
        return timezones_list


def main():
    parser = argparse.ArgumentParser(description='World Time Zones')
    parser.add_argument('--match', type=str, help='Display time zones matching the specified string')
    parser.add_argument('--offset', type=int, help='Display time zones matching the specified offset')
    args = parser.parse_args()

    try:
        timezones = get_timezones(args.match, args.offset)
        timezones_list = display_timezones(timezones)
        return timezones_list
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    timezones_list = main()
    print("Time Zones:-")
    for value in timezones_list:
        print(value, end="\n")
        print()
