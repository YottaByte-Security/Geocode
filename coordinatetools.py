# maptools.py

import csv, urllib, json, time
from math import sin, cos, sqrt, atan2


def distance(l1, lo1, l2, lo2, r = 3961):

# Calculates the distance between two map coordinates

# The formula comes from Bob Chamberlain (rgc@jpl.nasa.gov) of Caltech and
# NASA's Jet Propulsion Laboratory as described on the U.S. Census Bureau Web site.

# The function takes as arguments either floating point numbers or strings and an optional radius of the earth that
# defaults to 3961 miles.  Use r = 6373 for Kilometers.

    lat1 = float(l1)
    lat2 = float(l2)
    lon1 = float(lo1)
    lon2 = float(lo2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = (sin(dlat/2))**2 + cos(lat2) * cos(lat1) * (sin(dlon/2))**2
    c = 2 * atan2( sqrt(a), sqrt(1-a) )
    d = r * c
    return d

# -------------------------------------------------------------------------------------------------------------------

def uniq_coord_list(coordinate_list, precision=7):

# This function uniques a list of lat/lon coordinates and makes sure that all points have the same precision so that
# 12.1234 is treated the same as 12.1234000

# Taken from http://gis.stackexchange.com/questions/8650/how-to-measure-the-accuracy-of-latitude-and-longitude

# 1 is worth up to 11.1 km: it can distinguish the position of one large city from a neighboring large city.
# 2 is worth up to 1.1 km: it can separate one village from the next.
# 3 is worth up to 110 m: it can identify a large agricultural field or institutional campus.
# 4 is worth up to 11 m: it can identify a parcel of land. It is comparable to the typical accuracy of an uncorrected GPS
# unit with no interference.

# 5 is worth up to 1.1 m: it distinguish trees from each other. Accuracy to this level with commercial GPS units can only
#  be achieved with differential correction.

# 6 is worth up to 0.11 m: you can use this for laying out structures in detail, for designing landscapes, building
#  roads. It should be more than good enough for tracking movements of glaciers and rivers. This can be achieved by
#  taking painstaking measures with GPS, such as differentially corrected GPS.

# 7 is worth up to 11 mm: this is good for much surveying and is near the limit of what GPS-based techniques can achieve.
# 8 is worth up to 1.1 mm: this is good for charting motions of tectonic plates and movements of volcanoes. Permanent,
#  corrected, constantly-running GPS base stations might be able to achieve this level of accuracy.

# 9 is worth up to 110 microns: we are getting into the range of microscopy. For almost any conceivable application with
#  earth positions, this is overkill and will be more precise than the accuracy of any surveying device.

# 10 or more decimal places indicates a computer or calculator was used and that no attention was paid to the fact that
# the extra decimals are useless. Be careful, because unless you are the one reading these numbers off the device, this
# can indicate low quality processing!

# First deal with the representation issues with floating point numbers by moving the decimal point by the
# precision desired

    normalized = []
    sorted_normalized = []
    for item in coordinate_list:
        normalized.append((int(float(item[0])*10**precision), int(float(item[1])*10**precision)))

#  Next, sort the list of coordinates
    sorted_normalized = sorted(normalized)

# Uniq the list

    for count, item in enumerate(sorted_normalized):
        try:
            if sorted_normalized[count]== sorted_normalized[count+1]:
                del(sorted_normalized[count])
        except IndexError:
            pass

# return the uniq list as a list of floating point numbers
    uniq_list = []
    for item in sorted_normalized:
        uniq_list.append((str(float(item[0])/ 10**precision), str(float(item[1])/10**precision )))

    return uniq_list

def getKey(item):
    return item[2]

def get_street_info(point_data):

    '''

    This program takes as input a a list of dictionaries with indices of Lattitude and Longitude, calls the Google
    Maps API, gets information about that coordinate, writes the result to a list of dictionary items and finally,
    writes the information back out to another csv file.  The best way to call this program is interacively so the
    user can further manipulate the data structure.

    Note 1:  The Googlemaps API allows a maximum of 2500 connections per day and a maximum of 10 connections per second.
    The option to pay for more, up to 100,000 per day, is available.  That may solve a large file problem; but, users with
    bigger files will need to break their files into smaller chunks.  As written now, the program will work through a very
    large file for as long as it takes.  Users may want to break their files up into smaller chunks for manual operation.

    Note 2:  The results are maintained in a data structure and written at the same time.  The user can run python in
    interactive mode andvwork with the data.  A large enough file will exceed memory requirements.


    Feature enhancement 1: Future versions may introduce a safety to avoid exceeding available memory.

    Feature enhancement 2:  Allow the user to optionally configure the # of connections allowed per day and the # of
    connections per second to accomodate users that are paying for more and/or accomodate any change in Google's API
    limitations.


    '''





# Takes as input a dictionary with indices of Lattitude and Longitude.
# Access the google API and read the resulting json data for country, state, city, county, route.  Return the dictionary
# given as input with those additional indices.
# Note:  Google API allows 2500 attempts per day and only 10 attempts per second.  Try/Except statements address
# that restriction.

    try:
        a = urllib.urlopen('https://maps.googleapis.com/maps/api/geocode/json?latlng=' + point_data['Lattitude'] + ", " + point_data['Longitude'])
    except:
        time.sleep(1)
        print "Waiting 1 second to meet Google API restrictions."
        try:
            a = urllib.urlopen('https://maps.googleapis.com/maps/api/geocode/json?latlng=' + point_data['Lattitude'] + ", " + point_data['Longitude'])
        except:
            print "attempting to wait 1 day to meet Google API restrictions."
            time.sleep(86400)
            try:
                a = urllib.urlopen('https://maps.googleapis.com/maps/api/geocode/json?latlng=' + point_data['Lattitude'] + ", " + point_data['Longitude'])
            except:
                raise("unable to connect with Google for lat/lon info.  Tried 1 second and 1 day wait.")
    c = json.load(a)

                                                        # Create readable keys for the dictionary

    # Iterate through all 7 parts of the data returned from the API, Zip them with the keys and add to the dictionary
    # we created and cherry pick the results we want from the API return

    for x in c['results']:
        if str(x['address_components'][0]['types'][0]) == 'country':
            point_data['country'] = x['address_components'][0]['long_name']
        elif str(x['address_components'][0]['types'][0]) == 'administrative_area_level_1':
            point_data['state'] =  x['address_components'][0]['long_name']
        elif str(x['address_components'][0]['types'][0]) == 'administrative_area_level_2':
            point_data['county'] = x['address_components'][0]['long_name']
        elif str(x['address_components'][0]['types'][0]) == 'locality':
            point_data['city'] =  x['address_components'][0]['long_name']
        elif str(x['address_components'][0]['types'][0]) == 'route':
            point_data['route'] =  x['address_components'][0]['long_name']
        elif str(x['address_components'][0]['types'][0]) == 'postal_code':
            point_data['zip'] = x['address_components'][0]['long_name']
        else:
            pass
    #  Assign 'Unknown' to any missing entries
    if 'country' in point_data:
        pass
    else:
        point_data['country'] = 'UNKNOWN'
    if 'state' in point_data:
        pass
    else:
        point_data['state'] = 'UNKNOWN'
    if 'county' in point_data:
        pass
    else:
        point_data['county'] = 'UNKNOWN'
    if 'city' in point_data:
        pass
    else:
        point_data['city'] = 'UNKNOWN'
    if 'route' in point_data:
        pass
    else:
        point_data['route'] = 'UNKNOWN'
    if 'zip' in point_data:
        pass
    else:
        point_data['zip'] = 'UNKNOWN'

    return point_data


# ---------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    input_file = "./input_file.csv"
    output_file = "./output_file.csv"
    uniq_list = []
    coordinate_list = []
    with open(input_file,"r") as ih:
        i = csv.reader(ih)
        for item in i:
            coordinate_list.append(item)


# ---------------------------------------------------------------------------------------------------------------------
#                               Examples uses
#

# Example - read a file of coordinates into a list, unique the list and write it back out.
    uniq_list = uniq_coord_list(coordinate_list, 7)

# Example - read a file of coordinates into a list of dictionary items, then get street info
# LOD_coordinate_info = []                                        # Create the list to return to hold dictionaries
# point_data = {}                                                 # Create the dictionary
# with open(input_file,"r") as file_handle:                       # Open the csv file with coordinates
#   with open(output_file, "a") as fh:                          # Open the csv file to write to
#    o = csv.writer(fh)
#      f = csv.reader(file_handle)

#      header = ("Lattitude", "Longitude")                      # CSV file expected to be in this format ****
#      item = 'start'
#      while True:                                           # While there's still data in the input file
#        try:
#          item = next(f)
#          except StopIteration:                       # Python processes next different than for and the
#            exit()                                  # StopIteration has to be handled specifically
#          point_data = dict(zip(header, item))      # Begin by creating a dictionary item with lat/lon
#          pd = get_street_info(point_data)
#          LOD_coordinate_info.append(pd)            # update our dictionary
#          row = [pd['Lattitude'], pd['Longitude'], pd['route'], pd['city'], pd['county'], pd['state'], pd['country'], pd['zip']]
#          print row
#          o.writerow(row)

# Optionally -write the uniq coordinates out to a file

    with open(output_file, "w") as oh:
        for item in uniq_list:
            row = item[0] + ", " + item[1] + "\n"
            oh.write(row)