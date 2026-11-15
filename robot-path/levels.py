"""Writes levels.mtp: the levels of the robot path, for robot-path.mtp to import.

    uv run --no-project python levels.py

Each level is drawn below as rows of a 6 by 6 grid, the top row first: `.` an empty square, `#` a
rock, `*` a star, and the robot as `>`, `^`, `<` or `v`, the way it faces. The script finds the
fewest cards that collect every star, and refuses a level that needs more than MOST_CARDS, so a
child's longer route still fits in the 12 slots.
"""

from collections import deque
from pathlib import Path

SIZE = 6
SLOTS = 12
MOST_CARDS = 9
ROCKS, STARS = 16, 3  # each level's lists are padded to these lengths with OFF
OFF = (-9, -9)

LEVELS = [
    # 1. Straight ahead.
    """
    ......
    ......
    ......
    >..*..
    ......
    ......
    """,
    # 2. Two stars in a row.
    """
    ......
    ......
    ......
    >.*..*
    ......
    ......
    """,
    # 3. A turn to the left.
    """
    ......
    ......
    ...*..
    ......
    >.....
    ......
    """,
    # 4. A turn to the right.
    """
    >.....
    ......
    ......
    .*....
    ......
    ......
    """,
    # 5. Turn all the way around.
    """
    ......
    ......
    ......
    *.>...
    ......
    ......
    """,
    # 6. A rock in the way.
    """
    ......
    ......
    ...*..
    >.#...
    ......
    ......
    """,
    # 7. Up and over.
    """
    ......
    .*..*.
    .#..#.
    >#..#.
    ......
    ......
    """,
    # 8. Three stars around a corner.
    """
    ......
    ......
    ....*.
    ....*.
    >..*..
    ......
    """,
    # 9. A hallway.
    """
    ......
    .####.
    .#*...
    .####.
    .....^
    ......
    """,
    # 10. Around the box.
    """
    ......
    ......
    .##*..
    .##...
    ^.....
    ......
    """,
    # 11. Three stars.
    """
    ......
    .*..*.
    ......
    ......
    .*....
    .^....
    """,
    # 12. Over the wall.
    """
    ......
    ..#*..
    ..#...
    ..#...
    >.....
    ......
    """,
]

FACES = {">": 0, "^": 1, "<": 2, "v": 3}
AHEAD = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def parse(text):
    rows = [r.strip() for r in text.strip().splitlines()]
    assert len(rows) == SIZE and all(len(r) == SIZE for r in rows), text
    rocks, stars, start = [], [], None
    for j, row in enumerate(rows):
        y = SIZE - 1 - j
        for x, ch in enumerate(row):
            if ch == "#":
                rocks.append((x, y))
            elif ch == "*":
                stars.append((x, y))
            elif ch in FACES:
                start = ((x, y), FACES[ch])
            else:
                assert ch == ".", ch
    assert start and 1 <= len(stars) <= STARS and len(rocks) <= ROCKS, text
    return start, rocks, stars


def fewest_cards(start, rocks, stars):
    """The fewest cards (forward, left, right) that take the robot over every star, by search."""
    (p0, d0), rocks = start, set(rocks)
    full = (1 << len(stars)) - 1
    seen = {(p0, d0, 0): 0}
    todo = deque([(p0, d0, 0)])
    while todo:
        p, d, got = state = todo.popleft()
        if got == full:
            return seen[state]
        nexts = [(p, (d + 1) % 4, got), (p, (d + 3) % 4, got)]
        q = (p[0] + AHEAD[d][0], p[1] + AHEAD[d][1])
        if 0 <= q[0] < SIZE and 0 <= q[1] < SIZE and q not in rocks:
            g = got | sum(1 << i for i, s in enumerate(stars) if s == q)
            nexts.append((q, d, g))
        for s in nexts:
            if s not in seen:
                seen[s] = seen[state] + 1
                todo.append(s)
    return None


def pts(ps, n):
    ps = list(ps) + [OFF] * (n - len(ps))
    return "[" + " ".join(f"[{x} {y}]" for x, y in ps) + "]"


def main():
    starts, faces, rocks, stars, best = [], [], [], [], []
    for i, text in enumerate(LEVELS, 1):
        start, rk, st = parse(text)
        n = fewest_cards(start, rk, st)
        assert n is not None and n <= MOST_CARDS, f"level {i} needs {n} cards"
        print(f"level {i}: {n} cards")
        starts.append(start[0])
        faces.append(start[1])
        rocks.append(rk)
        stars.append(st)
        best.append(n)
    sep = "\n     "
    Path(__file__).with_name("levels.mtp").write_text(
        f"; The {len(LEVELS)} levels of the robot path, written by levels.py: do not edit by hand.\n"
        "; Level k starts the robot at level-start[k] facing level-face[k] (0 right, 1 up, 2 left,\n"
        f"; 3 down), with rocks at level-rocks[k] and stars at level-stars[k], padded with [{OFF[0]} {OFF[1]}].\n"
        "; level-best[k] is the fewest cards that take every star.\n\n"
        f"(list[point] level-start {pts(starts, len(starts))} (const))\n"
        f"(list[int] level-face [{' '.join(map(str, faces))}] (const))\n"
        f"(list[list[point]] level-rocks\n    [{sep.join(pts(r, ROCKS) for r in rocks)}]\n    (const))\n"
        f"(list[list[point]] level-stars\n    [{sep.join(pts(s, STARS) for s in stars)}]\n    (const))\n"
        f"(list[int] level-best [{' '.join(map(str, best))}] (const))\n"
    )


if __name__ == "__main__":
    main()
