'''
Importing the related functions and classes into the
'''
from city_country_csv_reader import create_cities_countries_from_CSV
from locations import City, Country, create_example_countries_and_cities
from trip import Trip
from vehicles import Vehicle, CrappyCrepeCar, DiplomacyDonutDinghy, TeleportingTarteTrolley, create_example_vehicles
from new_path_finding import find_shortest_path
from map_plotting import plot_trip
import time
import math

def create_vehicle_input_checker():
    '''
    Prompts the user for an input to choose a fleet of vehicle to be created.
    '''
    while True:
        print('Please Choose A Fleet to Create!')
        print('Press 1 To Create A Fleet of Vehicles From The Examples.')
        print('Press 2 To Create Your Own Fleet of Vehicles.\n')
        try:
            create_vehicle_input = int(input('Input Vehicle Option: ')) 
            if create_vehicle_input < 1 or create_vehicle_input > 2: #Check if users' input is 1 or 2
                print('\nWrong Input! Please Input 1 or 2.\n')
                continue
            return create_vehicle_input
        except ValueError: 
            print('\nWrong Input! Please Input 1 or 2.\n')  # if invalid index number inputted
            continue

def create_vehicle_type_input_checker():
    '''
    Prompts the user for an input to choose a vehicle type.
    '''     
    while True:
        print('\nPlease Choose One of The Vehicles Below!')
        print('Press 1 to Create CrappyCrepeCar.')
        print('Press 2 to Create DiplomacyDonutDinghy.')
        print('Press 3 to Create TeleportingTarteTrolley.\n')
        try:
            create_vehicle_type_input = int(input('Input Vehicle Type: '))
            if create_vehicle_type_input < 1 or create_vehicle_type_input > 3: #Check if users' input is 1 or 2 or 3
                print('\nWrong Input! Please Input a Number between 1 and 3.')
                continue
            return create_vehicle_type_input
        except ValueError: 
            print('\nWrong Input! Please Input a Number between 1 and 3.')  # if invalid index number inputted
            continue

def int_input_checker(atribute):
    '''
    Prompts the user for a value for the attributes.
    '''
    while True:
        try:
            atribute_value = int(input('\nInput ' + atribute + ': '))
            return atribute_value
        except ValueError: 
            print('\nInvalid Input!')  # if invalid index number inputted
            continue

def create_vehicle_fleet():
    '''
    Creates the vehicle fleet which is a list.
    If user input 1: example vehicle is used.
    If user input 2: users will create own vehicle by
    giving values to the attributes of the vehicle.
    '''
    create_vehicle_input = create_vehicle_input_checker()
    vehicles_fleet = []
    if create_vehicle_input == 1:
        return [CrappyCrepeCar(200), DiplomacyDonutDinghy(100, 500), TeleportingTarteTrolley(3, 2000)]
    elif create_vehicle_input == 2:
        while True:
            create_vehicle_type_input = create_vehicle_type_input_checker()
            if create_vehicle_type_input == 1:
                CCC_speed = int_input_checker('CCC Speed (km/h)')
                CCC = CrappyCrepeCar(CCC_speed)
                vehicles_fleet.append(CCC)
            elif create_vehicle_type_input == 2:
                DDD_in_country_speed = int_input_checker('DDD in Country Speed (km/h)')
                DDD_between_primary_speed = int_input_checker('DDD between Primary Speed (km/h)')
                DDD = DiplomacyDonutDinghy(DDD_in_country_speed, DDD_between_primary_speed)
                vehicles_fleet.append(DDD)
            else:
                TTT_travel_time = int_input_checker('TTT Travel Time (h)')
                TTT_max_distance = int_input_checker('TTT Max Distance (km)')
                TTT = TeleportingTarteTrolley(TTT_travel_time, TTT_max_distance)
                vehicles_fleet.append(TTT)
            stop_loop = input('\nPress 0 to Stop and Any Other Button To Continue: ') #Allows users to add another vehicle or stop.
            if stop_loop == '0':
                return vehicles_fleet
            else:
                continue
    else:
        return None

def city_input_checker(dep_or_arr):
    '''
    Prompts the user for an input of departure and arrival city.
    If the city does not exist it prompts the user to input again.
    '''
    while True:
        city_input = input('\nInput ' + dep_or_arr + ' City (Do not put any extra space!): ')
        for key in City.cities:
            if city_input == City.cities[key].name:
                print(City.cities[key])
                return City.cities[key]

def find_shortest_path_for_each_vehicle(vehicle_list):
    '''
    Show the trip the users has inputted.
    Find shortest path between 2 cities.
    Plot the path into the map.
    shows and returns fastest vehicle for trip.
    '''
    departure_city = city_input_checker('Departure')
    arrival_city = city_input_checker('Arrival')
    print('\nThe trip is from {} to {}.'.format(departure_city, arrival_city))
    total_travel_time_list=[]
    for vehicle in vehicle_list:  # how to know travel time
        find_shortest_path_return_list = find_shortest_path(vehicle, departure_city, arrival_city)

        if find_shortest_path_return_list==math.inf:
            print('There is no path for',vehicle)
            total_travel_time_list.append(math.inf)
        else:
            city_trip = find_shortest_path_return_list[0]
            total_travel_time = find_shortest_path_return_list[1]
            print("\nThe Shortest Path for {} from {} to {} is {}".format(vehicle, departure_city, arrival_city, city_trip) )
            total_travel_time_list.append(total_travel_time)
            plot_trip(city_trip)

    min_travel_time = min(total_travel_time_list)
    min_travel_time_index = total_travel_time_list.index(min_travel_time)
    fastest_vehicle = vehicle_list[min_travel_time_index]
    print('\nThe fastest vehicle is',fastest_vehicle)
    return fastest_vehicle

def use_example_trip(vehicle_list):
    '''
    Create a example of trips
    Returns the fastest vehicle for that trip.
    '''
    australia = Country.countries["Australia"]
    melbourne = australia.get_city("Melbourne")
    canberra = australia.get_city("Canberra")
    japan = Country.countries["Japan"]
    tokyo = japan.get_city("Tokyo")

    ex_trip1=Trip(canberra)
    ex_trip1.add_next_city(tokyo)
    ex_trip2=Trip(melbourne)
    ex_trip2.add_next_city(canberra)
    ex_trip2.add_next_city(tokyo)

    print('\nTrip 1 is',ex_trip1)
    print('Trip 2 is',ex_trip2,"\n")

    chosen_trip_input=chosen_trip_input_checker()

    if chosen_trip_input==1:
        chosen_trip=ex_trip1
    else:
        chosen_trip=ex_trip2

    vehicle, duration = chosen_trip.find_fastest_vehicle(vehicle_list)
    #Progress bar for the trip based on the total time travel for vehicle.
    for i in range(math.ceil(duration)): 
        print('|',end='')
        time.sleep(0.1)
    plot_trip(chosen_trip)
    print("\nThe trip {} will take {} hours with {}.".format(chosen_trip, duration, vehicle))

def chosen_trip_input_checker():
    '''
    Prompts the user for an input to choose an example trip.
    '''
    while True:
        print('Please Choose A Trip!')
        print('Press 1 To Use Example Trip 1.')
        print('Press 2 To Use Example Trip 2.\n')
        try:
            chosen_trip_input = int(input('Input Trip Option: '))
            if chosen_trip_input < 1 or chosen_trip_input > 2: #If inputted value not 1 or 2
                print('\nWrong Input! Please Input 1 or 2.\n')
                continue
            return chosen_trip_input
        except ValueError:
            print('\nWrong Input! Please Input 1 or 2.\n')  # if invalid index number inputted
            continue

def make_custom_trip(vehicle_list):
    '''
    Prompts the user for an input of cities for custom trip.
    Returns the fastest vehicle for that trip.
    '''
    departure_city = city_input_checker('Departure')
    custom_trip =Trip(departure_city)
    while True:
        next_city = city_input_checker('Next')
        custom_trip.add_next_city(next_city)
        stop_con = input('\nPress 0 to Stop and Any Other Button To Continue: ') #Allows users to choose between adding more cities or stop
        if stop_con=='0':
            break
    print("\nThe trip is {}.\n".format(custom_trip))
    vehicle, duration = custom_trip.find_fastest_vehicle(vehicle_list)
    plot_trip(custom_trip)
    print("The trip {} will take {} hours with {}.".format(custom_trip, duration, vehicle))

def main_input_checker():
    '''
    Prompts the user for an input to choose a trip type.
    '''
    while True:
        print('Please Choose A Trip!')
        print('Press 1 To Use Example.')
        print('Press 2 To Create Custom Trip.')
        print('Press 3 To Find Shortest Path.\n')
        try:
            main_input = int(input('Input Trip Option: '))
            if main_input < 1 or main_input > 3:
                print('\nWrong Input! Please Input 1, 2, or 3.\n')#If inputted value not 1 or 2 or 3
                continue
            return main_input
        except ValueError:
            print('\nWrong Input! Please Input 1, 2, or 3.\n') # if invalid index number inputted
            continue

def main():
    '''
    Running the python file.
    '''
    create_cities_countries_from_CSV("worldcities_truncated.csv")
    vehicles_fleet = create_vehicle_fleet()
    print('\nVehicle Fleet is', vehicles_fleet,"\n")
    main_input=main_input_checker()
    if main_input==1:
        use_example_trip(vehicles_fleet)
    elif main_input==2:
        make_custom_trip(vehicles_fleet)
    elif main_input == 3:
        find_shortest_path_for_each_vehicle(vehicles_fleet)

main()
