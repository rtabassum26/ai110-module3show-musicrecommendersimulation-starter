"""Command-line runner for the Music Recommender Simulation."""

from pathlib import Path

from .recommender import load_songs, recommend_songs


def main() -> None:
    csv_path = Path(__file__).resolve().parent.parent / "data" / "songs.csv"
    songs = load_songs(csv_path)
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"Loaded songs: {len(songs)}")
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


if __name__ == "__main__":
    main()
