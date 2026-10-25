"""Exotic Trade Pier compatibility: Roman Life menu tiles the pier swaps for recipe copies or moves to another tab."""
import os, re
from gather import MODS, CATS, load

MOD = "exotictradepier-khayi"
DIR = "[Gameplay] Exotic Trade Pier (Khayi)"
TILE = re.compile(r"Item\[Building='(\d+)'\]$")


def changes():
    """swaps {tile: (tab, [copies])}, moves {tile: (from tab, to tab)}, read from the installed pier."""
    exp = os.path.join(MODS, DIR, "data", "base", "config", "export")
    ops = []
    for f in sorted(os.listdir(exp)) if os.path.isdir(exp) else []:
        root = load(os.path.join(exp, f)) if f.endswith(".xml") else None
        for op in root.iter("ModOp") if root is not None else []:
            g, m = op.get("GUID", ""), TILE.search(op.get("Path", ""))
            if g in CATS and m:
                ops.append((op.get("Type"), g, m.group(1), [b.text for b in op.iter("Building")]))
    removed = {(g, b) for t, g, b, _ in ops if t == "remove"}
    swaps, moves = {}, {}
    for t, g, b, new in ops:
        if t != "addNextSibling":
            continue
        if (g, b) in removed:
            swaps[b] = (g, new)
        else:
            for n in new:
                src = [rg for rg, rb in removed if rb == n and rg != g]
                if src:
                    moves[n] = (src[0], g)
    return swaps, moves


if __name__ == "__main__":
    swaps, moves = changes()
    for b, (g, new) in swaps.items():
        print("swap", g, b, "->", new)
    for b, (g, to) in moves.items():
        print("move", b, g, "->", to)
