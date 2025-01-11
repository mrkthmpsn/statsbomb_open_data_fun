# Exploring correlations between player defensive output and 'high-sequence gameplay' in the 2015/16 'Big Five' men's European leagues

## Results

The initial quick correlation study between defensive action metrics and possession share of the player's team suggested little link between the two types of variable.

My assumption was that defensive actions may be more influenced by the amount of sequences, given that defensive actions often end a possession sequence. In other words, high-turnover games may yield high-defensive output numbers.

Surprisingly, that doesn't appear to be the case, with essentially no link. These are even weaker correlations than were found for a team's possession share (as defined by the team's passes as a share of the match's total while they were on the field).

|     | general_position     | count | clear_90 | tack_90 | block_90 | drib_past_90 | interc_90 | pressure_90 | corr_stdev | corr_mean |
| --: | :------------------- | ----: | -------: | ------: | -------: | -----------: | --------: | ----------: | ---------: | --------: |
|   0 | Attacking Midfielder |    55 |   -0.045 |  -0.003 |    0.132 |        0.089 |     0.102 |        0.25 |      0.104 |     0.087 |
|   1 | Center Back          |   385 |   -0.161 |    0.13 |    0.045 |        0.085 |     0.263 |       0.131 |       0.14 |     0.082 |
|   2 | Center Forward       |   192 |    0.008 |   -0.01 |    0.064 |       -0.044 |     0.196 |       0.095 |      0.087 |     0.052 |
|   3 | Center Midfielder    |   146 |   -0.034 |   0.023 |    0.046 |       -0.054 |    -0.102 |        0.25 |      0.124 |     0.022 |
|   4 | Defensive Midfielder |   300 |   -0.137 |   0.043 |    -0.01 |        0.023 |      0.13 |       0.182 |      0.112 |     0.038 |
|   5 | Full Back            |   363 |   -0.047 |   0.067 |    0.213 |       -0.027 |     0.291 |       0.145 |      0.134 |     0.107 |
|   6 | Goalkeeper           |   143 |    0.337 |  -0.092 |   -0.054 |        0.015 |    -0.112 |      -0.061 |      0.168 |     0.006 |
|   7 | Wide Midfielder      |    88 |    0.009 |   0.048 |    0.127 |        0.118 |     0.221 |       0.309 |      0.111 |     0.139 |
|   8 | Wing Back            |    31 |    0.113 |   0.232 |    0.196 |       -0.022 |    -0.157 |       0.389 |      0.194 |     0.125 |
|   9 | Winger               |   133 |    0.004 |  -0.006 |    0.151 |       -0.007 |     0.166 |       0.138 |      0.085 |     0.074 |

But is the league a confounding factor? Here are the mean sequences per 90 that each player in the sample experienced, split by league:

| league     | sequences_p90 |
| :--------- | ------------: |
| bundesliga |        183.12 |
| epl        |       176.225 |
| la_liga    |       190.268 |
| ligue_1    |       187.893 |
| serie_a    |       187.425 |

Yet even when separating these leagues, the correlation strengths are not that strong. Here we will show the leagues with lowest and highest average sequences experienced by players. (For ease of reading, results have been filtered to positions that had 20+ players in the sample).

Premier League
| | general_position | count | clear_90 | tack_90 | block_90 | drib_past_90 | interc_90 | pressure_90 | corr_stdev | corr_mean |
|---:|:---------------------|--------:|-----------:|----------:|-----------:|---------------:|------------:|--------------:|-------------:|------------:|
| 1 | Center Back | 69 | -0.162 | 0.016 | 0.088 | -0.047 | 0.038 | -0.039 | 0.087 | -0.018 |
| 2 | Center Forward | 33 | 0.216 | 0.207 | 0.283 | 0.212 | 0.352 | 0.376 | 0.075 | 0.274 |
| 3 | Center Midfielder | 46 | 0.01 | 0.149 | -0.088 | 0.079 | -0.009 | 0.072 | 0.082 | 0.036 |
| 4 | Defensive Midfielder | 57 | -0.174 | 0.161 | 0.06 | 0.015 | 0.185 | 0.156 | 0.135 | 0.067 |
| 5 | Full Back | 73 | 0.059 | -0.023 | 0.105 | -0.086 | 0.145 | 0.081 | 0.086 | 0.047 |
| 6 | Goalkeeper | 32 | 0.371 | -0.047 | -0.219 | -0.014 | 0.095 | 0.155 | 0.201 | 0.057 |
| 9 | Winger | 35 | -0.125 | -0.063 | 0.163 | -0.051 | -0.009 | 0.011 | 0.098 | -0.012 |

Ligue 1
| | general_position | count | clear_90 | tack_90 | block_90 | drib_past_90 | interc_90 | pressure_90 | corr_stdev | corr_mean |
|---:|:---------------------|--------:|-----------:|----------:|-----------:|---------------:|------------:|--------------:|-------------:|------------:|
| 1 | Center Back | 80 | 0.14 | 0.14 | 0.065 | -0.085 | 0.036 | 0.077 | 0.083 | 0.062 |
| 2 | Center Forward | 40 | 0.033 | 0.03 | 0.127 | -0.048 | 0.151 | 0.194 | 0.091 | 0.081 |
| 3 | Center Midfielder | 30 | 0.433 | 0.027 | -0.113 | -0.046 | 0.1 | -0.034 | 0.196 | 0.061 |
| 4 | Defensive Midfielder | 64 | 0.118 | 0.052 | 0.126 | 0.239 | 0.288 | 0.178 | 0.087 | 0.167 |
| 5 | Full Back | 84 | 0.349 | -0.007 | 0.229 | -0.139 | -0.195 | 0.158 | 0.215 | 0.066 |
| 6 | Goalkeeper | 33 | 0.331 | 0.267 | 0.227 | 0.156 | -0.061 | -0.019 | 0.159 | 0.15 |
| 9 | Winger | 29 | 0.37 | 0.103 | 0.277 | 0.08 | 0.119 | 0.271 | 0.119 | 0.203 |

And, just because it produces a particularly unexpected (to me) result, La Liga
| | general_position | count | clear_90 | tack_90 | block_90 | drib_past_90 | interc_90 | pressure_90 | corr_stdev | corr_mean |
|---:|:---------------------|--------:|-----------:|----------:|-----------:|---------------:|------------:|--------------:|-------------:|------------:|
| 1 | Center Back | 83 | 0.089 | 0.008 | -0.135 | 0.049 | 0.392 | 0.061 | 0.173 | 0.077 |
| 2 | Center Forward | 38 | -0.084 | 0.011 | 0.221 | 0.153 | 0.137 | 0.214 | 0.121 | 0.109 |
| 4 | Defensive Midfielder | 67 | -0.22 | -0.116 | -0.312 | -0.032 | -0.137 | 0.009 | 0.119 | -0.135 |
| 5 | Full Back | 77 | 0.066 | 0.187 | 0.169 | -0.145 | 0.409 | 0.205 | 0.182 | 0.149 |
| 6 | Goalkeeper | 31 | 0.451 | 0 | 0.089 | 0.15 | -0.051 | 0.173 | 0.177 | 0.135 |
| 9 | Winger | 32 | 0.353 | 0.028 | 0.262 | 0.021 | 0.328 | 0.178 | 0.145 | 0.195 |

### A note on positions and minutes

(This section copied from `data_exploration.md`)

The position assignation is a little imperfect on _my_ side of things. I've taken one position per player per match, which I take to be the starting position. Equally, the cut-off point for minutes played (450) is based on how many minutes a player has played in this 'single-position-assignation-per-match'.

This could introduce problems like a player starting as a 'Center Midfielder' but moving to a Full-Back position early in a match; if they did this several times, that could affect not only what position their defensive actions would count under but also potentially in them meeting the minutes threshold.

The minutes played are 'full' minutes, rather than 'capped' (see a [recent piece by Eliot McKinley on the effect of capping minutes played at 90](https://www.americansocceranalysis.com/home/2024/12/8/stoppage-time-matters-how-substitutions-and-using-all-minutes-played-affect-player-statistics)).

### Commentary

#### Confounding league factors

In the Premier League, strongest correlations found among Center Forwards; in Ligue 1, the strongest links generally found in clearances; in La Liga, negative correlations for defensive metrics for Defensive Midfielders! (I think the latter is an influence of certain distinct team approaches within that league).

#### It's all too complicated

Is there really anything meaningful to pick out here, other than that there's nothing meaningful to pick out?

## Code

### Load the data

```python
import statistics
import pandas as pd

combined_df = pd.read_csv("./poss_adjust_project/data/aggregated_data_teams_sequences.csv")
combined_df = combined_df[combined_df['mins_played']>=450]
```

### Create aggregated data - metrics vs sequences

```python
def _create_grouped_correlations(df: pd.DataFrame) -> pd.DataFrame:
    """Function to produce correlations between the defensive metrics and sequences per 90 statistic, for the dataframe that is passed to it. (Meaning that we can later split by the league)."""
    corr_action_col_names = [
        f"{action}_90"
        for action in ["clear", "tack", "block", "drib_past", "interc", "pressure"]
    ]
    correlation_results = df[["sequences_p90", *corr_action_col_names]].corr()

    # Count the number of instances for each general_position
    position_counts = (
        df.groupby("general_position").size().reset_index(name="count")
    )

    # Group by general_position and calculate correlation for each group
    grouped_correlations = (
        df.groupby("general_position")[["sequences_p90", *corr_action_col_names]]
        .corr()
        .unstack()
        .reset_index()
    )
    grouped_correlations = grouped_correlations[[col for col in grouped_correlations.columns if col[0] in ['general_position', 'sequences_p90']]]
    grouped_correlations.columns = grouped_correlations.columns.map(
        lambda x: (
            x[1]
            if x[0] == "sequences_p90"
            else x[0] if len(x) == 2 and x[1] != "sequences_p90" else x
        )
    )
    grouped_correlations = position_counts.merge(grouped_correlations).drop(columns=['sequences_p90'])

    grouped_correlations = grouped_correlations.fillna(0)

    grouped_correlations["corr_stdev"] = grouped_correlations.apply(
        lambda row: statistics.stdev([row[action] for action in corr_action_col_names]),
        axis=1,
    )
    grouped_correlations["corr_mean"] = grouped_correlations.apply(
        lambda row: statistics.mean([row[action] for action in corr_action_col_names]),
        axis=1,
    )

    for col_name in [*corr_action_col_names, "corr_stdev", "corr_mean"]:
        grouped_correlations[col_name] = grouped_correlations[col_name].round(decimals=3)

    return grouped_correlations

grouped_correlations = _create_grouped_correlations(df=combined_df)
```

### Leagues and sequences

```python
league_data_df = combined_df.groupby('league')[['clear_90', 'tack_90', 'block_90', 'drib_past_90', 'interc_90', 'pressure_90', 'sequences_p90']].mean()
league_position_data_df = combined_df.groupby(['league', 'general_position'])[['clear_90', 'tack_90', 'block_90', 'drib_past_90', 'interc_90', 'pressure_90', 'sequences_p90']].mean()
```

### Correlations data - sequences _and_ league

```python
league_split_results = {}
for league in list(combined_df['league'].unique()):
    league_df = combined_df[combined_df['league'] == league].copy()
    league_results = _create_grouped_correlations(df=league_df)
    league_split_results[league] = league_results

filtered_league_split_results = {}
for k, v in league_split_results.items():
    filtered_df = v[v['count']>=20]
    filtered_league_split_results[k] = filtered_df
```
