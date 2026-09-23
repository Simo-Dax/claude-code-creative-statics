#!/usr/bin/env python3
"""creative-eval - misura ogni PNG di un batch contro i benchmark del brand e il suo template.

    python3 eval_batch.py <batch_dir> [--benchmarks context/brand/eval_benchmarks.json]

Legge <batch_dir>/manifest.json (palette, ads[].file/template/route/bleeds). Senza manifest valuta
tutti i PNG della cartella con i soli controlli di canvas e margini (utile per misurare i template).

Scrive:  <batch_dir>/eval.json · <batch_dir>/contact_sheet.png · riga in output/eval_history.jsonl

Livello 1 - controlli misurati (punteggio 0-100, pesi in eval_benchmarks.json):
  canvas   dimensione esatta
  margins  inchiostro a >= floor px da ogni bordo non dichiarato come bleed
  ground   il colore di fondo e' un colore della palette
  palette  quota di pixel vicini a un colore della palette (route A: alta; B/hybrid: informativa)

Solo indicativo, NON entra nel punteggio: layout_hint = correlazione tra la mappa dei bordi dell'ad
e quella del suo template. Testato su ad reali approvate: il contenuto diverso la tiene bassa anche
quando la struttura e' giusta, quindi non basta a giudicare. La coerenza col template la giudica il
livello 2 (rubrica visiva, vedi SKILL.md) guardando le coppie ad|template del contact sheet.
"""
import json, pathlib, sys, datetime
import numpy as np
from PIL import Image, ImageDraw, ImageFont

DEFAULTS = {
    "canvas": [1080, 1350],
    "margin_floor": 48,
    "palette_tolerance": 40,
    "palette_min": {"A": 0.80, "A-composite": 0.80, "hybrid": 0.0, "B": 0.0},
    "pass_score": 80,
    "weights": {"canvas": 15, "margins": 40, "ground": 20, "palette": 25},
}


def hex_rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)])


def load(path):
    return np.asarray(Image.open(path).convert("RGB")).astype(int)


def ink_mask(a):
    return np.abs(a - a[5, 5]).sum(axis=2) > 30


def margins(a):
    m = ink_mask(a)
    cols, rows = np.where(m.sum(0) > 4)[0], np.where(m.sum(1) > 4)[0]
    if not len(cols) or not len(rows):
        return None
    h, w = m.shape
    return {"L": int(cols[0]), "T": int(rows[0]), "R": int(w - 1 - cols[-1]), "B": int(h - 1 - rows[-1])}


def edge_map(a, cell=90):
    g = a.mean(axis=2)
    m = ((np.abs(np.diff(g, axis=1))[:-1, :] + np.abs(np.diff(g, axis=0))[:, :-1]) > 40).astype(float)
    h, w = m.shape
    m = m[: h - h % cell, : w - w % cell]
    return m.reshape(m.shape[0] // cell, cell, m.shape[1] // cell, cell).mean(axis=(1, 3)).ravel()


def layout_hint(a, tpl_path):
    t = np.asarray(Image.open(tpl_path).convert("RGB").resize((a.shape[1], a.shape[0]))).astype(int)
    x, y = edge_map(a), edge_map(t)
    x, y = x - x.mean(), y - y.mean()
    d = np.sqrt((x * x).sum() * (y * y).sum())
    return float((x * y).sum() / d) if d else 0.0


def palette_share(a, palette, tol):
    d = np.stack([np.abs(a - c).sum(axis=2) for c in palette]).min(axis=0)
    return float((d <= tol).mean())


def evaluate(path, ad, palette, bm):
    a = load(path)
    route = ad.get("route", "A")
    w = bm["weights"]
    res = {"file": path.name, "route": route, "checks": {}, "fails": []}
    size = [a.shape[1], a.shape[0]]
    ok = size == bm["canvas"]
    res["checks"]["canvas"] = {"value": size, "pass": ok}
    if not ok:
        res["fails"].append(f"canvas {size[0]}x{size[1]}, atteso {bm['canvas'][0]}x{bm['canvas'][1]}")

    mg = margins(a)
    bleeds = set(ad.get("bleeds", ""))
    bad = [k for k, v in (mg or {}).items() if v < bm["margin_floor"] and k not in bleeds]
    res["checks"]["margins"] = {"value": mg, "bleeds": "".join(sorted(bleeds)), "pass": not bad}
    if bad:
        res["fails"].append(f"inchiostro dentro {bm['margin_floor']}px su {''.join(bad)} (bleed non dichiarato?)")

    if palette:
        ground = a[5, 5]
        dist = min(int(np.abs(ground - c).sum()) for c in palette)
        g_ok = dist <= bm["palette_tolerance"]
        res["checks"]["ground"] = {"value": "#%02X%02X%02X" % tuple(ground), "pass": g_ok}
        if not g_ok:
            res["fails"].append("fondo fuori palette")
        share = palette_share(a, palette, bm["palette_tolerance"])
        need = bm["palette_min"].get(route, 0.0)
        res["checks"]["palette"] = {"value": round(share, 3), "min": need, "pass": share >= need}
        if share < need:
            res["fails"].append(f"solo {share:.0%} dei pixel in palette (min {need:.0%})")

    tpl = ad.get("template")
    if tpl and pathlib.Path(tpl).exists():
        res["template"] = tpl
        res["layout_hint"] = round(layout_hint(a, tpl), 2)
    # livello 2: la compila Claude guardando contact_sheet.png (rubrica in SKILL.md)
    res["visual_rubric"] = None
    res["human"] = None

    got = sum(w[k] for k, c in res["checks"].items() if c["pass"])
    tot = sum(w[k] for k in res["checks"])
    res["score"] = round(100 * got / tot) if tot else 0
    res["pass"] = res["score"] >= bm["pass_score"] and not res["fails"]
    return res


def label_font(size=22):
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def contact_sheet(batch, results, out, cw=360):
    """Una cella per ad; se l'ad ha un template, il template sta accanto (per la rubrica visiva)."""
    ch = int(cw * 1350 / 1080)
    cells = []
    for r in results:
        cells.append(("ad", r))
        if r.get("template"):
            cells.append(("tpl", r))
    cols = min(4, len(cells)) or 1
    rows = (len(cells) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (cw + 20) + 20, rows * (ch + 70) + 20), "white")
    d, f = ImageDraw.Draw(sheet), label_font()
    for i, (kind, r) in enumerate(cells):
        x, y = 20 + (i % cols) * (cw + 20), 20 + (i // cols) * (ch + 70)
        src = batch / r["file"] if kind == "ad" else pathlib.Path(r["template"])
        sheet.paste(Image.open(src).convert("RGB").resize((cw, ch)), (x, y))
        if kind == "ad":
            tag = "PASS" if r["pass"] else "CHECK"
            d.text((x, y + ch + 6), r["file"], fill="black", font=f)
            d.text((x, y + ch + 34), f"{tag} {r['score']} · {r['route']}", fill="#0a7d2c" if r["pass"] else "#c0392b", font=f)
        else:
            d.text((x, y + ch + 6), "template: " + pathlib.Path(r["template"]).name[:30], fill="#555", font=f)
    sheet.save(out)


def main():
    argv = sys.argv[1:]
    if "--benchmarks" in argv:
        i = argv.index("--benchmarks")
        argv = argv[:i] + argv[i + 2:]
    args = [a for a in argv if not a.startswith("--")]
    batch = pathlib.Path(args[0] if args else ".")
    bm = dict(DEFAULTS)
    bm_path = pathlib.Path("context/brand/eval_benchmarks.json")
    if "--benchmarks" in sys.argv:
        bm_path = pathlib.Path(sys.argv[sys.argv.index("--benchmarks") + 1])
    if bm_path.exists():
        bm.update(json.loads(bm_path.read_text()))

    man_path = batch / "manifest.json"
    manifest = json.loads(man_path.read_text()) if man_path.exists() else {}
    palette = [hex_rgb(h) for h in manifest.get("palette", [])]
    ads = manifest.get("ads") or [{"file": p.name} for p in sorted(batch.glob("*.png")) if p.name != "contact_sheet.png"]

    results = []
    for ad in ads:
        p = batch / ad["file"]
        if not p.exists():
            print(f"MANCA {ad['file']} - renderizza prima")
            continue
        r = evaluate(p, ad, palette, bm)
        results.append(r)
        print(f"{'PASS ' if r['pass'] else 'CHECK'} {r['score']:>3}  {r['file']}  " + ("; ".join(r["fails"]) or "ok"))

    if not results:
        return 1
    summary = {
        "batch": manifest.get("batch", batch.name),
        "date": datetime.date.today().isoformat(),
        "n": len(results),
        "passed": sum(r["pass"] for r in results),
        "avg_score": round(sum(r["score"] for r in results) / len(results), 1),
        "benchmarks": {k: bm[k] for k in ("margin_floor", "palette_min", "pass_score")},
    }
    (batch / "eval.json").write_text(json.dumps({"summary": summary, "ads": results}, indent=2, ensure_ascii=False))
    contact_sheet(batch, results, batch / "contact_sheet.png")
    hist = pathlib.Path("output/eval_history.jsonl")
    if hist.parent.exists():
        with hist.open("a") as fh:
            fh.write(json.dumps(summary, ensure_ascii=False) + "\n")
    print(f"\n{summary['passed']}/{summary['n']} pass · media {summary['avg_score']} · eval.json + contact_sheet.png scritti")
    return 0


if __name__ == "__main__":
    sys.exit(main())
