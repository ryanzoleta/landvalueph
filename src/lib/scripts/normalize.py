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
    brgy_name = ""
    city = ""

    if (
        brgy["properties"]["ADM2_EN"]
        == "NCR, CITY OF MANILA, FIRST DISTRICT (Not a Province)"
    ):
        brgy_name = brgy["properties"]["ADM3_EN"]
        city = "CITY OF MANILA"
    else:
        brgy_name = brgy["properties"]["ADM4_EN"]
        city = brgy["properties"]["ADM3_EN"]

    if city in ["CALOOCAN CITY", "PASAY CITY"]:
        continue

    # if city not in [
    #     "CITY OF MANILA",
    #     "CITY OF MAKATI",
    # ]:
    #     continue

    normalized[brgy_name] = {}
    normalized[brgy_name]["name"] = brgy_name
    normalized[brgy_name]["city"] = city

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

    normalized[brgy_name]["position"] = {"lat": lat, "lng": lng}
    normalized[brgy_name]["color"] = random_color()

with open("src/lib/data/barangays.json", "w", encoding="utf-8") as json_file:
    json.dump(normalized, json_file)


# with open("src/lib/data/barangays.csv", mode="w") as csv_file:
#     fieldnames = ["ADM2_EN", "ADM3_EN", "ADM4_EN"]
#     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

#     writer.writeheader()

#     for brgy in all_brgy:
#         writer.writerow(
#             {
#                 "ADM2_EN": brgy["properties"]["ADM2_EN"],
#                 "ADM3_EN": brgy["properties"]["ADM3_EN"],
#                 "ADM4_EN": brgy["properties"]["ADM4_EN"],
#             }
#         )
