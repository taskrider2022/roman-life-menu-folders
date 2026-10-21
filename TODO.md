# Release TODO

## Current priority: artwork

- [x] Preserve the developer-supplied Latium and Albion illustrations in `media/sources/`.
- [x] Replace the previous icons with transparent PNGs made from these illustrations.
- [x] Create a 1920 x 1080 mod.io cover.
- [x] Create a menu-size comparison at 128, 64, 48 and 32 pixels.
- [x] Review the icons in game: crowded motifs may lose detail at small sizes.
- [x] If necessary, agree on simplified crops with the developer.
- [x] Select and install simplified B badges: laurel/R for Latium and triskele
  for Albion, with regional colors and a gold shield border.
- [x] Check the new B badges in game at the actual menu scale.
- [x] Choose a title-image proposal from `media/cover-proposals/`: dark,
  parchment or regional colors. All retain the supplied table illustrations.
  Selected B (parchment); exported as `media/modio-cover.png`.
- [x] Confirm artwork attribution and redistribution permission before publishing.

## Developer feedback: texts and tab behavior (next)

- [x] Use "Roman Life" for both regional tabs, including Imperial Blends content.
- [x] Add a useful description/tooltip for each tab; verify which game field
  ConstructionCategory actually displays.
  Standard/InfoDescription did not display in game. Corrected to
  ConstructionCategory/CategoryDescription (verified in the game schema and
  vanilla assets), with shared LineId 2110000100. Display confirmed by in-game
  screenshots in both regions. Wording revised to a warmer, more inviting tone.
- [x] Describe that the tab bundles enabled Roman Life modules, including
  Imperial Blends, in the appropriate population tier.
- [x] Add all supported game languages, not just English and German:
  Brazilian Portuguese, English, French, German, Italian, Japanese, Korean,
  Polish, Russian, Simplified Chinese, Spanish, Traditional Chinese.
- [x] Supply consistent draft tab descriptions and localized mod names/descriptions.
- [ ] Review translations and need-category terminology with the developer/native speakers.
- [x] Localize mod metadata (name and description). KnownIssues is empty.
- [x] Mention Imperial Blends in tooltips only when its parent mod is loaded;
  generate mutually exclusive descriptions for all twelve languages.
- [ ] Verify tooltip switching in game with and without Imperial Blends.

## mod.io and release

- [ ] Create or select the mod's GitHub repository and configure its remote.
- [ ] Choose the default branch and align the CI branch filter (currently main).
- [ ] Push local commits to GitHub and verify the tests and ZIP artifact in Actions.
- [ ] After release approval, create and push a matching version tag and verify
  the GitHub Release. Tag pushes trigger the release workflow.
- [ ] Review the cover and gallery screenshots with the developer.
- [ ] Prepare final short and full mod.io descriptions, requirements,
  compatibility notes, credits and installation/update instructions.
- [ ] Verify the status of GUID reservation PR #153 before claiming it is accepted:
  https://github.com/anno-mods/GuidRanges/pull/153
- [ ] Confirm permissions for the supplied images; exclude them from the
  project's MIT grant unless the rights holder explicitly licenses them under MIT.
- [ ] Complete the in-game release checklist in README.md, including the new icons.
- [ ] Bump release version, build the ZIP, inspect its contents and upload it.
- [ ] Configure optional automated mod.io uploads separately.
