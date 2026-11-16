"""Draw archived records without replacement within one campaign.

Every experiment is a new sample: within a campaign a record, once drawn, leaves its family. The state belongs to the campaign's own
random generator (every campaign in experiments 24-31 and in the chain study creates a fresh one), so it resets for each campaign. If a
family runs out of unused records before the budget does, a fresh shuffled pass of that family begins and the draw is counted in
REFILLS. TENKI_REPLACE=1 restores the earlier draw with replacement."""
import os

REPLACE = os.environ.get("TENKI_REPLACE", "0") == "1"
_STATE = {"rng": None, "classes": None, "left": {}}
REFILLS = {"draws": 0, "refills": 0}


def draw(classes, c, rng):
    """One archived value of family c."""
    vals = classes[c]
    if REPLACE:
        return vals[rng.integers(0, len(vals))]
    if _STATE["rng"] is not rng or _STATE["classes"] is not classes:
        _STATE.update(rng=rng, classes=classes, left={})
    left = _STATE["left"].get(c)
    if not left:
        if left is not None:
            REFILLS["refills"] += 1
        left = list(rng.permutation(len(vals)))
        _STATE["left"][c] = left
    REFILLS["draws"] += 1
    return vals[left.pop()]
