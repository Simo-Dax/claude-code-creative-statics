---
name: statics-higgsfield
description: Route B (generativa) - produce static ads o immagini con Higgsfield (MCP o CLI; fal.ai come backup) quando qualcosa va immaginato - foto, persone, scene, texture, illustrazione nuova. Template ufficiale sempre allegato come reference 1, pre-flight prima di spendere crediti, retry disciplinati. Include la modalità "solo immagine" per la route hybrid. Usala quando creative-router assegna B o hybrid.
---

# Statics Higgsfield (Route B)

Il layout si **descrive** al modello, con il template allegato perché lo copi invece di inventarlo.
È l'unica route che crea pixel nuovi. È anche quella che sbaglia testo, logo e geometria: per questo
il lavoro è metà prompt e metà disciplina.

**Accesso:** Higgsfield MCP (connettore in Claude) oppure CLI `higgsfield`. Backup: fal.ai MCP.
Verifica i modelli disponibili prima di ogni batch: i nomi cambiano.

---

## Step 0 - Pre-flight (nessun credito finché non è tutto vero)

`creative_production_guidelines.md` §4, otto punti. Poi stima i crediti e chiedi l'ok all'utente.

## Step 1 - Scegli la modalità

| Modalità | Quando | Cosa chiedi al modello |
|---|---|---|
| **Solo immagine** (hybrid) | il testo conta | la foto/illustrazione e basta. **Niente headline, niente logo, niente CTA nel prompt.** Il resto lo fa `statics-css` |
| **Ad completa** | testo minimo, l'immagine è l'ad | tutto, con template + specimen del font |
| **Edit** | correggere un render esistente | render sorgente come reference 1 + una sola modifica |

Default: **solo immagine**. L'ad completa generata è la scelta più costosa e meno affidabile.

## Step 2 - Scegli il modello

`creative_production_guidelines.md` §5.1. In sintesi: modello tipografico se c'è testo o layout da
rispettare; modello fotografico per foto e edit leggeri; edita con lo stesso modello dell'originale,
tranne i fix di testo/layout che vanno sempre al tipografico.

## Step 3 - Reference (in quest'ordine)

1. **Template PNG** del cluster (sempre; off-template = il più vicino). In modalità "solo immagine"
   allega invece un riferimento di stile (foto/illustrazione approvata del brand).
2. Asset che rompe l'ad se sbagliato (screenshot prodotto, illustrazione, prodotto fisico).
3. Specimen del font (solo ad completa): PNG con il font vero, ≥120px, alle righe esatte.
4. Logo (solo ad completa).

Con la CLI i path delle reference devono essere **assoluti**.

## Step 4 - Il prompt

**Ad completa** = [ruolo delle reference] + [contenuto: copy esatto riga per riga, fondo, accento] +
[frammento di geometria §5.2] + [vincoli fissi §5.4].

**Solo immagine** = soggetto + inquadratura + luce + palette (HEX del brand) + spazio negativo dove
andrà il testo ("keep the left 55% of the frame calm and uncluttered for type") + formato + vincoli:

```
No text, no letters, no logo, no watermark, no UI anywhere in the image. No AI-aesthetic tells
(no purple-blue gradients, no floating shapes, no fake reflections). Photorealistic, natural light.
```

**Edit** = i quattro blocchi di §5.4: ristabilisci la fonte → una sola modifica → nomina il difetto →
vincoli fissi.

Salva ogni prompt nel `manifest.json` (campo `prompt`) insieme a `model` e `refs`.

## Step 5 - Genera

- Max 4 job in parallelo.
- Scarica subito i risultati in `output/<batch>/` (gli URL scadono).
- Nomi con versione: `c2_a_v1.png`, `c2_a_v2.png`. Mai sovrascrivere un approvato.

CLI di riferimento (sintassi al 2026-09, verifica con `higgsfield --help`):

```bash
higgsfield generate create <modello> \
  --prompt "$(cat prompt.txt)" \
  --image-references "/ABS/path/template.png" \
  --image-references "/ABS/path/asset.png" \
  --aspect-ratio 4:5 --resolution 2k --wait --json > c2_a_v1.output
```

## Step 6 - Retry disciplinati

- Stesso difetto due volte → **smetti di promptare**. Se è testo/logo: passa a hybrid (tieni
  l'immagine, impagina su A). Se è l'immagine: cambia reference o modello, non aggettivi.
- Negazioni assolute ("REMOVE X ENTIRELY - no X anywhere"), non "remove X".
- Nomina il difetto, non solo il target.

## Step 7 - Verifica

`creative-eval` + guarda il contact sheet. Controlla a occhio: copy esatto lettera per lettera, nessuna
parola inventata, font giusto, logo giusto, screenshot fedele (numeri non cambiati), mani e volti.

## Dopo l'approvazione

Un'immagine approvata va in `context/brand/assets/illustrations/` o `photos/`. Da lì è un asset:
tutte le sue varianti di formato/copy/mercato si fanno su **Route A**.
