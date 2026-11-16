"""Load songs, match user tastes, and rank songs with explainable strategies."""

import csv
from dataclasses import asdict, dataclass
from math import isfinite
from typing import Dict, List, Tuple

from .scoring_modes import FEATURES, get_strategy


@dataclass
class Song:
    """Represent a song with baseline and advanced attributes."""

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
    popularity: int = 50
    release_decade: int = 2020
    duration_seconds: int = 210
    instrumentalness: float = 0.2
    detailed_mood_tags: tuple = ()


@dataclass
class UserProfile:
    """Represent user targets for the same eight scored features."""

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool = False  # Retained from the starter; not scored.
    target_popularity: int = 50
    preferred_decade: int = 2020
    target_duration: int = 210
    target_instrumentalness: float = 0.2
    preferred_tags: tuple = ()

    def preferences(self) -> Dict:
        """Convert object preferences into the shared dictionary interface."""
        prefs = asdict(self)
        prefs["genre"] = prefs.pop("favorite_genre")
        prefs["mood"] = prefs.pop("favorite_mood")
        prefs["energy"] = prefs.pop("target_energy")
        return prefs


def tags(value) -> set:
    """Normalize pipe-separated text or an iterable into distinct mood tags."""
    values = value.split("|") if isinstance(value, str) else value
    return {str(tag).strip().casefold() for tag in values if str(tag).strip()}


def checked_number(value, name: str, lower: float, upper=None) -> float:
    """Validate finite numeric values before computing similarities."""
    value = float(value)
    if not isfinite(value) or value < lower or (upper is not None and value > upper):
        raise ValueError(f"{name} must be finite and between {lower} and {upper or 'infinity'}.")
    return value


def similarity(value, target, span: float) -> float:
    """Reward closeness on a chosen scale and clip distant matches to zero."""
    return max(0.0, 1.0 - abs(value - target) / span)


def load_songs(csv_path: str) -> List[Dict]:
    """Load CSV dictionaries, converting numeric fields and detailed mood tags."""
    integer_fields = ("id", "popularity", "release_decade", "duration_seconds")
    float_fields = (
        "energy", "tempo_bpm", "valence", "danceability", "acousticness", "instrumentalness"
    )
    songs = []
    with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
        for row in csv.DictReader(csv_file):
            for field in integer_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            row["detailed_mood_tags"] = tuple(sorted(tags(row["detailed_mood_tags"])))
            songs.append(row)
    return songs


def feature_matches(user_prefs: Dict, song: Dict, advanced: bool) -> Dict:
    """Calculate separate similarities for the features used by a strategy."""
    energy = checked_number(song["energy"], "song energy", 0, 1)
    target = checked_number(user_prefs["energy"], "target energy", 0, 1)
    matches = {
        "genre": float(song["genre"].strip().casefold() == user_prefs["genre"].strip().casefold()),
        "mood": float(song["mood"].strip().casefold() == user_prefs["mood"].strip().casefold()),
        "energy": similarity(energy, target, 1),
    }
    if not advanced:
        return matches

    # Defaults allow a basic three-field profile to use advanced modes too.
    specifications = (
        ("popularity", "target_popularity", 50, 0, 100, 100),
        ("release_decade", "preferred_decade", 2020, 1900, 2100, 100),
        ("duration_seconds", "target_duration", 210, 1, None, 300),
        ("instrumentalness", "target_instrumentalness", 0.2, 0, 1, 1),
    )
    for field, preference, default, lower, upper, span in specifications:
        value = checked_number(song[field], field, lower, upper)
        target = checked_number(user_prefs.get(preference, default), preference, lower, upper)
        if field == "release_decade" and (value % 10 or target % 10):
            raise ValueError("Release decades must be multiples of 10, such as 1990.")
        matches[field] = similarity(value, target, span)

    requested = tags(user_prefs.get("preferred_tags", ()))
    available = tags(song["detailed_mood_tags"])
    union = requested | available
    matches["detailed_mood_tags"] = len(requested & available) / len(union) if union else 0.0
    return matches


def score_song(user_prefs: Dict, song: Dict, mode: str = "classic") -> Tuple[float, List[str]]:
    """Return a strategy's weighted song score and every enabled contribution."""
    strategy = get_strategy(mode)
    matches = feature_matches(user_prefs, song, advanced=mode != "classic")
    contributions = strategy.contributions(matches)
    reasons = []
    for feature, weight in zip(FEATURES, strategy.weights):
        if feature in contributions:
            points = contributions[feature]
            reasons.append(
                f"{feature}: match={matches[feature]:.3f}, "
                f"weight={weight:.2f} (+{points:.6f})"
            )
    return sum(contributions.values()), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, mode: str = "classic") -> List[Tuple[Dict, float, str]]:
    """Return top-k scored songs and explanations, resolving ties by song ID."""
    get_strategy(mode)
    if k <= 0:
        return []
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, mode)
        scored.append((song, score, "; ".join(reasons)))
    return sorted(scored, key=lambda item: (-item[1], item[0]["id"]))[:k]


class Recommender:
    """Adapt the object interface to the same scoring and ranking functions."""

    def __init__(self, songs: List[Song], mode: str = "classic"):
        """Store songs and validate the selected strategy."""
        get_strategy(mode)
        self.songs = songs
        self.mode = mode

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return song objects in the shared strategy's ranking order."""
        ranked = recommend_songs(user.preferences(), [asdict(s) for s in self.songs], k, self.mode)
        by_id = {s.id: s for s in self.songs}
        return [by_id[song["id"]] for song, _, _ in ranked]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain a song using the same strategy used for recommendations."""
        _, reasons = score_song(user.preferences(), asdict(song), self.mode)
        return "; ".join(reasons)
