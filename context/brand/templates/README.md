# Template ufficiali delle static ads

> **A cosa serve:** ogni static parte da qui. Il template è il layout approvato; l'agente lo *riempie*,
> non lo inventa. Su Route B il PNG è allegato come reference 1; su Route A è ricostruito in CSS.

## Come costruire la libreria (una volta sola)

1. Prendi le 15-30 static migliori del brand (approvate o top performer), esportate a **1080×1350**.
2. Raggruppale per **struttura**, non per colore o messaggio. Di solito escono 4-8 cluster.
3. Una cartella per cluster: `templates/<NomeCluster>/<NomeCluster>_01.png`, `_02.png`, ...
4. Per ogni cluster compila la tabella sotto: è quello che l'agente legge per scegliere.
5. Misura la geometria (`design_system.md` §6) e i fondi usati. Scrivi i numeri, non le impressioni.
6. Opzionale: se i template vivono in Figma, annota file key e node ID per poter leggere la geometria
   esatta via Figma MCP.

## Cluster

| # | Cluster (cartella) | N. ref | Cosa è | Usalo quando | Route di default | Figma node |
|---|---|---|---|---|---|---|
| 1 | `Headline&Subheading` | [n] | Tipografico: headline + 1-2 paragrafi brevi | hook a domanda, educazione, awareness | A | [opz.] |
| 2 | `Headline&Product` | [n] | Headline in card + screenshot prodotto grande che esce dal bordo | feature, ampiezza piattaforma | A | |
| 3 | `Headline&Stats` | [n] | Headline + 2-3 blocchi numero/etichetta + prodotto | ROI, outcome, numero che porta l'ad | A | |
| 4 | `Headline&List` | [n] | Headline + elenco con icone | "tutto in uno", moduli | A | |
| 5 | `SocialProof` | [n] | Headline + loghi clienti / tile case study | fiducia, "chi lo usa già" | A se i loghi sono file utilizzabili | |
| 6 | `Headline&Image` | [n] | Headline + foto o illustrazione protagonista | scena, emozione, lifestyle | **B** o hybrid (A se l'illustrazione esiste già) | |

> Rinomina, aggiungi o togli cluster. Quelli sopra sono un punto di partenza comune.

## Anatomia per cluster (compila)

### 1. `Headline&Subheading`
- Fondo: [...] · Accento: [...]
- Headline: posizione, righe, dimensione tipica
- Footer: [chip logo in basso a sinistra che esce dal bordo · banda piena · nessuno]
- Cosa **non** fa: [elementi che non ha e che non vanno aggiunti]

## Regola off-template

Un concept davvero nuovo può uscire dai cluster se nessuno può reggerne la struttura. Condizioni:
dichiarato nel `BRIEF.md` con il motivo, resta dentro il design system (font, colori, logo, geometria),
è una minoranza del set. Su Route B si allega comunque il template più vicino.
