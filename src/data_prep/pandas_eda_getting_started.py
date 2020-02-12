from pathlib import Path

import pandas as pd

# from typing import float




project_dir = str(Path(__file__).resolve().parents[2])


def make_interim_tips(save=False):

    chunksize = 10 ** 6
    file_path = project_dir + '/data/raw/' + 'Transportation_Network_Providers_-_Trips.csv'
    tips = None  # just here to stop pycharm complaining
    for i, chunk in enumerate(pd.read_csv(file_path, chunksize=chunksize)):
        print(i)

        if i == 0:
            tips = pd.DataFrame(chunk['Tip'])
        else:
            tips = tips.append(pd.DataFrame(chunk['Tip']))

    tips = tips.dropna().astype(int)

    if save:
        file_path = project_dir + '/data/interim/' + 'all_tips.csv'
        tips.to_csv(file_path, chunksize=chunksize, index=False)

    return tips


def load_interim_tips():
    read_file_path = project_dir + "/data/interim/" + 'all_tips.csv'
    tips = pd.read_csv(read_file_path)
    return tips


def calculate_percentage_with_tips(tips: pd.DataFrame) -> float:
    return (tips['Tip'] > 0).mean()



if __name__ == "__main__":
    print('running:', project_dir)
    # tips_df = make_interim_tips(save=False)
    tips_df = load_interim_tips()
    tip_fraction = calculate_percentage_with_tips(tips_df)
    pass