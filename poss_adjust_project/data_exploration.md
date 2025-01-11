# Exploring the data of team possession share and player defensive output in the 2015/16 'Big Five' men's European leagues

Note: This write-up was updated on 11 January with a correction to an error in the code. General trends were unaffected, but some of the particularly unusual findings didn't hold up in the updated results data.

## Results

The table below shows the data which the `Code` section produces. Left-to-right, the columns represent:

- player positions
- a count of the number of players who met a threshold of 450 minutes played in that position
- then, correlations between the share of possession that the player's team had during their time in that position compared with their average number of defensive actions per 90 minutes
- finally, the standard deviation and mean average of the correlations for that general position.

|     | general_position     | count | clear_90 | tack_90 | block_90 | drib_past_90 | interc_90 | pressure_90 | corr_stdev | corr_mean |
| --: | :------------------- | ----: | -------: | ------: | -------: | -----------: | --------: | ----------: | ---------: | --------: |
|   0 | Attacking Midfielder |    57 |   -0.227 |  -0.208 |   -0.415 |       -0.172 |    -0.228 |      -0.251 |      0.085 |     -0.25 |
|   1 | Center Back          |   381 |   -0.359 |  -0.003 |   -0.165 |        0.025 |     0.043 |      -0.134 |      0.154 |    -0.099 |
|   2 | Center Forward       |   197 |   -0.133 |  -0.111 |   -0.296 |       -0.009 |    -0.101 |      -0.242 |      0.104 |    -0.149 |
|   3 | Center Midfielder    |   148 |   -0.355 |  -0.082 |   -0.301 |       -0.111 |    -0.172 |      -0.272 |       0.11 |    -0.216 |
|   4 | Defensive Midfielder |   302 |    -0.21 |  -0.069 |   -0.167 |       -0.062 |    -0.087 |      -0.206 |      0.069 |    -0.134 |
|   5 | Full Back            |   361 |   -0.327 |  -0.129 |   -0.191 |        -0.08 |    -0.083 |      -0.169 |      0.092 |    -0.163 |
|   6 | Goalkeeper           |   142 |    0.016 |  -0.012 |   -0.044 |       -0.222 |     0.004 |      -0.144 |      0.095 |    -0.067 |
|   7 | Wide Midfielder      |    90 |   -0.314 |  -0.249 |   -0.189 |       -0.214 |    -0.286 |      -0.394 |      0.074 |    -0.274 |
|   8 | Wing Back            |    31 |   -0.323 |  -0.233 |   -0.016 |       -0.051 |    -0.376 |       -0.18 |      0.144 |    -0.197 |
|   9 | Winger               |   136 |   -0.307 |  -0.312 |   -0.268 |       -0.225 |    -0.319 |      -0.377 |      0.051 |    -0.301 |

### A note on positions and minutes

The position assignation is a little imperfect on _my_ side of things. I've taken one position per player per match, which I take to be the starting position. Equally, the cut-off point for minutes played (450) is based on how many minutes a player has played in this 'single-position-assignation-per-match'.

This could introduce problems like a player starting as a 'Center Midfielder' but moving to a Full-Back position early in a match; if they did this several times, that could affect not only what position their defensive actions would count under but also potentially in them meeting the minutes threshold.

The minutes played are 'full' minutes, rather than 'capped' (see a [recent piece by Eliot McKinley on the effect of capping minutes played at 90](https://www.americansocceranalysis.com/home/2024/12/8/stoppage-time-matters-how-substitutions-and-using-all-minutes-played-affect-player-statistics)).

### Commentary

#### Weak, generally negative correlations

Although the general tendency is for a higher possession share to be linked with a lower defensive action output, the correlations are generally very weak.

#### Block and clearance link strength

The defensive actions most strongly linked to possession share appear to be clearances and blocked shots. This would make sense when possession is viewed through its link to team quality.

#### Wide, attacking positions

The strongest correlations come in the Wide Midfielder and Winger positions. Attacking Midfielder group is relatively close behind, although the gap is slightly larger when excluding clearances and blocks from consideration (focusing on more 'open-field' defensive action types).

This comparison to the weaker correlation strengths for Center Back and Defensive Midfielder groups, the ones considered most 'defensive', is particularly notable.

#### Defensive vs Center Midfield

It seems interesting that the 'Center Midfielder' category has so many fewer players who meet the 450 minutes threshold than 'Defensive Midfielder'. My theory would be that in a 4-2-3-1 formation, the two 'double pivots' are classified by Statsbomb as left and right 'defensive' midfielders rather than 'center' midfielders. (The median `mins_played` value for qualifying players is noticeably higher for the Defensive Midfielder category (1066.2) than 'Center Midfielder' (762.5) too, so it doesn't look like this is caused by lots of Defensive Midfielder players sneaking just above the threshold).

## Code

### Load the data

```python
import statistics
import pandas as pd


combined_df = pd.read_csv("./poss_adjust_project/data/aggregated_data.csv")
```

### Create aggregated data

```python
corr_action_col_names = [
    f"{action}_90"
    for action in ["clear", "tack", "block", "drib_past", "interc", "pressure"]
]
correlation_results = combined_df[["poss_pct", *corr_action_col_names]].corr()

# Count the number of instances for each general_position
position_counts = (
    combined_df.groupby("general_position").size().reset_index(name="count")
)

# Group by general_position and calculate correlation for each group
grouped_correlations = (
    combined_df.groupby("general_position")[["poss_pct", *corr_action_col_names]]
    .corr()
    .unstack()
    .reset_index()
)
grouped_correlations = grouped_correlations[[col for col in grouped_correlations.columns if col[0] in ['general_position', 'poss_pct']]]
grouped_correlations.columns = grouped_correlations.columns.map(
    lambda x: (
        x[1]
        if x[0] == "poss_pct"
        else x[0] if len(x) == 2 and x[1] != "poss_pct" else x
    )
)
grouped_correlations = position_counts.merge(grouped_correlations).drop(columns=['poss_pct'])

grouped_correlations["corr_stdev"] = grouped_correlations.apply(
    lambda row: statistics.stdev([row[action] for action in corr_action_col_names]),
    axis=1,
)
grouped_correlations["corr_mean"] = grouped_correlations.apply(
    lambda row: statistics.mean([row[action] for action in corr_action_col_names]),
    axis=1,
)
grouped_correlations["open_field_corr_mean"] = grouped_correlations.apply(
    lambda row: statistics.mean([row[action] for action in ['tack_90', 'drib_past_90', 'interc_90', 'pressure_90']]),
    axis=1,
)

for col_name in [*corr_action_col_names, 'corr_stdev', 'corr_mean']:
    grouped_correlations[col_name] = grouped_correlations[col_name].round(decimals=3)
```
