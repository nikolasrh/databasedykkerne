# Steg 5: AI-agent integrasjon

Dette steget viser hvordan en AI-agent (f.eks. Claude, GPT, eller andre) kan bruke RAG-søk for å hente relevant informasjon før den svarer på spørsmål.

Filene `AGENTS.md` og `CLAUDE.md` (symlink) inneholder instruksjoner som AI-agenten leser for å forstå hvordan den skal utføre søk.

Åpne denne mappen med `claude` eller `opencode`, og agenten skal automatisk plukke opp instruksjonsfilene.

Test med å spørre agenten hva den ville gjort hvis den mottar et spørsmål, eller om den har lest noen instruksjonsfiler.

Hvis man har lastet eksempel-PDF-ene kan man f.eks. spørre om reglene til Kill Team.

> Help me find the rule for the Death Guard team that reduces damage taken.

## Frivillige oppgaver

- Bygg en MCP-server (Model Context Protocol) i stedet for å be agenten kjører docker-kommandoer
