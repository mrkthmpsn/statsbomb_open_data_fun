import json
import pandas as pd
from kloppy import statsbomb
from tqdm import tqdm
from sb_data_pipeline.utils import (
    _get_player_possession_presence,
    _get_player_presence_summary_stats,
    calculate_player_minutes_played,
)
from sb_data_pipeline.dataclasses import StatsBombEventFactory

# 23-Dec - Takes about 2.2-2.5s/it
def get_match_player_presence_stats(match_id: int) -> pd.DataFrame:
    """
    Docstring should go here
    """

    dataset = statsbomb.load_open_data(
        match_id=match_id, event_factory=StatsBombEventFactory()
    )
    match_player_id_list = [
        str(player.player_id)
        for team in dataset.metadata.teams
        for player in team.players
    ]

    # If I only need these event types, I can do this filtering in the original dataset call
    match_events_df = dataset.to_df("*", "possession", "statsbomb_xg")

    player_presence_df = _get_player_possession_presence(
        match_id=match_id, match_player_id_list=match_player_id_list
    )

    player_presence_stats_list = []

    # Precompute player presence sequences for all players in one go
    player_presence_sequences = {
        player.player_id: player_presence_df[
            player_presence_df[str(player.player_id)] == 1
        ]["possession"].astype(int)
        for team in dataset.metadata.teams
        for player in team.players
    }

    for team in dataset.metadata.teams:
        team_id = team.team_id
        for player in team.players:
            player_id = player.player_id

            # Use precomputed sequences
            individual_player_presence_sequences = player_presence_sequences[player_id]

            player_presence_stats = _get_player_presence_summary_stats(
                match_id=match_id,
                player_id=player_id,
                player_team_id=team_id,
                player_sequences_list=individual_player_presence_sequences,
                match_events_df=match_events_df,
            )
            player_presence_stats["mins_played"] = [
                calculate_player_minutes_played(
                    match_events_df=match_events_df,
                    player_sequences_list=individual_player_presence_sequences,
                    dataset_metadata=dataset.metadata,
                )
            ]
            # TODO: Not sure I'm getting a position for everyone who plays
            player_position = None
            if player.positions:
                player_position = player.positions[0].name
            player_presence_stats['position'] = [player_position]
            player_presence_stats_list.append(player_presence_stats)

    test_df = pd.concat(player_presence_stats_list).reset_index(drop=True)

    return test_df


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

# TODO: This is the kind of thing that I would want a db for probably
df_list = []
for match_id in tqdm(match_id_list):
    match_presence_stats = get_match_player_presence_stats(match_id)
    df_list.append(match_presence_stats)

# TODO: Group by match ID and team ID and then turn it to json to save
test_df = pd.concat(df_list)

to_save_obj = (
    test_df.dropna(subset=["match_id", "team_id"])
    .set_index(["match_id", "team_id", "player_id"])
    .to_json()
)
with open("./data/player_match_presence_stats.json", "w") as json_file:
    json.dump(to_save_obj, json_file)
