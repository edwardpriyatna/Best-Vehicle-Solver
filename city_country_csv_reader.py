import csv
from locations import City, Country, test_example_countries_and_cities

def create_cities_countries_from_CSV(path_to_csv: str) -> None:
    """
    Reads a CSV file given its path and creates instances of City and Country for each line.
    """
    with open(path_to_csv, 'r', encoding='utf-8') as fileref:
        csv_reader= csv.reader(fileref)
        list_of_column_names = []
        for header_row in csv_reader:
            list_of_column_names.append(header_row)
            break
        list_of_column_names=sum(list_of_column_names, [])

        city_ascii_index = list_of_column_names.index('city_ascii')
        lat_index = list_of_column_names.index('lat')
        lng_index = list_of_column_names.index('lng')
        country_index = list_of_column_names.index('country')
        iso3_index = list_of_column_names.index('iso3')
        capital_index = list_of_column_names.index('capital')
        id_index = list_of_column_names.index('id')

        for row in csv_reader:
            country_name = row[country_index]
            country_iso3 = row[iso3_index]

            if country_name in Country.countries.keys():
                pass
            else:
                new_country = Country(country_name, country_iso3)
                Country.countries[country_name] = new_country

            city_name = row[city_ascii_index]
            city_lat = row[lat_index]
            city_lng = row[lng_index]
            city_capital = row[capital_index]
            city_id = row[id_index]

            new_city = City(city_name, city_lat, city_lng, country_name, city_capital, city_id)
            City.cities[city_id] = new_city

if __name__ == "__main__":
    create_cities_countries_from_CSV("worldcities_truncated.csv")
    australia = Country.countries['Australia']
    print(australia.get_cities())
