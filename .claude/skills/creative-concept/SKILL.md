---
name: creative-concept
description: Trasforma un brief in 3-5 creative concept per static ads (angolo, leva, copy finale, template, brief di produzione per ad). Primo step del flusso, prima di qualsiasi immagine. Usala quando l'utente chiede concept, idee creative, headline per static, o "prepara il brief creativo".
---
<!-- Copyright (c) 2026 Simone Dassereto. All rights reserved. See LICENSE. -->

# Creative concept (static ads)

Un concept **non è un'immagine**: è un modo specifico di far percepire un problema o un desiderio,
ancorato a una verità del cliente e a una leva psicologica. L'immagine viene dopo.

**Output:** `output/<brand>_<campagna>_<data>/BRIEF.md`. Nessuna produzione parte senza.

---

## Step 0 - Leggi (in questa sessione, non a memoria)

- `context/campaign/brief.md` 🔴
- `context/brand/business_profile.md` 🔴 - soprattutto §3 proof point e §4 target
- `context/brand/tone_of_voice.md` 🔴
- `context/brand/templates/README.md` 🔴 - i cluster disponibili
- `context/brand/creative_production_guidelines.md` §8 (cosa regge la review) e §9 (registro)
- Opzionale: `context/references/` (ads di competitor, ads del brand che performano)

Campo 🔴 vuoto o `[COMPILA]` → fermati, elenca cosa manca, fai domande. Non inventare.

## Step 1 - Materia prima

Scrivi in `BRIEF.md`, sezione "Materia prima":
1. **Verità del cliente:** 3-5 dolori/desideri con le parole del cliente (da `business_profile.md` §4).
2. **Sea of sameness:** cosa dicono tutti i competitor (da evitare).
3. **White space:** cosa conta per il cliente e nessuno dice → qui nascono i concept forti.
4. **Proof disponibili:** gli ID della tabella proof point utilizzabili (P1, P2...).

## Step 2 - Genera 3-5 concept

Un concept = un angolo = un'idea testabile che può vincere o perdere da sola. Diversi su almeno **tre**
di questi assi: awareness · leva psicologica · angolo d'ingresso (problema / desiderio / obiezione /
identità / status quo) · cluster di template.

Scheda per concept:

| Campo | Contenuto |
|---|---|
| Nome | 2-4 parole |
| Big idea | una frase |
| Verità cliente | citazione + fonte |
| Leva psicologica | es. loss aversion, social proof, specificità, curiosity gap |
| Awareness | unaware → most aware |
| Headline | 2-4 righe, già spezzate come andranno sull'ad |
| Body (se serve) | max 2 frasi brevi |
| Proof | ID proof point o "nessuno" |
| CTA | da brief |
| Cluster template | nome + PNG scelto + **perché questa anatomia regge questo copy** |
| Visual | cosa si vede: screenshot X, illustrazione Y, foto di Z |
| Esiste già come file? | sì (quale) / no (cosa va immaginato) → indizio di route |
| Varianti A/B | cosa cambia (una variabile sola) |

## Step 3 - Criteri di qualità del copy (autocontrollo prima di consegnare)

Per ogni headline, rispondi sì/no. Un "no" = riscrivi.

1. Si capisce in 2 secondi su un telefono, senza il body?
2. Parla del cliente, non del prodotto?
3. È specifica (numero, scena, parola del cliente) invece che generica?
4. Rispetta `tone_of_voice.md` §4 (case, punto finale, trattini, lunghezza righe)?
5. Ogni numero è in `business_profile.md` §3? (grep, non memoria)
6. Nessuna parola da AI (rivoluzionario, sblocca, potenzia, seamless, game-changer, "nel mondo di oggi")?
7. Entra nell'anatomia del template scelto (righe, parole per riga)?

## Step 4 - Brief di produzione (tabella per ad)

| Ad | Concept | Template PNG | Fondo | Accento | Hero asset | Logo | Footer | Bleed | Mercato | Route (proposta) |
|---|---|---|---|---|---|---|---|---|---|---|

La colonna **Route** è una proposta: la conferma `creative-router`.

Chiudi il `BRIEF.md` con:
- **Criteri di successo** verificabili per questo batch (es. "5 ad, 0 errori di margine, eval ≥ 80").
- **Decisioni aperte** per l'umano (cliente citabile? claim approvato per paid?).

## 🚦 Gate

Mostra i concept all'utente e aspetta l'ok prima di passare a `creative-router`.

## Learning

Quando l'utente boccia un concept o riscrive una headline, aggiungi la ragione alla sezione
"Esempi bocciati" di `tone_of_voice.md` §6 o al registro §9 delle guidelines. Chiedi conferma prima di
scrivere nei file di contesto.
