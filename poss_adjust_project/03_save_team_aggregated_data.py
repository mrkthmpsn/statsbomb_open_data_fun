"""
File to save aggregated defensive action and possession share data, by both 
player ID and team ID, with competition details
"""

import numpy as np
import pandas as pd

from data.constants import (
    BUNDESLIGA_TEAMS,
    LIGUE_1_TEAMS,
    PREMIER_LEAGUE_TEAMS,
    SERIE_A_TEAMS,
)
from sb_data_pipeline.dataclasses import StatsbombPlayerPosition
from sb_data_pipeline.temp_utils import load_player_presence_stats_df

# Load in data
def_events_df = pd.read_csv("./poss_adjust_project/data/def_events.csv")
player_df = pd.read_csv("./data/statsbomb_players.csv")
team_df = pd.read_csv("./data/statsbomb_teams.csv")
presence_stats_df = load_player_presence_stats_df()

# Map player position to more general groups
position_mapping = {
    position.statsbomb_position: position.general_position
    for position in StatsbombPlayerPosition
}
position_group_mapping = {
    position.statsbomb_position: position.position_group
    for position in StatsbombPlayerPosition
}

presence_stats_df["general_position"] = presence_stats_df["position"].map(
    position_mapping
)
presence_stats_df["position_group"] = presence_stats_df["position"].map(
    position_group_mapping
)
presence_stats_df["seq_present"] = presence_stats_df["sequences_list"].apply(
    lambda x: len(x)
)

# Need to merge the presence data here to get the general position
presence_stats_df["player_id"] = presence_stats_df["player_id"].astype(int)
presence_stats_df["team_id"] = presence_stats_df["team_id"].astype(int)
presence_stats_df["match_id"] = presence_stats_df["match_id"].astype(float).astype(int)
def_events_df = def_events_df.merge(
    presence_stats_df[["match_id", "player_id", "team_id", "general_position"]]
)

# Aggregate the data
agg_def_events_df = (
    def_events_df.groupby(["player_id", "team_id", "general_position", "event_type"])
    .count()["event_id"]
    .reset_index()
)
agg_def_events_df = (
    agg_def_events_df.pivot(
        index=["player_id", "team_id", "general_position"],
        columns="event_type",
        values="event_id",
    )
    .fillna(0)
    .reset_index()
)

agg_presence_stats_df = (
    presence_stats_df[
        [
            "player_id",
            "team_id",
            "general_position",
            "mins_played",
            "successful_passes",
            "opp_successful_passes",
            "seq_present",
        ]
    ]
    .groupby(["player_id", "team_id", "general_position"])
    .sum()
    .reset_index(drop=False)
)
agg_presence_stats_df = agg_presence_stats_df[
    agg_presence_stats_df["general_position"] != "NA"
]

agg_presence_stats_df["total_pass"] = (
    agg_presence_stats_df["successful_passes"]
    + agg_presence_stats_df["opp_successful_passes"]
)
agg_presence_stats_df["poss_pct"] = (
    agg_presence_stats_df["successful_passes"] / agg_presence_stats_df["total_pass"]
)
agg_presence_stats_df["player_id"] = agg_presence_stats_df["player_id"].astype(int)
agg_presence_stats_df["team_id"] = agg_presence_stats_df["team_id"].astype(int)

combined_df = (
    player_df[["player_id", "player_name"]]
    .merge(
        agg_presence_stats_df[
            [
                "player_id",
                "team_id",
                "general_position",
                "mins_played",
                "poss_pct",
                "seq_present",
            ]
        ]
    )
    .merge(agg_def_events_df)
    .merge(team_df[["team_id", "team_name"]])
)

combined_df["league"] = np.where(
    combined_df["team_id"].isin(PREMIER_LEAGUE_TEAMS),
    "epl",
    np.where(
        combined_df["team_id"].isin(LIGUE_1_TEAMS),
        "ligue_1",
        np.where(
            combined_df["team_id"].isin(BUNDESLIGA_TEAMS),
            "bundesliga",
            np.where(combined_df["team_id"].isin(SERIE_A_TEAMS), "serie_a", "la_liga"),
        ),
    ),
)

# Rename the stat columns for ease
action_rename_dict = {
    "CLEARANCE": "clear",
    "DUEL": "tack",
    "GENERIC:Block": "block",
    "GENERIC:Dribbled Past": "drib_past",
    "INTERCEPTION": "interc",
    "PRESSURE": "pressure",
}

combined_df = combined_df.rename(columns=action_rename_dict)

# per 90 the defensive stats
for stat_type in action_rename_dict.values():
    combined_df[f"{stat_type}_90"] = combined_df[stat_type] / (
        combined_df["mins_played"] / 90
    )

combined_df["sequences_p90"] = combined_df["seq_present"] / (
    combined_df["mins_played"] / 90
)

combined_df.to_csv(
    "./poss_adjust_project/data/aggregated_data_teams_sequences.csv", index=False
)
