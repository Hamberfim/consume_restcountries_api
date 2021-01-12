# -*- coding: utf-8 -*-
"""
Program: consume_country_api.py
Created on 10/27/2020
@author: adhamlin

This program takes user input of a country and passes it to the api, returns information on that country.
This program pulls data from an api endpoint, https://restcountries.eu/
List all: https://restcountries.eu/rest/v2/all
"""
# imports
import urllib.request
import urllib.parse
from urllib.error import HTTPError
from urllib.error import URLError
import json

# base url to append with argument parameter
service_url = 'https://restcountries.eu/rest/v2/name/'


def get_country_data(country):
    """
    Function to get data about a country from the https://restcountries.eu API
    :param country: String input of a country name.
    :return: json formatted data on a country.
    """
    country_name = str(country)  # already a string via input but needed if input supplied via other source
    url = service_url + country_name
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
    #print("Type:\n", type(one_element))
    #print()  # space in console output
    # output one_element keys
    one_element_keys = one_element.keys()
    #print("Single element keys:\n", one_element_keys)
    #print()  # space in console output
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
