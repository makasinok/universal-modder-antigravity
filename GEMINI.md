# universal-modder for Antigravity & Gemini

This repository is a game-modding toolkit for AI coding agents, fully adapted for **Antigravity** (Google DeepMind) and Gemini models, as well as Claude Code, Codex, and Cursor.

When starting a modding task, invoke the **`mod-any-game`** skill (`skills/mod-any-game/SKILL.md` or `.agents/skills/mod-any-game/SKILL.md`) and adhere to the 10-step loop:
1. **Intake**: Clarify the user's mod idea and target game.
2. **Recon** (`game-recon`): Fingerprint engine, runtime (.NET, native, Java), loaders, anti-cheat, save paths.
3. **Route**: Select the cleanest, most maintainable modding path (e.g. Harmony, BepInEx, tModLoader, UE4SS, Lua, data patches).
4. **Lab**: Isolate test environment; back up user saves with `um backup`.
5. **Source of Truth** (`reverse-engineering`): Read actual decompiled game code / schemas before writing mods.
6. **Vertical Slice**: Implement the smallest playable feature end-to-end first.
7. **Assets** (`fal-assets` & `asset-pipeline`): Generate sprites, textures, 3D models, sound, voice, and convert to game-ready formats.
8. **Verify in Game** (`game-automation`): Launch game windowed, capture screenshots, check logs, simulate input safely.
9. **Showcase** (`showcase-video`): Record gameplay clips, compile contact sheets, edit trailer with titles and audio.
10. **Publish** (`publish-mod`): Run pre-release lint checks, generate clean README, disclose AI asset creation.

---

## Workspace Skills (`.agents/skills/` and `skills/`)

- `mod-any-game`: The master modding orchestrator with 12 engine playbooks (`skills/mod-any-game/references/engines/`).
- `game-recon`: Engine detection, save discovery, anti-cheat audit, produces `MODDING_PLAN.md`.
- `reverse-engineering`: Decompile, dump data formats, inspect memory, analyze render passes.
- `fal-assets`: AI generation for sprites, textures, PBR maps, image-to-3D, SFX, music, voice.
- `asset-pipeline`: Fit art to engine specs (nearest-neighbor scaling, palettes, sprite sheets, directional frames).
- `game-automation`: Windowed launch, GPU-safe screenshots, keyboard/mouse input, crash reporter handling.
- `showcase-video`: Clip capture, EDL timeline editing, titles, music sync, video compilation.
- `mashup-mods`: Cross-game mechanics, content ports, passthrough architectures.
- `publish-mod`: Linter against shipping game files, decompiled code or leaked secrets.

---

## Tooling & CLI (`bin/um`)

`bin/um` is the unified Python CLI for the modder agent:
- `um scan`: Locate Steam/Epic/Xbox games and fingerprint engines.
- `um fal`: Direct CLI for fal.ai generation (sprites, textures, 3D, audio).
- `um sprite`: 2D sprite processing (cutout, palette quantization, sheet generation).
- `um render3d`: GLB to sprite frames with custom camera angles (Blender).
- `um win`: Windows/WSL automation (launch, screenshot, game-audio recording, PID management).
- `um video`: Showcase video compiler and contact sheet generator.
- `um backup`: Snapshot and restore game saves.
- `um publish check`: Audit mod repository before publishing.

MCP integration is configured in `mcp_config.json` and `.mcp.json` (requires `FAL_KEY`).

---

## Hard Safety Rules

1. **Owned Games & Offline Only**: Only mod single-player, offline games owned by the user. Refuse to touch multiplayer games with anti-cheat, and never bypass anti-cheat, DRM, or ownership verification.
2. **Safe Backups**: Always run `um backup` before touching game folders or running modded saves.
3. **No Leaked Game Code or Assets**: Never ship original game files or decompiled code in the mod repository. Keep decompiles outside the project directory.
4. **PID-Based Process Control**: Always terminate processes using their specific PID (`um win kill`), never generic process name kills.
5. **User Consent**: Ask user permission before driving mouse/keyboard, installing mod loaders into game directories, editing system registries, or publishing.
6. **Mod Journal**: Maintain a `MODLOG.md` in the mod workspace tracking discoveries, entity IDs, offsets, and milestones.

---

*Adapted and configured by **Antigravity** (Google DeepMind)*
