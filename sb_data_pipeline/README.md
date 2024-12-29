# Saving Statsbomb open data

_'I apologise for the length of my data ingestion process; it would be smaller had I had the time'_

## Data/technologies used
✨ = new; 👨‍‍🏫 = learning; 🤝 = familiar

- **Statsbomb** open data 🤝
- `kloppy` as the main access point for the Statsbomb open data ✨
- `tqdm` as an indispensable progress bar during many-iteration processing tasks 🤝

## Outputs

The code contained in the `sb_data_pipeline` results in a number of files. These can roughly be split into groups of 'reference' and 'non-reference' data.

Reference data:

- `statsbomb_competition_seasons.json` and `statsbomb_season_matches.json`: information about competition-season and match availability in the Statsbomb open data, saved more or less directly from the `statsbombpy` package.
- `statsbomb_players.csv` and `statsbomb_teams.csv`: basic ID and name information collected from the `kloppy` dataset metadata and saved as reference data.

Non-reference data:

- `player_match_presence_stats.json`: a summary of the stats for a player's team and their opponents in matches they played in, as well as minutes played and position data

## Summary

In essence, the pipeline has two parts:

- Gather and save useful 'basic' data
- Do some more complicated data-fetching to save data about what happened when players were on the pitch, _specifically_ for the time they were on the field
  - (NOTE: at the moment, this doesn't account for red cards or injuries where a player was off-field receiving treatment)

### Basic data

File: `01_save_sb_season_matches_data.py`

- Fetch data on available competitions from `statsbombpy`

If a file `statsbomb_competition_seasons.json` doesn't already exist...

- Create the file using the data fetched from `statsbombpy`
- Iterate through the available competition-seasons and fetch the match data for each game, from `statsbombpy`

If the `statsbomb_competitions_seasons.json` _does_ exist...

- Load it and the `statsbomb_season_matches.json`, which should also exist
- Check for new seasons coming from `statsbombpy` which hadn't previously been saved
  - NOTE: This part of the process is still to be written

### 'On pitch' data

File: `02_proto_pipeline.py`

- Fetch relevant match IDs (using `statsbomb_season_matches.json`)
- For each match...
  - Fetch the match events
  - Use starting lineup and substitution events to gather the possession sequences that each player was on-field for
  - Iterate over players in the match and summarise certain stats for the sequences they were on-field for
  - Store these stats, along with the minutes that the player was on-field for, and their match position

## Commentary

The 'pipeline' is not an optimally efficient process. Part of that comes from wanting to get more familiar with the `kloppy` package; part is a 'my letter would have been shorter if I'd had the time' issue.

The desire to use `kloppy` means that there are repeated calls to the package's `statsbomb.load_open_data()` function _for the same match_. This is obviously inefficient, but I wanted to avoid the simpler approach of saving all of the raw event data and metadata, which could then have been used without calling on `kloppy`.
