
import requests
import json

import typing
from typing import List

from statistics import mean

from pathlib import Path

project_dir = str(Path(__file__).resolve().parents[2])

# manually download data from the following link and place it in external data

# https://data.cityofchicago.org/resource/m6dm-c72p.json?trip_start_timestamp=2019-03-21T13:15:00.000


# def get_data_sample(url: str = None) -> List[dict]:
#     """
#     downloads a json response from the given url and returns a list of dictionaries
#     default url argument of None downloads the data from this link:
#     'https://data.cityofchicago.org/resource/m6dm-c72p.json?trip_start_timestamp=2019-03-21T13:15:00.000'
#     which is provided by an example in the documentation here:
#     https://dev.socrata.com/foundry/data.cityofchicago.org/m6dm-c72p
#
#     parameters:: url: string
#     returns::    response: list of dictionaries
#     """
#     if url is None:
#         url = 'https://data.cityofchicago.org/resource/m6dm-c72p.json?trip_start_timestamp=2019-03-21T13:15:00.000'
#     response = requests.get(url)
#     json_object = json.load(response.text)
#     return json_object

def load_local_sample_data(file_path: str = None) -> List[dict]:
    if file_path is None:
        file_path = project_dir + '/data/external/' + 'm6dm-c72p_manual_download_2019-01-28.json'
    with open(file_path) as f:
        json_object = json.load(f)
    return json_object


def calculate_fraction_tips(ride_hailing_data: List[dict]) -> float:
    """ given a list of dictionaries with each dict representing a trip,
    calculate the fraction of those trips that left a tip"""
    list_ = []
    for dict_ in ride_hailing_data:
        tip_given = 1 if int(dict_['tip']) > 0 else 0
        list_.append(tip_given) # tip is rounded to integer number of dollars.
    return mean(list_)



# response = requests.get('https://data.cityofchicago.org/resource/m6dm-c72p.json?trip_start_timestamp=2019-03-21T13:15:00.000')


if __name__ == "__main__":
    print(f'running{Path(__file__)}')
    sample_ride_hailing_data = load_local_sample_data()
    tip_fraction = calculate_fraction_tips(sample_ride_hailing_data)
    print("the fraction of tips given in this sample data is:", tip_fraction)
