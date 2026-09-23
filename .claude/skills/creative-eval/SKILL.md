---
name: creative-eval
description: Valuta un batch di static ads prima della consegna - controlli misurati (canvas, margini, fondo, palette) + rubrica visiva di coerenza col template - e chiude il ciclo di self-learning confrontando il proprio voto con il verdetto umano e scrivendo le regole nuove nelle guidelines. Usala dopo ogni produzione (Route A o B) e dopo ogni round di review.
---

# Creative eval (self-assessment + learning)

Un batch non visto e non misurato **non è consegnato**. Questa skill fa tre cose:
1. **misura** (script, numeri oggettivi);
2. **guarda** (rubrica visiva: ad accanto al suo template);
3. **impara** (confronta il suo voto con quello umano e aggiorna regole e benchmark).

---

## Livello 1 - Controlli misurati

```bash
python3 .claude/skills/creative-eval/scripts/eval_batch.py output/<batch>
```

Legge `manifest.json` e i benchmark in `context/brand/eval_benchmarks.json`. Scrive `eval.json`,
`contact_sheet.png` (ogni ad con il suo template accanto) e una riga in `output/eval_history.jsonl`.

| Check | Cosa misura | Benchmark (default) |
|---|---|---|
| canvas | dimensione esatta | 1080×1350 |
| margins | inchiostro dal bordo, esclusi i bleed dichiarati nel manifest | ≥ 48px |
| ground | il fondo è un colore della palette | distanza ≤ 40 |
| palette | quota di pixel vicini alla palette | A ≥ 80% · B/hybrid solo informativo |

`layout_hint` (0-1) è solo indicativo: su ad reali approvate resta basso anche con la struttura giusta,
perché il contenuto è diverso. La coerenza col template la giudica il livello 2.

Un `CHECK` sui margini è quasi sempre una di due cose: un bleed voluto non dichiarato nel manifest
(dichiaralo e rilancia) o testo troppo vicino al bordo (correggi).

## Livello 2 - Rubrica visiva (la compili tu, guardando `contact_sheet.png`)

Apri il contact sheet e **guardalo**. Per ogni ad, confrontala con il template accanto e dai 0-2 per voce
(0 = sbagliato, 1 = accettabile, 2 = come il template):

| # | Voce | Domanda |
|---|---|---|
| 1 | Struttura | Stessa griglia e posizione dei blocchi del template? |
| 2 | Gerarchia | L'headline si legge per prima, poi prova/prodotto, poi logo? |
| 3 | Tipografia | Font giusti per ruolo, righe ben spezzate, nessuna parola orfana? |
| 4 | Copy | Testo esatto lettera per lettera, nessuna parola inventata o storta? |
| 5 | Colore | Un fondo + un accento, coppie ammesse? |
| 6 | Logo | File giusto per il fondo, dimensione e posizione come il template? |
| 7 | Asset | Screenshot/illustrazione fedeli, non deformati, non ridisegnati? |
| 8 | Niente di troppo | Nessun elemento che il template non ha? |
| 9 | Leggibilità mobile | Headline leggibile a dimensione thumbnail? |
| 10 | Brand | Se copri il logo, si capisce ancora di chi è? |

Scrivi il risultato in `eval.json → ads[i].visual_rubric` come `{"scores": {...}, "total": n, "notes": "..."}`.
Totale su 20. **Soglia: ≥ 16 e nessuno 0.** Sotto soglia → correggi prima di mostrare.

**Pass del batch** = livello 1 PASS **e** livello 2 sopra soglia, per ogni ad. Poi 🚦 mostra all'utente.

## Livello 3 - Learning (dopo la review umana)

Quando l'utente o il cliente dà il verdetto, registralo in `eval.json → ads[i].human`:
`{"verdict": "approved | changes | rejected", "notes": "..."}`.

Poi confronta:

| Tuo voto | Umano | Cosa significa | Azione |
|---|---|---|---|
| pass | approved | calibrato | niente |
| pass | changes / rejected | **falso positivo**: c'è un difetto che non misuri | scrivi la regola (sotto) |
| fail | approved | **falso negativo**: benchmark troppo severo o bleed non dichiarato | proponi di allentare quel benchmark, con i numeri |

Per ogni falso positivo:
1. Descrivi il difetto in una riga, generalizzato (non "c2 aveva il testo storto" ma "una riga di testo
   deve liberare il suo contenitore del padding del contenitore").
2. Scrivilo nel **registro §9** di `creative_production_guidelines.md` (data, difetto, regola, sezione).
3. Se è **misurabile** → aggiungilo al pre-flight (§3/§4) o proponi un nuovo check a `eval_batch.py`.
   Se è **visivo** → aggiungi una riga alla rubrica sopra.
4. Una regola può solo **stringere** un vincolo. Mai allentarne uno che stai per violare.

Chiedi conferma all'utente prima di modificare guidelines, benchmark o rubrica.

**Trend:** `output/eval_history.jsonl` tiene una riga per batch (pass, media). Se il pass rate umano
sale round dopo round, il sistema sta imparando; se il tuo pass rate è alto e quello umano no, la
rubrica è troppo generosa.
