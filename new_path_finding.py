import city_country_csv_reader
from locations import City, Country
from trip import Trip
from vehicles import Vehicle, create_example_vehicles
import math
import networkx as nx
import time

def find_shortest_path(vehicle: Vehicle, from_city: City, to_city: City) -> Trip:

    """
    Returns a list containing shortest path between two cities for a given vehicle, or None if there is no path. And shortest total travel time.
    A shortest path is one that has the smallest travel time for the given Vehicle. This is not about distance.
    Write a function find_shortest_path that returns a shortest path as a Trip from one City to another, for a given Vehicle.
    """
    graph=nx.Graph()
    graph.add_node(from_city)
    graph.add_node(to_city)

    for departure in City.cities.values(): #creating a graph with all cities connected to each other
        for arrival in City.cities.values():
            travel_time_each_part = vehicle.compute_travel_time(departure, arrival)
            if travel_time_each_part != math.inf: #only add node if the city can be traveled and also connect the node
                graph.add_node(departure)
                graph.add_node(arrival)
                graph.add_edge(departure,arrival,weight=travel_time_each_part)

    try:
        trip=Trip(from_city)
        shortest_path=nx.shortest_path(graph,source=from_city, target=to_city)
        for i in range(1,len(shortest_path)): #adding cities in shortest path to trip
            trip.add_next_city(shortest_path[i])

        shortest_total_travel_time=0
        for j in range( len(shortest_path)-1 ): #counting the shortest total travel time, we put len-1 because if it was the last city it can't compute travel time
            departure_city=shortest_path[j]
            arrival_city=shortest_path[j+1]
            shortest_total_travel_time += vehicle.compute_travel_time(departure_city,arrival_city)
        print('\nShortest total travel time is {} hours.'.format(shortest_total_travel_time))

        for j in range( math.ceil(shortest_total_travel_time) ): #printing progress bar
            print('|',end='')
            time.sleep(0.1)

        return [trip,shortest_total_travel_time]

    except nx.NetworkXNoPath: #return math.inf when there is no path
        return math.inf

if __name__ == "__main__":
    city_country_csv_reader.create_cities_countries_from_CSV("worldcities_truncated.csv")

    vehicles = create_example_vehicles()

    australia = Country.countries["Australia"]
    melbourne = australia.get_city("Melbourne")
    japan = Country.countries["Japan"]
    tokyo = japan.get_city("Tokyo")

    for vehicle in vehicles:
        print("The shortest path for {} from {} to {} is {}".format(vehicle, melbourne, tokyo, find_shortest_path(vehicle, melbourne, tokyo)))
