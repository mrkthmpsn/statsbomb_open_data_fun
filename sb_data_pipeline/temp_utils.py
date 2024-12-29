"""
Utils that should be made redundant by a refactor
"""

import json
from tqdm import tqdm
import pandas as pd


def load_player_presence_stats_df() -> pd.DataFrame:
    """
    Function to load the `player_match_presence_stats` JSON and convert it into a pandas dataframe
    """

    with open("./data/player_match_presence_stats.json", "r") as presence_json:
        saved_data = json.load(presence_json)

    loaded_presence_json = json.loads(saved_data)

    # Initialize an empty list to hold DataFrames for each stat
    dfs = []

    # Iterate through each stat in the JSON data
    for stat, stat_data in tqdm(loaded_presence_json.items()):
        # Create a DataFrame from the current stat data
        stat_df = pd.DataFrame(stat_data.items(), columns=["index", stat])

        # Split the index into separate columns without using eval
        stat_df[["match_id", "team_id", "player_id"]] = stat_df["index"].str.extract(
            r"\(([^,]+),\s*\'([^\']+)\',\s*\'([^\']+)\'\)"
        )

        # Drop the original index column if not needed
        stat_df = stat_df.drop(columns=["index"])

        # Append the DataFrame to the list
        dfs.append(stat_df)

    # Concatenate all DataFrames along columns (axis=1)
    final_df = pd.concat(dfs, axis=1)

    # Remove duplicate columns
    final_df = final_df.loc[:, ~final_df.columns.duplicated()]

    return final_df
