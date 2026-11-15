"""Writes levels.mtp: the levels of the hop run, for hop-run.mtp to import.

    uv run --no-project python levels.py

Each level is a line of characters, one per unit of ground, read left to right:
`_` ground, ` ` a gap, `r` a rock on the ground, `c` a coin just above the ground, which the
runner takes running past, `C` a coin high up, which takes a jump, and `F` the flag at the end.
A coin or a rock stands on ground, and the critter can stand on a rock. The script checks that
every gap can be jumped: a jump clears about 4 units, so a gap is at most 3 wide, with ground on
both sides. It also works out where the critter starts again after falling into each gap.
"""

from pathlib import Path

LEVELS = [
    # 1. Coins to run through, rocks to jump.
    "____c_c_c____r______c_c____r_____C_____r____F___",
    # 2. High coins, and two rocks side by side.
    "____c_c___r____C_C____rr______c_c___r___r_____F___",
    # 3. The first gaps.
    "____c_c____  ____c_c___r_____C__   ______r___C_C____F___",
    # 4. Rocks and gaps in turn.
    "____cc___r___r______  ___C____rr____C__   ____c_c___r__r_____F___",
    # 5. Wider gaps.
    "____c____r_r_______   ___C_C___rr_____c_c__  __r____C____   _____rr___F___",
    # 6. Three rocks in a row.
    "____cc__r____   ___C___r___r____CC____   __c_c__rrr____C___   ___r___r____F___",
    # 7. Close calls.
    "____c_c__rr____   ____C_C__r_r____   ___C___rrr_____c__   __r__C___   ____F___",
    # 8. Everything, fast.
    "____c__r___   __r____CC___rr___   ____C__r_r__   __C__rrr____   ___c_c__r___F___",
]
GAPS, ROCKS, COINS = 8, 16, 24  # each level's lists are padded to these lengths
LOW, HIGH = 1.0, 2.3  # the heights of the two kinds of coin
BACK = 4  # how far before a gap the critter starts again after falling in


def parse(level):
    gaps, rocks, coins, flag = [], [], [], None
    x = 0
    while x < len(level):
        ch = level[x]
        if ch == " ":
            end = x
            while end < len(level) and level[end] == " ":
                end += 1
            assert end - x <= 3 and x > 0 and end < len(level), f"gap at {x} in {level!r}"
            gaps.append((x, end))
            x = end
            continue
        if ch == "r":
            assert level[x - 1] != " " and level[x + 1] != " ", f"rock at {x} next to a gap"
            rocks.append(x + 0.5)
        elif ch in "cC":
            coins.append((x + 0.5, LOW if ch == "c" else HIGH))
        elif ch == "F":
            flag = x + 0.5
        else:
            assert ch == "_", ch
        x += 1
    assert flag is not None and len(gaps) <= GAPS and len(rocks) <= ROCKS and len(coins) <= COINS
    # Where the critter starts again after falling into each gap: the nearest clear ground at
    # least BACK before it, with no rock within a unit, so it has a run up.
    backs = []
    for g0, _ in gaps:
        x = g0 - BACK
        while not all(0 <= i < len(level) and level[i] in "_cC" for i in (x - 1, x, x + 1)):
            x -= 1
            assert x > 0, f"no ground to start again before the gap at {g0}"
        backs.append(x + 0.5)
    return gaps, rocks, coins, flag, len(level), backs


def fmt_points(ps, n, off):
    ps = list(ps) + [off] * (n - len(ps))
    return "[" + " ".join(f"[{a:g} {b:g}]" for a, b in ps) + "]"


def main():
    parsed = [parse(level) for level in LEVELS]
    sep = "\n     "
    gaps = sep.join(fmt_points(p[0], GAPS, (-99, -98)) for p in parsed)
    rocks = sep.join("[" + " ".join(f"{r:g}" for r in p[1] + [-99] * (ROCKS - len(p[1]))) + "]" for p in parsed)
    coins = sep.join(fmt_points(p[2], COINS, (-99, -99)) for p in parsed)
    backs = sep.join("[" + " ".join(f"{b:g}" for b in p[5] + [1] * (GAPS - len(p[5]))) + "]" for p in parsed)
    Path(__file__).with_name("levels.mtp").write_text(
        f"; The {len(LEVELS)} levels of the hop run, written by levels.py: do not edit by hand.\n"
        "; Level k has gaps in the ground from x to y for each [x y] of level-gaps[k], where the\n"
        "; critter starts again after falling into each at level-back[k], rocks at level-rocks[k],\n"
        "; coins at level-coins[k] and its flag at level-flag[k]; its ground ends at\n"
        "; level-length[k]. The lists are padded with things far to the left, at -99.\n\n"
        f"(list[list[point]] level-gaps\n    [{gaps}]\n    (const))\n"
        f"(list[list[real]] level-back\n    [{backs}]\n    (const))\n"
        f"(list[list[real]] level-rocks\n    [{rocks}]\n    (const))\n"
        f"(list[list[point]] level-coins\n    [{coins}]\n    (const))\n"
        f"(list[real] level-flag [{' '.join(f'{p[3]:g}' for p in parsed)}] (const))\n"
        f"(list[real] level-length [{' '.join(str(p[4]) for p in parsed)}] (const))\n"
    )
    for i, p in enumerate(parsed, 1):
        print(f"level {i}: {p[4]} long, {len(p[0])} gaps, {len(p[1])} rocks, {len(p[2])} coins")


if __name__ == "__main__":
    main()
