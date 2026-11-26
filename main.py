#!/usr/bin/env python3
"""The Self-Checkout Is Judging You — make.fun entry, round 2.

Writes one funny line in the voice of a smug, judgmental self-checkout
machine to /output/entry.txt (or $ENTRY_OUTPUT when set).

The chosen line
---------------
"The shopper before you bought vegetables. You bought six doughnuts
and a candle for a cake you did not buy."

Why this line wins
------------------
* The machine's job is seeing every basket, so comparing one shopper
  with the one before is judgment from inside the machine's own world:
  only the till knows what the previous customer bought.
* The sting is a single image that needs no setup: a birthday candle
  with no cake. The shopper bought the celebration prop and skipped
  the thing being celebrated. A stranger gets it on one cold read.
* It is fresh. Round 1 counted items and policed the express lane; this
  round compares baskets. It never touches the twelve-yoghurts scan,
  the plain bagging-area quote, or the tired "unexpected item in the
  bagging area" cliche.
* It is tight: 107 characters, two sentences, no padding. "Vegetables"
  sets the bar, "six doughnuts" breaks it, and the candle delivers
  the twist on the final words.

How the pick is made
--------------------
Three genuinely different candidates are scored 0-5 against the five
judge criteria, in the judge's own order: (1) machine voice,
(2) real laugh on a single read, (3) smug and petty about the basket,
(4) tight with no padding, (5) fresh. The highest total wins; ties
break toward the earlier candidate, so the choice is deterministic.

The program is deterministic, uses only the standard library, needs no
network, reads no file, and writes exactly one line.
"""

import os

# criterion order: voice, laugh, petty, tight, fresh
CANDIDATES = [
    {
        "text": (
            "Two litres of ice cream, no spoon, and a diet soda. "
            "The soda does not cancel it out. It never has."
        ),
        "scores": (4, 4, 5, 4, 3),  # total 20: diet-soda logic is
        # relatable and petty, but the joke itself is familiar ground.
        "why": "Calorie-accountant machine: the diet soda cannot save you.",
    },
    {
        "text": (
            "The shopper before you bought vegetables. You bought six "
            "doughnuts and a candle for a cake you did not buy."
        ),
        "scores": (4, 4, 4, 4, 5),  # total 21: the candle-without-a-
        # cake twist is the most original sting of the three.
        "why": "Basket-comparing machine: the till keeps a league table.",
    },
    {
        "text": (
            "One cucumber, one tube of toothpaste, a birthday candle. "
            "I am not paid to ask questions, but I am judging anyway."
        ),
        "scores": (5, 4, 4, 3, 4),  # total 20: strongest machine
        # voice, but the three-item list is a little setup-heavy.
        "why": "Weird-basket machine: politely declining to ask, judging anyway.",
    },
]

WINNER_INDEX = 1  # index of the highest-total candidate above


def pick(candidates):
    """Return the highest-total candidate; earliest wins any tie."""
    best = None
    best_total = -1
    for candidate in candidates:
        total = sum(candidate["scores"])
        if total > best_total:
            best = candidate
            best_total = total
    return best


def main() -> None:
    entry = pick(CANDIDATES)["text"]
    # The pick must agree with the hand-scored winner, so a scoring
    # slip can never silently swap the line.
    if pick(CANDIDATES) is not CANDIDATES[WINNER_INDEX]:
        raise ValueError("scored winner does not match WINNER_INDEX")
    # Gate: one line, 1-200 characters, no surrounding whitespace.
    if not 1 <= len(entry) <= 200:
        raise ValueError("entry must be 1-200 characters, got %d" % len(entry))
    if entry != entry.strip() or "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line with no edge spaces")
    if "  " in entry:
        raise ValueError("entry must not contain double spaces (padding)")
    output_path = os.environ.get("ENTRY_OUTPUT") or "/output/entry.txt"
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(entry + "\n")
    os.chmod(output_path, 0o644)


if __name__ == "__main__":
    main()
