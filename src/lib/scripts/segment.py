"""
This script takes in a cities json file that contains a "value" key, like so (position is irrelevant)

{
    "CITY OF MANILA": {
        "name": "Manila",
        "value": 219000,
        "position": { "lat": 14.5964947, "lng": 120.9883602 },
    },
    ...
}

It will then determine what "level" the value falls on a range and set the appropriate "level" and "color" on the data.

{
    "CITY OF MANILA": {
        "name": "Manila",
        "value": 219000,
        "position": { "lat": 14.5964947, "lng": 120.9883602 },
        "color": "#fda4af",
        "level": 3
    },
    ...
}

This script must be executed everytime the values or this script are updated.

Execute this script from the project root directory:

$ python3 src/lib/scripts/segment.py
"""

import sys
import json
import numpy as np

COLOR_MAP = ["#14532d", "#16a34a", "#86efac", "#fda4af", "#e11d48", "#881337"]


def get_segment_level(value, ranges):
    for i in range(len(ranges) - 1):
        if ranges[i] <= value <= ranges[i + 1]:
            return i


with open("src/lib/data/cities.json") as json_file:
    cities_data = json.load(json_file)

all_values = []

for city in cities_data.keys():
    if cities_data[city]["value"] != 0:
        all_values.append(cities_data[city]["value"])

num_segments = 6

min_val = min(all_values)
max_val = max(all_values)

ranges = np.linspace(min_val, max_val, num_segments + 1)

# segments = []
for city in cities_data.keys():
    if cities_data[city]["value"] != 0:
        cities_data[city]["level"] = get_segment_level(
            cities_data[city]["value"], ranges
        )

        cities_data[city]["color"] = COLOR_MAP[cities_data[city]["level"]]

with open("src/lib/data/cities.json", "w", encoding="utf-8") as json_file:
    json.dump(cities_data, json_file)
