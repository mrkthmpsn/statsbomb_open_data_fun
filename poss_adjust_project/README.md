# The possession-adjusting project

_In many cases, possession is not nine-tenths of the law_

## Project structure

There are three data-gathering files in this project (which build off data-gathering processes in the `sb_data_pipeline` folder). There are then two markdown files exploring the aggregated data with some basic correlation analysis and commentary.

The final aggregated data, used the markdown investigation files, are saved in the `data` folder - other pieces of data are reproducible using the code in the rest of the repo.

## Data used

- Statsbomb openly-available event data
- 2015/16 seasons in the English Premier League, French Ligue 1, German Bundesliga, Italian Serie A, and Spanish La Liga

This repo contains CSVs of the aggregated data which are used directly for the results in `data_exploration.md` and `data_exploration_pt2.md`, though not each complete stage of data. That data is reproducible through the code files, however.

## Data gathering process

The basic dataset comes from 'player presence statistics' - i.e. stats that happen while a player is on-field. (The process for gathering this is described in `sb_data_pipeline/README.md`).

This provides the information for the possession percentage for a player's team while they're on the pitch, as well as their position during the match (more on both of these in 'Commentary').

It's then straightforward to fetch defensive action events from the Statsbomb event data, which is saved as `./poss_adjust_project/def_events.csv`.

## Takeaways

Note: This project and its initial investigation was updated on 11 January with a correction to an error in the code. General trends were unaffected, but some of the particularly unusual findings didn't hold up in the updated results data.

Reassuringly for myself, the takeaways generally reflect the [previous work I did on the subject at the start of the decade](https://www.getgoalsideanalytics.com/duels-position-possession-adjusting/). There are a few strands to this:

1. The effects of possession share on defensive action numbers are so small as to be non-existent
2. The effects of possession share vary depending on player position
3. The effects of possession share also vary depending on defensive action type
4. The amount of possession sequences does not seem to be strongly linked to the defensive output

Results and commentary can be found in `data_exploration.md` and `data_exploration_pt2.md`.

## Commentary

### Implications of results

The practice of 'possession-adjusting' defensive statistics involves boosting the numbers for players on teams who have a lot of possession, and reducing the numbers for players on teams who have less.

The fundamental justification for this is the idea that players on teams without the ball spend more time defending, and therefore will inevitably make higher numbers of defensive actions. To put the idea another way, the lack of possession is 'boosting' their defensive action figures, and possession-adjusting puts a thumb on the scale to redress the balance.

However, if this were all the case, one would expect that possession share would be strongly correlated with the number of defensive actions that are made. This study has found that, when players are split by position, their defensive action numbers _do not_ have a strong correlation with possession share.

I don't want to completely disregard possession adjusting off the back of a very simple correlation analysis: it may be that the low correlation between possession share and defensive output is actually an offset of the quality gap between defensive players on high- and low-possession teams. In other words, perhaps there would be a link between defensive output and possession share _among players of similar quality_, but that this sample is obscured by the fact that (presumably) better defensive players are on high-possession teams and worse defensive players are on low-possession teams. This may be a case of finding steelmen in a field of scarecrows, but it is worth noting as a possibility.

There is another way to approach this theory, that high-turnover football might produce players with higher defensive output figures. Within this sample, this does not appear to be the case either. This appears surprising, given that the theory seems straightforward, but team style may be a confounding factor - high turnover football can appear in multiple ways (tackles in midfield, clearances from long balls), so perhaps this cancels out general trends.

### kloppy-Statsbomb event navigation

The premise of being able to navigate a set of event data without necessarily needing to be an expert in _that particular provider_ is tempting. Many of the differences between event data providers are merely differences of dialect than fundamental language (if that metaphor works). That said, the centralised/common framework relies on the sensibileness of the data providers, such that I imagine that users of a common framework will always need to refer to data provider documentation for _something_. I commend the contributors behind `kloppy` for their work and hope that the project continues to grow and improve.
