"""Run diverse preference profiles through the music recommender CLI."""

from pathlib import Path

from .recommender import load_songs, recommend_songs


def print_recommendations(name: str, user_prefs: dict, songs: list) -> None:
    """Print one profile's top five songs with scores and scoring reasons."""
    recommendations = recommend_songs(user_prefs, songs, k=5)
    print(f"=== {name} ===")
    print(
        f"User profile: genre={user_prefs['genre']}, "
        f"mood={user_prefs['mood']}, energy={user_prefs['energy']:.2f}"
    )
    print(f"\nTop {len(recommendations)} recommendations:")

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.3f}")
        print("   Reasons:")
        for reason in explanation.split("; ", maxsplit=2):
            print(f"   - {reason}")
    print()


def main() -> None:
    """Load the catalog and evaluate three typical profiles and two edge cases."""
    csv_path = Path(__file__).resolve().parent.parent / "data" / "songs.csv"
    songs = load_songs(csv_path)
    profiles = {
        "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.80},
        "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.40},
        "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.95},
        "Edge Case: Sad High-Energy Pop": {
            "genre": "pop", "mood": "sad", "energy": 0.90,
        },
        "Edge Case: Unknown Labels and Zero Energy": {
            "genre": "blues", "mood": "dreamy", "energy": 0.00,
        },
    }

    print(f"Loaded songs: {len(songs)}\n")
    for name, user_prefs in profiles.items():
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
