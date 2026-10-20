# claude-skills

Hook di avvio per Claude Code che accompagnano le mie skill personali. Le skill arrivano da claude.ai; qui c'è solo ciò che claude.ai non distribuisce. Funziona su Windows, macOS e Linux.

Il plugin `gsoli-setup` contiene un hook che, all'avvio di una sessione in una cartella senza `CLAUDE.md` né `AGENTS.md`, chiede a Claude di proporre (alla fine del primo compito, senza interrompere) i file che gli fanno ricordare il progetto, con la skill `scaffolding-project-files`. Se la cartella ha già quei file e c'è un `TO_CONTINUE.md`, gli ricorda di leggerlo.

## Installazione

Di solito non serve fare niente: la prima volta che una delle mie skill viene usata, Claude esegue da solo questi passi. A mano:

```
claude plugin marketplace add GSoli96/claude-skills
python3 ~/.claude/plugins/marketplaces/gsoli-skills/install.py
```

Su Windows `python` al posto di `python3`. Servono git e Claude Code; il repository è pubblico, quindi niente login. Con `--check` lo script aggiorna solo se il repository è cambiato. L'hook vale dalla sessione successiva.

## Licenza

MIT, vedi `LICENSE`.
