# 🎧 Model Card: VibeMatch 1.0

## 1. Model Name

**VibeMatch 1.0** — a simple music recommendation simulator.

---

## 2. Goal and Intended Use

The goal is to suggest songs that match a listener's preferred genre, mood, and energy. The system returns a ranked list with a score and reasons for each song.

**Intended use:** Classroom learning and small experiments with music preferences. It shows how data and scoring rules become recommendations.

**Non-intended use:** A production streaming service or a reliable prediction of someone's musical taste. It should not be used to judge song quality, artist value, or a listener's emotional state.

---

## 3. How the Model Works

This is a content-based system. It compares song attributes with one user's preferences. It does not learn from other listeners or train a machine learning model.

A genre match earns 0.4 points. A mood match earns 0.3 points. Energy earns up to 0.3 points, with more points for being closer to the user's target. Higher energy is not automatically better.

The system scores every song and sorts from highest to lowest. If scores tie, the smaller song ID comes first. It returns the top five songs in the CLI. Each result explains where its points came from. A score measures the match under these rules, not the chance that someone will enjoy the song.

I added CSV loading, numerical conversion, weighted scoring, explanations, and ranking to the starter functions. The CLI uses the dictionary-based functions. The starter OOP recommendation methods are still placeholders.

---

## 4. Data Used

The catalog contains 20 fictional songs. I kept the 10 starter songs and added 10 AI-generated examples. The added songs broaden the genres and moods. Their numerical values are illustrative, not measured from audio.

Each song has an ID, title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. The current score uses only genre, mood, and energy. IDs break ties, while titles and artists identify the results.

The catalog includes pop, lofi, rock, jazz, ambient, synthwave, indie pop, folk, soul, country, rnb, metal, hip hop, reggae, techno, classical, and salsa. Lofi has three songs, pop has two, and each other genre has one. Moods include happy, chill, intense, sad, and relaxed.

The dataset is too small to represent the full range of musical taste. It has no audio, lyrics, listening history, or real listener ratings. Some preferences, such as blues and dreamy, have no matching labels.

---

## 5. Strengths

The rules are easy to follow. Each recommendation shows its score and reasons.

The standard profiles produce sensible results based on the song attributes. Sunrise City leads for happy pop, Midnight Coding leads for chill lofi, and Storm Runner leads for intense rock. Energy matching rewards closeness to the requested intensity, including calm preferences.

---

## 6. Limitations and Bias

The fixed genre bonus can favor familiar styles and limit discovery, creating a possible filter bubble. For sad, high-energy pop, two songs without the sad label ranked above the only sad song. Doubling the energy weight pushed that sad song out of the top five. Exact matching also treats related labels, such as chill and relaxed, as unrelated. When genre and mood are missing from the catalog, the system still returns five songs based only on energy, even if the matches are weak.

---

## 7. Evaluation

I tested five profiles against the same 20-song catalog and checked each profile's top five songs, scores, and reasons. The comparisons below use the original weights: genre 0.4, mood 0.3, and energy 0.3. Full terminal outputs are recorded in `README.md`.

### Profiles Tested

| Profile | Preferred genre | Preferred mood | Target energy | First recommendation |
|---|---|---|---|---|
| High-Energy Pop | pop | happy | 0.80 | Sunrise City |
| Chill Lofi | lofi | chill | 0.40 | Midnight Coding |
| Deep Intense Rock | rock | intense | 0.95 | Storm Runner |
| Sad High-Energy Pop | pop | sad | 0.90 | Gym Hero |
| Unknown Labels and Zero Energy | blues | dreamy | 0.00 | Letters Unsent |

### What Surprised Me

Gym Hero appeared in the happy pop, intense rock, and sad pop lists. For happy pop, it ranks second because it is pop and has similar energy, even though its mood is intense. For intense rock, it ranks second because its intense mood and high energy fit. For sad pop, it ranks first because its pop genre and energy outweigh its missing sad mood match. This shows that a high rank means the song fits the scoring rules, rather than every preference.

Coffee Shop Stories could seem suitable for calm studying, but it receives no mood bonus for the Chill Lofi profile because relaxed and chill are treated as different labels. I was also surprised that the unknown-label profile still received five recommendations, even though none matched its genre or mood.

### Comparing Every Pair of Profiles

| Profile pair | What changed and why it makes sense under our rules |
|---|---|
| High-Energy Pop vs. Chill Lofi | Sunrise City leads the pop list, while Midnight Coding leads the lofi list. The preferences shift from happy, energetic pop toward calmer, chill lofi, and each leading song matches the requested genre and mood. |
| High-Energy Pop vs. Deep Intense Rock | The leader changes from Sunrise City to Storm Runner as the preferred genre changes to rock, the mood becomes intense, and the energy target rises. Gym Hero stays second in both lists: it matches genre for pop listeners and mood for intense-rock listeners. |
| High-Energy Pop vs. Sad High-Energy Pop | Gym Hero moves from second to first, while Sunrise City moves to second. Sunrise City loses its happy-mood bonus when the request becomes sad, and Gym Hero is closer to the new energy target of 0.90. After the Goodbye enters third because it is sad. |
| High-Energy Pop vs. Unknown Labels and Zero Energy | Sunrise City leads the pop list, but Letters Unsent leads the unknown-label list. With no blues or dreamy songs available, only energy counts, so the lowest-energy song wins instead of a pop or happy match. |
| Chill Lofi vs. Deep Intense Rock | Midnight Coding and Library Rain lead the calm list, while Storm Runner and Gym Hero lead the intense list. Changing genre, mood, and energy together shifts the results toward more intense songs; the two top-five lists have no songs in common. |
| Chill Lofi vs. Sad High-Energy Pop | The lofi list starts with Midnight Coding, while the sad pop list starts with Gym Hero and Sunrise City. The pop request rewards a different genre and much higher energy, even though those two pop songs do not match sadness; the two top-five lists have no songs in common. |
| Chill Lofi vs. Unknown Labels and Zero Energy | Midnight Coding leads when lofi and chill bonuses are available, but Letters Unsent leads when only low energy matters. Spacewalk Thoughts and Library Rain appear in both lists, but their positions change because genre and mood bonuses disappear for the unknown labels. |
| Deep Intense Rock vs. Sad High-Energy Pop | Storm Runner leads the rock list, while Gym Hero leads the sad pop list. Both profiles want high energy, so they share Storm Runner, Gym Hero, and Daybreak Parade, but the genre and mood bonuses change their order. After the Goodbye appears only in the sad pop list because of its sad label. |
| Deep Intense Rock vs. Unknown Labels and Zero Energy | Storm Runner leads the high-energy rock list, while Letters Unsent leads the low-energy list. The energy targets are near opposite ends of the scale, and the unknown labels provide no genre or mood bonuses; the two top-five lists have no songs in common. |
| Sad High-Energy Pop vs. Unknown Labels and Zero Energy | Gym Hero leads the sad pop list, while Letters Unsent leads the unknown-label list. After the Goodbye appears in both: it earns a sad-mood bonus in the first and benefits from its low energy in the second. The rest of the results shift toward calmer songs when the target drops to zero. |

### Weight Shift Experiment

I also temporarily halved the genre weight to 0.2 and doubled the energy weight to 0.6, leaving mood at 0.3. Rooftop Lights moved above Gym Hero for happy pop, and Spacewalk Thoughts moved above Focus Flow for chill lofi. After the Goodbye dropped out of the sad pop top five because its low energy became a larger disadvantage. The rock and unknown-label rankings stayed the same. The experimental maximum score was 1.1, so higher raw scores did not establish an improvement. I restored the original weights after recording the outputs.

The results follow the scoring recipe, but that does not prove real listening accuracy. These are fictional songs with illustrative attributes, and I evaluated their metadata rather than listening to audio or collecting listener ratings.


---

## 8. Ideas for Improvement

- Let users choose the weights and select more than one genre or mood. Give partial credit to related labels.
- Expand and balance the catalog. Use real listener feedback to check whether suggestions are useful.
- Add a discovery option for more variety. Warn users when no strong matches exist instead of always filling five slots.

---

## 9. Personal Reflection

My biggest learning moment was seeing how changing the weights changed the recommendations. When we gave energy more importance, the only sad song dropped out of the sad, high-energy profile's top five. That helped me understand that a correct calculation can still produce a result that misses something the user cares about.

AI helped me expand the dataset, implement the functions, and design profiles that exposed weaknesses. I still needed to run the program and check the scores, explanations, and ranking order. Comparing the terminal results with our scoring recipe helped me verify the behavior. The generated song attributes were examples, so they could not tell us whether the songs would actually sound right to a listener.

I was surprised that matching just genre, mood, and energy could produce lists that felt personalized based on the labels. Different profiles had different leading songs, even without training a model. The reasons also made it easy to understand why the same song could suit several profiles.

Next, I would let users adjust the weights and choose multiple genres or moods. I would also try a larger catalog and collect listener feedback. That would help me judge whether a change improves the recommendations instead of simply changing their order.
