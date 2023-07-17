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
import csv

COLOR_MAP = [
    "#052e16",
    "#166534",
    "#16a34a",
    "#4ade80",
    "#bbf7d0",
    "#fecaca",
    "#f87171",
    "#dc2626",
    "#991b1b",
    "#450a0a",
]

# NOT FINAL, GET ALL THE DATA FIRST THEN FIGURE OUT IDEAL THRESHOLD
HIGH_THRESHOLD = 60000000


def get_segment_level(value, ranges):
    if value > ranges[-1]:
        return len(ranges) - 2

    for i in range(len(ranges) - 1):
        if ranges[i] <= value <= ranges[i + 1]:
            return i


######### VALUE GENERATION #########

with open("src/lib/data/barangays.json") as json_file:
    brgy_data = json.load(json_file)


with open("src/lib/data/barangays_values.csv", mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        # brgy_data[row["id"]]["value"] = float(row["price"]) if row["price"] != "" else 0
        brgy_data[row["id"]]["value"] = float(row["value"]) if row["value"] != "" else 0


######### SEGMENTATION #########

all_values = []

for brgy_id in brgy_data.keys():
    if (
        brgy_data[brgy_id]["value"] != 0
        and brgy_data[brgy_id]["value"] <= HIGH_THRESHOLD
    ):
        all_values.append(brgy_data[brgy_id]["value"])

num_segments = 10

min_val = min(all_values)
max_val = max(all_values)

print(all_values)

ranges = np.linspace(min_val, max_val, num_segments + 1)

# segments = []
for brgy_id in brgy_data.keys():
    if brgy_data[brgy_id]["value"] != 0:
        brgy_data[brgy_id]["level"] = get_segment_level(
            brgy_data[brgy_id]["value"], ranges
        )
        brgy_data[brgy_id]["color"] = COLOR_MAP[brgy_data[brgy_id]["level"]]
    else:
        brgy_data[brgy_id]["color"] = "gray"

with open(
    "src/lib/data/barangays_with_values.json", "w", encoding="utf-8"
) as json_file:
    json.dump(brgy_data, json_file)
