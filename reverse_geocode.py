# This program reads the file latest.csv, a list of lat/lon coordinates, and attempts to reverse geocode them using
# Google Map's API.  The program appends the data to the file complete_trip_data.csv

import csv
from pygeocoder import Geocoder



# Let's open some files.  We need to open filename first to read it's contents.  Once we've read the contents, we'll
# open it for writing so all coordinates not looked up can be written back to the file.
# We need to open outfile.  It will contain country, state, county, city, postal_code, street_number, and
# route information from Google Maps.

def reverse_geo_lookup(filename, outfile):
# This function performs a reverse geo-lookup on coordinates using Google Maps.  The function does not return anything.
# All output is directed to the original file and the results file.

# The Google Maps API has a limit of 2500 lookups per day.  We'll count up to that.  Exceeding that number causes the
# program to appear to hang.  Don't exceed 2500.

    count = 0

    with open(filename,'r') as f:
        whole_file = f.readlines()
    with open(filename,"w") as remainder:
        with open(outfile,'a') as w:
            writer = csv.writer(w)

# This program doesn't use the csv module.  It expects a simple, 2-field csv file with latitude, longitude numbers.
# So, we read in the file, splitting out the latitude and longitude coordinates.  Strings are converted to float.
            for line in whole_file:
                if count <= 2450:
                    la, lo = line.split(",")
                    lat = float(la)
                    lon = float(lo)
# Try looking up the coordinates.  Any number of errors can happen here.  If there is an error looking up the
# coordinates, the coordinates are output to the outfile, and the next is tried.
                    try:
                        results = Geocoder.reverse_geocode(lat, lon)
                        wr = [lat, lon, results.country, results.state,results.county,results.city, results.postal_code, results.street_number, results.route]
                        writer.writerow(wr)
                        print(count + " - " + wr)
                        count += 1
                    except:
                        remainder.write(line)
                        count += 1
# Once we pass count lookups, we need to cleanup by writing the coordinates that weren't looked up back to the original
# file.
                else:
                    remainder.write(line)
                    count += 1

    print count
    return()

if __name__ == "__main__":

# Initialize variables - These can be changed by the user

    filename = "/Users/Bob/Desktop/Motorcycle Trips/latest.csv"
    outfile  = "/Users/Bob/Desktop/Motorcycle Trips/complete_trip_data.csv"

# Initialize variables - These can be changed by the user

# Initialized variables - These should not be changed by the user

    rows = []
    row  = []

# Initialize variables - These should not be changed by the user

    reverse_geo_lookup(filename, outfile)