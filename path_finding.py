import city_country_csv_reader
from locations import City, Country
from trip import Trip
from vehicles import Vehicle, create_example_vehicles
import math
import networkx as nx
import time

def find_shortest_path(vehicle: Vehicle, from_city: City, to_city: City) -> Trip:

    """
    Returns a shortest path between two cities for a given vehicle, or None if there is no path.
    A shortest path is one that has the smallest travel time for the given Vehicle. This is not about distance.
    Write a function find_shortest_path that returns a shortest path as a Trip from one City to another, for a given Vehicle.
    """
    # creating a graph with city object as nodes
    graph=nx.Graph()
    graph.add_node(from_city)
    graph.add_node(to_city)

    for departure in City.cities.values():  #creating graph where every city is connected to every other city
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

        return trip

    except nx.NetworkXNoPath: #when there is no path return None
        return None

if __name__ == "__main__":
    city_country_csv_reader.create_cities_countries_from_CSV("worldcities_truncated.csv")

    vehicles = create_example_vehicles()

    australia = Country.countries["Australia"]
    melbourne = australia.get_city("Melbourne")
    japan = Country.countries["Japan"]
    tokyo = japan.get_city("Tokyo")

    for vehicle in vehicles:
        print("The shortest path for {} from {} to {} is {}".format(vehicle, melbourne, tokyo, find_shortest_path(vehicle, melbourne, tokyo)))
