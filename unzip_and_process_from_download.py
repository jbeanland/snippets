"""
Download a zip file, and extract a single csv from it without saving any local files.
Std lib only.

Originally for downloading public transport stops in Oslo,
final step is reading the csv and building a json from it.
"""
import csv
import json
from urllib import request
import zipfile
from io import BytesIO, StringIO


# URL and filenames
url = "https://storage.googleapis.com/marduk-production/outbound/gtfs/rb_rut-aggregated-gtfs.zip"
zipped_file = "stops.txt"
output_file = "ruter_stops.json"

# Mapper from the vehicle ids to meaningful strings.
transport_types = {1000: 'ferry', 900: 'tram', 401: 'tbane', 700: 'bus'}

print("begin")

response = request.urlopen(url)       # response object
stopsdata: bytes = response.read()    # bytes object of the zip file
stopsdata = BytesIO(stopsdata)        # put it in a BytesIO so we can use it
print("response read")

with zipfile.ZipFile(stopsdata) as z:
    stops_file: str = z.read(zipped_file).decode()   # the decoded extrated csv file in str form
print("extracted")

csvfile = StringIO(stops_file)        # Put it in a StringIO object so we can use it

csv_reader = csv.reader(csvfile)
headers = next(csv_reader)
stops = [
    {
        "stop_id": row[0],
        "stop_name": row[2],
        "vehicle_type": transport_types[int(row[13])],
    }
    for row in csv_reader
]
print("created stops dict")
with open(output_file, "w") as f:
    json.dump(stops, f)

print("end")
