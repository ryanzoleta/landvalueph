import json
import csv
from random import choice


def calculate_center(coordinates):
    # Ensure the coordinates list is not empty
    if not coordinates:
        return None

    # Initialize variables to store sum of latitudes and longitudes
    sum_latitude = 0
    sum_longitude = 0

    # Iterate through all the coordinates and calculate the sum of latitudes and longitudes
    for lon, lat in coordinates:
        sum_latitude += lat
        sum_longitude += lon

    # Calculate the average latitude and longitude
    avg_latitude = sum_latitude / len(coordinates)
    avg_longitude = sum_longitude / len(coordinates)

    return avg_latitude, avg_longitude


def random_color():
    colors = [
        "#a3e635",
        "#22d3ee",
        "#a78bfa",
        "#e879f9",
        "#fb7185",
        "#f472b6",
        "#94a3b8",
        "#27272a",
    ]

    return choice(colors)


with open("src/lib/data/barangays_geodata.json") as json_file:
    raw_data = json.load(json_file)

all_brgy = raw_data["features"]
normalized = {}

for brgy in all_brgy:
    brgy_id = ""
    brgy_name = ""
    city = ""

    if (
        brgy["properties"]["ADM2_EN"]
        == "NCR, CITY OF MANILA, FIRST DISTRICT (Not a Province)"
    ):
        brgy_name = brgy["properties"]["ADM3_EN"]
        brgy_id = brgy["properties"]["ADM3_PCODE"]
        city = "CITY OF MANILA"
    else:
        brgy_name = brgy["properties"]["ADM4_EN"]
        brgy_id = brgy["properties"]["ADM4_PCODE"]
        city = brgy["properties"]["ADM3_EN"]

    if city in ["CALOOCAN CITY", "PASAY CITY"]:
        continue

    normalized[brgy_id] = {}

    normalized[brgy_id]["id"] = brgy_id
    normalized[brgy_id]["name"] = brgy_name
    normalized[brgy_id]["city"] = city

    try:
        coors = (
            brgy["geometry"]["coordinates"][0][0]
            if brgy["geometry"]["type"] == "MultiPolygon"
            else brgy["geometry"]["coordinates"][0]
        )
        lat, lng = calculate_center(coors)
    except:
        print(brgy)
        exit()

    ##### DATA CORRECTIONS #####
    if brgy_name == "MALATE":
        lat, lng = (14.570199, 120.991420)
    elif brgy_name == "PACO":
        lat, lng = (14.584858, 120.994482)
    elif brgy_name == "PANDACAN":
        lat, lng = (14.590920, 121.005592)
    elif brgy_name == "SANTA ANA":
        lat, lng = (14.576558, 121.006426)
    elif brgy_name == "SAMPALOC":
        lat, lng = (14.609748, 120.999008)
    elif brgy_name == "TONDO I / II":
        lat, lng = (14.618714, 120.965756)
    elif brgy_name == "SANTA CRUZ":
        lat, lng = (14.616860, 120.982948)
    elif brgy_name == "QUIAPO":
        lat, lng = (14.598240, 120.985848)
    elif brgy_name == "ERMITA":
        lat, lng = (14.582367, 120.984626)

    normalized[brgy_id]["position"] = {"lat": lat, "lng": lng}
    normalized[brgy_id]["color"] = random_color()

with open("src/lib/data/barangays.json", "w", encoding="utf-8") as json_file:
    json.dump(normalized, json_file)


with open("src/lib/data/barangays.csv", mode="w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=normalized[brgy_id].keys())

    writer.writeheader()
    for brgy in normalized.keys():
        writer.writerow(normalized[brgy])
