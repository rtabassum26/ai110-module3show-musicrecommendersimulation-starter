"""Run the CLI with a selected scoring strategy and taste profile."""

import argparse
from pathlib import Path

from .recommender import load_songs, recommend_songs
from .scoring_modes import SCORING_MODES

DEFAULT_MODE = "genre-first"

PROFILES = {
    "High-Energy Pop": {
        "genre": "pop", "mood": "happy", "energy": 0.80,
        "target_popularity": 85, "preferred_decade": 2020,
        "target_duration": 210, "target_instrumentalness": 0.05,
        "preferred_tags": ("euphoric", "bright"),
    },
    "Chill Lofi": {
        "genre": "lofi", "mood": "chill", "energy": 0.40,
        "target_popularity": 35, "preferred_decade": 2020,
        "target_duration": 210, "target_instrumentalness": 0.95,
        "preferred_tags": ("calm", "focused", "cozy"),
    },
    "Deep Intense Rock": {
        "genre": "rock", "mood": "intense", "energy": 0.95,
        "target_popularity": 60, "preferred_decade": 2010,
        "target_duration": 250, "target_instrumentalness": 0.05,
        "preferred_tags": ("aggressive", "driven"),
    },
    "Edge Case: Sad High-Energy Pop": {
        "genre": "pop", "mood": "sad", "energy": 0.90,
        "target_popularity": 60, "preferred_decade": 2010,
        "target_duration": 240, "target_instrumentalness": 0.05,
        "preferred_tags": ("heartbroken", "reflective", "lonely"),
    },
    "Edge Case: Unknown Labels and Zero Energy": {
        "genre": "blues", "mood": "dreamy", "energy": 0.00,
        "target_popularity": 30, "preferred_decade": 1990,
        "target_duration": 270, "target_instrumentalness": 0.90,
        "preferred_tags": ("dreamy", "calm"),
    },
}


def print_recommendations(name: str, prefs: dict, songs: list, mode: str) -> None:
    """Print a profile's top five songs with every score contribution."""
    results = recommend_songs(prefs, songs, k=5, mode=mode)
    print(f"=== {name} | mode={mode} ===")
    print(f"User preferences: {prefs}")
    print(f"\nTop {len(results)} recommendations:")
    for rank, (song, score, explanation) in enumerate(results, start=1):
        print(f"\n{rank}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.6f}")
        print("   Reasons:")
        for reason in explanation.split("; "):
            print(f"   - {reason}")
    print()


def main() -> None:
    """Select a mode and run one named profile or all evaluation profiles."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=tuple(SCORING_MODES), default=DEFAULT_MODE)
    parser.add_argument("--profile", choices=("all", *PROFILES), default="all")
    args = parser.parse_args()
    csv_path = Path(__file__).resolve().parent.parent / "data" / "songs.csv"
    songs = load_songs(csv_path)
    print(f"Loaded songs: {len(songs)}\n")
    profiles = PROFILES if args.profile == "all" else {args.profile: PROFILES[args.profile]}
    for name, prefs in profiles.items():
        print_recommendations(name, prefs, songs, args.mode)


if __name__ == "__main__":
    main()
