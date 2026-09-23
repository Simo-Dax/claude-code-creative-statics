---
name: creative-router
description: Decide per ogni static ad la route di produzione - A (CSS deterministico), B (Higgsfield generativo), hybrid (B per l'immagine + A per l'impaginazione) o A-composite (cambio copy su un'ad già consegnata) - esegue il pre-flight e passa il lavoro alla skill giusta. Usala dopo creative-concept, o quando l'utente chiede "come la produco", "Higgsfield o CSS?", "fai le varianti".
---
<!-- Copyright (c) 2026 Simone Dassereto. All rights reserved. See LICENSE. -->

# Creative router

La route **non è una preferenza**: segue da cosa serve all'ad. Decidila prima di produrre, scrivila,
poi delega.

**Input:** `output/<batch>/BRIEF.md` (da `creative-concept`).
**Output:** colonna Route confermata nel `BRIEF.md` + `manifest.json` inizializzato + skill lanciata.

---

## Step 1 - La domanda (per ogni ad)

> **Ogni elemento visivo esiste già come file in `context/brand/assets/`, e il layout viene da un
> template in `context/brand/templates/`?**

```
                        ┌─ l'ad esiste già ed è cambiato solo il copy? ──► A-composite  (statics-css, modalità composite)
                        │
brief di produzione ────┼─ tutto esiste come file ───────────────────────► A            (statics-css)
                        │
                        ├─ serve un'immagine nuova + testo che conta ────► HYBRID       (statics-higgsfield solo immagine → statics-css)
                        │
                        └─ l'immagine È l'ad, testo minimo o assente ────► B            (statics-higgsfield)
```

Tabella rapida:

| Situazione | Route | Perché |
|---|---|---|
| Headline + screenshot prodotto reale | A | lo screenshot esiste, i numeri nell'UI devono essere veri |
| Headline tipografica + illustrazione del brand già in repo | A | tutto esiste |
| Headline + loghi clienti (file utilizzabili) | A | tutto esiste |
| Foto di una persona nel contesto d'uso | B o hybrid | va immaginata |
| Scena/prodotto fotografico nuovo + headline importante | **hybrid** | il modello sbaglia il testo; tu no |
| Illustrazione nuova in stile brand | B (poi l'illustrazione entra in `assets/` e da lì è A) | |
| 10 formati / 5 mercati / 3 varianti di copy | **A**, sempre | un loop, non N generazioni |
| Cliente cambia una parola su un'ad consegnata | **A-composite** | si tocca solo quel blocco |

In caso di dubbio: **A**. Costa zero e fallisce in modo visibile (asset mancante), non in modo
silenzioso (testo storto).

## Step 2 - Inventario asset

Per ogni ad elenca gli asset e verifica che esistano su disco (`ls`, non memoria):
font · logo (file giusto per il fondo, `design_system.md` §3) · screenshot (mercato giusto) ·
illustrazione · icone. Un asset mancante sposta l'ad su B/hybrid **ora**, oppure diventa una domanda
per l'utente ("hai lo screenshot X?").

## Step 3 - Pre-flight

Esegui la checklist della route in `creative_production_guidelines.md` (§3 per A, §4 per B, entrambe per
hybrid). Tutti i punti veri o ti fermi e dici quale no. Su B nessun credito si spende prima.

Per Route B e hybrid: stima i crediti (n. ad × varianti × retry attesi) e chiedi l'ok all'utente.

## Step 4 - Manifest

Crea `output/<batch>/manifest.json`:

```json
{
  "batch": "<brand>_<campagna>_<data>",
  "palette": ["#______", "#______"],
  "ads": [
    {
      "id": "c1_a",
      "file": "c1_a.png",
      "concept": "Nome concept",
      "template": "context/brand/templates/<Cluster>/<Cluster>_02.png",
      "route": "A | B | hybrid | A-composite",
      "route_reason": "screenshot reale disponibile, nessuna immagine da immaginare",
      "assets": ["context/brand/assets/product-screens/x.png"],
      "bleeds": "B",
      "model": null
    }
  ]
}
```

`palette` e `bleeds` servono a `creative-eval`. `bleeds` = lati dove un elemento esce volutamente dal
canvas (L, T, R, B).

## Step 5 - Delega

- A e A-composite → skill `statics-css`
- B → skill `statics-higgsfield`
- hybrid → `statics-higgsfield` in modalità "solo immagine", poi `statics-css` con l'immagine come asset

Quando la produzione torna, lancia sempre `creative-eval`. Non consegnare prima.

## Quando combinare le route (non solo hybrid)

- **B esplora, A scala.** Prima round: 3-4 immagini generate su B per trovare il visual che funziona.
  Approvato → l'immagine diventa asset → tutte le varianti su A.
- **A per la struttura, B per la texture.** Layout e testo su A; un fondo fotografico o un oggetto
  generato su B, senza testo, inserito come layer.
- **A-composite per i round cliente** su qualsiasi ad, anche nata su B.
