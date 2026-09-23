# Creative Statics Kit per Claude Code

Static ads con l'AI **senza l'effetto "AI ad"**: un agente che parte dal contesto del brand, scrive il
concept, sceglie la route di produzione giusta e verifica il risultato con numeri, non a occhio.

Due route, una domanda per scegliere:

| | **Route A - deterministica (CSS)** | **Route B - generativa (Higgsfield)** |
|---|---|---|
| Quando | ogni elemento esiste già come file e il layout viene da un template | qualcosa va *immaginato*: foto, persone, scene, illustrazione nuova |
| Come | il layout si *scrive* in HTML/CSS e si rasterizza con Chrome | il layout si *descrive*, con il template allegato come reference 1 |
| Precisione | margini, logo e screenshot esatti per costruzione | approssimata, verificata dopo |
| Costo / retry | zero crediti, zero retry | crediti, spesso più tentativi |
| Permutazioni | un loop | una generazione ciascuna |

**Hybrid** = immagine generata su B (senza testo) + impaginazione su A. Quasi sempre la scelta migliore
quando serve un'immagine nuova *e* il copy conta.

---

## Il flusso

```
brief ─► creative-concept ─► creative-router ─┬─► statics-css          (Route A, A-composite)
         concept + copy      route + pre-flight├─► statics-higgsfield   (Route B)
         🚦 ok umano                            └─► B solo immagine → A  (hybrid)
                                                          │
                                   creative-eval ◄────────┘
                                   misura + rubrica visiva 🚦 ok umano
                                   └─► learning: regole nuove nelle guidelines
```

## Cosa c'è dentro

```
CLAUDE.md                       system prompt dell'agente creativo (orchestrazione)
.claude/skills/
  creative-concept/             brief → 3-5 concept, copy, brief di produzione
  creative-router/              A / B / hybrid / A-composite + pre-flight + manifest
  statics-css/                  Route A: template HTML, build.py, render.sh
  statics-higgsfield/           Route B: modelli, reference, anatomia prompt, retry
  creative-eval/                controlli misurati + rubrica + self-learning (eval_batch.py)
context/brand/
  business_profile.md           chi sei, proof point approvati (ogni numero sull'ad viene da qui)
  tone_of_voice.md              come suona il copy, esempi approvati e bocciati
  design_system.md              colori, font, scala tipografica, geometria - in numeri
  creative_production_guidelines.md   manuale di produzione + registro delle review
  eval_benchmarks.json          soglie dell'eval
  templates/                    i tuoi template ufficiali (PNG 1080×1350 per cluster)
  assets/                       font, logo, icone, illustrazioni, screenshot prodotto
context/campaign/brief.md       il brief della campagna
output/                         dove finiscono i batch
```

## Quickstart

1. **Prerequisiti:** [Claude Code](https://claude.com/claude-code), Google Chrome o Chromium, Python 3
   con `pip install pillow numpy`. Per Route B: account Higgsfield (connettore MCP in Claude o CLI).
   Opzionale: Figma MCP per leggere template e screenshot direttamente dai file Figma.
2. **Clona** il repo e aprilo con Claude Code.
3. **Compila il contesto** (è il 90% della qualità): `business_profile.md`, `tone_of_voice.md`,
   `design_system.md`. Metti i template in `context/brand/templates/` e gli asset in `context/brand/assets/`.
4. **Compila** `context/campaign/brief.md`.
5. Scrivi a Claude: *"Crea le static ads per il brief"*. Segue il flusso sopra e si ferma ai due gate.

Prova la Route A senza contesto (font di sistema, logo testuale):

```bash
mkdir -p output/demo
cp .claude/skills/statics-css/templates/ads.example.json output/demo/ads.json
cp .claude/skills/statics-css/templates/manifest.example.json output/demo/manifest.json
python3 .claude/skills/statics-css/scripts/build.py output/demo
.claude/skills/statics-css/scripts/render.sh output/demo
python3 .claude/skills/creative-eval/scripts/eval_batch.py output/demo
```

## I documenti di contesto, in ordine di importanza

| File | Senza questo... |
|---|---|
| `templates/` + `README.md` | l'AI inventa layout generici: il "look AI" nasce qui |
| `design_system.md` | colori e font "interpretati", margini a caso |
| `business_profile.md` §3 proof point | numeri inventati sull'ad |
| `creative_production_guidelines.md` | ogni batch ripete gli errori del precedente |
| `tone_of_voice.md` | copy corretto ma di nessuno |
| `assets/` | Route A impossibile, tutto finisce su Route B |

## Usarlo fuori da Claude Code

`CLAUDE.md` funziona come system prompt in un Claude Project: allega i file di `context/` come
knowledge e le skill come istruzioni. Gli script vanno eseguiti in locale.

## Licenza

MIT.
