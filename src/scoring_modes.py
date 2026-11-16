"""Small scoring strategies that share the same feature-matching rules."""

from dataclasses import dataclass
from math import isclose

FEATURES = (
    "genre", "mood", "energy", "popularity", "release_decade",
    "duration_seconds", "instrumentalness", "detailed_mood_tags",
)


@dataclass(frozen=True)
class ScoringStrategy:
    """Combine feature similarities using one named set of weights."""

    name: str
    weights: tuple

    def __post_init__(self):
        """Reject policies that would break the zero-to-one score range."""
        if len(self.weights) != len(FEATURES):
            raise ValueError("Each feature needs one weight.")
        if any(weight < 0 for weight in self.weights) or not isclose(sum(self.weights), 1):
            raise ValueError("Weights must be nonnegative and sum to 1.")

    def contributions(self, matches: dict) -> dict:
        """Return weighted points for every enabled feature."""
        return {
            feature: weight * matches[feature]
            for feature, weight in zip(FEATURES, self.weights)
            if weight > 0
        }


SCORING_MODES = {
    "classic": ScoringStrategy("classic", (0.4, 0.3, 0.3, 0, 0, 0, 0, 0)),
    "genre-first": ScoringStrategy(
        "genre-first", (0.30, 0.15, 0.15, 0.08, 0.07, 0.07, 0.08, 0.10)
    ),
    "mood-first": ScoringStrategy(
        "mood-first", (0.10, 0.30, 0.15, 0.05, 0.05, 0.05, 0.10, 0.20)
    ),
    "energy-focused": ScoringStrategy(
        "energy-focused", (0.10, 0.10, 0.40, 0.07, 0.06, 0.07, 0.10, 0.10)
    ),
}


def get_strategy(mode: str) -> ScoringStrategy:
    """Resolve a scoring mode or raise a readable error."""
    if mode not in SCORING_MODES:
        raise ValueError(f"Unknown mode {mode!r}; choose from {', '.join(SCORING_MODES)}.")
    return SCORING_MODES[mode]
