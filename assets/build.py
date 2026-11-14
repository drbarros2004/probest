"""Build lessons and reference sheets with the explain-diff-html renderer.

The look (CSS, light/dark theme, KaTeX, quiz) comes from
~/.claude/skills/explain-diff-html/render.py. This wrapper only adds what the
renderer lacks: numeric answer inputs (assets/check.js) and Portuguese UI strings.

Usage from a lesson source:  from build import build, prior_post, mc, quote
"""
import html
import importlib.util
import re
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent
RENDER = Path.home() / ".claude" / "skills" / "explain-diff-html" / "render.py"

_spec = importlib.util.spec_from_file_location("render", RENDER)
render = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(render)

# Numeric inputs reuse the renderer's tokens, so they follow the light/dark theme.
EXTRA_CSS = """
  .check-group { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 1.2rem 1.5rem; margin: 1.2rem 0; }
  .check-group input { font: inherit; font-size: .92rem; width: 6rem; padding: .25rem .4rem; text-align: right;
    color: var(--fg); background: var(--bg); border: 1px solid var(--border); border-radius: 5px; }
  .check-group input.right { background: var(--ok-bg); border-color: var(--ok-border); }
  .check-group input.wrong { background: var(--bad-bg); border-color: var(--bad-border); }
  .check-group button.check { font-family: inherit; font-size: .95rem; padding: .45rem 1.1rem; margin-top: .6rem; cursor: pointer;
    color: var(--fg); background: var(--surface); border: 1px solid var(--accent); border-radius: 6px; }
  .check-group button.check:hover { background: var(--hover); }
  .check-group td, .check-group th { text-align: right; }
  .check-group td:first-child, .check-group th:first-child { text-align: left; }
  td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; }
  td.hl { color: var(--accent); font-weight: 700; }
  body { font-size: 18px; }
  blockquote.src { margin: 1.2rem 0; padding: .8rem 1.2rem; background: var(--surface); border: 1px solid var(--border);
    border-left: 4px solid var(--muted); border-radius: 0 6px 6px 0; font-size: .95em; }
  blockquote.src > :first-child { margin-top: 0; }
  blockquote.src footer { margin-top: .6rem; font-size: .8rem; color: var(--muted); font-family: sans-serif; }
  blockquote.src footer::before { content: "\\2014  "; }
  blockquote.src table { font-size: .85rem; }
  .check-group button.reveal { border-color: var(--border); color: var(--muted); margin-left: .5rem; }
  .check-group input.revealed { border-style: dashed; color: var(--muted); }
  table.bayes-auto td.num { color: var(--muted); font-variant-numeric: tabular-nums; white-space: nowrap; }
  table.bayes-auto .pd { font-weight: 700; white-space: nowrap; }
  html { scroll-behavior: smooth; }
  h2[id], h3[id] { scroll-margin-top: 1rem; }
  /* In-page links are frequent, so they stay quiet: text color, dotted underline, accent only on hover. */
  a[href^="#"]:not(.toc a) { color: inherit; text-decoration: underline dotted var(--muted); text-underline-offset: 3px; }
  a[href^="#"]:not(.toc a):hover { color: var(--accent); text-decoration-color: var(--accent); }
  .quiz-ref { font-size: .8rem; color: var(--muted); margin: -.4rem 0 .6rem; }
  .quiz-ref a[href^="#"] { color: var(--muted); }
  /* Formulas never break inside a table cell; a table too wide for the screen scrolls in its own box (.tw, added in build()). */
  td .katex, th .katex { white-space: nowrap; }
  .tw { overflow-x: auto; margin: 1rem 0; } .tw > table { margin: 0; }
  blockquote.src td, blockquote.src th { white-space: nowrap; padding: .4rem .55rem; }
  /* Exercise tables: cells never wrap on their own (an input must not drop below its symbol); line breaks are written as <br>. */
  .check-group td, .check-group th { white-space: nowrap; padding: .4rem .55rem; }
  /* A letter that check.js replaces by the value from an earlier item once that item is right. */
  [data-show] { font-family: KaTeX_Math, serif; font-style: italic; }
  [data-show].shown { font-family: inherit; font-style: normal; color: var(--accent); font-weight: 700; }
  /* "Na prova:" pointer from an explanation to the formula to use. */
  p.uso { font-size: .9rem; color: var(--muted); border-left: 3px solid var(--accent); padding-left: .7rem; }
  details { margin: .5rem 0; } summary { cursor: pointer; color: var(--accent); }
  nav.crumbs { font-size: .85rem; color: var(--muted); }
  nav.crumbs a { color: var(--accent); }
"""


def quote(body, source, lang="en"):
    """Verbatim excerpt from a source (MIT notes, lists). body is HTML; keep the original wording."""
    return f'<blockquote class="src" lang="{lang}">{body}<footer>{source}</footer></blockquote>'


def _br(x, d=2):
    """Number with a decimal point (the course writes 0.2, never 0,2)."""
    return f"{x:.{d}f}"


def prior_post(rows, caption="", top=None):
    """Slope chart: prior (left) to posterior (right), one line per hypothesis.
    rows: [(label, prior, posterior)]. Each right label shows the factor posterior/prior,
    which equals likelihood / P(D). Lines that go up use the accent color."""
    vals = [v for _, p, q in rows for v in (p, q)]
    lo, hi = min(vals), max(vals)
    pad = (hi - lo) * 0.08
    lo, top = lo - pad, (top or hi + pad)  # slope charts encode position, so the axis need not start at 0
    W, H, X0, X1, Y0, Y1 = 560, 320, 170, 380, 45, 300
    y = lambda v: Y1 - (Y1 - Y0) * (v - lo) / (top - lo)  # noqa: E731
    parts = [
        f'<line x1="{X0}" y1="{Y0-10}" x2="{X0}" y2="{Y1}" stroke="var(--border)" stroke-width="2"/>',
        f'<line x1="{X1}" y1="{Y0-10}" x2="{X1}" y2="{Y1}" stroke="var(--border)" stroke-width="2"/>',
        f'<text x="{X0}" y="{Y0-18}" text-anchor="middle" fill="var(--muted)" font-size="14">prior</text>',
        f'<text x="{X1}" y="{Y0-18}" text-anchor="middle" fill="var(--muted)" font-size="14">posterior</text>',
    ]
    left = {}
    for label, p, q in rows:
        up = q > p
        color = "var(--accent)" if up else "var(--muted)"
        tip = f"{label}: {_br(p)} → {_br(q, 3)} (× {_br(q/p)})"
        parts.append(f'<g><title>{tip}</title>'
                     f'<line x1="{X0}" y1="{y(p):.1f}" x2="{X1}" y2="{y(q):.1f}" stroke="{color}" stroke-width="2.5"/>'
                     f'<circle cx="{X0}" cy="{y(p):.1f}" r="5" fill="{color}"/><circle cx="{X1}" cy="{y(q):.1f}" r="5" fill="{color}"/>'
                     f'<text x="{X1+12}" y="{y(q)+4.5:.1f}" fill="var(--fg)" font-size="16"><tspan font-weight="700">{label}</tspan> {_br(q, 3)}'
                     f'<tspan fill="var(--muted)" font-size="13">  × {_br(q/p)}</tspan></text></g>')
        left.setdefault(round(p, 6), []).append(label)
    for p, labels in left.items():
        parts.append(f'<text x="{X0-12}" y="{y(p)+4.5:.1f}" text-anchor="end" fill="var(--fg)" font-size="16">'
                     f'<tspan font-weight="700">{", ".join(labels)}</tspan> {_br(p)}</text>')
    svg = f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" style="max-width:{W}px;display:block;margin:auto;font-family:Georgia,serif">{"".join(parts)}</svg>'
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<figure><div class="diagram">{svg}</div>{cap}</figure>'


def pdf_plot(curves, caption="", ymax=None, shade=None, strip=None, marks=(), n=200, xlabel="θ"):
    """Density curves on [0, 1] (prior/posterior pdfs of a parameter).
    curves: [(label, fn, color, dashed, label_x[, label_y])]; the label sits on the curve at label_x,
    or at (label_x, label_y) in data units when the curve is crowded there.
    shade: (a, b, fn, text) fills the area under fn on [a, b] (a probability as area).
    strip: (x, width, fn, text) draws one thin bar of height fn(x) (the f(x) dx idea).
    marks: [(x, fn, text, color)] vertical dashed line from the axis to fn(x), labelled on top
    (e.g. where a posterior peaks)."""
    W, H, X0, X1, Y0, Y1 = 560, 300, 48, 530, 28, 262
    top = ymax or max(fn(i / n) for _, fn, *_ in curves for i in range(n + 1)) * 1.12
    sx = lambda x: X0 + (X1 - X0) * x  # noqa: E731
    sy = lambda v: Y1 - (Y1 - Y0) * v / top  # noqa: E731
    parts = [f'<line x1="{X0}" y1="{Y1}" x2="{X1}" y2="{Y1}" stroke="var(--border)" stroke-width="1.5"/>',
             f'<line x1="{X0}" y1="{Y0-8}" x2="{X0}" y2="{Y1}" stroke="var(--border)" stroke-width="1.5"/>']
    for t in (0, 0.25, 0.5, 0.75, 1):
        parts.append(f'<text x="{sx(t):.1f}" y="{Y1+18}" text-anchor="middle" fill="var(--muted)" font-size="13">{t:g}</text>')
    step = 0.5 if top <= 2.6 else 1
    v = step
    for _ in range(int(top / step)):
        parts.append(f'<line x1="{X0-4}" y1="{sy(v):.1f}" x2="{X1}" y2="{sy(v):.1f}" stroke="var(--border)" stroke-width=".5" stroke-dasharray="2 4"/>'
                     f'<text x="{X0-8}" y="{sy(v)+4:.1f}" text-anchor="end" fill="var(--muted)" font-size="13">{v:g}</text>')
        v += step
    parts.append(f'<text x="{X1}" y="{Y1+36}" text-anchor="end" fill="var(--muted)" font-size="13" font-style="italic">{xlabel}</text>')
    if shade:
        a, b, fn, text = shade
        pts = " ".join(f"{sx(a + (b-a)*i/n):.1f},{sy(fn(a + (b-a)*i/n)):.1f}" for i in range(n + 1))
        parts.append(f'<polygon points="{sx(a):.1f},{Y1} {pts} {sx(b):.1f},{Y1}" fill="var(--accent)" fill-opacity=".18" stroke="none"/>'
                     f'<text x="{sx((a+b)/2):.1f}" y="{Y1-14}" text-anchor="middle" fill="var(--fg)" font-size="14">{text}</text>')
    if strip:
        x, w, fn, text = strip
        parts.append(f'<rect x="{sx(x-w/2):.1f}" y="{sy(fn(x)):.1f}" width="{sx(w)-X0:.1f}" height="{Y1-sy(fn(x)):.1f}" fill="var(--accent)" fill-opacity=".55"/>'
                     f'<text x="{sx(x)-10:.1f}" y="{sy(fn(x))-4:.1f}" text-anchor="end" fill="var(--fg)" font-size="14">{text}</text>')
    for label, fn, color, dashed, lx, *ly in curves:
        tx, ty = sx(lx) + 6, (sy(ly[0]) if ly else sy(fn(lx)) - 8)
        pts = " ".join(f"{sx(i/n):.1f},{sy(fn(i/n)):.1f}" for i in range(n + 1))
        dash = ' stroke-dasharray="6 5"' if dashed else ""
        parts.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.5"{dash}/>'
                     f'<text x="{tx:.1f}" y="{ty:.1f}" fill="{color}" font-size="15" font-weight="700">{label}</text>')
    for x, fn, text, color in marks:
        parts.append(f'<line x1="{sx(x):.1f}" y1="{Y1}" x2="{sx(x):.1f}" y2="{sy(fn(x)):.1f}" stroke="{color}" stroke-width="1.5" stroke-dasharray="3 3"/>'
                     f'<circle cx="{sx(x):.1f}" cy="{sy(fn(x)):.1f}" r="4.5" fill="{color}"/>'
                     f'<text x="{sx(x):.1f}" y="{sy(fn(x))-12:.1f}" text-anchor="middle" fill="{color}" font-size="13" font-weight="700">{text}</text>')
    svg = (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" style="max-width:{W}px;display:block;margin:auto;'
           f'font-family:Georgia,serif">{"".join(parts)}</svg>')
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<figure><div class="diagram">{svg}</div>{cap}</figure>'


def bayes_table(rows, ok="", lik_header="likelihood", weight_header="prior",
                prod_header="numerador (automático)", total="\\(P(D)\\)", carry_weight=False):
    """Fill-in table where each row multiplies two typed columns; check.js computes the
    product column and its sum live.
    Bayes update: weight = prior, product = numerator, sum = P(D), plus a typed posterior column.
    Predictive: weight = posterior, lik = P(next | H), sum = predictive probability; pass posterior None.
    rows: [(label, weight_answer, lik_answer, posterior_answer or None)], answers as "1/16" or "0.6847".
    carry_weight: the weight column comes from an earlier exercise, so a "Preencher anteriores"
    button (check.js) can fill it."""
    has_post = any(q is not None for *_, q in rows)
    wcls = "prior carry" if carry_weight else "prior"
    trs = "".join(
        f'<tr data-h><td>{label}</td>'
        f'<td><input class="{wcls}" data-answer="{p}" data-tol="0.003"></td>'
        f'<td><input class="lik" data-answer="{lk}" data-tol="0.0005"></td>'
        f'<td class="num"></td>'
        + (f'<td><input data-answer="{q}" data-tol="0.003"></td>' if has_post else "") + "</tr>"
        for label, p, lk, q in rows)
    post_th = "<th>posterior</th>" if has_post else ""
    post_tot = "<th>1</th>" if has_post else ""
    return (f'<div class="check-group" data-ok="{html.escape(ok)}"><table class="bayes-auto">'
            f'<tr><th>hipótese</th><th>{weight_header}</th><th>{lik_header}</th><th>{prod_header}</th>{post_th}</tr>'
            f'{trs}<tr><th>total</th><th>1</th><th></th><th>{total} = <span class="pd"></span></th>{post_tot}</tr>'
            f'</table><button class="check">Verificar</button><div class="feedback"></div></div>')


def mc(question, options):
    """Inline multiple-choice question (same widget as the renderer's end quiz).
    options: [(text, correct, feedback)]. Order is kept as given."""
    btns = "".join(
        f'<button class="quiz-opt" data-correct="{"true" if c else "false"}" data-feedback="{html.escape(f)}">{t}</button>'
        for t, c, f in options)
    return f'<div class="quiz-q"><p><strong>{question}</strong></p>{btns}</div>'


def build(spec, out):
    """Render spec (render.py format) to the path out, with the extras injected."""
    spec.setdefault("math", True)
    spec.setdefault("_base", str(Path(out).parent))
    page = render.render(spec)
    # Quiz questions may carry "ref": [(anchor_id, label), ...]: a "Rever:" line linking to the section.
    for q in spec.get("quiz", []):
        if q.get("ref"):
            head = f'<p><strong>{html.escape(q["question"])}</strong></p>'
            links = " · ".join(f'<a href="#{a}">{lbl}</a>' for a, lbl in q["ref"])
            page = page.replace(head, head + f'\n<p class="quiz-ref">Rever: {links}</p>', 1)
    page = re.sub(r"(<table\b.*?</table>)", r'<div class="tw">\1</div>', page, flags=re.S)
    check_js = (ASSETS / "check.js").read_text(encoding="utf-8")
    page = (page
            .replace('<html lang="en">', '<html lang="pt-BR">')
            .replace("<strong>Contents</strong>", "<strong>Sumário</strong>")
            .replace('<a href="#quiz">Quiz</a>', '<a href="#quiz">Quiz final</a>')
            .replace('<h2 id="quiz">Quiz</h2>', '<h2 id="quiz">Quiz final</h2>')
            .replace("</style>", EXTRA_CSS + "</style>", 1)
            .replace("</body>", f"<script>{check_js}</script>\n</body>"))
    if spec.get("crumbs"):
        page = page.replace("<h1>", f'<nav class="crumbs">{spec["crumbs"]}</nav>\n<h1>', 1)
    Path(out).write_text(page, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    sys.exit("Import this module from a lesson source; see lessons/src/.")
