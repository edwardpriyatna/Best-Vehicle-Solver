import city_country_csv_reader
from locations import create_example_countries_and_cities
from trip import Trip, create_example_trips
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np  

def plot_trip(trip: Trip, projection='robin', line_width=2, colour='r') -> None: #robin is to draw the entire earth map
    """
    Plots a trip on a map and writes it to a file.
    Ensures a size of at least 50 degrees in each direction.
    Ensures the cities are not on the edge of the map by padding by 5 degrees.
    The name of the file is map_city1_city2_city3_..._cityX.png.
    """
    if trip==None:
        return None

    for i in range(len(trip.cities_to_go)):
        x_coor = []
        y_coor = []

        for cities in trip.cities_to_go:
            longitude, latitude = cities.longitude, cities.latitude

            x_coor.append(float(longitude))
            y_coor.append(float(latitude))


    fig = plt.figure(figsize=(12,10))
    m = Basemap(projection='mill', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180,resolution='c')
    m.drawcoastlines()
    #m.drawcountries()
    m.drawparallels(np.arange(-90,90,10),labels=[True,False,False,False])
    m.drawmeridians(np.arange(-180,180,30),labels=[0,0,0,1])
    xpt, ypt = m(x_coor, y_coor)
    m.plot(xpt, ypt, "ro", markersize=4,linewidth=5)   # Plotting the cities
    m.plot(xpt,ypt)  # Plotting the connecting line 

    file_name = "Map_" + str(trip.cities_to_go[0].name)
    for cities in trip.cities_to_go[1:]:
        file_name += "_" + cities.name
    file_name = file_name + ".png"

    plt.savefig(file_name)
    plt.imread(file_name)
    plt.clf()

if __name__ == "__main__":
    #city_country_csv_reader.create_cities_countries_from_CSV("worldcities_truncated.csv")
    
    trips = create_example_trips()

    for trip in trips:
        plot_trip(trip)
