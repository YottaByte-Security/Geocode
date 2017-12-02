# This program reads the file latest.csv, a csv file of lattitude/longitude coordinates
# and compares that list to a file complete_trip_data.csv.  Complete_trip_data.csv
# contains the reverse geocoded data.  The output is a file newfile.csv that contains
# all the coordinates that have not been reverse_geocoded.


def return_coordinates(file_name):

# Returns a set ((lat, lon), (lat,lon)) of the first two fields of a comma separated values file.  It is expected that
# the first two fields will be lattitude and longitude.  Lattitude and Longigude will be floating point numbers.  If
# there is an error, the file name and line number in the file that caused the problem is printed to stdout.  This is
# useful if the problem occurs in a file of thousands of lat/lon coordinates.

    import csv
    c_data=set()
    with open(file_name,"r") as file:
        c_file = csv.reader(file)
        for index, row in enumerate(c_file):
            try:
                c_data.add((float(row[0]),float(row[1])))
            except:
                print("problem in file: ", file, "  on line: ", index)
                exit()
    return(c_data)

def write_coordinates(file, data):

# Writes a file of coordinates from data which is a set of lattitude and longitude coordinates ((lat, lon), (lat, lon))

    with open(file,"w") as output:
        for row in data:
                output_string=(str(row[0])+","+str(row[1])+"\n")
                output.write(output_string)
    return()

if __name__ == "__main__":
    source ="/Users/Bob/Desktop/Motorcycle Trips/file.csv"
    master = "/Users/Bob/Desktop/Motorcycle Trips/20171022-uniq.csv"
    new_file = "/Users/Bob/Desktop/Motorcycle Trips/newfile.csv"
    source_coordinates = set()
    master_coordinates = set()


    source_coordinates = return_coordinates(source)
    master_coordinates = return_coordinates(master)

    difference = master_coordinates - source_coordinates

    write_coordinates(new_file, difference)
