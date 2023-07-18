import math
from abc import ABC, abstractmethod

from locations import CapitalType, City, Country, create_example_countries_and_cities

class Vehicle(ABC):
    """
    A Vehicle defined by a mode of transportation, which results in a specific duration.
    """

    def __init__(self, speed: int) -> None:
        """
        Creates a vechile with a given speed in km/h.
        """
        self.speed=speed
    

    @abstractmethod
    def compute_travel_time(self, departure: City, arrival: City) -> float:
        """
        Returns the travel duration of a direct trip from one city
        to another, in hours, rounded up to an integer.
        Returns math.inf if the travel is not possible.
        """
        distance_between = departure.distance(arrival)
        travel_time = distance_between/self.speed
        travel_time=math.ceil(travel_time)
        travel_time = int(travel_time)
        return travel_time
        
    @abstractmethod
    def __str__(self) -> str:
        """
        Returns the class name and the parameters of the vehicle in parentheses.
        """
        return self.name


class CrappyCrepeCar(Vehicle):
    """
    A type of vehicle that:
        - Can go from any city to any other at a given speed.
    """

    def __init__(self, speed: int) -> None:
        """
        Creates a CrappyCrepeCar with a given speed in km/h.
        """
        self.speed=speed

    
    def compute_travel_time(self, departure: City, arrival: City) -> float:
        """
        Returns the travel duration of a direct trip from one city
        to another, in hours, rounded up to an integer.
        """
        distance_between = departure.distance(arrival)
        travel_time = distance_between / self.speed
        travel_time = math.ceil(travel_time)
        travel_time = int(travel_time)
        return travel_time

    def __str__(self) -> str:
        """
        Returns the class name and the parameters of the vehicle in parentheses.
        For example "CrappyCrepeCar (100 km/h)"
        """
        return "CrappyCrepeCar (" + str(self.speed) + ' km/h)'

    def __repr__(self):
        return self.__str__()

class DiplomacyDonutDinghy(Vehicle):
    """
    A type of vehicle that:
        - Can travel between any two cities in the same country.
        - Can travel between two cities in different countries only if they are both "primary" capitals.
        - Has different speed for the two cases.
    """

    def __init__(self, in_country_speed: int, between_primary_speed: int) -> None:
        """
        Creates a DiplomacyDonutDinghy with two given speeds in km/h:
            - one speed for two cities in the same country.
            - one speed between two primary cities.
        """
        self.in_country_speed=in_country_speed
        self.between_primary_speed=between_primary_speed

    def compute_travel_time(self, departure: City, arrival: City) -> float:
        """
        Returns the travel duration of a direct trip from one city
        to another, in hours, rounded up to an integer.
        Returns math.inf if the travel is not possible.
        """
        distance_between=departure.distance(arrival)
        if departure.country==arrival.country:
            travel_time = distance_between/self.in_country_speed
            travel_time = math.ceil(travel_time)
            travel_time = int(travel_time)
            return travel_time

        elif departure.capital_type==CapitalType.primary and arrival.capital_type==CapitalType.primary and departure.country!=arrival.country:
            travel_time = distance_between / self.between_primary_speed
            travel_time = math.ceil(travel_time)
            travel_time = int(travel_time)
            return travel_time

        else:
            return math.inf

    def __str__(self) -> str:
        """
        Returns the class name and the parameters of the vehicle in parentheses.
        For example "DiplomacyDonutDinghy (100 km/h | 200 km/h)"
        """
        return "DiplomacyDonutDinghy (" + str(self.in_country_speed) + ' km/h | '+ str(self.between_primary_speed) + ' km/h)'

    def __repr__(self):
        return self.__str__()

class TeleportingTarteTrolley(Vehicle):
    """
    A type of vehicle that:
        - Can travel between any two cities if the distance is less than a given maximum distance.
        - Travels in fixed time between two cities within the maximum distance.
    """

    def __init__(self, travel_time:int, max_distance: int) -> None:
        """
        Creates a TarteTruck with a distance limit in km.
        """
        self.travel_time=travel_time
        self.max_distance=max_distance

    def compute_travel_time(self, departure: City, arrival: City) -> float:
        """
        Returns the travel duration of a direct trip from one city
        to another, in hours, rounded up to an integer.
        Returns math.inf if the travel is not possible.
        """
        distance_between=departure.distance(arrival)
        max_distance=float(self.max_distance)
        if distance_between<max_distance:
            return self.travel_time
        else:
            return math.inf

    def __str__(self) -> str:
        """
        Returns the class name and the parameters of the vehicle in parentheses.
        For example "TeleportingTarteTrolley (5 h | 1000 km)"
        """
        return "TeleportingTarteTrolley (" + str(self.travel_time) + ' h | ' + str(self.max_distance) + ' km)'

    def __repr__(self):
        return self.__str__()


def create_example_vehicles() -> list[Vehicle]:
    """
    Creates 3 examples of vehicles.
    """
    return [CrappyCrepeCar(200), DiplomacyDonutDinghy(100, 500), TeleportingTarteTrolley(3, 2000)]
