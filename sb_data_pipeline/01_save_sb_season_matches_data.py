"""
File to save basic matches information from the `statsbombpy` package.

The aim is to have a script which can create a file if one doesn't exist, and -
if one does exist - to add new information to it, rather than completely
re-write it.
"""

import datetime
import pandas as pd
from pydantic import BaseModel
from statsbombpy import sb
import json
import os

from tqdm import tqdm


class SBSeasonCheckData(BaseModel):
    competition_id: int
    season_id: int
    competition_gender: str
    match_available: datetime.datetime | None
    match_available_360: datetime.datetime | None
    match_updated: datetime.datetime | None
    match_updated_360: datetime.datetime | None

    model_config = {"arbitrary_types_allowed": True}


def _get_statsbomb_season_matches_data(
    competition_id: int, season_id: int
) -> pd.DataFrame:
    """Basic wrapper for `sb.matches`, given a Statsbomb competition and season ID."""
    matches_df = sb.matches(competition_id=competition_id, season_id=season_id)
    return matches_df


# Grab the competitions and save the file
gathered_comps_df = sb.competitions()


# Check if there's a file by the name of 'statsbomb_competition_seasons.csv' in the same folder as this file
file_exists = os.path.exists("./data/statsbomb_competition_seasons.json")
if file_exists:
    with open("./data/statsbomb_competition_seasons.json", "r") as saved_json_file:
        saved_data = saved_json_file.read()

    saved_competitons_df = pd.DataFrame.from_dict(json.loads(saved_data))

    with open("./data/statsbomb_season_matches.json", "r") as saved_json_file:
        saved_data = saved_json_file.read()
    # Wait - how am I going to get things back into this format?
    # Would have to remove the object from
    saved_match_json_records = json.loads(saved_data)
    saved_matches_df = pd.json_normalize(saved_match_json_records, "matches")

    saved_season_essential_data = []
    for _, comp_season in saved_competitons_df.iterrows():
        temp_obj = SBSeasonCheckData(**comp_season)
        saved_season_essential_data.append(temp_obj)

    gathered_season_essential_data = [
        SBSeasonCheckData(**comp_season)
        for _, comp_season in gathered_comps_df.iterrows()
    ]

    for gathered_season in gathered_season_essential_data:
        if not any(
            gathered_season == saved_season
            for saved_season in saved_season_essential_data
        ):
            # TODO - Fetch and save the competition matches data
            pass

else:
    print("No saved competitions data to compare to.")
    # Save the competitions JSON to a file
    with open("./data/statsbomb_competition_seasons.json", "w") as json_file:
        json.dump(gathered_comps_df.to_dict(), json_file)

    # The competition genders that statsbomb uses
    matches_skeleton = []
    for _, comp_season in tqdm(
        gathered_comps_df.iterrows(), total=gathered_comps_df.shape[0]
    ):
        comp_season_matches_df = _get_statsbomb_season_matches_data(
            competition_id=comp_season["competition_id"],
            season_id=comp_season["season_id"],
        )
        matches_skeleton.append(
            {
                "competition_id": comp_season["competition_id"],
                "competition_name": comp_season["competition_name"],
                "competition_gender": comp_season["competition_gender"],
                "season_id": comp_season["season_id"],
                "season_name": comp_season["season_name"],
                "matches": comp_season_matches_df.to_dict(orient="records"),
            }
        )

    with open("./data/statsbomb_season_matches.json", "w") as json_file:
        json.dump(matches_skeleton, json_file)
