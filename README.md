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

An alternative profile represents someone looking for calm study music. The CLI defaults to pop, happy, and energy 0.80:

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

Running `python -m src.main` with the expanded 20-song catalog and the default pop/happy profile produces:

```text
Loaded songs: 20
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

Sunrise City ranks first because it matches both genre and mood and has energy close to the target. Gym Hero ranks above Rooftop Lights because the genre match contributes more than the mood match. Cornerstone and Night Drive Loop receive only energy similarity points.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

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



