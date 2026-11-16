"""Check advanced-feature influence, mode behavior, and interface consistency."""

import math
import re
import subprocess
import sys
import unittest
from dataclasses import asdict
from pathlib import Path

from src.main import PROFILES
from src.recommender import Recommender, Song, UserProfile, load_songs, recommend_songs, score_song
from src.scoring_modes import FEATURES, SCORING_MODES

ROOT = Path(__file__).resolve().parent.parent


class AdvancedRecommenderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.songs = load_songs(ROOT / "data/songs.csv")

    def setUp(self):
        self.prefs = {
            "genre": "pop", "mood": "happy", "energy": 0.5,
            "target_popularity": 50, "preferred_decade": 2000,
            "target_duration": 240, "target_instrumentalness": 0.5,
            "preferred_tags": ("warm", "bright"),
        }
        self.perfect = dict(self.songs[0], energy=0.5, popularity=50,
                            release_decade=2000, duration_seconds=240,
                            instrumentalness=0.5, detailed_mood_tags=("warm", "bright"))

    def test_catalog_schema_and_ranges(self):
        self.assertEqual(len(self.songs), 20)
        self.assertEqual(len({s["id"] for s in self.songs}), 20)
        for song in self.songs:
            self.assertTrue(set(FEATURES) <= song.keys())
            self.assertIsInstance(song["popularity"], int)
            self.assertIsInstance(song["detailed_mood_tags"], tuple)
            self.assertTrue(0 <= song["popularity"] <= 100)
            self.assertTrue(0 <= song["instrumentalness"] <= 1)
            self.assertEqual(song["release_decade"] % 10, 0)
            self.assertGreater(song["duration_seconds"], 0)

    def test_perfect_matches_and_normalized_modes(self):
        for mode, strategy in SCORING_MODES.items():
            self.assertAlmostEqual(sum(strategy.weights), 1)
            score, reasons = score_song(self.prefs, self.perfect, mode)
            self.assertAlmostEqual(score, 1)
            self.assertEqual(len(reasons), 3 if mode == "classic" else 8)

    def test_each_new_feature_changes_scores_by_expected_amount(self):
        changes = {
            "popularity": (0, 0.5),
            "release_decade": (1900, 1),
            "duration_seconds": (540, 1),
            "instrumentalness": (0, 0.5),
            "detailed_mood_tags": (("dark",), 1),
        }
        for mode, strategy in SCORING_MODES.items():
            if mode == "classic":
                continue
            weights = dict(zip(FEATURES, strategy.weights))
            for feature, (value, lost_similarity) in changes.items():
                altered = dict(self.perfect, **{feature: value})
                score, _ = score_song(self.prefs, altered, mode)
                self.assertAlmostEqual(1 - score, weights[feature] * lost_similarity)

    def test_tags_use_overlap_and_normalize_case(self):
        song = dict(self.perfect, detailed_mood_tags=" WARM |bright|warm ")
        self.assertAlmostEqual(score_song(self.prefs, song, "mood-first")[0], 1)
        song["detailed_mood_tags"] = ("warm",)
        self.assertAlmostEqual(score_song(self.prefs, song, "mood-first")[0], 0.9)

    def test_actual_profiles_have_bounded_scores_and_matching_reasons(self):
        for mode in SCORING_MODES:
            for prefs in PROFILES.values():
                for song in self.songs:
                    score, reasons = score_song(prefs, song, mode)
                    self.assertTrue(0 <= score <= 1)
                    points = [float(re.search(r'\(\+([0-9.]+)\)', r).group(1)) for r in reasons]
                    self.assertAlmostEqual(sum(points), score, delta=0.000005)

    def test_modes_change_ranking_for_same_profile(self):
        prefs = PROFILES["High-Energy Pop"]
        genre = recommend_songs(prefs, self.songs, mode="genre-first")
        mood = recommend_songs(prefs, self.songs, mode="mood-first")
        self.assertEqual(genre[1][0]["title"], "Gym Hero")
        self.assertEqual(mood[1][0]["title"], "Rooftop Lights")

    def test_classic_preserves_all_five_original_rankings(self):
        expected = ([1,5,10,16,8], [2,4,9,6,7], [3,5,15,20,18],
                    [5,1,12,3,20], [19,6,12,11,4])
        for prefs, ids in zip(PROFILES.values(), expected):
            self.assertEqual([s["id"] for s, _, _ in recommend_songs(prefs, self.songs)], ids)

    def test_ties_limits_and_input_order(self):
        songs = [dict(self.perfect, id=9), dict(self.perfect, id=2)]
        recs = recommend_songs(self.prefs, songs, k=10, mode="genre-first")
        self.assertEqual([s["id"] for s, _, _ in recs], [2, 9])
        self.assertEqual([s["id"] for s in songs], [9, 2])
        self.assertEqual(recommend_songs(self.prefs, songs, 0), [])
        self.assertEqual(recommend_songs(self.prefs, [], 5), [])

    def test_bad_modes_and_nonfinite_values(self):
        with self.assertRaises(ValueError):
            recommend_songs(self.prefs, [], mode="missing")
        for value in (-0.1, 1.1, math.nan, math.inf):
            with self.assertRaises(ValueError):
                score_song(dict(self.prefs, energy=value), self.perfect, "energy-focused")
        with self.assertRaises(ValueError):
            score_song(dict(self.prefs, preferred_decade=1995), self.perfect, "genre-first")

    def test_object_interface_matches_dictionary_interface(self):
        objects = [Song(**song) for song in self.songs]
        user = UserProfile("pop", "happy", 0.8, target_popularity=85,
                           target_instrumentalness=0.05, preferred_tags=("euphoric", "bright"))
        recommender = Recommender(objects, mode="mood-first")
        actual = recommender.recommend(user)
        expected = recommend_songs(user.preferences(), self.songs, mode="mood-first")
        self.assertEqual([s.id for s in actual], [s["id"] for s, _, _ in expected])
        self.assertEqual(recommender.explain_recommendation(user, actual[0]), expected[0][2])

    def test_cli_runs_every_mode_and_rejects_unknown_modes(self):
        for mode in SCORING_MODES:
            output = subprocess.check_output(
                [sys.executable, "-m", "src.main", "--mode", mode], cwd=ROOT, text=True)
            self.assertIn("Loaded songs: 20", output)
            self.assertEqual(output.count("   Score:"), 25)
            self.assertEqual(output.count("   - "), 75 if mode == "classic" else 200)
        result = subprocess.run([sys.executable, "-m", "src.main", "--mode", "bad"],
                                cwd=ROOT, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid choice", result.stderr)


if __name__ == "__main__":
    unittest.main()
