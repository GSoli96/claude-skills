#!/usr/bin/env python3
"""SessionStart hook: when the project has no rulebook, remind Claude to offer the scaffolding-project-files skill;
when TO_CONTINUE.md exists, remind Claude to read it. Folders listed in scaffold_declined.txt (one absolute path per
line, written when the user answers "Nothing") are never asked again.
Reads the hook JSON on stdin (uses cwd), prints JSON with additionalContext. Never fails the session."""
import json
import os
import sys

# The plugin cache is replaced at every update: keep the declined list in the user's folder.
DECLINED = os.path.join(os.path.expanduser('~'), '.claude', 'hooks', 'scaffold_declined.txt')

try:
    data = json.load(sys.stdin)
except Exception:
    data = {}
cwd = os.path.normcase(os.path.abspath(data.get('cwd') or os.getcwd()))

declined = set()
try:
    with open(DECLINED, encoding='utf-8') as f:
        declined = {os.path.normcase(os.path.abspath(line.strip())) for line in f if line.strip()}
except OSError:
    pass

home = os.path.normcase(os.path.expanduser('~'))
names = ('CLAUDE.md', os.path.join('.claude', 'CLAUDE.md'), 'AGENTS.md', 'CLAUDE.local.md')
rulebook = [n for n in names if os.path.isfile(os.path.join(cwd, n))]
notes = []
if not rulebook and cwd not in declined and cwd != home:
    notes.append(
        "This folder has no CLAUDE.md or AGENTS.md. Do not interrupt: if the user's first message is a task, do the task first "
        "and at the end offer, in one line, to prepare memory files for this project with the personal skill "
        "`scaffolding-project-files`. Ask before the task only if the user asks for the setup or only greets. "
        "Use the flow and exact texts of the skill's references/questions.md: deduce the scenario from the folder and the request (section 1), ask only its questions, end with the summary. "
        "'Più tardi' means ask again next session; 'Mai in questa cartella' means create nothing, append this folder's absolute "
        f"path to {DECLINED} and tell the user they can ask later with 'prepara i file per Claude'. "
        "Create no file before the final summary is confirmed.")
elif rulebook:
    if os.path.isfile(os.path.join(cwd, 'TO_CONTINUE.md')):
        notes.append("TO_CONTINUE.md exists in this project: read it right after the rulebook and resume from its 'Restart from' list.")

if notes:
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": " ".join(notes)}}))
sys.exit(0)
