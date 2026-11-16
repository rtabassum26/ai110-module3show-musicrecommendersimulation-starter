# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world platforms such as Spotify and YouTube use listening or viewing history, likes, skips, and patterns across users to predict what someone might enjoy. Collaborative filtering uses other users' behavior, while content-based filtering matches item attributes to a user's preferences. My simulator will use content-based filtering and prioritize genre, mood, and energy, with genre receiving slightly more weight than the other features.

The song dictionaries use these fields:

- `Song`: `id`, `title`, and `artist` to identify and display each song; `genre`, `mood`, and `energy` for scoring. Energy ranges from 0 to 1.
- The CLI user preference dictionary uses `genre`, `mood`, and `energy`, with target energy ranging from 0 to 1. The starter `UserProfile` dataclass uses `favorite_genre`, `favorite_mood`, `target_energy`, and `likes_acoustic`; its OOP recommendation methods are still placeholders.

### Example User Profile

An alternative profile represents someone looking for calm study music. The CLI evaluates five profiles, starting with pop, happy, and energy 0.80:

```python
user_profile = {
    "genre": "lofi",
    "mood": "chill",
    "energy": 0.40,
}
```

### Algorithm Recipe

For each song in the CSV:

1. Award **0.4 points** if its genre exactly matches the preferred genre.
2. Award **0.3 points** if its mood exactly matches the preferred mood.
3. Add up to **0.3 points** based on how close its energy is to the target:

```text
energy_match = 1 - abs(song.energy - user_prefs["energy"])
score = 0.4 * genre_match + 0.3 * mood_match + 0.3 * energy_match
```

Genre and mood matches each equal 1 for an exact match and 0 otherwise. Both energy values must be between 0 and 1. An exact energy match earns the full 0.3 points; larger differences earn fewer points. The total score ranges from 0 to 1 and measures relevance under these rules, rather than the probability that the user will like a song.

After scoring every song, sort by highest score first, break ties by ascending song ID, and return the top K songs. Genre has the largest individual weight because musical style matters, while mood and energy together contribute 60% of the score to account for the desired vibe.

### Data Flow

1. **Input:** Load the song catalog from `data/songs.csv` and the user preference dictionary.
2. **Process:** Loop through every song, calculate its score, and store the song with its score.
3. **Rank:** Sort the complete scored list using the ranking rule.
4. **Output:** Return the first K recommendations.

For example, Midnight Coding matches the example profile's genre and mood and has energy 0.42. It earns `0.4 + 0.3 + 0.3 * (1 - abs(0.42 - 0.40)) = 0.994`, then joins the list to be ranked against the other songs.

### Expected Biases

- **Genre preference:** Exact genre matches receive the largest individual bonus, so a suitable song from another genre may rank lower even if it fits the user's mood and energy.
- **Limited discovery:** Repeatedly favoring existing preferences may create a filter bubble and reduce exposure to unfamiliar styles.
- **Labels and catalog coverage:** Mood labels are subjective, and exact matching treats related labels such as `chill` and `relaxed` as different. The small catalog also gives genres with more songs more opportunities to appear in the recommendations.


---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

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

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



