"""
File to collect defensive statistics from event data.
"""

from kloppy import statsbomb
from tqdm import tqdm
import pandas as pd

from sb_data_pipeline.temp_utils import load_player_presence_stats_df


presence_stats_df = load_player_presence_stats_df()


def _get_filtered_events(match_id: int) -> pd.DataFrame:
    """
    Simple function to get a bunch of defensive events from a match's Statsbomb data
    """
    dataset = statsbomb.load_open_data(
        match_id=match_id,
        # Dribbled Past and Block events are under kloppy's 'generic' umbrella
        event_types=["duel", "interception", "clearance", "pressure", "generic"],
    )

    # So I just need to groupby and count, really, right?
    test_df = dataset.to_df("*", "raw_event")
    # Filter out the non-ground duel DUEL events
    # All events with kloppy duel_event_type of 'GROUND' are Statsbomb Tackles. Code below.
    # ground_duels_df = test_df[test_df["duel_type"] == "GROUND"]
    # ground_duels_df["duel_type_detailed"] = ground_duels_df["raw_event"].apply(
    #     lambda x: x.get("duel", {}).get("type", {}).get("name", None)
    # )
    filtered_df = test_df[
        ~((test_df["event_type"] == "DUEL") & (test_df["duel_type"] != "GROUND"))
    ]
    # Filter out unwanted GENERIC events
    filtered_df = filtered_df[
        filtered_df["event_type"].isin(
            [
                "DUEL",
                "PRESSURE",
                "INTERCEPTION",
                "CLEARANCE",
                "GENERIC:Dribbled Past",
                "GENERIC:Block",
            ]
        )
    ]
    filtered_df["match_id"] = match_id

    return filtered_df


# Fetch match IDs
matches_df = pd.read_json("./data/statsbomb_season_matches.json").explode("matches")
selected_matches_df = matches_df[
    (
        matches_df["competition_name"].isin(
            ["1. Bundesliga", "La Liga", "Ligue 1", "Premier League", "Serie A"]
        )
    )
    & (matches_df["season_name"] == "2015/2016")
]

match_id_list = [match_obj["match_id"] for match_obj in selected_matches_df["matches"]]

df_list = []
# Runs at about 1.1-1.2 it/s
for match_id in tqdm(match_id_list):
    temp_df = _get_filtered_events(match_id=match_id)
    df_list.append(temp_df)

total_df = pd.concat(df_list).reset_index(drop=True)
total_df.to_csv("./poss_adjust_project/data/def_events.csv", index=False)
