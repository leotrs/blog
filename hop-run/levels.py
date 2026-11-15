"""Writes levels.mtp: the levels of the hop run, for hop-run.mtp to import.

    uv run --no-project python levels.py

Each level is a line of characters, one per unit of ground, read left to right:
`_` ground, ` ` a gap, `r` a rock on the ground, `c` a coin just above the ground, which the
runner takes running past, `C` a coin high up, which takes a jump, and `F` the flag at the end.
A coin or a rock stands on ground. The script checks that every gap and every rock can be jumped:
a jump clears about 3 units, so a gap is at most 2 wide and has ground on both sides.
"""

from pathlib import Path

LEVELS = [
    # 1. Coins to run through, one rock.
    "____c_c_c_______r_______c_c_c____F___",
    # 2. Two rocks and high coins.
    "____c_c___r____C_C_______r_____c_c_c____F___",
    # 3. The first gap.
    "____c_c_c____  ____c_c____r______C___ _____F___",
    # 4. Rocks and gaps in turn.
    "____c___r____cc____  ___C___r_____c_c__  ___C_C___r_____F___",
    # 5. Longer, with coins over the gaps' far side.
    "____cc___r___r_______  _C____c_c_c___r_____  __C_____r___cc_______F___",
    # 6. Everything.
    "____c_c___r____  __C___r___r______C_C____  ____c_c_c___r____ ____cc__r____C____F___",
]
GAPS, ROCKS, COINS = 8, 12, 24  # each level's lists are padded to these lengths
LOW, HIGH = 1.0, 2.3  # the heights of the two kinds of coin


def parse(level):
    gaps, rocks, coins, flag = [], [], [], None
    x = 0
    while x < len(level):
        ch = level[x]
        if ch == " ":
            end = x
            while end < len(level) and level[end] == " ":
                end += 1
            assert end - x <= 2 and x > 0 and end < len(level), f"gap at {x} in {level!r}"
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
    return gaps, rocks, coins, flag, len(level)


def fmt_points(ps, n, off):
    ps = list(ps) + [off] * (n - len(ps))
    return "[" + " ".join(f"[{a:g} {b:g}]" for a, b in ps) + "]"


def main():
    parsed = [parse(level) for level in LEVELS]
    sep = "\n     "
    gaps = sep.join(fmt_points(p[0], GAPS, (-99, -98)) for p in parsed)
    rocks = sep.join("[" + " ".join(f"{r:g}" for r in p[1] + [-99] * (ROCKS - len(p[1]))) + "]" for p in parsed)
    coins = sep.join(fmt_points(p[2], COINS, (-99, -99)) for p in parsed)
    Path(__file__).with_name("levels.mtp").write_text(
        f"; The {len(LEVELS)} levels of the hop run, written by levels.py: do not edit by hand.\n"
        "; Level k has gaps in the ground from x to y for each [x y] of level-gaps[k], rocks at\n"
        "; level-rocks[k], coins at level-coins[k] and its flag at level-flag[k]; its ground ends at\n"
        "; level-length[k]. The lists are padded with things far to the left, at -99.\n\n"
        f"(list[list[point]] level-gaps\n    [{gaps}]\n    (const))\n"
        f"(list[list[real]] level-rocks\n    [{rocks}]\n    (const))\n"
        f"(list[list[point]] level-coins\n    [{coins}]\n    (const))\n"
        f"(list[real] level-flag [{' '.join(f'{p[3]:g}' for p in parsed)}] (const))\n"
        f"(list[real] level-length [{' '.join(str(p[4]) for p in parsed)}] (const))\n"
    )
    for i, p in enumerate(parsed, 1):
        print(f"level {i}: {p[4]} long, {len(p[0])} gaps, {len(p[1])} rocks, {len(p[2])} coins")


if __name__ == "__main__":
    main()
