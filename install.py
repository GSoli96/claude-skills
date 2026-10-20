#!/usr/bin/env python3
"""Installa o aggiorna il plugin gsoli-setup (hook di avvio) su questa macchina: Windows, macOS, Linux.

Uso, dalla copia del repository che Claude Code scarica con il marketplace:
    python3 ~/.claude/plugins/marketplaces/gsoli-skills/install.py            # installa o aggiorna
    python3 ~/.claude/plugins/marketplaces/gsoli-skills/install.py --check    # aggiorna solo se serve
Su Windows `python` al posto di `python3`. Servono git e Claude Code; il repository è pubblico, niente login.
Prima volta: claude plugin marketplace add GSoli96/claude-skills, poi questo script.

Sul PC principale (file ~/.claude/gsoli-skills.source) non fa nulla: lì gli hook sono già configurati a mano.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

REPO = "GSoli96/claude-skills"
MARKETPLACE = "gsoli-skills"
PLUGIN = f"gsoli-setup@{MARKETPLACE}"
SOURCE_MARK = os.path.join(os.path.expanduser("~"), ".claude", "gsoli-skills.source")
ENV = dict(os.environ, CLAUDE_CODE_PLUGIN_PREFER_HTTPS="1")


def run(*cmd, check=False):
    exe = shutil.which(cmd[0])
    if not exe:
        sys.exit(f"Manca il comando '{cmd[0]}': installalo e riprova.")
    r = subprocess.run([exe, *cmd[1:]], capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=ENV, stdin=subprocess.DEVNULL)
    if check and r.returncode != 0:
        sys.exit(f"Errore in '{' '.join(cmd)}':\n{r.stderr.strip() or r.stdout.strip()}")
    return r


def installed_version():
    r = run("claude", "plugin", "list", "--json")
    try:
        for p in json.loads(r.stdout or "[]"):
            if p.get("id") == PLUGIN:
                return p.get("version") or ""
    except json.JSONDecodeError:
        pass
    return None


def remote_head():
    r = run("git", "ls-remote", f"https://github.com/{REPO}.git", "HEAD")
    return r.stdout.split()[0] if r.returncode == 0 and r.stdout.strip() else None


def main():
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="aggiorna solo se il repository è cambiato")
    a = ap.parse_args()

    if os.path.isfile(SOURCE_MARK):
        print("PC principale: gli hook sono configurati a mano. Niente da fare.")
        return
    head = remote_head()
    version = installed_version()
    if a.check and head and version and head.startswith(version):
        print(f"gsoli-setup aggiornato (versione {version}).")
        return

    if run("claude", "plugin", "marketplace", "update", MARKETPLACE).returncode != 0:
        run("claude", "plugin", "marketplace", "add", REPO, check=True)
    if version is None:
        run("claude", "plugin", "install", PLUGIN, check=True)
        print("Hook di avvio installati.")
    else:
        run("claude", "plugin", "update", PLUGIN, check=True)
        print("Hook di avvio aggiornati.")
    print("Valgono dalla prossima sessione di Claude Code.")


if __name__ == "__main__":
    main()
