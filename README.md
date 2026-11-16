# 🎵 VibeMatch 1.0: Music Recommender Simulation

## Project Summary

VibeMatch is a working CLI-first music recommender. It loads 20 fictional songs, scores each song against a taste profile, and returns the top five with reasons. It includes three advanced scoring modes and a classic mode for comparison. It uses Python's standard library.

## How The System Works

Real-world platforms combine listening behavior, patterns across users, and information about content. This simulator uses content-based filtering: it matches a song's attributes to the listener's stated preferences. It does not train a model or use other listeners' histories.

1. Load `data/songs.csv` as dictionaries, converting numbers and mood tags.
2. Read a user profile and select a scoring strategy.
3. Calculate each feature's similarity, then multiply it by its strategy weight.
4. Add the contributions, sort by descending score, and break ties by ascending song ID.
5. Return the top K songs with a reason for every scored feature.

### Song and User Data

`Song` stores all 15 CSV columns. The dictionary interface uses the same names. `UserProfile` stores the targets listed below; its object interface uses `favorite_genre`, `favorite_mood`, and `target_energy` for the three baseline preferences. The CLI dictionaries use `genre`, `mood`, and `energy`. Both interfaces now share the same scoring functions.

| Scored song attribute | Dictionary preference | Match rule |
|---|---|---|
| genre | genre | Exact label match, ignoring case and surrounding spaces |
| mood | mood | Exact label match, ignoring case and surrounding spaces |
| energy (0–1) | energy | One minus the absolute difference |
| popularity (0–100), new | target_popularity | One minus the gap divided by 100 |
| release_decade, new | preferred_decade | One minus the decade-year gap divided by 100 |
| duration_seconds, new | target_duration | One minus the gap in seconds divided by 300 |
| instrumentalness (0–1), new | target_instrumentalness | One minus the absolute difference |
| detailed_mood_tags, new | preferred_tags | Shared tags divided by all distinct tags across the song and preference |

Numerical similarities are clipped at zero. Larger values are not automatically better: each feature rewards closeness to the requested target. Release decades are multiples of 10 between 1900 and 2100; durations must be positive. Tags use `|` in the CSV and become tuples when loaded. Tag matching ignores case, whitespace, duplicates, and ordering. With no requested tags, the tag contribution is zero.

The baseline fields `id`, `title`, and `artist` identify results. Tempo, valence, danceability, and acousticness are retained but are not currently scored. The starter `likes_acoustic` preference is retained for compatibility but is not scored; acousticness and instrumentalness describe different properties.

### Scoring Modes and Design Pattern

The lightweight Strategy pattern uses a `ScoringStrategy` object for each weight preset. `src/scoring_modes.py` holds the registry. Shared matching logic stays in `src/recommender.py`, so each mode uses the same explanations, validation, and ranking rules. Switching a mode changes the weight policy rather than duplicating the scoring code.

| Feature | Genre-First | Mood-First | Energy-Focused |
|---|---:|---:|---:|
| genre | 0.30 | 0.10 | 0.10 |
| mood | 0.15 | 0.30 | 0.10 |
| energy | 0.15 | 0.15 | 0.40 |
| popularity | 0.08 | 0.05 | 0.07 |
| release_decade | 0.07 | 0.05 | 0.06 |
| duration_seconds | 0.07 | 0.05 | 0.07 |
| instrumentalness | 0.08 | 0.10 | 0.10 |
| detailed_mood_tags | 0.10 | 0.20 | 0.10 |

Every advanced mode gives positive weight to all five new attributes. Each mode's weights sum to 1, so scores range from 0 to 1. Scores are relevance points, not probabilities. `classic` uses only the original genre/mood/energy weights of 0.4/0.3/0.3. Functional and object APIs default to classic for compatibility; the CLI defaults to genre-first. Change `DEFAULT_MODE` in `main.py` or pass `--mode`.

All CLI profiles explicitly include the new preferences. For a basic three-field dictionary in an advanced mode, defaults are popularity 50, decade 2020, duration 210 seconds, instrumentalness 0.2, and no tags. These defaults influence results and should be adjusted for the listener.

## Getting Started

No third-party packages are required for the simulation or the added tests. Run these commands from the project root:

```bash
python -m src.main
python -m src.main --mode mood-first
python -m src.main --mode energy-focused --profile "Chill Lofi"
python -m src.main --mode classic
python -m src.main --help
```

### Running Tests

```bash
python -m unittest discover -s tests -p 'test_advanced_recommender.py' -v
```

All 11 added tests pass. They check the five new features independently, score totals, mode-sensitive rankings, classic rankings, tags, invalid values, tie-breaking, object/function consistency, and CLI execution. The original project test file was not provided, so it has not been run here.

## Advanced Mode Evaluation

All modes were run against all five profiles. This table summarizes the top three:

| Profile | Genre-First top 3 | Mood-First top 3 | Energy-Focused top 3 |
|---|---|---|---|
| High-Energy Pop | Sunrise City (0.960), Gym Hero (0.744), Rooftop Lights (0.652) | Sunrise City (0.928), Rooftop Lights (0.821), Gym Hero (0.522) | Sunrise City (0.955), Rooftop Lights (0.843), Gym Hero (0.761) |
| Chill Lofi | Midnight Coding (0.984), Library Rain (0.926), Focus Flow (0.795) | Midnight Coding (0.988), Library Rain (0.880), Spacewalk Thoughts (0.678) | Midnight Coding (0.979), Library Rain (0.915), Focus Flow (0.845) |
| Deep Intense Rock | Storm Runner (0.947), Gym Hero (0.574), No More Silence (0.439) | Storm Runner (0.917), Gym Hero (0.714), No More Silence (0.424) | Storm Runner (0.937), Gym Hero (0.773), No More Silence (0.687) |
| Edge Case: Sad High-Energy Pop | Sunrise City (0.700), Gym Hero (0.700), After the Goodbye (0.589) | After the Goodbye (0.794), Gym Hero (0.464), Sunrise City (0.463) | Gym Hero (0.746), Sunrise City (0.734), Storm Runner (0.683) |
| Edge Case: Unknown Labels and Zero Energy | Spacewalk Thoughts (0.435), Library Rain (0.384), Coffee Shop Stories (0.377) | Spacewalk Thoughts (0.460), Library Rain (0.367), Focus Flow (0.354) | Spacewalk Thoughts (0.615), Library Rain (0.547), Letters Unsent (0.547) |

For the same pop/happy profile, Mood-First places Rooftop Lights above Gym Hero because mood and detailed tags receive more weight. Genre-First keeps Gym Hero above Rooftop Lights. This demonstrates a mode change with the catalog and user profile held constant.

### Data and Bias Notes

The five new attributes were assigned as illustrative values for fictional songs. Popularity values are not real stream counts, and release decades are not verified release dates. Most genres still have only one example. Popularity matching can favor already popular songs when the listener requests high popularity. Detailed tags can double-count some mood information and reflect subjective labeling. Mode weights and normalization scales are design choices, not learned preferences. No listener study establishes that any mode is more accurate.

## Sample Recommendation Output

These are actual outputs for the same High-Energy Pop profile in each advanced mode. Running without `--profile` prints all five profiles.

### genre-first

```text
Loaded songs: 20

=== High-Energy Pop | mode=genre-first ===
User preferences: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'target_popularity': 85, 'preferred_decade': 2020, 'target_duration': 210, 'target_instrumentalness': 0.05, 'preferred_tags': ('euphoric', 'bright')}

Top 5 recommendations:

1. Sunrise City by Neon Echo
   Score: 0.960100
   Reasons:
   - genre: match=1.000, weight=0.30 (+0.300000)
   - mood: match=1.000, weight=0.15 (+0.150000)
   - energy: match=0.980, weight=0.15 (+0.147000)
   - popularity: match=0.970, weight=0.08 (+0.077600)
   - release_decade: match=1.000, weight=0.07 (+0.070000)
   - duration_seconds: match=0.983, weight=0.07 (+0.068833)
   - instrumentalness: match=1.000, weight=0.08 (+0.080000)
   - detailed_mood_tags: match=0.667, weight=0.10 (+0.066667)

2. Gym Hero by Max Pulse
   Score: 0.743633
   Reasons:
   - genre: match=1.000, weight=0.30 (+0.300000)
   - mood: match=0.000, weight=0.15 (+0.000000)
   - energy: match=0.870, weight=0.15 (+0.130500)
   - popularity: match=0.930, weight=0.08 (+0.074400)
   - release_decade: match=1.000, weight=0.07 (+0.070000)
   - duration_seconds: match=0.933, weight=0.07 (+0.065333)
   - instrumentalness: match=0.980, weight=0.08 (+0.078400)
   - detailed_mood_tags: match=0.250, weight=0.10 (+0.025000)

3. Rooftop Lights by Indigo Parade
   Score: 0.652300
   Reasons:
   - genre: match=0.000, weight=0.30 (+0.000000)
   - mood: match=1.000, weight=0.15 (+0.150000)
   - energy: match=0.960, weight=0.15 (+0.144000)
   - popularity: match=0.930, weight=0.08 (+0.074400)
   - release_decade: match=1.000, weight=0.07 (+0.070000)
   - duration_seconds: match=0.983, weight=0.07 (+0.068833)
   - instrumentalness: match=0.980, weight=0.08 (+0.078400)
   - detailed_mood_tags: match=0.667, weight=0.10 (+0.066667)

4. Cornerstone by Verse Atlas
   Score: 0.442167
   Reasons:
   - genre: match=0.000, weight=0.30 (+0.000000)
   - mood: match=0.000, weight=0.15 (+0.000000)
   - energy: match=0.990, weight=0.15 (+0.148500)
   - popularity: match=0.990, weight=0.08 (+0.079200)
   - release_decade: match=1.000, weight=0.07 (+0.070000)
   - duration_seconds: match=0.967, weight=0.07 (+0.067667)
   - instrumentalness: match=0.960, weight=0.08 (+0.076800)
   - detailed_mood_tags: match=0.000, weight=0.10 (+0.000000)

5. Daybreak Parade by Sol del Barrio
   Score: 0.421333
   Reasons:
   - genre: match=0.000, weight=0.30 (+0.000000)
   - mood: match=0.000, weight=0.15 (+0.000000)
   - energy: match=0.920, weight=0.15 (+0.138000)
   - popularity: match=0.870, weight=0.08 (+0.069600)
   - release_decade: match=0.800, weight=0.07 (+0.056000)
   - duration_seconds: match=0.833, weight=0.07 (+0.058333)
   - instrumentalness: match=0.930, weight=0.08 (+0.074400)
   - detailed_mood_tags: match=0.250, weight=0.10 (+0.025000)
```

### mood-first

```text
Loaded songs: 20

=== High-Energy Pop | mode=mood-first ===
User preferences: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'target_popularity': 85, 'preferred_decade': 2020, 'target_duration': 210, 'target_instrumentalness': 0.05, 'preferred_tags': ('euphoric', 'bright')}

Top 5 recommendations:

1. Sunrise City by Neon Echo
   Score: 0.928000
   Reasons:
   - genre: match=1.000, weight=0.10 (+0.100000)
   - mood: match=1.000, weight=0.30 (+0.300000)
   - energy: match=0.980, weight=0.15 (+0.147000)
   - popularity: match=0.970, weight=0.05 (+0.048500)
   - release_decade: match=1.000, weight=0.05 (+0.050000)
   - duration_seconds: match=0.983, weight=0.05 (+0.049167)
   - instrumentalness: match=1.000, weight=0.10 (+0.100000)
   - detailed_mood_tags: match=0.667, weight=0.20 (+0.133333)

2. Rooftop Lights by Indigo Parade
   Score: 0.821000
   Reasons:
   - genre: match=0.000, weight=0.10 (+0.000000)
   - mood: match=1.000, weight=0.30 (+0.300000)
   - energy: match=0.960, weight=0.15 (+0.144000)
   - popularity: match=0.930, weight=0.05 (+0.046500)
   - release_decade: match=1.000, weight=0.05 (+0.050000)
   - duration_seconds: match=0.983, weight=0.05 (+0.049167)
   - instrumentalness: match=0.980, weight=0.10 (+0.098000)
   - detailed_mood_tags: match=0.667, weight=0.20 (+0.133333)

3. Gym Hero by Max Pulse
   Score: 0.521667
   Reasons:
   - genre: match=1.000, weight=0.10 (+0.100000)
   - mood: match=0.000, weight=0.30 (+0.000000)
   - energy: match=0.870, weight=0.15 (+0.130500)
   - popularity: match=0.930, weight=0.05 (+0.046500)
   - release_decade: match=1.000, weight=0.05 (+0.050000)
   - duration_seconds: match=0.933, weight=0.05 (+0.046667)
   - instrumentalness: match=0.980, weight=0.10 (+0.098000)
   - detailed_mood_tags: match=0.250, weight=0.20 (+0.050000)

4. Daybreak Parade by Sol del Barrio
   Score: 0.406167
   Reasons:
   - genre: match=0.000, weight=0.10 (+0.000000)
   - mood: match=0.000, weight=0.30 (+0.000000)
   - energy: match=0.920, weight=0.15 (+0.138000)
   - popularity: match=0.870, weight=0.05 (+0.043500)
   - release_decade: match=0.800, weight=0.05 (+0.040000)
   - duration_seconds: match=0.833, weight=0.05 (+0.041667)
   - instrumentalness: match=0.930, weight=0.10 (+0.093000)
   - detailed_mood_tags: match=0.250, weight=0.20 (+0.050000)

5. Cornerstone by Verse Atlas
   Score: 0.392333
   Reasons:
   - genre: match=0.000, weight=0.10 (+0.000000)
   - mood: match=0.000, weight=0.30 (+0.000000)
   - energy: match=0.990, weight=0.15 (+0.148500)
   - popularity: match=0.990, weight=0.05 (+0.049500)
   - release_decade: match=1.000, weight=0.05 (+0.050000)
   - duration_seconds: match=0.967, weight=0.05 (+0.048333)
   - instrumentalness: match=0.960, weight=0.10 (+0.096000)
   - detailed_mood_tags: match=0.000, weight=0.20 (+0.000000)
```

### energy-focused

```text
Loaded songs: 20

=== High-Energy Pop | mode=energy-focused ===
User preferences: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'target_popularity': 85, 'preferred_decade': 2020, 'target_duration': 210, 'target_instrumentalness': 0.05, 'preferred_tags': ('euphoric', 'bright')}

Top 5 recommendations:

1. Sunrise City by Neon Echo
   Score: 0.955400
   Reasons:
   - genre: match=1.000, weight=0.10 (+0.100000)
   - mood: match=1.000, weight=0.10 (+0.100000)
   - energy: match=0.980, weight=0.40 (+0.392000)
   - popularity: match=0.970, weight=0.07 (+0.067900)
   - release_decade: match=1.000, weight=0.06 (+0.060000)
   - duration_seconds: match=0.983, weight=0.07 (+0.068833)
   - instrumentalness: match=1.000, weight=0.10 (+0.100000)
   - detailed_mood_tags: match=0.667, weight=0.10 (+0.066667)

2. Rooftop Lights by Indigo Parade
   Score: 0.842600
   Reasons:
   - genre: match=0.000, weight=0.10 (+0.000000)
   - mood: match=1.000, weight=0.10 (+0.100000)
   - energy: match=0.960, weight=0.40 (+0.384000)
   - popularity: match=0.930, weight=0.07 (+0.065100)
   - release_decade: match=1.000, weight=0.06 (+0.060000)
   - duration_seconds: match=0.983, weight=0.07 (+0.068833)
   - instrumentalness: match=0.980, weight=0.10 (+0.098000)
   - detailed_mood_tags: match=0.667, weight=0.10 (+0.066667)

3. Gym Hero by Max Pulse
   Score: 0.761433
   Reasons:
   - genre: match=1.000, weight=0.10 (+0.100000)
   - mood: match=0.000, weight=0.10 (+0.000000)
   - energy: match=0.870, weight=0.40 (+0.348000)
   - popularity: match=0.930, weight=0.07 (+0.065100)
   - release_decade: match=1.000, weight=0.06 (+0.060000)
   - duration_seconds: match=0.933, weight=0.07 (+0.065333)
   - instrumentalness: match=0.980, weight=0.10 (+0.098000)
   - detailed_mood_tags: match=0.250, weight=0.10 (+0.025000)

4. Cornerstone by Verse Atlas
   Score: 0.688967
   Reasons:
   - genre: match=0.000, weight=0.10 (+0.000000)
   - mood: match=0.000, weight=0.10 (+0.000000)
   - energy: match=0.990, weight=0.40 (+0.396000)
   - popularity: match=0.990, weight=0.07 (+0.069300)
   - release_decade: match=1.000, weight=0.06 (+0.060000)
   - duration_seconds: match=0.967, weight=0.07 (+0.067667)
   - instrumentalness: match=0.960, weight=0.10 (+0.096000)
   - detailed_mood_tags: match=0.000, weight=0.10 (+0.000000)

5. Daybreak Parade by Sol del Barrio
   Score: 0.653233
   Reasons:
   - genre: match=0.000, weight=0.10 (+0.000000)
   - mood: match=0.000, weight=0.10 (+0.000000)
   - energy: match=0.920, weight=0.40 (+0.368000)
   - popularity: match=0.870, weight=0.07 (+0.060900)
   - release_decade: match=0.800, weight=0.06 (+0.048000)
   - duration_seconds: match=0.833, weight=0.07 (+0.058333)
   - instrumentalness: match=0.930, weight=0.10 (+0.093000)
   - detailed_mood_tags: match=0.250, weight=0.10 (+0.025000)
```

## Earlier Evaluation and Weight Experiment

The following archived outputs were captured before adding advanced features. Their scores and order are still reproduced by `--mode classic`, although the current CLI uses the newer explanation format. They document the original three-feature experiment; they are not advanced-mode outputs.

## Archived Baseline Recommendation Output

Run `python -m src.main` to evaluate all five profiles. These outputs were captured from the expanded 20-song catalog shared during this project.

```text
Loaded songs: 20
```

### High-Energy Pop

```text
=== High-Energy Pop ===
User profile: genre=pop, mood=happy, energy=0.80

Top 5 recommendations:

1. Sunrise City by Neon Echo
   Score: 0.994
   Reasons:
   - genre match (+0.400)
   - mood match (+0.300)
   - energy similarity 0.980 (song=0.82, target=0.80; +0.294)

2. Gym Hero by Max Pulse
   Score: 0.661
   Reasons:
   - genre match (+0.400)
   - mood does not match (+0.000)
   - energy similarity 0.870 (song=0.93, target=0.80; +0.261)

3. Rooftop Lights by Indigo Parade
   Score: 0.588
   Reasons:
   - genre does not match (+0.000)
   - mood match (+0.300)
   - energy similarity 0.960 (song=0.76, target=0.80; +0.288)

4. Cornerstone by Verse Atlas
   Score: 0.297
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.990 (song=0.81, target=0.80; +0.297)

5. Night Drive Loop by Neon Echo
   Score: 0.285
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.950 (song=0.75, target=0.80; +0.285)
```

### Chill Lofi

```text
=== Chill Lofi ===
User profile: genre=lofi, mood=chill, energy=0.40

Top 5 recommendations:

1. Midnight Coding by LoRoom
   Score: 0.994
   Reasons:
   - genre match (+0.400)
   - mood match (+0.300)
   - energy similarity 0.980 (song=0.42, target=0.40; +0.294)

2. Library Rain by Paper Lanterns
   Score: 0.985
   Reasons:
   - genre match (+0.400)
   - mood match (+0.300)
   - energy similarity 0.950 (song=0.35, target=0.40; +0.285)

3. Focus Flow by LoRoom
   Score: 0.700
   Reasons:
   - genre match (+0.400)
   - mood does not match (+0.000)
   - energy similarity 1.000 (song=0.40, target=0.40; +0.300)

4. Spacewalk Thoughts by Orbit Bloom
   Score: 0.564
   Reasons:
   - genre does not match (+0.000)
   - mood match (+0.300)
   - energy similarity 0.880 (song=0.28, target=0.40; +0.264)

5. Coffee Shop Stories by Slow Stereo
   Score: 0.291
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.970 (song=0.37, target=0.40; +0.291)
```

### Deep Intense Rock

```text
=== Deep Intense Rock ===
User profile: genre=rock, mood=intense, energy=0.95

Top 5 recommendations:

1. Storm Runner by Voltline
   Score: 0.988
   Reasons:
   - genre match (+0.400)
   - mood match (+0.300)
   - energy similarity 0.960 (song=0.91, target=0.95; +0.288)

2. Gym Hero by Max Pulse
   Score: 0.594
   Reasons:
   - genre does not match (+0.000)
   - mood match (+0.300)
   - energy similarity 0.980 (song=0.93, target=0.95; +0.294)

3. No More Silence by Iron Harbor
   Score: 0.294
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.980 (song=0.97, target=0.95; +0.294)

4. Daybreak Parade by Sol del Barrio
   Score: 0.279
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.930 (song=0.88, target=0.95; +0.279)

5. Glass Labyrinth by Lumen Circuit
   Score: 0.276
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.920 (song=0.87, target=0.95; +0.276)
```

### Edge Case: Sad High-Energy Pop

```text
=== Edge Case: Sad High-Energy Pop ===
User profile: genre=pop, mood=sad, energy=0.90

Top 5 recommendations:

1. Gym Hero by Max Pulse
   Score: 0.691
   Reasons:
   - genre match (+0.400)
   - mood does not match (+0.000)
   - energy similarity 0.970 (song=0.93, target=0.90; +0.291)

2. Sunrise City by Neon Echo
   Score: 0.676
   Reasons:
   - genre match (+0.400)
   - mood does not match (+0.000)
   - energy similarity 0.920 (song=0.82, target=0.90; +0.276)

3. After the Goodbye by Clara Vale
   Score: 0.417
   Reasons:
   - genre does not match (+0.000)
   - mood match (+0.300)
   - energy similarity 0.390 (song=0.29, target=0.90; +0.117)

4. Storm Runner by Voltline
   Score: 0.297
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.990 (song=0.91, target=0.90; +0.297)

5. Daybreak Parade by Sol del Barrio
   Score: 0.294
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.980 (song=0.88, target=0.90; +0.294)
```

### Edge Case: Unknown Labels and Zero Energy

```text
=== Edge Case: Unknown Labels and Zero Energy ===
User profile: genre=blues, mood=dreamy, energy=0.00

Top 5 recommendations:

1. Letters Unsent by Elena Frost
   Score: 0.228
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.760 (song=0.24, target=0.00; +0.228)

2. Spacewalk Thoughts by Orbit Bloom
   Score: 0.216
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.720 (song=0.28, target=0.00; +0.216)

3. After the Goodbye by Clara Vale
   Score: 0.213
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.710 (song=0.29, target=0.00; +0.213)

4. Golden Porch by Willow Creek
   Score: 0.204
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.680 (song=0.32, target=0.00; +0.204)

5. Library Rain by Paper Lanterns
   Score: 0.195
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.650 (song=0.35, target=0.00; +0.195)
```

---

## Experiments You Tried

I evaluated three distinct taste profiles and two edge cases using the same scoring weights and catalog:

- **High-Energy Pop:** Sunrise City ranks first (0.994), matching genre and mood with energy close to 0.80. Gym Hero ranks second because genre has more weight than mood.
- **Chill Lofi:** Midnight Coding (0.994) and Library Rain (0.985) lead. Focus Flow ranks third despite its different mood because it matches genre and target energy.
- **Deep Intense Rock:** Storm Runner ranks first (0.988). Gym Hero ranks second through its intense mood and similar energy, even though it is pop. Related genres such as metal do not receive a rock genre bonus.
- **Sad High-Energy Pop:** This combination is valid, but no song in the catalog matches all three preferences. Gym Hero ranks first (0.691), while the only sad song, After the Goodbye, ranks third (0.417). The result shows how the fixed genre bonus can outweigh the requested mood and how a top-ranked song can still miss an important preference.
- **Unknown Labels and Zero Energy:** Neither blues nor dreamy appears in the catalog. All songs therefore receive only energy similarity points. Letters Unsent ranks first (0.228) because its energy, 0.24, is lowest. The system still returns five songs without a warning or minimum score, even though none matches the genre or mood.

These checks verify ranking behavior under the stated recipe. They do not establish whether real listeners would enjoy the songs. The results suggest allowing users to change weights, supporting related labels, and warning when the catalog has no strong matches.

### Weight Shift Experiment

I temporarily halved the genre weight from 0.4 to 0.2 and doubled the energy weight from 0.3 to 0.6, leaving mood at 0.3. I ran `python -m src.main` again with the same five profiles and 20 songs.

```text
experimental_score = 0.2 * genre_match + 0.3 * mood_match + 0.6 * energy_match
```

The math remains valid: each component is nonnegative, and the maximum total is 1.1. The scores are relevance points, not probabilities. Dividing every experimental score by 1.1 would put them on a 0–1 scale without changing their order. Higher raw scores alone do not indicate an improvement because the total weight changed.

| Profile | Original top 5 | Energy-shift top 5 |
|---|---|---|
| High-Energy Pop | Sunrise City → Gym Hero → Rooftop Lights → Cornerstone → Night Drive Loop | Sunrise City → Rooftop Lights → Gym Hero → Cornerstone → Night Drive Loop |
| Chill Lofi | Midnight Coding → Library Rain → Focus Flow → Spacewalk Thoughts → Coffee Shop Stories | Midnight Coding → Library Rain → Spacewalk Thoughts → Focus Flow → Coffee Shop Stories |
| Deep Intense Rock | Storm Runner → Gym Hero → No More Silence → Daybreak Parade → Glass Labyrinth | Storm Runner → Gym Hero → No More Silence → Daybreak Parade → Glass Labyrinth |
| Edge Case: Sad High-Energy Pop | Gym Hero → Sunrise City → After the Goodbye → Storm Runner → Daybreak Parade | Gym Hero → Sunrise City → Storm Runner → Daybreak Parade → Glass Labyrinth |
| Edge Case: Unknown Labels and Zero Energy | Letters Unsent → Spacewalk Thoughts → After the Goodbye → Golden Porch → Library Rain | Letters Unsent → Spacewalk Thoughts → After the Goodbye → Golden Porch → Library Rain |

For Chill Lofi, Spacewalk Thoughts moves above Focus Flow: its chill mood and energy similarity now outweigh Focus Flow's genre match and exact energy. Spacewalk Thoughts earns 0.828, while Focus Flow earns 0.800.

For High-Energy Pop, Rooftop Lights moves above Gym Hero. Its happy mood and closer energy outweigh Gym Hero's pop genre bonus. In the sad/high-energy case, After the Goodbye falls out of the top five because its energy is far below the target. For unknown genre and mood labels, the ranking stays the same because energy was already the only contributing feature.

The change produced different tradeoffs, rather than demonstrated better accuracy. It favors the desired energy and sometimes mood over genre, which could help listeners seeking a particular vibe. However, it makes the sad/high-energy example less responsive to the requested sadness. Without real listener feedback, I cannot claim the recommendations became more accurate. I restored the original 0.4/0.3/0.3 weights after capturing this experiment.

#### Captured Experimental CLI Output

```text
Loaded songs: 20

=== High-Energy Pop ===
User profile: genre=pop, mood=happy, energy=0.80

Top 5 recommendations:

1. Sunrise City by Neon Echo
   Score: 1.088
   Reasons:
   - genre match (+0.200)
   - mood match (+0.300)
   - energy similarity 0.980 (song=0.82, target=0.80; +0.588)

2. Rooftop Lights by Indigo Parade
   Score: 0.876
   Reasons:
   - genre does not match (+0.000)
   - mood match (+0.300)
   - energy similarity 0.960 (song=0.76, target=0.80; +0.576)

3. Gym Hero by Max Pulse
   Score: 0.722
   Reasons:
   - genre match (+0.200)
   - mood does not match (+0.000)
   - energy similarity 0.870 (song=0.93, target=0.80; +0.522)

4. Cornerstone by Verse Atlas
   Score: 0.594
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.990 (song=0.81, target=0.80; +0.594)

5. Night Drive Loop by Neon Echo
   Score: 0.570
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.950 (song=0.75, target=0.80; +0.570)

=== Chill Lofi ===
User profile: genre=lofi, mood=chill, energy=0.40

Top 5 recommendations:

1. Midnight Coding by LoRoom
   Score: 1.088
   Reasons:
   - genre match (+0.200)
   - mood match (+0.300)
   - energy similarity 0.980 (song=0.42, target=0.40; +0.588)

2. Library Rain by Paper Lanterns
   Score: 1.070
   Reasons:
   - genre match (+0.200)
   - mood match (+0.300)
   - energy similarity 0.950 (song=0.35, target=0.40; +0.570)

3. Spacewalk Thoughts by Orbit Bloom
   Score: 0.828
   Reasons:
   - genre does not match (+0.000)
   - mood match (+0.300)
   - energy similarity 0.880 (song=0.28, target=0.40; +0.528)

4. Focus Flow by LoRoom
   Score: 0.800
   Reasons:
   - genre match (+0.200)
   - mood does not match (+0.000)
   - energy similarity 1.000 (song=0.40, target=0.40; +0.600)

5. Coffee Shop Stories by Slow Stereo
   Score: 0.582
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.970 (song=0.37, target=0.40; +0.582)

=== Deep Intense Rock ===
User profile: genre=rock, mood=intense, energy=0.95

Top 5 recommendations:

1. Storm Runner by Voltline
   Score: 1.076
   Reasons:
   - genre match (+0.200)
   - mood match (+0.300)
   - energy similarity 0.960 (song=0.91, target=0.95; +0.576)

2. Gym Hero by Max Pulse
   Score: 0.888
   Reasons:
   - genre does not match (+0.000)
   - mood match (+0.300)
   - energy similarity 0.980 (song=0.93, target=0.95; +0.588)

3. No More Silence by Iron Harbor
   Score: 0.588
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.980 (song=0.97, target=0.95; +0.588)

4. Daybreak Parade by Sol del Barrio
   Score: 0.558
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.930 (song=0.88, target=0.95; +0.558)

5. Glass Labyrinth by Lumen Circuit
   Score: 0.552
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.920 (song=0.87, target=0.95; +0.552)

=== Edge Case: Sad High-Energy Pop ===
User profile: genre=pop, mood=sad, energy=0.90

Top 5 recommendations:

1. Gym Hero by Max Pulse
   Score: 0.782
   Reasons:
   - genre match (+0.200)
   - mood does not match (+0.000)
   - energy similarity 0.970 (song=0.93, target=0.90; +0.582)

2. Sunrise City by Neon Echo
   Score: 0.752
   Reasons:
   - genre match (+0.200)
   - mood does not match (+0.000)
   - energy similarity 0.920 (song=0.82, target=0.90; +0.552)

3. Storm Runner by Voltline
   Score: 0.594
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.990 (song=0.91, target=0.90; +0.594)

4. Daybreak Parade by Sol del Barrio
   Score: 0.588
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.980 (song=0.88, target=0.90; +0.588)

5. Glass Labyrinth by Lumen Circuit
   Score: 0.582
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.970 (song=0.87, target=0.90; +0.582)

=== Edge Case: Unknown Labels and Zero Energy ===
User profile: genre=blues, mood=dreamy, energy=0.00

Top 5 recommendations:

1. Letters Unsent by Elena Frost
   Score: 0.456
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.760 (song=0.24, target=0.00; +0.456)

2. Spacewalk Thoughts by Orbit Bloom
   Score: 0.432
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.720 (song=0.28, target=0.00; +0.432)

3. After the Goodbye by Clara Vale
   Score: 0.426
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.710 (song=0.29, target=0.00; +0.426)

4. Golden Porch by Willow Creek
   Score: 0.408
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.680 (song=0.32, target=0.00; +0.408)

5. Library Rain by Paper Lanterns
   Score: 0.390
   Reasons:
   - genre does not match (+0.000)
   - mood does not match (+0.000)
   - energy similarity 0.650 (song=0.35, target=0.00; +0.390)
```

---

## Limitations and Risks

The catalog is small and synthetic. Exact genre and mood labels miss related styles. Fixed weights can overlook important preferences, and the system still returns top-five results without a minimum-match threshold. The advanced defaults also affect users who provide only basic preferences. New metadata adds detail but does not establish real listening quality.

## Reflection

The project showed how a simple set of rules can produce different recommendations for different profiles. The weight experiment and scoring modes also showed that different rankings do not necessarily mean better recommendations. Explanations helped verify the math and identify missing preferences.

See [model_card.md](model_card.md) for the full evaluation and reflection, and [ai_interactions.md](ai_interactions.md) for the challenge workflow and verification notes.
