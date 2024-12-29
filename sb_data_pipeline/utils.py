"""
Util functions for the statsbomb data ingestion 'pipeline'
"""

from sb_data_pipeline.dataclasses import StatsBombEventFactory
from kloppy.domain.models.event import EventDataset
from kloppy.domain.models.common import Metadata
import pandas as pd
from kloppy import statsbomb


from typing import List, Optional


def _get_player_possession_presence(
    match_id: int,
    match_player_id_list: List[int],
    dataset: Optional[EventDataset] = None,
) -> pd.DataFrame:
    """
    Gathers a dataframe of data for whether players were on the pitch during possession sequences.

    Args:
        match_id (int): Statsbomb match ID.
        match_player_id_list (List[int]): List of Statsbomb player IDs who played in the match.
        dataset (EventDataset): kloppy dataset

    Returns:
        pd.DataFrame: Dataframe with possession IDs as rows and player IDs as columns, with a 1 or 0 indicating whether the player was on the field of play during that row's possession sequence.
    """

    if dataset is None:
        dataset = statsbomb.load_open_data(
            match_id=match_id, event_factory=StatsBombEventFactory()
        )
    match_events_df = dataset.to_df("*", "possession")

    # Set up the dataframe with all the player IDs from the match
    match_players_df = pd.DataFrame(
        columns=["event_id", "period_id", "timestamp", *match_player_id_list]
    )

    # Optimize starting lineup extraction
    starting_lineup_df = match_events_df[
        match_events_df["event_type"] == "GENERIC:Starting XI"
    ]
    starting_lineup_records = [
        {
            "event_id": event_id,
            "period_id": kloppy_event.period.id,
            "timestamp": kloppy_event.timestamp,
            **{
                str(player): 1
                for player in [
                    player["player"]["id"]
                    for player in kloppy_event.raw_event["tactics"]["lineup"]
                ]
            },
        }
        for event_id in starting_lineup_df["event_id"]
        if (kloppy_event := dataset.get_event_by_id(event_id)) is not None
    ]

    starting_lineups_df = pd.DataFrame(starting_lineup_records)

    sub_events_df = match_events_df[match_events_df["event_type"] == "SUBSTITUTION"]
    substitution_records = [
        {
            "event_id": event_id,
            "period_id": kloppy_event.period.id,
            "timestamp": kloppy_event.timestamp,
            str(raw_event["player"]["id"]): 0,
            str(raw_event["substitution"]["replacement"]["id"]): 1,
        }
        for event_id in sub_events_df["event_id"]
        if (kloppy_event := dataset.get_event_by_id(event_id)) is not None
        and (raw_event := kloppy_event.raw_event) is not None
    ]

    sub_events_df = pd.DataFrame(substitution_records)

    # Combine dataframes more efficiently
    match_players_df = pd.concat(
        [match_players_df, starting_lineups_df, sub_events_df], ignore_index=True
    )

    # Get the starting event in each sequence
    filtered_events_df = match_events_df.sort_values(
        by=["period_id", "timestamp"]
    ).drop_duplicates(subset="possession", keep="first")
    filtered_events_df = filtered_events_df[
        ~filtered_events_df["event_type"].isin(["GENERIC:Starting XI", "SUBSTITUTION"])
    ]
    filtered_events_df = filtered_events_df[
        ["event_id", "period_id", "timestamp", "possession", "team_id"]
    ]

    player_present_df = pd.concat(
        [match_players_df, filtered_events_df], ignore_index=True
    ).sort_values(["period_id", "timestamp"])

    # Forward fill presence info more efficiently
    player_present_df = player_present_df.ffill(axis=0).fillna(0)

    # Dropping timestamp partly as its not JSON serializable
    player_present_df = player_present_df.drop(columns=["timestamp"])

    player_present_df["match_id"] = match_id

    # If we're storing possession-level info, don't need event or team IDs
    player_present_df = player_present_df.drop(columns=["event_id", "team_id"])

    return player_present_df


def _get_player_presence_summary_stats(
    match_id: int,
    player_id: int,
    player_team_id: int,
    player_sequences_list: List[int],
    match_events_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Summarises Statsbomb event data during a player's on-pitch presence in a match, with statistics for their own team and the opposition team.

    Args:
        match_id (int): Statsbomb match ID.
        player_id (int): Statsbomb player ID.
        player_team_id (int): Statsbomb team ID of the player's team.
        player_sequences_list (List[int]): List of sequence IDs that the player was on-pitch for.
        match_events_df (pd.DataFrame): Dataframe of Statsbomb events.

    Returns:
        pd.DataFrame: DataFrame in which columns are player ID and various match statistics (e.g. shots, xG, successful passes) which are the values of their team and the opposition team while they were on-field during the match.
    """

    reduced_df = match_events_df[
        match_events_df["possession"].isin(player_sequences_list)
    ]
    reduced_df = reduced_df[reduced_df["event_type"].isin(["PASS", "SHOT"])]

    summary_df = reduced_df.groupby("team_id").agg(
        shots=pd.NamedAgg(column="event_type", aggfunc=lambda x: (x == "SHOT").sum()),
        successful_passes=pd.NamedAgg(
            column="event_type",
            aggfunc=lambda x: (
                (x == "PASS") & (reduced_df.loc[x.index, "result"] == "COMPLETE")
            ).sum(),
        ),
        goals=pd.NamedAgg(
            column="event_type",
            aggfunc=lambda x: (
                (x == "SHOT") & (reduced_df.loc[x.index, "result"] == "GOAL")
            ).sum(),
        ),
        xg=pd.NamedAgg(column="statsbomb_xg", aggfunc="sum"),
    )
    summary_df = summary_df.reset_index()

    for col in ["shots", "successful_passes", "goals", "xg"]:
        summary_df[f"opp_{col}"] = list(summary_df[col][::-1])

    summary_df["total_passes"] = (
        summary_df["successful_passes"] + summary_df["opp_successful_passes"]
    )
    summary_df["poss_pct"] = (
        summary_df["successful_passes"] / summary_df["total_passes"]
    )

    # So, from this dataframe I then need to choose the correct row
    summary_df = summary_df[summary_df["team_id"] == player_team_id]
    summary_df["player_id"] = player_id
    # TODO: Don't need to add match_id by this route
    summary_df["match_id"] = int(match_id)
    summary_df["sequences_list"] = [set(player_sequences_list)]

    return summary_df


def calculate_player_minutes_played(
    match_events_df: pd.DataFrame,
    player_sequences_list: List[int],
    dataset_metadata: Metadata,
) -> float:
    """Calculate the total minutes a player has played in a match based on their sequences.

    Args:
        match_events_df (pd.DataFrame): DataFrame containing match events.
        player_sequences_list (List[int]): List of possession sequences the player was involved in.

    Returns:
        float: Total minutes played by the player.
    """
    # Filter events related to the player's sequences
    player_events_df = match_events_df[
        match_events_df["possession"].isin(player_sequences_list)
    ]

    if player_events_df.empty:
        return 0.0  # Player has not participated in any sequences

    # Get the entry and exit times
    entry_time = player_events_df.iloc[0]["timestamp"]
    exit_time = player_events_df.iloc[-1]["timestamp"]

    # Get the period IDs for entry and exit
    start_period_id = player_events_df["period_id"].iloc[0]
    end_period_id = player_events_df["period_id"].iloc[-1]

    # Calculate total time played
    total_time_played = 0.0

    # Add durations for periods before the entry period
    for match_period in dataset_metadata.periods:
        if match_period.id == start_period_id:
            # Add time from entry to the end of the first period
            total_time_played += (
                match_period.duration.total_seconds() / 60.0
            ) - entry_time.total_seconds() / 60.0
        elif match_period.id > start_period_id and match_period.id <= end_period_id:
            # Add full duration for periods between entry and exit
            total_time_played += match_period.duration.total_seconds() / 60.0
            if match_period.id == end_period_id:
                # Subtract time from the start of the period to the exit time
                total_time_played -= (
                    match_period.duration.total_seconds() / 60.0
                ) - exit_time.total_seconds() / 60.0

    return total_time_played


def get_match_player_id_list(dataset: EventDataset) -> List[str]:
    """Simple extraction util to get the list of player IDs from the given StatsBomb dataset.

    Args:
        dataset: A kloppy dataset of a Statsbomb match, containing match metadata.

    Returns:
        List[str]: A list of player IDs as strings.
    """
    return [
        str(player.player_id)
        for team in dataset.metadata.teams
        for player in team.players
    ]
