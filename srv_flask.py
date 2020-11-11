# -*- coding: utf-8 -*-
"""
Program: srv_flask.py
Created on 11/10/2020
@author: adhamlin

"""
# imports
import urllib.request
import urllib.parse
from urllib.error import HTTPError
from urllib.error import URLError
from flask import Flask
from flask import render_template
import json


app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD=True,  # force reload/refresh -must be listed before debug or will not reload template
    DEBUG=True
)

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


# country_user_input = input("Enter a country name: ")  # user input of country
country_user_input = 'italy'  # replace with user input form
data = get_country_data(country_user_input)  # as a string

json_obj1 = json.loads(data)  # load data as a list

# print(json_obj1[0])
# print(type(json_obj1[0]))  # says its a dict


@app.route("/")
def home():
    """
    :return:
    """
    data_dict = json_obj1[0]
    return render_template('home.html', data=data_dict)


# main/driver
if __name__ == '__main__':
    app.run()
