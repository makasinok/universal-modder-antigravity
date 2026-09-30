"""Diagnose the modding agent environment: OS, Python, tools, Steam, Proton, codecs, fal key.

    um doctor
    um doctor --json
"""
from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from um.common import find_steam_cmd, is_linux, is_mac, is_windows, is_wsl
from um.scan import heroic_games, lutris_games, steam_games, steam_roots


def _check_cmd(cmd: str) -> dict:
    p = shutil.which(cmd)
    if not p:
        return dict(status="MISSING", path=None, version=None)
    ver = None
    try:
        r = subprocess.run([p, "--version"], capture_output=True, text=True, timeout=5)
        out = (r.stdout or r.stderr).strip().splitlines()
        ver = out[0] if out else "installed"
    except Exception:
        ver = "installed"
    return dict(status="OK", path=p, version=ver)


def diagnose() -> dict:
    os_name = "Linux" if is_linux() else "WSL" if is_wsl() else "Windows" if is_windows() else "macOS" if is_mac() else sys.platform
    display = os.environ.get("XDG_SESSION_TYPE") or ("Wayland" if os.environ.get("WAYLAND_DISPLAY") else "X11" if os.environ.get("DISPLAY") else "unknown")

    report = {
        "system": {
            "os": os_name,
            "kernel": platform.release(),
            "machine": platform.machine(),
            "display_server": display,
            "python": sys.version.split()[0],
        },
        "core_tools": {
            "uv": _check_cmd("uv"),
            "ffmpeg": _check_cmd("ffmpeg"),
            "blender": _check_cmd("blender"),
            "git": _check_cmd("git"),
        },
        "linux_automation": {},
        "game_stores": {},
        "reverse_engineering": {
            "dotnet": _check_cmd("dotnet"),
            "ilspycmd": _check_cmd("ilspycmd"),
            "ghidra": _check_cmd("ghidra"),
        },
        "fal_ai": {
            "key_set": bool(os.environ.get("FAL_KEY")),
            "status": "OK" if os.environ.get("FAL_KEY") else "MISSING (export FAL_KEY=...)",
        }
    }

    if is_linux() or is_wsl():
        report["linux_automation"] = {
            "xdotool": _check_cmd("xdotool"),
            "xprop": _check_cmd("xprop"),
            "import (imagemagick)": _check_cmd("import"),
            "grim": _check_cmd("grim"),
            "ydotool": _check_cmd("ydotool"),
        }

    # Steam & Proton status
    roots = steam_roots()
    steam_cmd = find_steam_cmd()
    games = steam_games()
    proton_dirs = []
    for r in roots:
        compat = r / "steamapps" / "compatdata"
        if compat.is_dir():
            proton_dirs += [str(p) for p in compat.iterdir() if (p / "pfx").is_dir()]

    report["game_stores"] = {
        "steam_cmd": " ".join(steam_cmd),
        "steam_libraries": [str(r) for r in roots],
        "steam_games_found": len(games),
        "proton_prefixes_found": len(proton_dirs),
        "heroic_games_found": len(heroic_games()),
        "lutris_games_found": len(lutris_games()),
    }

    # Codecs check
    ff = shutil.which("ffmpeg")
    codecs = []
    if ff:
        for c in ("h264_nvenc", "hevc_nvenc", "h264_vaapi", "h264_qsv", "libx264"):
            try:
                r = subprocess.run([ff, "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                                    "-i", "color=black:s=256x256:d=0.1", "-c:v", c, "-f", "null", "-"],
                                   capture_output=True, text=True, timeout=5)
                if r.returncode == 0:
                    codecs.append(c)
            except Exception:
                pass
    report["ffmpeg_hardware_encoders"] = codecs

    return report


def run_doctor(args):
    data = diagnose()
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return

    sys_info = data["system"]
    print("=" * 60)
    print(" universal-modder system doctor")
    print("=" * 60)
    print(f" OS:             {sys_info['os']} ({sys_info['machine']}, {sys_info['kernel']})")
    print(f" Display Server: {sys_info['display_server']}")
    print(f" Python:         {sys_info['python']}")
    print()

    print("--- Core Tools ---")
    for name, item in data["core_tools"].items():
        st = item["status"]
        sym = "✓" if st == "OK" else "✗"
        ver = f" ({item['version']})" if item.get("version") else ""
        print(f"  [{sym}] {name:<12} {st:<8} {ver}")
    print()

    if data.get("linux_automation"):
        print("--- Linux Automation (Input / Window Capture) ---")
        for name, item in data["linux_automation"].items():
            st = item["status"]
            sym = "✓" if st == "OK" else "✗"
            print(f"  [{sym}] {name:<22} {st:<8}")
        print()

    print("--- Game Platforms & Runtimes ---")
    gs = data["game_stores"]
    print(f"  Steam launcher:    {gs['steam_cmd']}")
    print(f"  Steam libraries:   {len(gs['steam_libraries'])} found")
    print(f"  Steam games:       {gs['steam_games_found']} installed")
    print(f"  Proton prefixes:   {gs['proton_prefixes_found']} active")
    print(f"  Heroic games:      {gs['heroic_games_found']} installed")
    print(f"  Lutris games:      {gs['lutris_games_found']} installed")
    print()

    print("--- Reverse Engineering Tools ---")
    for name, item in data["reverse_engineering"].items():
        st = item["status"]
        sym = "✓" if st == "OK" else "✗"
        print(f"  [{sym}] {name:<12} {st:<8}")
    print()

    print("--- Asset Pipeline (fal.ai) ---")
    fal_st = data["fal_ai"]["status"]
    sym = "✓" if data["fal_ai"]["key_set"] else "!"
    print(f"  [{sym}] FAL_KEY:     {fal_st}")
    print()

    print("--- FFmpeg Video Encoders ---")
    encs = data.get("ffmpeg_hardware_encoders", [])
    print(f"  Available: {', '.join(encs) if encs else 'none'}")
    print("=" * 60)


def register(sub):
    p = sub.add_parser("doctor", help="diagnose environment, installed tools, Steam/Proton, and codecs")
    p.add_argument("--json", action="store_true", help="output machine-readable JSON report")
    p.set_defaults(func=run_doctor)
