# -*- coding: utf-8 -*-
"""
Program: consume_api_with_df_wrapper.py
Created on 10/27/2020
@author: adhamlin

This program pulls data from an api endpoint, https://restcountries.eu/
List all: https://restcountries.eu/rest/v2/all
"""
# imports
import urllib.request
import urllib.parse
from urllib.error import HTTPError
from urllib.error import URLError
import json
import pandas as pd

# base url to append with argument parameter
serviceurl = 'https://restcountries.eu/rest/v2/name/'


def get_country_data(country):
    """
    Function to get data about a country from the https://restcountries.eu API
    :param country: String input of a country name.
    :return: json formatted data on a country.
    """
    country_name = str(country)  # already a string via input but needed if input supplied via other source
    url = serviceurl + country_name
    try:
        uh = urllib.request.urlopen(url)
    except HTTPError as e:
        print("Sorry! Nothing to retrieve on {}.".format(country_name), e)
        return None
    except URLError as e:
        print("Failed to reach a server.")
        print("Reason: ", e.reason)
        return None
    else:
        read_data = uh.read().decode()
        print("Retrieved data on {}. Total of {} characters read.".format(country_name, len(read_data)))
        return read_data


# base data to pass to the function example: 'Switzerland'
country_user_input = input("Enter a country name: ")  # user input of country
data = get_country_data(country_user_input)
print()  # space in console output

try:
    # check json data
    json_data = json.loads(data)
    # load one element to check
    one_element = json_data[0]
    print("Type:\n", type(one_element))
    print()  # space in console output
    # output one_element keys
    one_element_keys = one_element.keys()
    print("Single element keys:\n", one_element_keys)
    print()  # space in console output
    # one_element = json_data[0] pretty output
    print("=== Key/Value pairs of the json object ===")
    for k, v in one_element.items():
        print(f"{k}: {v}")
    print()  # space in console output
    # extract languages spoke in the provided country
    print("Languages spoken in", country_user_input)
    for lang in one_element['languages']:
        print(lang['name'])

except TypeError as te:
    print("Nothing was gathered so the JSON object is empty or a NoneType. ERROR:", te)

print()  # space in console output


# wrapper function for pandas dataframe of multiple countries
def build_country_db(country_lst):
    """
    Takes in a list of country names.
    :param country_lst: a list of country names
    :return: a dataframe with specific information on those countries
    """
    # Define an dictionary keys with empty lists pandas dataframe
    country_dict = {'Country': [], 'Capital': [], 'Region': [], 'Sub-region': [], 'Population': [],
                    'Latitude': [], 'Longitude': [], 'Area': [], 'Gini': [], 'Timezones': [],
                    'Currencies': [], 'Languages': []}

    for c in country_lst:
        country_data = get_country_data(c)  # extract data for each country
        if country_data is not None:
            json_obj_data = json.loads(country_data)
            one_element_json_obj_data = json_obj_data[0]
            # extract data from json and append to empty lists in the dictionary
            country_dict['Country'].append(one_element_json_obj_data['name'])
            country_dict['Capital'].append(one_element_json_obj_data['capital'])
            country_dict['Region'].append(one_element_json_obj_data['region'])
            country_dict['Sub-region'].append(one_element_json_obj_data['subregion'])
            country_dict['Population'].append(one_element_json_obj_data['population'])
            country_dict['Latitude'].append(one_element_json_obj_data['latlng'][0])
            country_dict['Longitude'].append(one_element_json_obj_data['latlng'][1])
            country_dict['Area'].append(one_element_json_obj_data['area'])
            country_dict['Gini'].append(one_element_json_obj_data['gini'])

            # handle possibility of multiple timezones as a list
            if len(one_element_json_obj_data['timezones']) > 1:
                country_dict['Timezones'].append(','.join(one_element_json_obj_data['timezones']))
            else:
                country_dict['Timezones'].append(one_element_json_obj_data['timezones'][0])

            # handle possibility of multiple currencies as dictionaries
            if len(one_element_json_obj_data['currencies']) > 1:
                lst_currencies = []
                for i in one_element_json_obj_data['currencies']:
                    lst_currencies.append(i['name'])
                country_dict['Currencies'].append(','.join(lst_currencies))
            else:
                country_dict['Currencies'].append(one_element_json_obj_data['currencies'][0]['name'])

            # handle possibility of multiple languages as dictionaries
            if len(one_element_json_obj_data['languages']) > 1:
                lst_languages = []
                for i in one_element_json_obj_data['languages']:
                    lst_languages.append(i['name'])
                country_dict['Languages'].append(','.join(lst_languages))
            else:
                country_dict['Languages'].append(one_element_json_obj_data['languages'][0]['name'])

        # Return as a Pandas dataframe
    return pd.DataFrame(country_dict)


# build the list to pass to the build_country_db function with 'Pixal' being erroneous
seven_countries_df = build_country_db(['Belgium', 'Switzerland', 'France', 'Pixal', 'Spain', 'Italy', 'Greece'])
print()  # space in console output
pd.set_option('display.max_columns', None)  # show all the columns
print(seven_countries_df)

# TODO: Separate wrapper and build out visual presentation layer using Flask or Django, and sqlite3 or PostgreSQL
