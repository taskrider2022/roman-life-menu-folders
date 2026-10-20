import re, os
from collections import defaultdict
from xml.etree import ElementTree as ET

import sys
_argv = sys.argv
MODS = os.environ.get("ANNO_MODS", r"d:\Anno 117 - Pax Romana\mods")
if "--mods" in _argv:
    MODS = _argv[_argv.index("--mods") + 1]
SELF = "[QoL] Roman Life Menu Folders"
CATS = {"41327", "41328", "41329", "41330", "41331", "41362", "41363", "41364", "41365"}
FAMILIES = {
    "[Content] Roman Life - Latium (Khayi)": "latium",
    "[Content] Roman Life - Albion (Khayi)": "albion",
    "[Content] Roman Life - Imperial Blends (Khayi)": "imperial",
    "[Gameplay] Celtic Independence Overhaul (Jtmzac)": "celtic",
}

def modid(d):
    while len(d) > len(MODS):
        for n in ("modinfo.json", "modinfo.jsonc"):
            p = os.path.join(d, n)
            if os.path.exists(p):
                m = re.search(r'"ModID"\s*:\s*"([^"]+)"', open(p, encoding="utf-8-sig", errors="ignore").read())
                return m.group(1) if m else os.path.basename(d)
        d = os.path.dirname(d)

def load(path):
    try:
        return ET.parse(path).getroot()
    except (ET.ParseError, OSError):
        return None

data = defaultdict(list)  # (family, category) -> [(building, conds, modid)]

def handle_op(op, conds, fam, mid):
    c = op.get("Condition")
    if c:
        conds = conds + [c]
    attrs = " ".join(op.attrib.values())
    if "BuildingList" not in attrs or op.get("Type", "").lower() == "remove" or "remove" in op.attrib:
        return
    cats = set()
    g = op.get("GUID")
    if g:
        cats |= set(x.strip() for x in g.split(","))
    cats |= set(re.findall(r"@(\d+)", attrs))
    cats &= CATS
    if not cats:
        return
    for b in op.iter("Building"):
        if b.text and b.text.isdigit() and int(b.text) >= 1000000:
            for cat in cats:
                data[(fam, cat)].append((b.text, conds, mid))

def walk(node, base, conds, fam, mid, seen):
    for ch in node:
        c = ch.get("Condition")
        cc = conds + [c] if c else conds
        if ch.tag == "Include":
            p = os.path.normpath(os.path.join(base, ch.get("File", "")))
            if p in seen or not os.path.exists(p):
                continue
            root = load(p)
            if root is not None:
                walk(root, os.path.dirname(p), cc, fam, mid, seen | {p})
        elif ch.tag == "Group":
            walk(ch, base, cc, fam, mid, seen)
        elif ch.tag == "ModOp":
            handle_op(ch, conds, fam, mid)

for top in sorted(os.listdir(MODS)):
    if top == SELF:
        continue
    tp = os.path.join(MODS, top)
    if not os.path.isdir(tp):
        continue
    for dp, _, fs in os.walk(tp):
        if "assets.xml" in fs and dp.replace("\\", "/").endswith("data/base/config/export"):
            p = os.path.join(dp, "assets.xml")
            root = load(p)
            if root is None:
                continue
            fam = FAMILIES.get(top, "other")
            walk(root, dp, [], fam, modid(dp), {p})

if __name__ == "__main__":
    for k in sorted(data):
        print(k, len(data[k]))
