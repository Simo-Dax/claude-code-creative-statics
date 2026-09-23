<!-- Copyright (c) 2026 Simone Dassereto. All rights reserved. See LICENSE. -->
# Creative Production Guidelines - [NOME BRAND]

> **A cosa serve:** il manuale operativo di produzione. Il design system dice *quali* sono i numeri;
> questo file dice *come* si produce un'ad senza sbagliarli, su entrambe le route, e **raccoglie ogni
> regola nata da una review umana** (§9). È un documento vivo: cresce a ogni round.
>
> Letto da `creative-router`, `statics-css`, `statics-higgsfield`, `creative-eval` - **ogni sessione,
> non ricordato da quella prima**.

---

## 0. Mappa delle fonti - ogni input ha un solo posto

| # | Cosa serve | Dove sta (unica fonte) |
|---|---|---|
| 1 | Layout (cluster) | `templates/README.md` + PNG di riferimento |
| 1b | Layout, geometria esatta dei layer | Figma: file `[FILE_KEY]`, pagina `[NODE_ID]` - via Figma MCP (§6) |
| 2 | Geometria (margini, colonne, footer) | `design_system.md` §4 |
| 3 | Screenshot di prodotto | `assets/product-screens/` oppure Figma (§6). **Mai generati, mai ridisegnati** |
| 4 | Logo | `assets/logos/` - scelta per fondo in `design_system.md` §3 |
| 5 | Illustrazioni | `assets/illustrations/` - riusa prima di generare |
| 6 | Icone | `assets/icons/` - set unico, `design_system.md` §5 |
| 7 | Font | `assets/fonts/` - ruoli in `design_system.md` §2 |
| 8 | Claim e numeri | `business_profile.md` §3 - ogni numero deve essere lì |
| 9 | Voce | `tone_of_voice.md` |
| 10 | Brief di campagna | `context/campaign/brief.md` |

---

## 1. Procedura da zero (per ogni batch)

1. Leggi il brief. Se c'è un numero, trovalo in `business_profile.md` §3 **prima** di disegnarci sopra.
2. Scegli il cluster in `templates/README.md`. Metti le tue righe di copy *dentro* l'anatomia del
   template: se il dispositivo del template combatte le parole, è il template sbagliato.
3. Decidi la route (§2). Scrivila nel `BRIEF.md` prima di costruire.
4. Raccogli gli asset (righe 3-7 di §0). Da Figma subito, non a metà build.
5. Produci: Route A → skill `statics-css`. Route B → skill `statics-higgsfield`. Hybrid → B solo
   immagine, poi A.
6. Verifica: skill `creative-eval`. Un batch non visto e non misurato non è consegnato.
7. Scrivi `manifest.json` con route, template, asset, modello.
8. Dopo la review umana, scrivi le regole nuove in §9 **prima** di chiudere il round.

---

## 2. Le due route - una domanda sola

> **Ogni elemento visivo dell'ad esiste già come file, e il layout viene da un template?**

- **Sì → Route A (CSS deterministico).** Il layout si *scrive*.
- **No → Route B (Higgsfield, generativo).** Qualcosa va *immaginato*: foto, persone, scene, texture,
  illustrazione nuova.
- **In parte → Hybrid.** Genera solo l'immagine su B, impagina su A.
- **Cambio copy su un'ad già consegnata → A-composite.** Mai rigenerare.
- **Permutazioni (formati, mercati, test di copy) → sempre A.** Un loop, non N generazioni.

| | Route B - Higgsfield | Route A - CSS |
|---|---|---|
| Geometria | approssimata, verificata dopo | esatta per costruzione |
| Testo sull'immagine | errore n.1, richiede retry | impaginato, mai sbagliato |
| Logo / UI prodotto | ridisegnati dal modello | i file veri |
| Retry per variante | spesso diversi | zero |
| Crediti | sì | no |
| 20 permutazioni | 20 generazioni | un loop |
| Immagini nuove | **l'unica che può** | impossibile |

| Cluster / asset | Route di default |
|---|---|
| [cluster 1] | [A / B] - [perché] |
| Foto prodotto, lifestyle, persone | B |
| Variante di formato/mercato/copy | A |

---

## 3. Pre-flight Route A (tutti veri prima di scrivere CSS)

1. Questo file letto in questa sessione.
2. Template scelto, PNG aperto e guardato, pattern footer identificato.
3. Ogni asset presente su disco (font, logo giusto per il fondo, screenshot del mercato giusto).
   Asset mancante → l'ad è B o hybrid, decidilo ora.
4. Valori di geometria scritti come letterali nel CSS, con il riferimento al paragrafo in commento.
5. Copy finale, case e punteggiatura secondo `tone_of_voice.md` §4.
6. Logo scelto dalla tabella in base al fondo **su cui poggia** (chip o pannello, non la pagina).
7. Coppia testo/fondo presente tra quelle ammesse.
8. UI di prodotto = frame reale, mai ridisegnato.

## 4. Pre-flight Route B (nessun credito speso finché non sono tutti veri)

1. Questo file letto in questa sessione.
2. Template scelto e **allegato come reference 1**. Un prompt senza template non parte.
3. Geometria nel prompt (frammento §5.2).
4. Fondo scelto → logo guardato in tabella.
5. Copy finale, corretto, con il case giusto.
6. Ruoli font assegnati; **specimen del font** allegato se il testo sull'immagine conta.
7. Coppia testo/fondo ammessa.
8. UI di prodotto e illustrazioni = file veri allegati, mai generati.

---

## 5. Playbook Higgsfield (Route B)

### 5.1 Scelta del modello (la leva più importante)

> Osservazioni empiriche, aggiorna con le tue. I modelli cambiano: verifica sempre la lista aggiornata.

| | modello "tipografico" (es. `gpt_image_2`) | modello "fotografico" (es. `nano_banana_pro`) |
|---|---|---|
| Rispetta lo specimen del font | sì, affidabile | spesso no |
| Rispetta una specifica di layout (%, bande, righe) | sì | debolmente |
| Edit leggero preservando la composizione | buono | molto buono |
| Fotorealismo | molto buono | molto buono |
| Reference massime | ~4 in pratica | fino a 14 |

**Regola:** edita con lo stesso modello che ha fatto l'originale. **Eccezione:** fix di tipografia o
layout → modello tipografico, sempre. Annotalo nel manifest.

### 5.2 Frammento di geometria (incolla in ogni prompt, con i tuoi numeri)

```
Canvas 1080x1350 (4:5). 50px outer margin left, right and top; no type closer than 48px to any
edge; text column max 980px, left aligned, ragged right. Headline in [HEADLINE FONT] Bold at about
105px, tracking 0, line pitch equal to type size, 2-4 lines. Body in [BODY FONT] Medium at about
65px, tracking 0, line pitch 1.2x. Bottom 134px is the footer: the wordmark sits in a solid
rounded chip anchored bottom-left, bleeding off the edge. Panel corners 8-12px, gaps 30px.
Devices and illustrations may bleed off the canvas; type never does.
```

### 5.3 Ordine delle reference

1. **Template PNG** (sempre, anche off-template: il più vicino).
2. L'asset che rompe l'ad se sbagliato: screenshot prodotto o illustrazione.
3. Specimen del font (PNG con il font vero, grande, alle righe esatte che vuoi).
4. Logo.

Nel prompt, di' cosa è ogni reference:
> Reference 1 is the official layout template. Reproduce its structure exactly: grid, block positions,
> type hierarchy, logo chip placement, colour distribution. Replace only the content with what this
> brief specifies. Do not copy the template's placeholder words.

### 5.4 Anatomia di un prompt di edit (quattro blocchi, in ordine)

1. **Ristabilisci la fonte:** "Recreate reference image 1 exactly: ..." + ciò che deve restare.
2. **Una sola modifica:** "SINGLE CHANGE: ..." - capped, esplicita.
3. **Nomina il difetto:** "The headline is set in the WRONG typeface. Set it in the exact typeface of
   reference 2." Nominare l'errore batte descrivere solo il target.
4. **Vincoli fissi** (verbatim, sempre):

```
Constraints: no button or CTA text unless described. No AI-aesthetic tells (no purple-blue
gradients, no floating geometric shapes, no fake light reflections). Every named asset (product
screen, illustration, logo) rendered with absolute fidelity to the uploaded reference. No garbled
text: every visible word is a real, correctly spelled word. Type is never stretched or condensed.
No fabricated rating, review count, press logo or testimonial.
```

Le negazioni devono essere assolute: "REMOVE THE COINS ENTIRELY - no coins, no currency symbols
anywhere" funziona; "remove coins" viene ignorato.

### 5.5 Disciplina dei retry

- Due tentativi falliti sullo stesso difetto tipografico → smetti di promptare, passa a **hybrid**
  (tieni l'immagine, impagina il testo su Route A).
- Max 4 job in parallelo. Scarica subito gli URL: scadono.

---

## 6. Figma via MCP (opzionale ma potente)

- Il Figma MCP ufficiale legge i file: `get_metadata` (struttura e node ID), `get_screenshot` (PNG di
  un nodo), `get_design_context` (geometria e stili dei layer).
- Usalo per: (a) la **geometria esatta** di un template su Route A invece di stimarla dal PNG;
  (b) esportare lo **screenshot di prodotto giusto** per mercato/lingua.
- Tieni un indice `figma_index.md` "mi serve X → file Y, nodo Z". Passa sempre il node ID della pagina
  o sezione: chiamare `get_metadata` su una pagina intera di un file grande esplode il contesto.
- I seat View hanno un budget di chiamate basso: esporta in locale ciò che usi spesso.

---

## 7. Cosa non deve mai succedere

- Ridisegnare in CSS qualcosa che esiste come file (logo, icone, screenshot).
- Usare la Route A per fabbricare immagini (esce riempitivo geometrico).
- Usare la Route B per le permutazioni.
- Saltare il template.
- Consegnare senza `creative-eval`.
- Un numero sull'ad che non è in `business_profile.md`.

---

## 8. Pattern creativi che reggono la review

> Riempi con quello che il tuo brand/cliente approva. Esempi generici che valgono quasi sempre:

- **Device reale batte screenshot piatto.** Lo stesso screen dentro un telefono/laptop legge "prodotto".
- **Una illustrazione, che significa qualcosa.** Due illustrazioni nello stesso frame vengono tagliate;
  una decorativa viene bocciata.
- **Il numero grande porta l'ad** solo se è un proof point approvato e sta sotto l'headline per peso.
- **Un'anatomia di template regge una certa forma di copy**, non qualsiasi copy.

---

## 9. Registro delle review (si scrive dopo ogni round, prima di chiuderlo)

> Formato: data · cosa è tornato indietro · regola nuova · dove si applica. Una regola può solo
> stringere un vincolo, mai allentarne uno che stai per violare.

| Data | Difetto trovato in review | Regola nuova | Sezione aggiornata |
|---|---|---|---|
| [AAAA-MM-GG] | [es. testo a 4px dal bordo della sua card] | [es. ogni riga libera il suo contenitore del padding del contenitore, su entrambi i lati] | [§3] |
