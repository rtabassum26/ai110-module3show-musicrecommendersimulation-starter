import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load CSV songs as dictionaries with integer IDs and float audio features."""
    songs = []
    float_fields = (
        "energy", "tempo_bpm", "valence", "danceability", "acousticness"
    )

    with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            row["id"] = int(row["id"])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Return a song's weighted genre, mood, and energy score with reasons."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["genre"]:
        score += 0.4
        reasons.append("genre match (+0.400)")
    else:
        reasons.append("genre does not match (+0.000)")

    if song["mood"] == user_prefs["mood"]:
        score += 0.3
        reasons.append("mood match (+0.300)")
    else:
        reasons.append("mood does not match (+0.000)")

    song_energy = song["energy"]
    target_energy = user_prefs["energy"]
    if not 0.0 <= song_energy <= 1.0 or not 0.0 <= target_energy <= 1.0:
        raise ValueError("Song energy and target energy must be between 0 and 1.")

    energy_match = 1 - abs(song_energy - target_energy)
    energy_points = 0.3 * energy_match
    score += energy_points
    reasons.append(
        f"energy similarity {energy_match:.3f} "
        f"(song={song_energy:.2f}, target={target_energy:.2f}; "
        f"+{energy_points:.3f})"
    )

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top k songs with scores and explanations, breaking ties by ID."""
    if k <= 0:
        return []

    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored_songs.append((song, score, explanation))

    # Highest score first; ascending song ID resolves tied scores.
    ranked_songs = sorted(scored_songs, key=lambda item: (-item[1], item[0]["id"]))
    return ranked_songs[:k]
