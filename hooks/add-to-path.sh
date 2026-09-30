#!/usr/bin/env bash
# SessionStart / setup hook: put universal-modder's bin/ on PATH for every later Bash call in the session,
# so skills can just say `um ...`. Arg 1: the toolkit root (plugin root or the cloned repo).
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fallback_root="$(cd "$script_dir/.." && pwd)"
root="${1:-${ANTIGRAVITY_PROJECT_DIR:-${GEMINI_PROJECT_DIR:-${WORKSPACE_ROOT:-${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PROJECT_DIR:-$fallback_root}}}}}}"

if [ -n "$root" ] && [ -x "$root/bin/um" ]; then
  if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
    if ! grep -qs "universal-modder-path" "$CLAUDE_ENV_FILE"; then
      printf 'export PATH="%s/bin:$PATH"  # universal-modder-path\n' "$root" >> "$CLAUDE_ENV_FILE"
    fi
  fi
  export PATH="$root/bin:$PATH"
fi
exit 0
