#!/usr/bin/env python3
"""SessionStart hook: keeps this machine's personal Claude Code setup current, without asking Claude to do anything.

1. Writes 'gsoli-setup: ok' in the session context, so the skill configura-pc is not run again.
2. Copies regole-globali.md of the skill configura-pc (synced from claude.ai) to ~/.claude/CLAUDE.md
   when they differ, keeping a dated copy of the previous file.
3. At most once a day, at startup, starts install.py --check in the background to update this plugin.
Does nothing but step 1 on the main PC (~/.claude/gsoli-skills.source). Never fails the session.
"""
import filecmp
import glob
import json
import os
import shutil
import subprocess
import sys
import time

CLAUDE_DIR = os.path.join(os.path.expanduser("~"), ".claude")
SOURCE_MARK = os.path.join(CLAUDE_DIR, "gsoli-skills.source")
STAMP = os.path.join(CLAUDE_DIR, "gsoli-setup.lastcheck")
LOG = os.path.join(CLAUDE_DIR, "gsoli-setup.log")
INSTALL = os.path.join(CLAUDE_DIR, "plugins", "marketplaces", "gsoli-skills", "install.py")


def sync_rules():
    found = glob.glob(os.path.join(CLAUDE_DIR, "skills", "synced", "*", "configura-pc", "regole-globali.md"))
    if not found:
        return None
    src = max(found, key=os.path.getmtime)
    dst = os.path.join(CLAUDE_DIR, "CLAUDE.md")
    if os.path.isfile(dst):
        if filecmp.cmp(src, dst, shallow=False):
            return None
        shutil.copy2(dst, f"{dst}.bak-{time.strftime('%Y%m%d-%H%M%S')}")
    shutil.copy2(src, dst)
    return "regole globali aggiornate da claude.ai in ~/.claude/CLAUDE.md (valgono dalla prossima sessione)"


def check_update():
    try:
        if time.time() - os.path.getmtime(STAMP) < 20 * 3600:
            return
    except OSError:
        pass
    if not os.path.isfile(INSTALL):
        return
    with open(STAMP, "w", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S\n"))
    log = open(LOG, "a", encoding="utf-8")
    kw = {"stdin": subprocess.DEVNULL, "stdout": log, "stderr": log, "cwd": CLAUDE_DIR}
    if os.name == "nt":
        kw["creationflags"] = subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW
    else:
        kw["start_new_session"] = True
    subprocess.Popen([sys.executable, INSTALL, "--check"], **kw)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    notes = ["gsoli-setup: ok (regole globali e hook di avvio installati su questa macchina)."]
    if not os.path.isfile(SOURCE_MARK):
        try:
            msg = sync_rules()
            if msg:
                notes.append(msg[0].upper() + msg[1:] + ".")
        except OSError:
            pass
        if data.get("source", "startup") == "startup":
            try:
                check_update()
            except OSError:
                pass
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": " ".join(notes)}}))


if __name__ == "__main__":
    main()
