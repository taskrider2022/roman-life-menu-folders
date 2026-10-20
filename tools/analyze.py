import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from gather import data, MODS
from collections import defaultdict, Counter
from xml.etree import ElementTree as ET

ROOTS = [os.path.join(MODS, d) for d in os.listdir(MODS) if "Roman Life" in d or "Khayi" in d]
asset_re = re.compile(r"<Asset>\s*<Template>(\w+)</Template>(.*?)</Asset>", re.S)

needs = {}      # need guid -> (category, product)
triggers = []   # (unlocked guids set, context, amount)
for r in ROOTS:
    for dp, _, fs in os.walk(r):
        for f in fs:
            if not f.endswith(".xml") or f.startswith("texts_") or f == "modinfo.json":
                continue
            try:
                root = ET.parse(os.path.join(dp, f)).getroot()
            except ET.ParseError:
                continue
            for a in root.iter("Asset"):
                tpl = a.findtext("Template")
                v = a.find("Values")
                if not tpl or v is None:
                    continue
                g = v.findtext("Standard/GUID")
                if not g:
                    continue
                if tpl == "Need":
                    needs[g] = v.findtext("Need/NeedCategoryType")
                elif tpl.startswith("Trigger"):
                    ua = {x.text for x in v.iter("Asset") if x.text and x.text.isdigit()}
                    ctx = v.findtext(".//ConditionPlayerCounter/Context")
                    amt = v.findtext(".//ConditionPlayerCounter/CounterAmount")
                    if ua:
                        triggers.append((ua, ctx, int(amt) if amt else None))

def info(b):
    cat = ctx = amt = None
    for ua, c, a in triggers:
        if b in ua:
            for x in ua:
                if x in needs:
                    cat = needs[x]
            ctx, amt = c, a
            if cat:
                break
    return cat, ctx, amt

if __name__ == "__main__":
    seen = {}
    for (fam, cat), items in sorted(data.items()):
        for b, _, mid in items:
            seen[(cat, b)] = (fam, mid)
    miss = 0
    cnt = Counter()
    for (cat, b), (fam, mid) in sorted(seen.items()):
        n, c, a = info(b)
        cnt[(cat, n, c)] += 1
        if n is None or c is None:
            miss += 1
            print("MISSING", cat, b, mid, n, c, a)
    print("total", len(seen), "missing", miss)
    for k, v in sorted(cnt.items(), key=lambda x: str(x)):
        print(k, v)
