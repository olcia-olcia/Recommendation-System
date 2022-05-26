#!/usr/bin/env python3
import pandas as pd
import os
from typing import List


def get_files_from_directory(path: str, extension: str) -> List[str]:

    files_list = os.listdir(path)
    files_list = [os.path.join(path, f) for f in files_list if extension in f]
    files_list.sort()

    return(files_list)


def join_ratings_with_metadata(rating_path: str,
                               metadata_path: str) -> pd.DataFrame:

    """ Function reads and merges user ratings with product metadata
        returning dataframe

        Args:
            rating_path: path to csv file containing user ratings
            metadata_path: path to json file containing product metadata
    """

    # assign headers
    csv_headers = ['itemID', 'userID', 'rating', 'unixReviewTime']

    # read data
    ratings = pd.read_csv(rating_path, header=None, names=csv_headers)
    metadata = pd.read_json(metadata_path, lines=True)

    # join tables
    joined_data = ratings.merge(metadata,
                                left_on=['itemID'],
                                right_on=['asin'],
                                how='inner')

    return joined_data


def calculate_statistics(df: pd.DataFrame) -> pd.Series:
    """
    function calculates statistics for provided dataframe including:
    - Number of users
    - Number of items
    - Total number of ratings
    - Average number of reviews per user
    - Size of the rating matrix (number of users x number of items)
    - Sparsity of the dataset
        (what percentage of the rating matrix has no records)
    """

    numbers = df.agg({"itemID": 'nunique',
                      "userID": 'nunique',
                      'rating': 'count'})
    numbers['avg_number_reviews'] = numbers['rating'] / numbers['userID']
    numbers['rating_mx_shape'] = numbers['userID'] * numbers['itemID']
    numbers['sparsity'] = 1 - (numbers['rating'] / numbers['rating_mx_shape'])

    return numbers
