# Roman Life Menu Folders

Anno 117 - Pax Romana mod. Groups the Roman Life construction menu entries
(Latium, Albion, Imperial Blends by Khayi) into one folder per population tier.
Items from other mods (Celtic Independence Overhaul, Pizza Margherita, ...) are left untouched.

## Layout

```
mod/                 the mod itself, generated output (committed, usable without Python)
tools/gen.py         generator: assets.xml, texts, modinfo.json (LoadAfter), icons
tools/gather.py      collects the buildings Roman Life adds to the tier categories (41327-41331 Albion, 41362-41365 Latium), with conditions
tools/analyze.py     reads need category and unlock order from the Roman Life game data
tools/icons.py       draws the two folder icons
tools/guidrange.py   GUID range of this mod + local replay of the GuidRanges registration
tools/package.py     reproducible ZIP builder (dist/)
tests/test_mod.py    static checks (XML, GUID range, LoadAfter, texts, icons, ZIP layout)
.github/workflows/   CI: tests + ZIP on push, GitHub Release on tag vX.Y.Z
```

## Regenerating

Needs Python 3 with Pillow (`python -m pip install -r requirements.txt`).
Run it after any Roman Life update that adds or moves menu items:

    python -X utf8 tools/gen.py --mods "D:\path\to\Anno 117 - Pax Romana\mods"

`--mods` can be replaced by the `ANNO_MODS` environment variable. `--out <dir>` overrides the output folder (default `mod/`).
`mod/modinfo.json` must exist before the first run, the script only updates `Version`, `ModID`, `ModName`, `Description` and `LoadAfter`.

## Tests and ZIP

    python -m unittest discover -s tests -v
    python tools/package.py          # writes dist/roman-life-menu-folders-gammelflei-<version>.zip

The ZIP contains `[QoL] Roman Life Menu Folders (Gammelflei)/`.
ModID: `roman-life-menu-folders-gammelflei`. Replace the previous installation,
do not enable both ModIDs at the same time. Internal icons use
`data/roman-life-menu-folders-gammelflei/ui/`.

The tests prove the files are well-formed and consistent. They do not prove the game accepts the mod, see the checklist below.

## GUID range

The mod uses the proposed range **2.110.000.000 - 2.110.000.999** (`tools/guidrange.py`),
9 folder GUIDs reused as title LineIds, plus shared description LineId 2110000100.
The registration for `gammelflei` is submitted in
[GuidRanges PR #153](https://github.com/anno-mods/GuidRanges/pull/153).
It is pending approval, not yet an accepted reservation.

Registration follows [anno-mods/GuidRanges](https://github.com/anno-mods/GuidRanges): fork it, add one row to the
"Public GUID Ranges" table in `117/guids.md` (sorted by start ID), open a pull request. Discord is linked from that repo.

Local replay of that process (no push):

    git clone https://github.com/anno-mods/GuidRanges.git
    python tools/guidrange.py check GuidRanges    # safe range, size, overlap with every registered range
    python tools/guidrange.py apply GuidRanges    # adds the row on branch add-gammelflei-range and commits it

`apply` prints the diff that would go into the pull request. The real PR still has to be opened from your own GitHub fork.
If the range is taken by the time of the PR, change `RANGE_START`/`RANGE_END` in `tools/guidrange.py`, run `gen.py`, bump the version.

## Releasing

Plain-text release notes in German and English are kept in
[CHANGELOG.md](CHANGELOG.md). Each uploaded ZIP has its own changelog on mod.io:
copy only the notes for that version and the desired language, without Markdown
formatting or earlier versions. The first upload (0.5.1) lists the full feature
set; subsequent entries list only changes since the previous version, not the
full feature set or internal documentation tasks. Before uploading, finalize
the entry and its upload date.

1. Bump `Version` (in `tools/gen.py`), regenerate, run the tests.
2. Commit, tag `v<version>` (must equal `Version` in `mod/modinfo.json`), push the tag.
3. CI creates a GitHub Release (pre-release) with the ZIP.
4. mod.io upload is manual for now: create the mod page, upload `dist/*.zip`. The reference repo `loispostula/anno117-olive-oil-amphora` shows how to automate it (needs `MODIO_GAME_ID`, `MODIO_MOD_ID` variables and `MODIO_TOKEN`, `MODIO_DOMAIN` secrets).

### mod.io publication checklist (internal)

- Use the player-facing copy in [media/modio-texts.md](media/modio-texts.md);
  do not include this checklist in the listing.
- Review the listing before publishing. Tab titles, tooltips and localization
  tasks are tracked in [TODO.md](TODO.md).
- Verify the final ZIP in game.
- Check the [GUID reservation status](https://github.com/anno-mods/GuidRanges/pull/153).
- Confirm the artwork attribution and redistribution terms before publishing.
- Use [media/modio-cover.png](media/modio-cover.png) (1920 x 1080) as the cover.
- Gallery images with the submenus open:
  [Latium](media/screenshots/menu-latium.png) and
  [Albion](media/screenshots/menu-albion.png), each 1920 x 1080.
  These are cropped game screenshots with a title overlay; originals are kept
  in `media/sources/`.
- For each ZIP, paste only that version's plain-text notes from
  [CHANGELOG.md](CHANGELOG.md), in the desired language.

## In-game test checklist

- Latium: folders for all four tiers appear in the construction bar, items inside are sorted Food, Culture, Fashion, Household.
- Albion tiers I-III and Roman Way II: Roman Life items (including Imperial Blends and sub-mods such as Bog Butter) are inside the folder, nothing from Roman Life is left in the flat menu.
- Celtic Independence items stay in the flat menu where that mod puts them.
- Remove the mod mid-save: the game loads, items return to the flat menu (`SafeToRemove`).

## Notes

- Tooltip text mentions Imperial Blends only when `#rl-shared-khayi` is loaded.
  This checks the parent mod's presence, not which individual modules contribute
  to a particular tab. Both condition branches are generated for all twelve languages.

- Menu icons use the selected B badges: laurel/R for Latium and triskele for
  Albion. The detailed table illustrations remain on the cover images.
  Run `python tools/media.py` to rebuild icons, previews and the three title-image
  proposals in `media/cover-proposals/`. Original-mod covers are style references
  only and are not composited into the images.

- Release tasks and developer feedback are tracked in [TODO.md](TODO.md).
- Run `python tools/media.py` to rebuild the supplied-artwork icons, the
  1920 x 1080 mod.io cover and the small-size comparison in `media/`.
  Sources are kept in `media/sources/`; the cover and preview are not shipped in the mod ZIP.

- Load order: the mod must load after all Roman Life mods (`LoadAfter`), otherwise late insertions stay in the flat menu.
- Both regional tabs are titled "Roman Life", covering enabled modules including
  Imperial Blends. `tools/localization.py` provides draft descriptions and mod
  metadata for all twelve game languages. Native-speaker review is pending.
- All tabs reference the shared description through
  `ConstructionCategory/CategoryDescription`, defined as Text in the game's
  `properties-meta.xml` and used by vanilla construction categories.
  The earlier `Standard/InfoDescription` attempt did not display in game.
  The corrected field still needs an in-game check in both regions.
- The tier-to-category mapping and "Culture = Dienste" come from game data and are only tested in-game for Latium and Albion.

## Licensing

[MIT](LICENSE) for the project code. The developer-supplied artwork in
`media/sources/` and images derived from it (including the menu icons) are
excluded from this grant; confirm the rights holder's redistribution terms
before publishing. Roman Life game-data files are not redistributed.
Anno and its names belong to their respective owners.
