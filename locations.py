from __future__ import annotations
from enum import Enum
from math import ceil
from geopy.distance import great_circle as GRC


class CapitalType(Enum):
    """
    The different types of capitals (e.g. "primary").
    """
    primary = "primary"
    admin = "admin"
    minor = "minor"
    unspecified = ""

    def __str__(self):
        return self.value


class Country():
    """
    Represents a country.
    """

    countries = {}  # a dict that associates country names to instances.

    # a list filled with country name

    def __init__(self, name, iso3):
        """
        Creates an instance with a country name and a country ISO code with 3 characters.
        """
        self.name = name
        self.iso3 = iso3
        self.country_city = {}  # Each country instance will have a dictionary of cities that belong to that country
        Country.countries[self.name] = self  # for example Australia: object(Australia)

    def add_city(self, city):
        """
        Adds a city to the country.
        Adds city object to the Country's country.city {} dictionary
        """
        self.country_city[city.name] = city  # use city name because look at get cities in example it uses city name
        return self.country_city

    def get_cities(self, capital_types: list[CapitalType] = None):
        """
        Returns a list of cities of this country.

        The argument capital_types can be given to specify a subset of the capital types that must be returned.
        Cities that do not correspond to these capital types are not returned.
        If no argument is given, all cities are returned.
        """
        valid_cities = []
        if capital_types is None:  # Return all cities from respective country's city dictionary
            for key in self.country_city:
                valid_cities.append(self.country_city[key])
            return valid_cities
        else:
            for key in self.country_city:
                if self.country_city[key].capital_type in capital_types:
                    valid_cities.append(self.country_city[key])
            return valid_cities


    def get_city(self, city_name: str):
        """
        Returns a city of the given name in this country.
        Returns None if there is no city by this name.
        If there are multiple cities of the same name, returns an arbitrary one.
        """

        # For every city in the country city dictionary, if the city
        for key in self.country_city:
            if self.country_city[key].name == city_name:
                return self.country_city[key]
        return None

    def __str__(self) -> str:
        """
        Returns the name of the country.
        """
        return self.name

    def __repr__(self):
        return self.__str__()


class City():
    """
    Represents a city.
    """

    cities = {}  # a dict that associates city IDs to instances.

    # a dict filled with city IDs

    def __init__(self, name: str, latitude: str, longitude: str, country: str, capital_type: str, city_id: str) -> None:
        """
        Initialises a city with the given data.
        """
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.country = country

        self.capital_type = capital_type
        self.make_type_enum()

        self.city_id = city_id
        City.cities[self.city_id] = self  #Store this city in the cities dictionary

        # Everytime we initiate a new instance of a city, we check the country it belongs to and add it to that country's city dictionary
        for key in Country.countries:
            if key == country:
                Country.countries[key].add_city(self)

    def distance(self, other_city):
        """
        Returns the distance in kilometers between two cities using the great circle method,
        rounded up to an integer.
        """
        coord1 = (self.latitude, self.longitude)
        coord2 = (other_city.latitude, other_city.longitude)
        return ceil(GRC(coord1,coord2).km)

    def get_iso3_from_country(self, country):
        # we can call Country.countries
        for key in Country.countries:
            if key == country:
                return Country.countries[key].iso3
        return None

    def make_type_enum(self):
        if self.capital_type == 'primary':
            self.capital_type = CapitalType.primary
        elif self.capital_type == 'admin':
            self.capital_type = CapitalType.admin
        else:
            self.capital_type = CapitalType.minor

    def get_type(self):
        return self.capital_type

    def __str__(self):
        string = self.name + ' (' + self.get_iso3_from_country(self.country) + ')'
        return string

    def __repr__(self):
        return self.__str__()


def create_example_countries_and_cities() -> None:
    """
    Creates a few Countries and Cities for testing purposes.
    """
    australia = Country("Australia", "AUS")
    melbourne = City("Melbourne", "-37.8136", "144.9631", "Australia", "admin", "1036533631")
    canberra = City("Canberra", "-35.2931", "149.1269", "Australia", "primary", "1036142029")
    sydney = City("Sydney", "-33.865", "151.2094", "Australia", "admin", "1036074917")

    japan = Country ("Japan", "JPN")
    tokyo = City("Tokyo", "35.6839", "139.7744", "Japan", "primary", "1392685764")


def test_example_countries_and_cities() -> None:
    """
    Assuming the correct cities and countries have been created, runs a small test.
    """
    australia = Country.countries['Australia']
    canberra =  australia.get_city("Canberra")
    melbourne = australia.get_city("Melbourne")
    sydney = australia.get_city("Sydney")
    
    print("The distance between {} and {} is {}km".format(melbourne, sydney, melbourne.distance(sydney)))

    for city in australia.get_cities([CapitalType.admin, CapitalType.primary]):
        print("{} is a {} capital of {}".format(city, city.capital_type, city.country))


if __name__ == "__main__":
    create_example_countries_and_cities()
    test_example_countries_and_cities()
