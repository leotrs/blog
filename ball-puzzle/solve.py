"""Writes solutions.mtp: full solutions of the ball puzzle, for ball-puzzle.mtp to import.

    uv run --no-project python solve.py [count]

Each solution places all twelve pieces on the 5 by 11 board, so freeing any k of its pieces
gives a puzzle that can always be finished. A piece is placed as in ball-puzzle.mtp: its
position is where its offset [0 0] lands, and its turn is 0 to 3 quarter turns, or 4 to 7 the
same after flipping it over (see turned there).
"""

import random
import sys
from pathlib import Path

# The same shapes, in the same order, as `shapes` in ball-puzzle.mtp.
SHAPES = [
    [(0, 0), (1, 0), (0, 1)],
    [(0, 0), (1, 0), (2, 0), (0, 1)],
    [(0, 0), (1, 0), (0, 1), (1, 1)],
    [(0, 0), (1, 0), (2, 0), (1, 1)],
    [(1, 0), (2, 0), (0, 1), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (3, 1)],
    [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)],
    [(0, 0), (2, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)],
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (3, 0), (1, 1)],
]
WIDTH, HEIGHT = 11, 5


def turned(c, o):
    """The same as turned in ball-puzzle.mtp."""
    x, y = (-c[0], c[1]) if o >= 4 else c
    k = o % 4
    return [(x, y), (-y, x), (-x, -y), (y, -x)][k]


def placements(piece):
    """Every way to put a piece on the board: (turn, position, cells), distinct by cells."""
    seen, out = set(), []
    for o in range(8):
        offsets = [turned(c, o) for c in SHAPES[piece]]
        for px in range(-4, WIDTH + 4):
            for py in range(-4, HEIGHT + 4):
                cells = frozenset((px + dx, py + dy) for dx, dy in offsets)
                if cells in seen or not all(0 <= x < WIDTH and 0 <= y < HEIGHT for x, y in cells):
                    continue
                seen.add(cells)
                out.append((o, (px, py), cells))
    return out


PLACEMENTS = [placements(p) for p in range(12)]


def solve(rnd):
    """One full solution, as a list of (turn, position) by piece, found in a random order."""
    filled, placed = set(), {}

    def first_empty():
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if (x, y) not in filled:
                    return x, y
        return None

    def search():
        hole = first_empty()
        if hole is None:
            return True
        pieces = [p for p in range(12) if p not in placed]
        rnd.shuffle(pieces)
        for p in pieces:
            options = [pl for pl in PLACEMENTS[p] if hole in pl[2] and not pl[2] & filled]
            rnd.shuffle(options)
            for o, pos, cells in options:
                placed[p] = (o, pos)
                filled.update(cells)
                if search():
                    return True
                filled.difference_update(cells)
                del placed[p]
        return False

    search()
    return [placed[p] for p in range(12)]


def cells_of(solution):
    """The holes each piece covers in a solution."""
    return [
        {(px + dx, py + dy) for dx, dy in (turned(c, o) for c in SHAPES[i])}
        for i, (o, (px, py)) in enumerate(solution)
    ]


def growing_order(solution, rnd):
    """The pieces in an order where each one touches an earlier one, starting from a random piece.

    The first k pieces of it then always cover one connected region, so taking them off the board
    leaves a single hole.
    """
    cells = cells_of(solution)

    def touch(a, b):
        return any((x + dx, y + dy) in cells[b] for x, y in cells[a] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))

    order = [rnd.randrange(12)]
    while len(order) < 12:
        nexts = [p for p in range(12) if p not in order and any(touch(p, q) for q in order)]
        order.append(rnd.choice(nexts))
    return order


def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    rnd = random.Random(2026)
    solutions, seen = [], set()
    while len(solutions) < count:
        s = solve(rnd)
        key = tuple(s)
        if key not in seen:
            seen.add(key)
            solutions.append(s)
    pos = "\n     ".join("[" + " ".join(f"[{x} {y}]" for _, (x, y) in s) + "]" for s in solutions)
    turn = "\n     ".join("[" + " ".join(str(o) for o, _ in s) + "]" for s in solutions)
    order = "\n     ".join("[" + " ".join(str(p) for p in growing_order(s, rnd)) + "]" for s in solutions)
    Path(__file__).with_name("solutions.mtp").write_text(
        f"; {count} full solutions of the ball puzzle, written by solve.py: do not edit by hand.\n"
        "; For solution s, piece i sits at solution-pos[s][i] with turn solution-turn[s][i].\n"
        "; solution-order[s] lists the pieces so that each touches an earlier one: the first k of\n"
        "; them, taken off the board, leave a single hole.\n\n"
        f"(list[list[point]] solution-pos\n    [{pos}]\n    (const))\n"
        f"(list[list[int]] solution-turn\n    [{turn}]\n    (const))\n"
        f"(list[list[int]] solution-order\n    [{order}]\n    (const))\n"
    )
    print(f"wrote {count} solutions")


if __name__ == "__main__":
    main()
