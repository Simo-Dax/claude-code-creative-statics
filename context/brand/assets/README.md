# Asset del brand

Tutto quello che Route A compone e Route B allega come reference. Se un file non è qui, per l'agente
non esiste: o lo aggiungi, o l'ad diventa Route B / hybrid.

```
assets/
├── fonts/             file dei font (.otf/.ttf/.woff2) - licenza web verificata
├── logos/             logo in ogni colorway, SVG preferito (logo_01.svg ... )
├── icons/             UN solo set di icone (es. Phosphor, Lucide) - mai disegnate, mai generate
├── illustrations/     illustrazioni approvate del brand (PNG trasparente)
├── product-screens/   screenshot reali del prodotto, per mercato/lingua (es. dashboard_it.png, dashboard_us.png)
└── photos/            foto approvate (o generate in Route B e promosse qui dopo l'approvazione)
```

Regole:
- Nomi file parlanti e con il mercato quando conta: `forecast_uk.png`, `forecast_us.png`.
- Controlla se uno screenshot esportato ha già la sua cornice device: va ritagliato, non incorniciato di nuovo.
- Un'immagine generata in Route B e approvata entra in `illustrations/` o `photos/`: da lì in poi è
  un asset e le sue varianti vanno su Route A.
