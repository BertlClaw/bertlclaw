# Reminder / Ops Hardening

## Beobachtungen
Der aktuelle Hourly-Heartbeat-Job ist aktiv und grundsätzlich funktionsfähig.

### Aktive Konfiguration
- Jobname: `bertlclaw-reminder-heartbeat`
- Schedule: `0 * * * *`
- Zeitzone: `Europe/Vienna`
- zusätzlich gesetzt: `staggerMs: 300000`

## Interpretation
Die fehlenden Slots passen zu einer Konstellation, in der:
- der Job grundsätzlich läuft
- aber nicht jede Stunde sauber ankommt
- `staggerMs` bis zu 5 Minuten Verzögerung einführt
- historische Ausfälle vor Wiederherstellung der Skripte weiter sichtbar bleiben

## Wahrscheinliche Ursachen
1. Skripte waren früher zeitweise nicht vorhanden
2. ältere Stunden sind deshalb real verloren
3. das Staggering verzögert aktuelle Läufe zusätzlich
4. die Audit-Logik war vorher strenger und wurde inzwischen verbessert

## Sichere Härtungsschritte

### Stufe 1 — Beobachten
- Noch 2–3 Stunden weiterlaufen lassen
- prüfen, ob neue Stunden kontinuierlich erscheinen
- wenn ja: historische Gaps nicht überbewerten

### Stufe 2 — Stagger prüfen
- `staggerMs: 300000` kann zu unnötiger Varianz führen
- falls präzisere Stundentakte gewünscht sind: auf `0` oder kleinen Wert reduzieren

### Stufe 3 — Monitoring stärken
- Audit-Report nach jeder Stunde beobachten
- bei 2+ aufeinanderfolgenden neuen Gaps: Scheduler-Problem annehmen

## Aktueller praktischer Schluss
Der Job wirkt derzeit wieder funktionsfähig. Die noch gemeldeten fehlenden Slots sind wahrscheinlich überwiegend Altlasten plus zeitliche Varianz, nicht zwingend ein neuer akuter Totalausfall.
