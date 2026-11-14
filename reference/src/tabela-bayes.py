"""Reference sheet source. Build: python reference/src/tabela-bayes.py"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "assets"))
from build import build  # noqa: E402

body = r"""
$$P(H \mid D) = \frac{P(D \mid H)\,P(H)}{P(D)}, \qquad P(D) = \sum_H P(D \mid H)\,P(H), \qquad \text{posterior} \propto \text{likelihood} \times \text{prior}$$

<table>
<tr><th>coluna</th><th>o que é</th><th>soma</th></tr>
<tr><td>prior \(P(H)\)</td><td>crença antes do dado; proporção ÷ total</td><td>1</td></tr>
<tr><td>likelihood \(P(D \mid H)\)</td><td>probabilidade do dado se \(H\) for verdadeira</td><td>não soma</td></tr>
<tr><td>numerador</td><td>prior × likelihood</td><td>\(P(D)\)</td></tr>
<tr><td>posterior \(P(H \mid D)\)</td><td>numerador ÷ \(P(D)\)</td><td>1</td></tr>
</table>
<h3>Vários dados, independentes dada a hipótese</h3>
<p>Multiplique as likelihoods, \((1/n)^k\) para \(k\) lançamentos de um dado de \(n\) faces, e normalize só no fim. Dá o mesmo que atualizar passo a passo (MIT11 §4).</p>
<div class="callout"><b>Armadilhas.</b> Confundir \(P(D \mid H)\) com \(P(H \mid D)\) (falácia da taxa-base, MIT11 §5) ·
usar a proporção como prior sem dividir pelo total · somar a coluna likelihood · esquecer que um dado impossível zera a hipótese ·
achar que o MLE é a hipótese mais provável.</div>
"""

SPEC = {
    "title": "Ficha: tabela de atualização bayesiana",
    "subtitle": "Hipóteses discretas · MIT11 §3–4",
    "crumbs": 'COE241 · P2 · Ficha &nbsp;·&nbsp; aprendida na <a href="../lessons/0001-tabela-de-atualizacao-bayesiana.html">lição 0001</a>',
    "sections": [{"id": "ficha", "heading": "Resumo", "html": body}],
}

if __name__ == "__main__":
    build(SPEC, ROOT / "reference" / "tabela-bayes.html")
