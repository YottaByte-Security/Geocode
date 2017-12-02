def make_geo_dictionary (geofile_name):

# This function builds a dictionary from geofile_name.  Two formats are given.  More can be added by changing field_names.
# The OBJECTID, lat, lon, street, zip, neighborhood, city, state, country format is Esri's format.
# The lat, lon, country, state, county, city, zip, s_number, street comes from latlonlookup.py via Google Maps.

    with open(geofile_name,"r") as geofile_handle:
        geofile = geofile_handle.readlines()

        g = []
        g_dict={}
#        field_names = ['lat', 'lon', 'country', 'state', 'county', 'city','zip', 's_number', 'street']
        field_names = ['OBJECTID','lat','lon','street','zip','neighborhood','city','state','country']
        for row in geofile:
            r = row.split(',')
            g.append(dict(zip(field_names, r)))

    return g


def search_geo(result, search_field, search_object, dct_2b_searched):

# Search the dictionary for search_object in the field specified by search_field.  Return results.
# If coordinates are to be returned, answer hold (lat,lon) and t becomes a list of all longitudes
# and s becomes a list of all longitudes.
# Likewise, if the requested output is both city and state 'city-state', a list of
# [(city, state), (city, state)] is returned.

    if result == 'coordinates':
        for row in g:
            if (row[search_field] == search_object):
                answer = (row['lat'], row['lon'])
#        answer = (((row['lat'], row['lon']) for row in g if row[search_field] == search_object))
    elif result == 'city-state':
        answer = (((row['city'], row['state']) for row in g if row[search_field] == search_object))
    else:
        answer = ((row[result] for row in g if row[search_field] == search_object))
    return answer

if __name__ == "__main__":

# Initialize some variables - Change these as needed
    geofile_name = "/Users/Bob/Desktop/Motorcycle Trips/geocoded.d/g.csv"
    result = 'coordinates'
    search_field = 'country'
    search_object = 'USA\r\n'
# Initialize some variables - Change these as needed

# Initialize other variables - Do not change these
    answer = []
# Initialize some variables - Do not change these

# Make a dictionary for the data
    g = make_geo_dictionary(geofile_name)

# Search the dictionary

    answer = search_geo(result, search_field, search_object, g)

# Write the results to standard out

    for row in answer:
        print row