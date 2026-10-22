# Development and publishing

Player-facing installation and usage instructions are in [README.md](README.md).

## Repository layout

- `mod/`: generated, committed game files; usable without Python.
- `tools/`: generation, artwork and packaging tools.
- `tests/`: static checks for metadata, XML, localization, images and ZIP layout.
- `media/`: artwork sources, covers, gallery images and mod.io copy.
- `.github/workflows/ci.yml`: tests and packaging on main/PRs; releases on version tags.

## Regenerating the mod

Use Python 3.12, as in CI, and install the declared dependencies:

```powershell
python -m pip install -r requirements.txt
python -X utf8 tools\gen.py --mods "D:\path\to\Anno 117 - Pax Romana\mods"
```

Run from the repository root. The generator reads the installed upstream mods.
Regenerate after relevant Roman Life updates that add or move menu items.
`ANNO_MODS` can replace `--mods`. `--out <dir>` changes the output directory;
that directory must already contain `modinfo.json`.

Version is set in `tools/gen.py`. Generation updates the assets, translations,
icons and the Version, ModID, ModName, Description and LoadAfter metadata fields.
Avoid making persistent changes only in generated output.

## Tests and packaging

```powershell
python -m unittest discover -s tests -v
python tools\package.py
```

The package is written to
`dist/roman-life-menu-folders-gammelflei-<version>.zip`, containing
`[QoL] Roman Life - Menu Folders (Gammelflei)/`.
Only files from `mod/` are shipped.

Packaging is reproducible for identical input bytes. Windows and Linux
checkouts can have different text line endings and therefore different ZIP hashes.
Tests check consistency, not full game compatibility.

Approved deployed icons are checked against pixel SHA-256 snapshots in
`tests/test_images.py`, not against a platform-dependent redraw.
Update those snapshots only after intentionally changing and visually approving
the icons. Font and Pillow differences can affect regenerated artwork.

## Technical notes

- ModID: `roman-life-menu-folders-gammelflei`.
- Proposed GUID range: 2110000000-2110000999. Folder GUIDs are
  2110000000-2110000008; shared description LineId is 2110000100.
  [Registration PR #153](https://github.com/anno-mods/GuidRanges/pull/153)
  is open, not accepted (checked 2026-10-22).
- `tools/guidrange.py` maintains the allocation and can check it against a local
  checkout of `anno-mods/GuidRanges`.
- `LoadAfter` covers the supported Roman Life modules so late insertions are
  included. Preserve upstream conditions when moving entries.
- Tooltips use `ConstructionCategory/CategoryDescription`; display has been
  confirmed in both regions.
- `tools/localization.py` provides twelve-language metadata and descriptions.
  Mutually exclusive text operations check `#rl-shared-khayi` and its absence
  to select wording with or without Imperial Blends.
- `python tools\media.py` rebuilds badges, the selected parchment cover,
  cover proposals and previews. Detailed table illustrations are promotional
  artwork, not the deployed menu icons. Gallery screenshots are separate files.

## In-game release checks

- Latium: folders appear for all four tiers; entries follow need and unlock order.
- Albion: folders appear for all five supported tiers, including Roman Way tiers;
  enabled Roman Life and Imperial Blends entries are inside.
- Other mods' entries remain where their own mods place them.
- Check tooltip wording with and without Imperial Blends.
- Check removal mid-save: the save loads and entries return to the original menu
  (`SafeToRemove` is declared, but still needs release testing).

## Publishing

1. Update the version in `tools/gen.py`, regenerate, test and inspect the ZIP.
2. Add player-facing plain-text notes to [CHANGELOG.md](CHANGELOG.md).
   Each ZIP on mod.io has its own changelog. The first upload (0.5.1) lists the
   full feature set; later versions list only changes since the previous version.
   Copy only the relevant version and language, not internal development tasks.
3. Commit and push to `main`; verify Actions succeeds.
4. Create and push a matching tag, for example `v<version>`. It must match
   Version in `mod/modinfo.json`.
5. The workflow builds and attaches the mod ZIP to a GitHub pre-release.
   After testing, edit the release to remove the pre-release flag when ready.
   This is a manual convention, not an enforced approval gate. A pre-release is
   public, not a draft. Version 0.5.1 has already been promoted to a regular release.
6. Upload the actual mod ZIP to mod.io manually. Actions artifact downloads wrap
   it in another ZIP; the release asset is the direct mod ZIP.

Use the English or German player-facing text in
[media/modio-texts.md](media/modio-texts.md). Do not paste this document into the
listing. Cover: [media/modio-cover.png](media/modio-cover.png), 1920 x 1080.
Before/after gallery images are in [media/screenshots/](media/screenshots/);
originals remain in [media/sources/](media/sources/).

Check GUID reservation status and artwork permissions before publishing.
Supplied artwork is excluded from the project's MIT grant.
Remaining reviews are tracked in [TODO.md](TODO.md).
Automated mod.io uploads are not configured.
