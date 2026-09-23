# Design System - [NOME BRAND]

> **A cosa serve:** i numeri del brand. Colori, font, scala tipografica, geometria del canvas.
> Non sono opinioni: sono valori **misurati** (dal brand book e dai template ufficiali). Un'ad che li
> rispetta è on-brand per costruzione; un'ad che li "interpreta" no.
> Letto da tutte le skill. Se questo file e `creative_production_guidelines.md` sono in disaccordo,
> **vince questo file**.
>
> Fonte: [brand book, versione, pagine] + misurazione dei template in `templates/` (vedi §6).

---

## 1. Colori 🔴

### Palette

| Token | Nome | HEX | Ruolo |
|---|---|---|---|
| `--c-primary` | [COMPILA] | `#______` | accento principale, numeri chiave, CTA |
| `--c-dark` | [COMPILA] | `#______` | fondo scuro, testo su chiaro |
| `--c-light` | [COMPILA] | `#______` | fondo chiaro (mai bianco puro se il brand ha un off-white) |
| `--c-accent-2` | [COMPILA] | `#______` | secondo accento |
| `--c-deep` | [COMPILA] | `#______` | fondo alternativo |

### Coppie testo/fondo ammesse (contrasto verificato)

| Fondo | Testo ammesso |
|---|---|
| `--c-dark` | `--c-light`, `--c-primary` |
| `--c-light` | `--c-dark` |
| [COMPILA] | |

### Fondi usati davvero dai template (misurati)

> Conta su quale colore di fondo poggiano i template ufficiali (campiona i 40px esterni di ogni PNG).
> Scoperta tipica: un colore della palette **non** è mai usato come fondo. Scriverlo evita metà degli errori.

| Fondo | N. template | Note |
|---|---|---|
| [COMPILA] | [n] | |

**Regola:** un fondo + **un** accento per ad. Due accenti sono un'ad diversa.

## 2. Tipografia 🔴

| Ruolo | Font (file in `assets/fonts/`) | Peso | Tracking | Interlinea |
|---|---|---|---|---|
| Headline | [COMPILA] | [700] | **0** | **100%** |
| Subheading | [COMPILA] | [500] | 0 | 120% |
| Body / footer | [COMPILA] | [500] | 0 | 120% |

- Case: [sentence case]. Ruoli fissi: non si scambiano mai.
- **Tracking 0 è letterale:** se una riga entra solo con tracking negativo, è la *dimensione* sbagliata
  (o la riga è troppo lunga).

### Scala tipografica per le ad (canvas master 1080×1350, misurata sui template)

| Ruolo | Range | Tipico |
|---|---|---|
| Headline | [es. 98-135px] | [105px] |
| Body | [es. 61-72px] | [65px] |
| Footer / CTA | [es. ~40px] | |

Su canvas 2× (es. story 2160×3840) si raddoppia.

## 3. Logo

| File | Colore del segno | Su quali fondi |
|---|---|---|
| `assets/logos/logo_01.svg` | [scuro] | [fondi chiari] |
| `assets/logos/logo_02.svg` | [chiaro] | [fondi scuri] |

La scelta del file è una **lookup su questa tabella**, mai un giudizio estetico. Larghezza minima: [px].

## 4. Geometria del canvas (misurata sui template) 🔴

| | Valore |
|---|---|
| Canvas master | **1080 × 1350** (4:5, feed Meta). Gli altri formati derivano da qui. |
| Margine esterno | [es. 50px] |
| Distanza minima testo-bordo | [es. 48px] - il testo non va mai più vicino |
| Colonna testo max | [es. 980px] |
| Gap tra pannelli | [es. 30px] |
| Raggio angoli pannelli / chip | [es. 8-12px / 20-24px] |
| Fascia footer | [es. ultimi 134px, logo in chip che esce dal bordo] |
| Righe headline | [es. 2-4, 3-5 parole per riga] |

**Bleed:** device, illustrazioni e chip logo *possono* uscire dal canvas. Il testo mai.

## 5. Icone

- Set unico: [es. Phosphor · Lucide · set proprietario] in `assets/icons/`. Peso: [Bold alle dimensioni ad].
- Mai disegnate in CSS, mai generate da AI.

## 6. Come ho misurato (ripetibile)

1. Esporta i template ufficiali a 1080×1350 in `templates/<cluster>/`.
2. Fondo: campiona il riquadro esterno di 40px, prendi il colore dominante.
3. Margini: `python3 .claude/skills/creative-eval/scripts/eval_batch.py templates/<cluster>` riporta i
   margini d'inchiostro per ogni PNG; il minimo ricorrente è il tuo margine.
4. Dimensione font: misura l'altezza d'inchiostro delle maiuscole e dividi per il rapporto cap-height del
   font (renderizza "H" a 200px in Chrome, misura, dividi per 200).
