# claude-skills

Hook di avvio per Claude Code che accompagnano le mie skill personali. Le skill arrivano da claude.ai; qui c'è solo ciò che claude.ai non distribuisce. Funziona su Windows, macOS e Linux.

Il plugin `gsoli-setup` ha due hook di avvio:
- `gsoli_setup.py`, a ogni avvio: scrive nel contesto `gsoli-setup: ok`, copia in `~/.claude/CLAUDE.md` le regole globali arrivate da claude.ai con la skill `configura-claude` quando sono cambiate (tenendo una copia datata della versione precedente) e, al massimo una volta al giorno, controlla in background se c'è una versione nuova di questo plugin;
- `check_scaffold.py`, in una cartella senza `CLAUDE.md` né `AGENTS.md`: chiede a Claude di proporre, alla fine del primo compito e senza interrompere, i file che gli fanno ricordare il progetto (skill `scaffolding-project-files`); se la cartella ha già quei file e c'è un `TO_CONTINUE.md`, gli ricorda di leggerlo.

## Installazione

Di solito non serve fare niente: su una macchina nuova, al primo messaggio, la skill `configura-claude` (da claude.ai) esegue questi passi. A mano:

```
claude plugin marketplace add GSoli96/claude-skills
python3 ~/.claude/plugins/marketplaces/gsoli-skills/install.py
```

Su Windows `python` al posto di `python3`. Servono git, Python 3 e Claude Code; il repository è pubblico, quindi niente login. Con `--check` lo script aggiorna solo se il repository è cambiato. Gli hook valgono dalla sessione successiva.

## Licenza

MIT, vedi `LICENSE`.
