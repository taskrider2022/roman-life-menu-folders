# Release TODO

## Current priority: artwork

- [x] Preserve the developer-supplied Latium and Albion illustrations in `media/sources/`.
- [x] Replace the previous icons with transparent PNGs made from these illustrations.
- [x] Create a 1920 x 1080 mod.io cover.
- [x] Create a menu-size comparison at 128, 64, 48 and 32 pixels.
- [ ] Review the icons in game: crowded motifs may lose detail at small sizes.
- [ ] If necessary, agree on simplified crops with the developer.
- [x] Select and install simplified B badges: laurel/R for Latium and triskele
  for Albion, with regional colors and a gold shield border.
- [ ] Check the new B badges in game at the actual menu scale.
- [x] Choose a title-image proposal from `media/cover-proposals/`: dark,
  parchment or regional colors. All retain the supplied table illustrations.
  Selected B (parchment); exported as `media/modio-cover.png`.
- [x] Confirm artwork attribution and redistribution permission before publishing.

## Developer feedback: texts and tab behavior (next)

- [ ] Agree on accurate tab titles. "Roman Life - Latium" can imply Latium-only
  contents even though Imperial Blends contributes entries; Albion has the same issue.
  Candidate: "Roman Life" for both regional menus, with region/content explained
  in the tooltip. Do not change titles until this is agreed.
- [ ] Add a useful description/tooltip for each tab; verify which game field
  ConstructionCategory actually displays.
- [ ] Describe that the tab bundles enabled Roman Life modules, including
  Imperial Blends, in the appropriate population tier.
- [ ] Add all supported game languages, not just English and German:
  Brazilian Portuguese, English, French, German, Italian, Japanese, Korean,
  Polish, Russian, Simplified Chinese, Spanish, Traditional Chinese.
- [ ] Translate tab titles and descriptions consistently; review terminology
  and the mapping of need categories with the developer.
- [ ] Localize mod metadata (name, description, known issues) where appropriate.

## mod.io and release

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
