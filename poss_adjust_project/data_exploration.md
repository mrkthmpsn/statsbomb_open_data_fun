# Exploring the data of team possession share and player defensive output in the 2015/16 'Big Five' men's European leagues

## Results

The table below shows the data which the `Code` section produces. Left-to-right, the columns represent:

- player positions
- a count of the number of players who met a threshold of 450 minutes played in that position
- then, correlations between the share of possession that the player's team had during their time in that position compared with their average number of defensive actions per 90 minutes
- finally, the standard deviation and mean average of the correlations for that general position.

|     | general_position     | count | clear_90 | tack_90 | block_90 | drib_past_90 | interc_90 | pressure_90 | corr_stdev | corr_mean |
| --: | :------------------- | ----: | -------: | ------: | -------: | -----------: | --------: | ----------: | ---------: | --------: |
|   0 | Attacking Midfielder |    57 |   -0.345 |   -0.22 |   -0.282 |       -0.216 |    -0.296 |      -0.228 |      0.052 |    -0.265 |
|   1 | Center Back          |   381 |   -0.118 |   0.132 |    0.087 |        0.144 |      0.12 |       0.104 |      0.098 |     0.078 |
|   2 | Center Forward       |   197 |    -0.19 |  -0.185 |    -0.27 |       -0.126 |     -0.13 |      -0.214 |      0.054 |    -0.186 |
|   3 | Center Midfielder    |   148 |   -0.253 |  -0.118 |    -0.19 |        -0.09 |    -0.186 |       -0.16 |      0.058 |    -0.166 |
|   4 | Defensive Midfielder |   302 |   -0.034 |   0.081 |    0.037 |        0.099 |     0.054 |       0.032 |      0.046 |     0.045 |
|   5 | Full Back            |   361 |    -0.19 |  -0.067 |   -0.101 |        -0.03 |    -0.071 |      -0.066 |      0.055 |    -0.087 |
|   6 | Goalkeeper           |   142 |    0.017 |  -0.018 |   -0.042 |       -0.223 |     0.004 |       -0.11 |      0.091 |    -0.062 |
|   7 | Wide Midfielder      |    90 |   -0.205 |   -0.17 |   -0.103 |       -0.183 |    -0.203 |       -0.13 |      0.041 |    -0.166 |
|   8 | Wing Back            |    31 |   -0.418 |  -0.407 |   -0.327 |       -0.379 |     -0.38 |      -0.382 |      0.032 |    -0.382 |
|   9 | Winger               |   136 |   -0.355 |  -0.339 |   -0.365 |       -0.297 |    -0.309 |      -0.386 |      0.034 |    -0.342 |

### A note on positions and minutes

The position assignation is a little imperfect on _my_ side of things. I've taken one position per player per match, which I take to be the starting position. Equally, the cut-off point for minutes played (450) is based on how many minutes a player has played in this 'single-position-assignation-per-match'.

This could introduce problems like a player starting as a 'Center Midfielder' but moving to a Full-Back position early in a match; if they did this several times, that could affect not only what position their defensive actions would count under but also potentially in them meeting the minutes threshold.

The minutes played are 'full' minutes, rather than 'capped' (see a [recent piece by Eliot McKinley on the effect of capping minutes played at 90](https://www.americansocceranalysis.com/home/2024/12/8/stoppage-time-matters-how-substitutions-and-using-all-minutes-played-affect-player-statistics)).

### Commentary

#### Weak, mostly negative correlations

Although the general tendency is for a higher possession share to be linked with a lower defensive action output, the correlations are generally very weak.

The (very weak, barely present) positive correlations for Center Back and Defensive Midfielder categories are notable. Even if they don't indicate that higher possession share is linked with _higher_ defensive action output, they're notable for how clearly they show the _lack_ of link between the two variables.

#### Wide, attacking positions

The strongest correlations come in the Winger and Wing Back positions (although the sample of players who meet the minutes threshold for Wing Back is very small).

However, this may be a symptom of the role requirements differing within the same position based on team strength (which is often linked to possession share). For example, wingers in a weaker team will often spend more time 'in the midfield line' than 'in the forward line' when out of possession, as the team is pushed into a deeper block.

That all said, if the suspicion that stronger correlations for the 'Winger' position is a symptom of team strength differences, this raises interesting philosophical questions about the extent that 'role' assignations can be made independently from team strength.

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

for col_name in [*corr_action_col_names, 'corr_stdev', 'corr_mean']:
    grouped_correlations[col_name] = grouped_correlations[col_name].round(decimals=3)
```
