"""Build lessons and reference sheets with the explain-diff-html renderer.

The look (CSS, light/dark theme, KaTeX, quiz) comes from
~/.claude/skills/explain-diff-html/render.py. This wrapper only adds what the
renderer lacks: numeric answer inputs (assets/check.js), Portuguese UI strings, the
pen layer from ~/.claude/skills/explain-diff-html-ink/ink.js and the post-it notes layer
(~/.claude/skills/explain-diff-html-notes/add_notes.py).

Usage from a lesson source:  from build import build, prior_post, mc, quote
"""
import html
import importlib.util
import random
import re
import subprocess
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent
SKILLS = Path.home() / ".claude" / "skills"
RENDER = SKILLS / "explain-diff-html" / "render.py"
# Pen layer from explain-diff-html-ink: strokes saved in the artifact db (collection "ink").
INK_JS = SKILLS / "explain-diff-html-ink" / "ink.js"
# Post-it notes layer from explain-diff-html-notes: notes saved in the artifact db (collection "notes").
ADD_NOTES = SKILLS / "explain-diff-html-notes" / "add_notes.py"

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
  /* Lists whose items are long explanations get room between items. */
  ul.spaced > li, ol.spaced > li { margin-bottom: .7rem; }
  p.uso { font-size: .9rem; color: var(--muted); border-left: 3px solid var(--accent); padding-left: .7rem; }
  details { margin: .5rem 0; } summary { cursor: pointer; color: var(--accent); }
  nav.crumbs { font-size: .85rem; color: var(--muted); }
  nav.crumbs a { color: var(--accent); }
  /* The notes toggle sits bottom-left too, so the pen button moves up above it. */
  body .ink-ui { bottom: 56px; }
  /* Two live plots stacked: the renderer's svg.plot draws one curve, so a second svg (same axes) goes on top. */
  .plot-stack { position: relative; }
  .plot-stack > svg.plot + svg.plot { position: absolute; inset: 0; background: none; border-color: transparent; }
  .plot-stack > svg.plot + svg.plot .grid, .plot-stack > svg.plot + svg.plot text { display: none; }
  svg.plot.second .plot-line { stroke: var(--muted); stroke-dasharray: 6 5; }
  svg.plot.second .plot-area { fill: var(--muted); }
  /* A narrow data-shade band used as a marker for the slider's value. */
  svg.plot.marker .plot-area { opacity: .75; }
  .controls button.reset { font: .8rem sans-serif; margin: .4rem 0 .1rem; padding: .3rem .8rem; cursor: pointer; color: var(--muted);
    background: none; border: 1px solid var(--border); border-radius: 6px; }
  .controls button.reset:hover { color: var(--accent); border-color: var(--accent); }
  .plot-key { font-family: sans-serif; font-size: .8rem; color: var(--muted); margin: .3rem 0 0; }
  .plot-key b { color: var(--accent); }
"""

# Functions the sliders' expressions can call (data-fn, data-expr, \\live). In <head>, so they
# exist before the renderer's script draws the plots.
LIVE_JS = """
function fact(n) { var r = 1; for (var i = 2; i <= n; i++) r *= i; return r; }
function beta(x, a, b) { return fact(a + b - 1) / (fact(a - 1) * fact(b - 1)) * Math.pow(x, a - 1) * Math.pow(1 - x, b - 1); }
function normal(x, m, v) { return Math.exp(-(x - m) * (x - m) / (2 * v)) / Math.sqrt(2 * Math.PI * v); }
"""


def slider(var, label, lo, hi, step, value, show=None):
    """One slider row for a .controls box: input[data-var] plus its readout (show: JS expr, default var)."""
    return (f'<label class="control"><span>{label}</span> <input type="range" data-var="{var}" min="{lo}" max="{hi}" '
            f'step="{step}" value="{value}"> <output data-expr="{show or var}"></output></label>')


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


def _g(x, d=3):
    """Number without trailing zeros (0.4, 0.005, 0.199)."""
    return f"{round(x, d):g}"


def bayes_square(cols, caption="", display=None, post=True, wlabel="prior", total="P(D)", live=None):
    """3Blue1Brown's Bayes square: column width = prior, shaded height = likelihood,
    shaded area = Bayes numerator, total shaded = P(D), posterior = share of the shaded area.
    cols: [(label, prior, likelihood)], drawn to scale by default.
    display: [(width, height)] to draw out of scale (e.g. a 0.5% prior). The shaded areas must keep
    the true proportions, so the posterior bar stays honest; this is asserted.
    post: draw the posterior bar (the shaded pieces laid side by side).
    wlabel / total: names for the widths and the shaded total (e.g. a posterior predictive).
    live: (prior0, lik0, lik1) JS expressions in the slider variables, for two columns: SQUARE_JS
    redraws the square and the bar as the sliders move (prior1 = 1 - prior0)."""
    num = [p * lk for _, p, lk in cols]
    tot = sum(num)
    shape = display or [(p, lk) for _, p, lk in cols]
    dtot = sum(w * h for w, h in shape)
    assert all(abs(w * h / dtot - n / tot) < .005 for (w, h), n in zip(shape, num)), "display distorts the posterior"
    S, X0, Y0 = 250, 66, 24
    ops = [.85, .5, .3, .7, .4]
    W, H = (560 if post else S + 2 * X0), Y0 + S + 74
    parts, x = [], X0
    for i, ((label, p, lk), (w, h)) in enumerate(zip(cols, shape)):
        cw, ch = w * S, h * S
        top = Y0 + S - ch
        inside = h > .85 and cw > 40
        ly = top + 16 if inside else (Y0 - 6 if top - 6 < Y0 + 12 else top - 6)
        parts.append(f'<g><title class="sq-tt">{label}: prior {_g(p, 3)} × likelihood {_g(lk, 3)} = {_g(p*lk, 4)}</title>'
                     f'<rect x="{x:.1f}" y="{Y0}" width="{cw:.1f}" height="{S}" fill="none" stroke="var(--border)" stroke-width="1.5" class="sq-o"/>'
                     f'<rect x="{x:.1f}" y="{top:.1f}" width="{cw:.1f}" height="{ch:.1f}" fill="var(--accent)" fill-opacity="{ops[i % 5]}" class="sq-f"/>'
                     f'<text x="{x+cw/2:.1f}" y="{ly:.1f}" text-anchor="middle" font-size="13" '
                     f'fill="var(--fg)" class="sq-l">{_g(lk, 3)}</text>'
                     f'<text x="{x+cw/2:.1f}" y="{Y0+S+18}" text-anchor="middle" font-size="14" font-weight="700" fill="var(--fg)" class="sq-n">{label}</text>'
                     f'<text x="{x+cw/2:.1f}" y="{Y0+S+35}" text-anchor="middle" font-size="13" fill="var(--muted)" class="sq-p">{_g(p, 3)}</text></g>')
        x += cw
    parts.append(f'<text x="{X0+S/2}" y="{Y0+S+60}" text-anchor="middle" font-size="14" fill="var(--fg)" class="sq-t" data-pre="área pintada = {total} = ">'
                 f'área pintada = {total} = {_g(tot, 5)}</text>'
                 f'<text x="{X0-8}" y="{Y0+S+35}" text-anchor="end" font-size="12" fill="var(--muted)">{wlabel}</text>')
    if post:
        BX, BW, BY = 356, 190, 120
        parts.append(f'<text x="{BX}" y="{BY-14}" font-size="14" fill="var(--muted)">só a área pintada, juntada:</text>')
        bx = BX
        for i, ((label, *_), n) in enumerate(zip(cols, num)):
            sw = BW * n / tot
            parts.append(f'<rect x="{bx:.1f}" y="{BY}" width="{sw:.1f}" height="34" fill="var(--accent)" fill-opacity="{ops[i % 5]}" stroke="var(--surface)" class="sq-b"/>'
                         f'<text x="{bx+sw/2:.1f}" y="{BY+52}" text-anchor="middle" font-size="14" font-weight="700" fill="var(--fg)" class="sq-bn">{label}</text>'
                         f'<text x="{bx+sw/2:.1f}" y="{BY+69}" text-anchor="middle" font-size="13" fill="var(--fg)" class="sq-bp">{_g(n/tot, 3)}</text>')
            bx += sw
        parts.append(f'<text x="{BX}" y="{BY+94}" font-size="14" fill="var(--muted)">fatia de cada um = posterior</text>')
    svg = f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" style="max-width:{W}px;display:block;margin:auto;font-family:Georgia,serif">{"".join(parts)}</svg>'
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    data = f' data-square="{html.escape(";".join(live))}"' if live else ""
    return f'<figure{data}><div class="diagram">{svg}</div>{cap}</figure>'


# Live Bayes square (bayes_square(live=...)): same layout constants as bayes_square. A prior under 10% is
# drawn 10% wide so the column shows, and both shaded areas scale by the same k, so the bar stays true.
SQUARE_JS = """
document.addEventListener('click', function (e) {
  var b = e.target.closest('.controls button.reset');
  if (b) b.closest('.controls').querySelectorAll('input[data-var]').forEach(function (i) {
    i.value = i.defaultValue; i.dispatchEvent(new Event('input', { bubbles: true }));
  });
});
document.querySelectorAll('figure[data-square]').forEach(function (fig) {
  var ex = fig.dataset.square.split(';').map(function (s) { return new Function('v', 'with (Math) { with (v) { return (' + s + '); } }'); });
  var q = function (c) { return [].slice.call(fig.querySelectorAll('.' + c)); };
  var g = function (x, d) { return String(+x.toFixed(d)); };
  var S = 250, X0 = 66, Y0 = 24, BX = 356, BW = 190, BY = 120;
  function draw() {
    var v = {};
    document.querySelectorAll('input[data-var]').forEach(function (i) { v[i.dataset.var] = parseFloat(i.value); });
    var p = [ex[0](v)], l = [ex[1](v), ex[2](v)];
    p.push(1 - p[0]);
    var n = [p[0] * l[0], p[1] * l[1]], tot = n[0] + n[1];
    var w = [Math.max(p[0], .1)]; w.push(1 - w[0]);
    var k = Math.min(w[0] / n[0], w[1] / n[1]), x = X0, bx = BX;
    [0, 1].forEach(function (i) {
      var cw = w[i] * S, h = k * n[i] / w[i], ch = h * S, top = Y0 + S - ch;
      var ly = h > .85 && cw > 40 ? top + 16 : (top - 6 < Y0 + 12 ? Y0 - 6 : top - 6);
      q('sq-o')[i].setAttribute('x', x); q('sq-o')[i].setAttribute('width', cw);
      var f = q('sq-f')[i]; f.setAttribute('x', x); f.setAttribute('width', cw); f.setAttribute('y', top); f.setAttribute('height', ch);
      var t = q('sq-l')[i]; t.setAttribute('x', x + cw / 2); t.setAttribute('y', ly); t.textContent = g(l[i], 3);
      q('sq-n')[i].setAttribute('x', x + cw / 2);
      t = q('sq-p')[i]; t.setAttribute('x', x + cw / 2); t.textContent = g(p[i], 3);
      q('sq-tt')[i].textContent = q('sq-n')[i].textContent + ': prior ' + g(p[i], 3) + ' × likelihood ' + g(l[i], 3) + ' = ' + g(n[i], 4);
      var sw = BW * n[i] / tot;
      f = q('sq-b')[i]; if (f) { f.setAttribute('x', bx); f.setAttribute('width', sw);
        q('sq-bn')[i].setAttribute('x', bx + sw / 2); t = q('sq-bp')[i]; t.setAttribute('x', bx + sw / 2); t.textContent = g(n[i] / tot, 3); }
      x += cw; bx += sw;
    });
    q('sq-t')[0].textContent = q('sq-t')[0].dataset.pre + g(tot, 5);
    // The caption says whether the drawing is to scale, and by how much both shaded areas were enlarged.
    var scaled = w[0] !== p[0], big = k > 1.05;
    fig.querySelectorAll('[data-sq-k]').forEach(function (e) {
      e.textContent = (scaled ? 'Fora de escala: com ' + g(100 * p[0], 1) + '% de largura, a faixa dos doentes quase não apareceria, então ela foi desenhada com 10%. ' : '')
        + (big ? 'As duas áreas pintadas foram ampliadas ' + g(k, 1) + ' vezes, por igual, então a proporção entre elas (e a barra da direita) é a verdadeira.'
               : 'O desenho está em escala: largura = prior, altura pintada = likelihood.');
    });
  }
  document.addEventListener('input', function (e) { if (e.target.matches('input[data-var]')) draw(); });
  draw();
});
"""


def pdf_plot(curves, caption="", ymax=None, shade=None, strip=None, marks=(), n=200, xlabel="θ", fills=(), xscale=1):
    """Density curves on [0, 1] (prior/posterior pdfs of a parameter).
    curves: [(label, fn, color, dashed, label_x[, label_y])]; the label sits on the curve at label_x,
    or at (label_x, label_y) in data units when the curve is crowded there.
    shade: (a, b, fn, text) fills the area under fn on [a, b] (a probability as area).
    strip: (x, width, fn, text) draws one thin bar of height fn(x) (the f(x) dx idea).
    marks: [(x, fn, text, color[, "ur"])] vertical dashed line from the axis to fn(x), labelled on top
    (e.g. where a posterior peaks); "ur" puts the label up-right of the point, clear of the lines through it.
    fills: [(fn, color, text, tx, ty[, "hatch"])] the whole area under fn, lightly filled (or hatched),
    with text at (tx, ty) (e.g. "área 1" inside each pdf).
    xscale: the axis shows [0, xscale] (tick labels only; fn and every x above stay in [0, 1])."""
    W, H, X0, X1, Y0, Y1 = 560, 300, 48, 530, 28, 262
    top = ymax or max(fn(i / n) for _, fn, *_ in curves for i in range(n + 1)) * 1.12
    sx = lambda x: X0 + (X1 - X0) * x  # noqa: E731
    sy = lambda v: Y1 - (Y1 - Y0) * v / top  # noqa: E731
    parts = [f'<line x1="{X0}" y1="{Y1}" x2="{X1}" y2="{Y1}" stroke="var(--border)" stroke-width="1.5"/>',
             f'<line x1="{X0}" y1="{Y0-8}" x2="{X0}" y2="{Y1}" stroke="var(--border)" stroke-width="1.5"/>']
    for t in (0, 0.25, 0.5, 0.75, 1):
        parts.append(f'<text x="{sx(t):.1f}" y="{Y1+18}" text-anchor="middle" fill="var(--muted)" font-size="13">{t * xscale:g}</text>')
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
    for k, (fn, color, text, tx, ty, *style) in enumerate(fills):
        pts = " ".join(f"{sx(i/n):.1f},{sy(fn(i/n)):.1f}" for i in range(n + 1))
        paint = f'fill="{color}" fill-opacity=".14"'
        if style == ["hatch"]:  # diagonal lines, so an area that overlaps a filled one still reads as its own shape
            pid = f"hatch{k}-{abs(hash(color)) % 10**6}"
            parts.append(f'<defs><pattern id="{pid}" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                         f'<line x1="0" y1="0" x2="0" y2="7" stroke="{color}" stroke-width="1.5" stroke-opacity=".55"/></pattern></defs>')
            paint = f'fill="url(#{pid})"'
        parts.append(f'<polygon points="{X0},{Y1} {pts} {X1},{Y1}" {paint} stroke="none"/>'
                     f'<text x="{sx(tx):.1f}" y="{sy(ty):.1f}" text-anchor="middle" fill="{color}" font-size="14">{text}</text>')
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
    for x, fn, text, color, *pos in marks:
        lx, ly, anchor = (sx(x) + 8, sy(fn(x)) - 8, "start") if pos == ["ur"] else (sx(x), sy(fn(x)) - 12, "middle")
        parts.append(f'<line x1="{sx(x):.1f}" y1="{Y1}" x2="{sx(x):.1f}" y2="{sy(fn(x)):.1f}" stroke="{color}" stroke-width="1.5" stroke-dasharray="3 3"/>'
                     f'<circle cx="{sx(x):.1f}" cy="{sy(fn(x)):.1f}" r="4.5" fill="{color}"/>'
                     f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" fill="{color}" font-size="13" font-weight="700">{text}</text>')
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


# Runs after the renderer's quiz handler, which wrote the feedback as text: feedback that
# build() pre-rendered with KaTeX is shown as HTML instead.
QUIZ_MATH_JS = """
document.querySelectorAll('.quiz-opt').forEach(function (o) {
  if (!(o.dataset.feedback || '').includes('class="katex')) return;
  o.addEventListener('click', function () {
    var fb = o.nextElementSibling;
    if (fb && fb.classList.contains('feedback'))
      fb.innerHTML = (o.dataset.correct === 'true' ? '\\u2705 ' : '\\u274c ') + o.dataset.feedback;
  });
});
"""


def _visible(s):
    """Rough visible text of an option: LaTeX delimiters, commands and braces dropped."""
    s = re.sub(r"\\[()\[\],;! ]|[{}$]", "", s)
    return re.sub(r"\\[a-zA-Z]+", "x", s).strip()  # a command such as \theta shows as one symbol


def check_options(question, options):
    """Refuse options that give the answer away by length (the "long correct answer" flaw):
    the correct one may not be clearly the longest, and all must be about the same size.
    options: [(text, correct)]."""
    lens = [len(_visible(t)) for t, _ in options]
    right = [n for n, (_, c) in zip(lens, options) if c]
    wrong = [n for n, (_, c) in zip(lens, options) if not c]
    assert len(right) == 1, f"one correct option expected: {question[:60]}"
    problems = []
    if right[0] > max(wrong) + 3:
        problems.append("a certa é a mais longa")
    if max(lens) - min(lens) > max(6, .25 * max(lens)):
        problems.append("tamanhos muito diferentes")
    if problems:
        raise SystemExit(f"Quiz com pista ({', '.join(problems)}): {lens}\n  {question[:90]}")


def mc(question, options):
    """Inline multiple-choice question (same widget as the renderer's end quiz).
    options: [(text, correct, feedback)], checked by check_options and shuffled with a seed taken
    from the question, so the order is not a cue and a rebuild keeps it."""
    check_options(question, [(t, c) for t, c, _ in options])
    options = list(options)
    random.Random(question).shuffle(options)
    # Math in a feedback attribute is rendered now: the page-wide KaTeX pass would put raw HTML
    # (with quotes) inside the attribute and break the button. QUIZ_MATH_JS shows it as HTML.
    options = [(t, c, render.render_math(html.escape(f, quote=False)) if "\\(" in f else f) for t, c, f in options]
    btns = "".join(
        f'<button class="quiz-opt" data-correct="{"true" if c else "false"}" data-feedback="{html.escape(f)}">{t}</button>'
        for t, c, f in options)
    return f'<div class="quiz-q"><p><strong>{question}</strong></p>{btns}</div>'


def build(spec, out):
    """Render spec (render.py format) to the path out, with the extras injected."""
    spec.setdefault("math", True)
    spec.setdefault("_base", str(Path(out).parent))
    for q in spec.get("quiz", []):
        check_options(q["question"], [(o["text"], o["correct"]) for o in q["options"]])
    # The renderer shows quiz feedback as plain text, so math in it is rendered here, ahead of
    # time; QUIZ_MATH_JS then shows that feedback as HTML.
    for q in spec.get("quiz", []):
        for o in q["options"]:
            if "\\(" in o.get("feedback", ""):
                o["feedback"] = render.render_math(html.escape(o["feedback"], quote=False))
    page = render.render(spec)
    # Quiz questions may carry "ref": [(anchor_id, label), ...]: a "Rever:" line linking to the section.
    # Matched by position (the end quiz keeps question order), since math changes the question text.
    head, sep, tail = page.partition('<h2 id="quiz">')
    blocks = tail.split('<div class="quiz-q">')
    for i, q in enumerate(spec.get("quiz", []), 1):
        if q.get("ref") and i < len(blocks):
            links = " · ".join(f'<a href="#{a}">{lbl}</a>' for a, lbl in q["ref"])
            blocks[i] = blocks[i].replace("</strong></p>", f'</strong></p>\n<p class="quiz-ref">Rever: {links}</p>', 1)
    page = head + sep + '<div class="quiz-q">'.join(blocks)
    page = re.sub(r"(<table\b.*?</table>)", r'<div class="tw">\1</div>', page, flags=re.S)
    check_js = (ASSETS / "check.js").read_text(encoding="utf-8")
    ink_js = INK_JS.read_text(encoding="utf-8")
    page = (page
            .replace('<html lang="en">', '<html lang="pt-BR">')
            .replace("<strong>Contents</strong>", "<strong>Sumário</strong>")
            .replace('<a href="#quiz">Quiz</a>', '<a href="#quiz">Quiz final</a>')
            .replace('<h2 id="quiz">Quiz</h2>', '<h2 id="quiz">Quiz final</h2>')
            .replace("</style>", EXTRA_CSS + "</style>", 1)
            .replace("</head>", f"<script>{LIVE_JS}</script>\n</head>", 1)
            .replace("</body>", f"<script>{check_js}</script>\n<script>{QUIZ_MATH_JS}</script>\n<script>{ink_js}</script>\n<script>{SQUARE_JS}</script>\n</body>"))
    if spec.get("crumbs"):
        page = page.replace("<h1>", f'<nav class="crumbs">{spec["crumbs"]}</nav>\n<h1>', 1)
    Path(out).write_text(page, encoding="utf-8")
    subprocess.run([sys.executable, str(ADD_NOTES), str(out)], check=True)


if __name__ == "__main__":
    sys.exit("Import this module from a lesson source; see lessons/src/.")
