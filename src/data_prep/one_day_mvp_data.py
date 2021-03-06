
import requests
import json

import typing
from typing import List

from statistics import mean
import pandas as pd
from pathlib import Path
import datetime

import os


project_dir = str(Path(__file__).resolve().parents[2])


def isolate_2019_07_17_trips(save=False):
    chunksize = 10 ** 6
    file_path = project_dir + '/data/raw/' + 'Transportation_Network_Providers_-_Trips.csv'
    df = None  # just here to stop pycharm complaining
    first = True
    for i, chunk in enumerate(pd.read_csv(file_path, chunksize=chunksize)):
        # if i <= 3:
        #     continue # done comment me out
        #
        # if i > 10:
        #     break  # done comment me out
        #     pass

        print(i)
        chunk.columns = [s.lower().replace(" ", "_") for s in chunk.columns]

        chunk['trip_start_timestamp'] = pd.to_datetime(chunk['trip_start_timestamp'], format="%m/%d/%Y %I:%M:%S %p")
        chunk['trip_end_timestamp'] = pd.to_datetime(chunk['trip_end_timestamp'], format="%m/%d/%Y %I:%M:%S %p")

        chunk = chunk.drop(['trip_id', 'pickup_centroid_location', 'dropoff_centroid_location'], axis=1)

        the_day_of = datetime.date(2019, 7, 17)
        chunk = chunk[chunk['trip_start_timestamp'].dt.date == the_day_of]
        if first:
            df = pd.DataFrame(chunk)
            first = False
        else:
            df = df.append(chunk)
        print('df.shape =', df.shape)

    print('done')

    if save:
        file_path = project_dir + '/data/interim/' + 'day_2019-07-17_trips.csv'
        df.to_csv(file_path)

