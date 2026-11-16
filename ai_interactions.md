# AI Interactions Log

> **Stretch features only.** This log covers the advanced song features and multiple scoring modes completed for this project.

---

## Agentic Workflow (SF8)

**What task did you give the agent?**

I asked ChatGPT to complete both stretch challenges. The task was to add at least five new song attributes, include them in scoring, create switchable ranking modes, and document the changes and verification.

**Prompts used:**

I provided the challenge instructions, including these requirements:

> Introduce **5 or more** complex attributes to your dataset that are not currently present in the baseline data.

> Update both `data/songs.csv` and the scoring logic in `src/recommender.py` so scoring accounts for the new attributes.

> Build two or more different ranking strategies (e.g., "Genre-First," "Mood-First," or "Energy-Focused") so a user can switch between modes in `main.py`.

My final instruction was:

> complete these two challenges as the last step to our work

The assistant completed the work in this chat. I did not use a separate AI assistant or open another chat for it.

**What did the agent generate or change?**

- `data/songs.csv`: Added popularity, release decade, duration in seconds, instrumentalness, and detailed mood tags to all 20 songs. The values are illustrative metadata for fictional songs.
- `src/recommender.py`: Added numerical conversion, tag parsing, advanced feature matching, weighted explanations, and input validation. Both object and dictionary interfaces now share the scoring logic.
- `src/scoring_modes.py`: Added strategy objects for Genre-First, Mood-First, and Energy-Focused. Classic mode preserves the original three-feature scoring.
- `src/main.py`: Added mode and profile selection. The five evaluation profiles now include targets for the advanced features.
- `tests/test_advanced_recommender.py`: Added 11 automated tests. All passed in the assistant's environment.
- `README.md` and `model_card.md`: Documented the new attributes, mode weights, actual CLI outputs, comparison results, and limitations.
- `ai_interactions.md`: Recorded the workflow and design pattern using this template.

The assistant ran all four modes against all five profiles. Checks confirmed that each new feature affects the advanced scores, mode weights sum to 1, and explanations account for the totals. Tests also covered tag overlap, invalid inputs, ties, object/function consistency, and preservation of the five classic rankings. The original repository test file was not provided, so it was not run.

**What did you verify or fix manually?**

Before the stretch work, I ran the baseline CLI and shared the outputs for all five profiles. The results matched the original scoring rules. I also reviewed the explanations for surprising recommendations, such as Gym Hero appearing for several different preferences.

Manual verification of the new stretch features on my computer is still pending. The assistant's automated checks passed, but I have not yet confirmed these new outputs locally. I also supplied this log template after the implementation so the documentation could follow the required format.

To finish the local checks, I will run:

```bash
python -m src.main --mode genre-first --profile "High-Energy Pop"
python -m src.main --mode mood-first --profile "High-Energy Pop"
python -m src.main --mode energy-focused --profile "Chill Lofi"
python -m src.main --mode classic
python -m unittest discover -s tests -p "test_advanced_recommender.py" -v
```

I will check that each advanced recommendation has eight feature reasons and that Rooftop Lights moves above Gym Hero in Mood-First for the same pop/happy profile. I will also run the original repository tests. No commit or push was performed by the assistant because its workspace is not my Git repository.

---

## Design Pattern (SF10)

**Which design pattern did you use?**

A lightweight Strategy pattern.

**How did AI help you brainstorm or implement it?**

The assistant considered separate scoring functions for each mode and a shared scorer with different weight strategies. Separate functions would repeat the feature matching and explanation code. It chose strategy objects so the modes could change weights while sharing the same matching, validation, and ranking rules.

This keeps each strategy small and makes comparisons easier. For the same pop/happy profile, Genre-First places Gym Hero second, while Mood-First places Rooftop Lights second. The profile and catalog stay the same; the selected weights explain the difference.

**How does the pattern appear in your final code?**

`ScoringStrategy` in `src/scoring_modes.py` stores a mode's name and weights. It validates the weights and calculates weighted feature contributions. The `SCORING_MODES` registry holds the presets, and `get_strategy()` selects one by name.

In `src/recommender.py`, `score_song()` calculates shared feature similarities and applies the selected strategy. `recommend_songs()` sorts those scores without needing separate ranking code for each mode. In `src/main.py`, `--mode` selects the strategy; `DEFAULT_MODE` sets the default.
