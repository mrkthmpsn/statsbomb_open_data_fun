"""
File to save aggregated defensive action and possession share data
"""

import pandas as pd

from sb_data_pipeline.dataclasses import StatsbombPlayerPosition
from sb_data_pipeline.temp_utils import load_player_presence_stats_df

# Load in data
def_events_df = pd.read_csv("./poss_adjust_project/data/def_events.csv")
player_df = pd.read_csv("./data/statsbomb_players.csv")
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

# Aggregate the data
agg_def_events_df = (
    def_events_df.groupby(["player_id", "event_type"]).count()["event_id"].reset_index()
)
agg_def_events_df = (
    agg_def_events_df.pivot(index="player_id", columns="event_type", values="event_id")
    .fillna(0)
    .reset_index()
)

# TODO: Add team ID here - didn't in the initial study in case it reduced the amount of qualifying players
agg_presence_stats_df = (
    presence_stats_df[
        [
            "player_id",
            "general_position",
            "mins_played",
            "successful_passes",
            "opp_successful_passes",
        ]
    ]
    .groupby(["player_id", "general_position"])
    .sum()
    .reset_index(drop=False)
)
# TODO: Move the mins_played to the analysis
agg_presence_stats_df = agg_presence_stats_df[
    (agg_presence_stats_df["mins_played"] >= 450)
    & (agg_presence_stats_df["general_position"] != "NA")
]


agg_presence_stats_df["total_pass"] = (
    agg_presence_stats_df["successful_passes"]
    + agg_presence_stats_df["opp_successful_passes"]
)
agg_presence_stats_df["poss_pct"] = (
    agg_presence_stats_df["successful_passes"] / agg_presence_stats_df["total_pass"]
)
agg_presence_stats_df["player_id"] = agg_presence_stats_df["player_id"].astype(int)

combined_df = (
    player_df[["player_id", "player_name"]]
    .merge(
        agg_presence_stats_df[
            ["player_id", "general_position", "mins_played", "poss_pct"]
        ]
    )
    .merge(agg_def_events_df)
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

# possession adjust the per 90 stats
for stat_type in action_rename_dict.values():
    combined_df[f"{stat_type}_90_possadj"] = combined_df[f"{stat_type}_90"] * (
        combined_df["poss_pct"] * 2
    )

combined_df.to_csv("./poss_adjust_project/data/aggregated_data.csv", index=False)
