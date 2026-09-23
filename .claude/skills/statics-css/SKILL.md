---
name: statics-css
description: Route A (deterministica) - costruisce static ads in HTML/CSS alla geometria esatta del design system partendo da un template ufficiale, e le rasterizza con Chrome headless. Zero crediti, zero retry, logo e screenshot veri. Include la modalità A-composite per cambiare il copy su un'ad già consegnata. Usala quando creative-router assegna A, A-composite o la seconda metà di un hybrid, e per tutte le permutazioni (formati, mercati, varianti di copy).
---

# Statics CSS (Route A)

Il layout si **scrive**, non si descrive: un margine di 50px *è* 50px, il logo *è* il file SVG, lo
screenshot *è* il PNG reale. Funziona solo perché il brand è specificato in numeri
(`design_system.md`). Se i numeri mancano, compilali prima.

---

## Step 0 - Pre-flight

`creative_production_guidelines.md` §3, tutti veri. In particolare: ogni asset esiste su disco.

## Step 1 - Leggi il template

Apri il PNG del cluster scelto (`context/brand/templates/<Cluster>/...`) e **guardalo**. Annota:
griglia, gerarchia, posizione del logo, pattern del footer, cosa esce dal bordo, cosa il template
**non** ha (non si aggiunge ornamento).

Se il template è in Figma e il Figma MCP è collegato: `get_design_context` sul node ID del template dà
la geometria esatta dei layer. Meglio della stima dal PNG.

## Step 2 - Costruisci

Un file HTML autosufficiente per ad:
- canvas `.canvas` 1080×1350, `overflow:hidden`, tutto in `position:absolute`;
- font, logo, screenshot, illustrazioni inlineati come **data URI** (renderizza identico ovunque);
- valori del design system **letterali** con il paragrafo in commento (`/* §4 margine 50 */`);
- tracking 0, interlinea 100% headline / 120% body.

Per partire veloce c'è un template funzionante e un builder:

```bash
# 1. crea output/<batch>/ads.json (formato nel docstring di build.py)
python3 .claude/skills/statics-css/scripts/build.py output/<batch>
# 2. rasterizza
.claude/skills/statics-css/scripts/render.sh output/<batch>
```

`templates/headline_subheading.html` è un esempio di cluster: duplicalo per ogni cluster del tuo brand
(una volta sola), poi ogni batch è solo `ads.json`.

**Dimensionare il testo:** parti dal tipico del design system; se una riga non entra nella colonna,
**accorcia la riga** o scendi di dimensione dentro il range. Mai tracking negativo. Mai forzare una
dimensione che la colonna non regge.

## Step 3 - Permutazioni

Formati (1080×1080, 1080×1920), mercati (valuta, screenshot localizzato, lessico), varianti di copy:
una riga in più in `ads.json`, non una generazione. Per formati diversi passa la dimensione a render:
`render.sh output/<batch> 1080,1920` (e adatta la geometria del template per quel formato).

## Step 4 - Verifica

Lancia `creative-eval`. Poi guarda il contact sheet con i tuoi occhi.

Controlli interni che la scansione dei bordi non vede (fai tu, sui numeri del builder):
1. ogni riga di testo libera il **suo contenitore** (card, chip, pannello) del padding su entrambi i lati;
2. ogni asset dentro un pannello è centrato nel pannello (misura il bbox dell'inchiostro, non del file);
3. due angoli arrotondati mai sovrapposti allo stesso punto (antialiasing = filo di colore);
4. uno screenshot con cornice propria va ritagliato, non incorniciato di nuovo.

---

## Modalità A-composite - cambio copy su un'ad già consegnata

Quando il cliente cambia una data, una parola, un mercato su un PNG già approvato. **Mai rigenerare,
mai ricostruire da zero** (cambieresti pixel che nessuno ha chiesto di cambiare).

1. Il PNG sorgente è il fondo della pagina (`<img>` a 1080×1350, data URI).
2. Un **patch opaco** del colore esatto del fondo (campionato dal PNG, non dalla palette) copre solo il
   blocco che cambia.
3. Il nuovo copy si impagina sopra, nel font vero, a una dimensione **misurata sul sorgente**
   (altezza inchiostro delle maiuscole ÷ rapporto cap-height del font).
4. Prova: diff pixel tra sorgente e nuovo render **fuori dai patch = 0**. Se non è 0, hai toccato
   qualcosa che non dovevi.

```python
from PIL import Image, ImageChops
a, b = Image.open("source.png").convert("RGB"), Image.open("new.png").convert("RGB")
diff = ImageChops.difference(a, b)
for (l, t, r, bt) in PATCHES:              # azzera le zone patchate
    diff.paste((0, 0, 0), (l, t, r, bt))
assert diff.getbbox() is None, f"pixel cambiati fuori dai patch: {diff.getbbox()}"
```

Cartella: `build.py` · `render.sh` · `verify.py` · il PNG sorgente · `FIT.md` (dimensioni misurate).

---

## Cosa non fare mai

- Disegnare in CSS un logo, un'icona o uno screenshot che esiste come file.
- Usare Route A per fabbricare un'immagine (esce riempitivo geometrico): quello è Route B.
- Aggiungere elementi che il template non ha perché "sembra vuoto": la soluzione è un hero più grande.
- Consegnare senza `creative-eval`.
