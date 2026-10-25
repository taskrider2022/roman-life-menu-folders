# Roman Life - Menu Folders

**Less scrolling, more building.**

A construction-menu organizer for Anno 117: Pax Romana and Khayi's Roman Life
mods. Buildings from Roman Life - Latium, Albion and Imperial Blends are grouped
into submenus for each population tier, without changing gameplay.

![Roman Life - Menu Folders](media/modio-cover.png)

## Download and installation

Download the mod ZIP from [GitHub Releases](https://github.com/taskrider2022/roman-life-menu-folders/releases).
Choose the attached `roman-life-menu-folders-gammelflei-<version>.zip`,
not GitHub's automatically generated source-code archives.

1. Extract the ZIP into the game's `mods` directory.
2. Check that it contains a folder named
   `[QoL] Roman Life - Menu Folders (Gammelflei)` with `modinfo.json` inside.
3. Enable the mod alongside the Roman Life modules you want to use.

For updates, replace the previous installation instead of enabling two copies.
Python and the development tools are not needed to play.

## What it does

- Nine population-tier submenus: four for Latium and five for Albion.
- Buildings sorted by need category and unlock requirements.
- Regional icons: laurel wreath with R for Latium, triskele for Albion.
- Descriptive tooltips and localized mod information in all twelve game languages.
- Respects the original Roman Life module conditions.
- With Exotic Trade and Imperial Games, groups its alternative Roman Life
  recipe chains into the matching folders and respects its incense tier change.
  Standalone Exotic Trade entries stay outside these folders.
- Leaves other mods' menu entries, production recipes, needs and balancing unchanged.

## Using the menus

Open the construction menu for the population tier you want and select
**Roman Life**. Choose a building inside the submenu and place it as usual.

The available buildings depend on your enabled Roman Life modules. This mod
organizes existing content; it does not add the Roman Life buildings itself.
It is not a general compatibility patch for other mods.
The load order after supported Roman Life modules is specified automatically.

## Before and after

### Latium

| Without Menu Folders | With Menu Folders |
| --- | --- |
| ![Latium without Menu Folders](media/screenshots/menu-latium-without-mod.png) | ![Latium with Menu Folders](media/screenshots/menu-latium.png) |

### Albion

| Without Menu Folders | With Menu Folders |
| --- | --- |
| ![Albion without Menu Folders](media/screenshots/menu-albion-without-mod.png) | ![Albion with Menu Folders](media/screenshots/menu-albion.png) |

## Current limitations

- Translations are provided for all twelve game languages, but not all have
  been reviewed by native speakers.
- The tooltip mentions Imperial Blends when its parent mod is loaded, regardless
  of which individual modules contribute to that particular submenu.
  Switching this text with and without Imperial Blends still needs an in-game check.
- The proposed GUID range is awaiting approval in
  [GuidRanges PR #153](https://github.com/anno-mods/GuidRanges/pull/153).

## Credits and licensing

Menu organization by **gammelflei**. Roman Life content by
[Khayi on mod.io](https://mod.io/g/anno-117-pax-romana/u/khayi).
This is an unofficial companion mod.

The promotional illustrations were created using AI. Gallery images are
in-game screenshots, cropped and supplemented with title overlays.

Project code is licensed under [MIT](LICENSE). Supplied illustrations and
their derivatives are excluded from that grant; it does not grant rights to
game screenshots or third-party game assets. Roman Life game-data files are
not redistributed. Anno and its names belong to their respective owners.

## Project documentation

- [Changelog](CHANGELOG.md): per-version release notes in German and English.
- [Development and publishing](DEVELOPMENT.md): generation, tests, packaging and releases.
- [Task list](TODO.md): completed work and outstanding checks.
- [mod.io listing](media/modio-texts.md): player-facing copy in English and German.
