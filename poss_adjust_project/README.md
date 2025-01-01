# The possession-adjusting project

_In many cases, possession is not nine-tenths of the law_

## Takeaways

Reassuringly for myself, the takeaways reflect the [previous work I did on the subject at the start of the decade](https://www.getgoalsideanalytics.com/duels-position-possession-adjusting/). There are essentially three strands to this:

1. The effects of possession share on defensive action numbers are so small as to be non-existent
2. The effects of possession share vary depending on player position
3. The effects of possession share vary (slightly less) depending on defensive action type

A few words can be found on these below, and results can be found in `data_exploration.md`.

**Effect of possession share on defensive action numbers are tiny (in this sample, at least)**
Summary: The correlation strengths are not really 'strengths' as much as 'presences'. There's generally no relationship between the amount of possession a player's team has and the amount of defensive actions they make. This is important, because 'players on teams with lower possession naturally make more defensive actions' is the fundamental premise of possession-adjusting player stats.

Technical: No correlation between the possession percentage of a player's team while they were on the pitch compared to their average defensive action statistics per 90 minutes reached a level of +-0.42. In most positions, they rarely reached a level of +-0.2.

**Different effects for different player positions**
Summary: Wide attackers seem to be affected most by possession, while the effects on defensive midfielders are the least.

Technical: The effects on Wing Back and Winger positions is curiously large in comparison with others. Each defensive action has a correlation stronger than -0.29 (all negative), with most stronger than -0.35. In other positions, only clearances for Attacking Midfielders has a correlation strength stronger than the -0.29 that represents the weakest correlation in the 'Wing Back-plus-Winger' set.

For Defensive Midfielders, no correlation is stronger than +-0.1, something almost shared by Full Backs (where there is, though, a stronger correlation among clearances (-0.19)). Defensive Midfielders, however, share a trait with Center Backs - positive correlations for some defensive action types (although still very, very weak ones).

Attacking Midfielders and Center Forwards form a halfway house between the Defensive Midfielders and Wing-Back/Winger groups. Generally, the correlations are between -0.1 and -0.25 in strength.

**Different effects for different defensive action types**
Summary: Clearances generally have the strongest negative correlation with possession (though still not a _strong_ correlation).

Technical: The standard deviation of correlations for defensive action type was around 0.05 for each group (6 of 10 falling between 0.04 and 0.06). This relatively small standard deviation has to be compared to the average correlation for defensive action types, which usually (in 7 of 10 cases) wasn't larger than +-0.19.

Clearances had the strongest negative correlation for 7 of 10 positions, although for Center Backs and Defensive Midfielders it was the _only_ negative correlation. (There is little point noting this, given the relatively small sample sizes and the absolutely small correlation strengths, but the position groups which are most associated with defending, Center Backs and Defensive Midfielders, actually have a _positive_ correlation between defensive action numbers and possession share in this sample).

## Data used

- Statsbomb openly-available event data
- 2015/16 seasons in the English Premier League, French Ligue 1, German Bundesliga, Italian Serie A, and Spanish La Liga

This repo contains a CSV of the aggregated data which is used directly for the results in `data_exploration.md`, though not each complete stage of data. That data is reproducible through the code files, however.

## Data gathering process

The basic dataset comes from 'player presence statistics' - i.e. stats that happen while a player is on-field. (The process for gathering this is described in `sb_data_pipeline/README.md`).

This provides the information for the possession percentage for a player's team while they're on the pitch, as well as their position during the match (more on both of these in 'Commentary').

It's then straightforward to fetch defensive action events from the Statsbomb event data, which is saved as `./poss_adjust_project/def_events.csv`.

## Commentary

### Implications of results

The practice of 'possession-adjusting' defensive statistics involves boosting the numbers for players on teams who have a lot of possession, and reducing the numbers for players on teams who have less.

The fundamental justification for this is the idea that players on teams without the ball spend more time defending, and therefore will inevitably make higher numbers of defensive actions. To put the idea another way, the lack of possession is 'boosting' their defensive action figures, and possession-adjusting puts a thumb on the scale to redress the balance.

However, if this were all the case, one would expect that possession share would be strongly correlated with the number of defensive actions that are made. This study has found that, when players are split by position, their defensive action numbers _do not_ have a strong correlation with possession share.

I don't want to completely disregard possession adjusting off the back of a very simple correlation analysis: it may be that the low correlation between possession share and defensive output is actually an offset of the quality gap between defensive players on high- and low-possession teams. In other words, perhaps there would be a link between defensive output and possession share _among players of similar quality_, but that this sample is obscured by the fact that (presumably) better defensive players are on high-possession teams and worse defensive players are on low-possession teams. This may be a case of finding steelmen in a field of scarecrows, but it is worth noting as a possibility.

### kloppy-Statsbomb event navigation

The premise of being able to navigate a set of event data without necessarily needing to be an expert in _that particular provider_ is tempting. Many of the differences between event data providers are merely differences of dialect than fundamental language (if that metaphor works). That said, the centralised/common framework relies on the sensibileness of the data providers, such that I imagine that users of a common framework will always need to refer to data provider documentation for _something_. I commend the contributors behind `kloppy` for their work and hope that the project continues to grow and improve.
