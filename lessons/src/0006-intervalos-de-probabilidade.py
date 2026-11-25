"""Lesson 0006 source. Build: python lessons/src/0006-intervalos-de-probabilidade.py

Quotes from MIT16 are verbatim from the PDF text extracted with pymupdf (MIT OCW 18.05 Spring 2022, CC BY-NC-SA 4.0).
Unlike MIT13/MIT15, the symbols came out clean; they are written in LaTeX only for rendering.
Beta(8,6) quantiles: scipy.stats.beta(8, 6).ppf, matching the MEX2G solution (qbeta in R).
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "assets"))
from build import build, mc, quote, pdf_plot  # noqa: E402

MIT16 = "https://drive.google.com/file/d/1Pk-4I5S6gOVdQcJVH7u6k1-Lo0KdnzDy/view"
MEX2 = "https://drive.google.com/file/d/1GrVVl5QZtlKpjc1ZMferBVI-sTk3rwMA/view"
MEX2G = "https://drive.google.com/file/d/1QqJq3wXWRIiaJaonbzpUTus8JRrpDAgb/view"
P2 = "https://drive.google.com/file/d/1UC2kRa6K_6zXryQe7irAKbvfMTQh12um/view"
LESSON0, LESSON3, LESSON5 = "0000-mle.html", "0003-prior-continua.html", "0005-priors-conjugadas.html"

ACC, MUT, FG = "var(--accent)", "var(--muted)", "var(--fg)"


def src(where):
    return f'<a href="{MIT16}">MIT16</a>, {where}'


def num(answer, tol="0.002", width=None):
    w = f' style="width:{width}"' if width else ""
    return f'<input data-answer="{answer}" data-tol="{tol}"{w}>'


def check(body, ok):
    return (f'<div class="check-group" data-ok="{ok}">{body}'
            f'<button class="check">Verificar</button><div class="feedback"></div></div>')


def beta_pdf(a, b):
    c = math.factorial(a + b - 1) / (math.factorial(a - 1) * math.factorial(b - 1))
    return lambda x: c * x ** (a - 1) * (1 - x) ** (b - 1)


b86, b75 = beta_pdf(8, 6), beta_pdf(7, 5)
tri = lambda x: 2 * x  # noqa: E731


def malaria_table():
    """MIT16 §4.1: flat prior on the 6×6 grid, likelihood θS²(1−θS)¹³ θN¹⁴(1−θN); cells with θN > θS shaded."""
    v = [0, .2, .4, .6, .8, 1]
    lik = {(s, n): s**2 * (1 - s)**13 * n**14 * (1 - n) for s in v for n in v}
    tot = sum(lik.values())
    post = {k: x / tot for k, x in lik.items()}
    assert abs(sum(x for (s, n), x in post.items() if n > s) - 0.99995) < 1e-5  # MIT16 value
    shade = ' style="background:var(--callout-bg);font-weight:600"'
    head = "".join(f'<th class="num">{s:g}</th>' for s in v)
    rows = []
    for n in reversed(v):
        cells = "".join(f'<td class="num"{shade if n > s else ""}>{"0" if post[(s, n)] < 5e-6 else format(post[(s, n)], ".5f")}</td>'
                        for s in v)
        rows.append(f'<tr><th class="num">{n:g}</th>{cells}</tr>')
    return (r'<table style="table-layout:fixed"><tr><th>\(\theta_N\) \ \(\theta_S\)</th>' + head + "</tr>" + "".join(rows) + "</table>"
            r'<p style="font-size:.85rem;color:var(--muted)">Posterior de cada par \((\theta_S, \theta_N)\). '
            r'Casas pintadas: \(\theta_N > \theta_S\), o gene protege. Os valores são os da tabela do MIT16, §4.1.</p>')

# Beta(8,6) quantiles (scipy; MEX2G gives the same with qbeta)
Q = {0.05: 0.35480, 0.25: 0.48330, 0.5: 0.57492, 0.75: 0.66319, 0.95: 0.77604}
CDF_HALF = 0.29053

# ---------------------------------------------------------------- recordação
recordacao = rf"""
<p>Esta lição usa três coisas das lições anteriores: a regra da Beta (<a href="{LESSON5}">0005</a>), o MAP (<a href="{LESSON3}">0003</a>)
e o MLE (<a href="{LESSON0}">0000</a>). Tente sem voltar lá.</p>
""" + check(
    r"""<p>1. A prior de \(\theta\) é Beta(2, 2). Numa amostra de 10 pessoas, 6 dizem "sim" e 4 dizem "não". A posterior é Beta("""
    + num("8", "0.01", "2.6rem") + ", " + num("6", "0.01", "2.6rem") + r""").</p>
<p>2. Uma posterior tem numerador \(c\,\theta^7(1-\theta)^5\). O pico dela (o MAP) fica em \(\theta\) = """ + num("7/12", "0.002", "4rem") + r"""</p>
<p>3. Uma moeda dá 6 caras em 10 lançamentos. O MLE de \(\theta\) (a probabilidade de cara) é """ + num("0.6", "0.002", "4rem") + "</p>",
    "Isso. 1: 2 + 6 = 8 e 2 + 4 = 6. 2: o pico de θ^m(1−θ)^n fica em m/(m+n) = 7/12 ≈ 0.583. "
    "3: o MLE é o pico de θ⁶(1−θ)⁴, ou seja, 6/10.")

# ---------------------------------------------------------------- intervalo
intervalo = r"""
<p>O MAP diz onde a posterior é mais alta, mas não diz quanta probabilidade fica perto dele. Uma posterior Beta(8, 6) tem MAP
\(7/12 \approx 0.58\), acima de 0.5. Isso basta para dizer que \(\theta > 0.5\)? Depende de quanta área a posterior tem abaixo de 0.5,
e o MAP não mostra isso. O que mostra é um intervalo com a probabilidade dele:</p>
""" + quote(r"""<p>Definition: A \(p\)-probability interval for \(\theta\) is an interval \([a, b]\) with \(P(a \le \theta \le b) = p\).</p>
<p>Notes. 1. In the discrete case with pmf \(p(\theta)\), this means \(\sum_{a \le \theta_i \le b} p(\theta_i) = p\). 2. In the continuous case with
pdf \(f(\theta)\), this means \(\int_a^b f(\theta)\,d\theta = p\).</p>""", src("<i>Probability intervals</i>, §2")) + r"""
<p>Um <b>intervalo de probabilidade</b> \(p\) é um trecho \([a, b]\) do eixo de \(\theta\) onde fica uma fração \(p\) da probabilidade
(o MIT também chama de <i>credible interval</i>). Com pmf, soma-se a posterior das hipóteses dentro do trecho; com pdf, é a área sob a curva
entre \(a\) e \(b\).</p>
<h3>Quantis</h3>
<p>Para achar \(a\) e \(b\), o MIT16 usa quantis:</p>
""" + quote(r"""<p>Recall that the \(s\)-quantile for \(\theta\) is the value \(q_s\) with \(P(\theta \le q_s) = s\). So for \(s \le t\), the amount of probability
between the \(s\)-quantile and the \(t\)-quantile is just \(t - s\). In these terms, a \(p\)-probability interval is any interval \([q_s, q_t]\) with
\(t - s = p\).</p>""", src("<i>Probability intervals</i>, §2")) + r"""
<p>O <b>quantil</b> \(q_s\) é o ponto que deixa a probabilidade \(s\) à esquerda. \(q_{0.5}\) é a mediana. Entre \(q_{0.25}\) e \(q_{0.75}\)
fica \(0.75 - 0.25 = 0.5\) da probabilidade.</p>
<p>Para fazer a conta inteira à mão, um exemplo pequeno. Uma moeda torta tem probabilidade de cara \(\theta\) desconhecida. Sem nenhuma
informação sobre \(\theta\), a prior é plana: \(f(\theta) = 1\) em \([0, 1]\). A moeda é lançada uma vez e dá cara. A likelihood dessa cara é
\(\theta\), então o numerador de Bayes é \(1 \cdot \theta = \theta\). A área sob \(\theta\) entre 0 e 1 é \(1/2\); dividindo por ela, a posterior é</p>
$$f(\theta \mid \text{cara}) = 2\theta, \qquad 0 \le \theta \le 1$$
<p>É a mesma conta do exemplo da <a href="0003-prior-continua.html#flat">prior plana na lição 0003</a>. A posterior cresce com \(\theta\): uma moeda que dá
mais cara explica melhor a cara observada. A probabilidade à esquerda de um ponto \(q\) é</p>
$$P(\theta \le q) = \int_0^q 2\theta\,d\theta = q^2$$
<p>Para achar o quantil \(q_s\), resolva \(q^2 = s\): \(q_s = \sqrt{s}\). Então \(q_{0.25} = \sqrt{0.25} = 0.5\) e \(q_{0.75} = \sqrt{0.75} \approx 0.866\),
e \([0.5,\ 0.866]\) é um intervalo de probabilidade 0.5.</p>
""" + pdf_plot(
    [("f(θ) = 2θ", tri, ACC, False, .15, 1.0)],
    "Posterior 2θ: a área pintada entre q₀.₂₅ = 0.5 e q₀.₇₅ ≈ 0.866 é 0.5, metade da área total.",
    ymax=2.3, shade=(0.5, math.sqrt(.75), tri, "área 0.5")) + check(
    r"""<p>Ainda com \(f(\theta) = 2\theta\): o intervalo de probabilidade 0.9 que deixa 0.05 de cada lado é
\([q_{0.05},\ q_{0.95}]\) = [""" + num(str(math.sqrt(.05)), "0.002", "4rem") + ", " + num(str(math.sqrt(.95)), "0.002", "4rem") + "]</p>",
    "Isso: √0.05 ≈ 0.224 e √0.95 ≈ 0.975. Entre eles fica 0.95 − 0.05 = 0.9 da probabilidade.") + r"""
<h3>Qual intervalo escolher</h3>
<p>Para o mesmo \(p\) há muitos intervalos: \([q_{0.25}, q_{0.75}]\) e \([q_{0.05}, q_{0.55}]\) têm os dois probabilidade 0.5. O MIT16
recomenda dois:</p>
""" + quote(r"""<p>The interval \([q_{0.25}, q_{0.75}]\) is symmetric because the amount of probability remaining on either side of the interval is the
same, namely 0.25. If the pdf is not too skewed, the symmetric interval is usually a good default choice.</p>
<p>[…] We can make the width smaller by centering the interval under the highest part of the pdf. Such an interval is usually a good choice
since it contains the most likely values.</p>""", src("<i>Probability intervals</i>, §2")) + r"""
<p>O <b>intervalo simétrico</b> deixa a mesma sobra dos dois lados: \([q_{(1-p)/2},\ q_{(1+p)/2}]\). Para 50%, sobra
0.5 no total, 0.25 de cada lado: \([q_{0.25}, q_{0.75}]\). Quando o enunciado não diz qual, use o simétrico.</p>
""" + mc(
    "Você tem um intervalo de probabilidade 0.8 e quer um de 0.9 com a mesma ideia (simétrico). O novo intervalo é…",
    [("mais largo, porque precisa conter mais área", True,
      "Isso. O MIT16 responde a essa mesma pergunta: \"A bigger probability requires a bigger interval.\""),
     ("mais estreito, porque a certeza ficou maior", False,
      "Aqui 0.9 foi lido como \"mais certeza sobre θ\". É só mais área a cobrir, e cobrir mais área exige um trecho mais largo."),
     ("do mesmo tamanho, porque a posterior é a mesma", False,
      "A posterior é a mesma, mas o intervalo de 0.9 precisa juntar mais área que o de 0.8, então ele estica.")])

# ---------------------------------------------------------------- região
regiao = r"""
<p>Às vezes a pergunta não é "onde está \(\theta\)?", e sim "a afirmação \(\theta > 0.5\) é verdadeira?". A resposta bayesiana é a
probabilidade posterior da afirmação: some a posterior de todas as hipóteses em que ela vale. Com uma pdf, a soma vira a área sob a
posterior nessa região.</p>
<p>O MIT16 faz essa conta com um experimento real. Quinze portadores do gene da anemia falciforme e quinze não portadores receberam o
parasita da malária: 2 portadores e 14 não portadores ficaram doentes. Há dois parâmetros, \(\theta_S\), a probabilidade de um portador
ficar doente, e \(\theta_N\), a de um não portador. O gene protege se \(\theta_N > \theta_S\). Cada hipótese é um par \((\theta_S, \theta_N)\)
com os dois valores em \(\{0, 0.2, 0.4, 0.6, 0.8, 1\}\), o que dá 36 pares, todos com prior \(1/36\).</p>
<p>A likelihood de um par é a chance de ver exatamente esses doentes e sãos (a menos de uma constante, que some ao normalizar):</p>
$$P(\text{dados} \mid \theta_S, \theta_N) \propto \underbrace{\theta_S^{2}(1-\theta_S)^{13}}_{\text{portadores: 2 doentes, 13 sãos}}\;
\underbrace{\theta_N^{14}(1-\theta_N)^{1}}_{\text{não portadores: 14 doentes, 1 são}}$$
<p>Como a prior é a mesma em todos os pares, a posterior é essa likelihood dividida pela soma dela nos 36 pares. Na tabela, cada linha é um
valor de \(\theta_N\), cada coluna um valor de \(\theta_S\), e as casas pintadas são as do gene protegendo:</p>
""" + malaria_table() + r"""
<p>A probabilidade de "o gene protege" é a soma das casas pintadas: \(P(\theta_N > \theta_S \mid \text{dados}) \approx 0.99995\). Quase toda
a posterior está em \(\theta_S = 0.2\) com \(\theta_N = 0.8\) ou 0.6, bem acima da diagonal. Depois dos dados, é praticamente certo que o gene
protege. O MIT16 descreve a conta assim:</p>
""" + quote(r"""<p>To decide whether \(S\) confers protection against malaria, we compute the posterior probabilities of ‘some protection’ and of ‘strong
protection’. These are computed by summing the corresponding squares in the posterior table.</p>""", src("<i>Choosing priors</i>, §4.1")) + r"""
<p>Com uma pdf é a mesma ideia, trocando a soma pela área. Na moeda, a posterior é \(2\theta\), e a afirmação "\(\theta \le 0.5\)" vale
para todo \(\theta\) entre 0 e 0.5. A probabilidade dela é a área sob \(2\theta\) nesse trecho:</p>
$$P(\theta \le 0.5) = \int_0^{0.5} 2\theta\,d\theta = \Big[\theta^2\Big]_0^{0.5} = 0.5^2 - 0^2 = 0.25$$
<p>É a fórmula \(P(\theta \le q) = q^2\) da seção anterior, com \(q = 0.5\). Dá para conferir sem integral: sob a reta \(2\theta\), o trecho
de 0 a 0.5 é um triângulo de base 0.5 e altura \(2 \cdot 0.5 = 1\), com área \(\tfrac{0.5 \cdot 1}{2} = 0.25\).</p>
""" + check(
    r"""<p>Na posterior \(2\theta\): \(P(\theta > 0.5)\) = """ + num("0.75", "0.002", "4rem") + "</p>",
    "Isso: 1 − P(θ ≤ 0.5) = 1 − 0.25 = 0.75.")

# ---------------------------------------------------------------- objetivo: MEX2 13
objetivo = quote(r"""<p>Peter and Jerry disagree over whether 18.05 students prefer Bayesian or frequentist statistics. They decide to pick a random sample
of 10 students from the class and get Shelby to ask each student which they prefer. They agree to start with a prior \(f(\theta) \sim \text{Beta}(2, 2)\),
where \(\theta\) is the percent that prefer Bayesian. […]</p>
<p>(b) Compute the posterior distribution of \(\theta\) given \(x_1 = 6\).</p>
<p>(c) Use R to compute 50% and 90% probability intervals for \(\theta\). Center the intervals so that the leftover probability in both tails is
the same.</p>
<p>(d) The maximum a posteriori (MAP) estimate of \(\theta\) (the peak of the posterior) is given by \(\hat\theta = 7/12\), leading Jerry to concede
that a majority of students are Bayesians. In light of your answer to part (c) does Jerry have a strong case?</p>""",
                 f'<a href="{MEX2}">MEX2</a>, problema 13') + r"""
<h3>(b) A posterior</h3>
<p>Dos 10 alunos, \(x_1 = 6\) preferem Bayes e 4 preferem a estatística frequentista. A prior é Beta(2, 2).</p>
""" + check(
    r"""<p>Posterior de \(\theta\): Beta(""" + num("8", "0.01", "2.6rem") + ", " + num("6", "0.01", "2.6rem") + r""")</p>
<details><summary>Dica</summary><p>Regra da Beta (lição 0005): prior Beta(\(a, b\)) com \(s\) sucessos e \(f\) fracassos dá Beta(\(a + s,\ b + f\)).
Aqui o sucesso é preferir Bayes.</p></details>""",
    f"Isso: 2 + 6 = 8 e 2 + 4 = 6, então Beta(8, 6). Confira no <a href='{MEX2G}'>MEX2G</a>, problema 13(b).") + r"""
<p>O MIT16 usa essa mesma Beta(8, 6) para mostrar por que um intervalo comunica melhor que o nome da distribuição:</p>
""" + quote(r"""<p>Even with a beta distribution, it’s easier to interpret “I think \(\theta\) is between 0.45 and 0.65 with 50% probability” than “I think
\(\theta\) follows a beta(8,6) distribution”.</p>""", src("<i>Probability intervals</i>, §3.1")) + rf"""
<h3>(c) Os intervalos</h3>
<p>A Beta(8, 6) não tem quantil por fórmula simples: a integral dela é um polinômio de grau 14. Por isso o MEX2 manda usar o R
(<code>qbeta</code>). O enunciado pede o intervalo simétrico: "leftover probability in both tails is the same" quer dizer
que sobra a mesma probabilidade nas duas pontas. Os quantis abaixo foram calculados com software; o que fica com você é escolher quais usar.</p>
<table>
<tr><th>\(s\)</th><td class="num">0.05</td><td class="num">0.25</td><td class="num">0.5</td><td class="num">0.75</td><td class="num">0.95</td></tr>
<tr><th>\(q_s\) da Beta(8, 6)</th><td class="num">{Q[0.05]:.3f}</td><td class="num">{Q[0.25]:.3f}</td><td class="num">{Q[0.5]:.3f}</td><td class="num">{Q[0.75]:.3f}</td><td class="num">{Q[0.95]:.3f}</td></tr>
</table>
""" + check(
    r"""<p>Intervalo simétrico de 50%: [""" + num(str(Q[0.25]), "0.002", "4rem") + ", " + num(str(Q[0.75]), "0.002", "4rem") + r"""]</p>
<p>Intervalo simétrico de 90%: [""" + num(str(Q[0.05]), "0.002", "4rem") + ", " + num(str(Q[0.95]), "0.002", "4rem") + "]</p>"
    + r"""<details><summary>Dica</summary><p>Simétrico de probabilidade \(p\): sobra \((1-p)/2\) de cada lado. Para 50%, sobra 0.25 de cada lado.</p></details>""",
    f"Isso: 50% vai de q₀.₂₅ a q₀.₇₅, [0.483, 0.663]; 90% vai de q₀.₀₅ a q₀.₉₅, [0.355, 0.776]. "
    f"Confira no <a href='{MEX2G}'>MEX2G</a>, problema 13(c).") + pdf_plot(
    [("Beta(8, 6)", b86, ACC, False, .8)],
    "Posterior Beta(8, 6). A área pintada, de 0.483 a 0.663, é o intervalo de 50%; fora dele fica 0.25 de cada lado.",
    ymax=3.6, shade=(Q[0.25], Q[0.75], b86, "50%")) + rf"""
<h3>(d) O caso do Jerry</h3>
<p>O MAP é o pico da posterior, \(7/12 \approx 0.58\). Como ele fica acima de 0.5, Jerry concluiu que a maioria prefere Bayes. Mas o pico é
um ponto só, e não diz quanta probabilidade a posterior dá ao contrário, "a maioria é frequentista", ou seja, \(\theta \le 0.5\).</p>
<p>Essa probabilidade sai como na <a href="#regiao">seção da afirmação</a>: é a área sob a posterior à esquerda de 0.5,
\(P(\theta \le 0.5)\). Na Beta(8, 6) essa integral não sai à mão, e o software dá \(P(\theta \le 0.5) = {CDF_HALF:.3f}\).</p>
""" + pdf_plot(
    [("Beta(8, 6)", b86, ACC, False, .8)],
    "A área pintada, à esquerda de 0.5, é P(θ ≤ 0.5) ≈ 0.29. O pico fica à direita de 0.5, mas quase um terço da probabilidade fica à esquerda.",
    ymax=3.6, fills=[(lambda x: b86(x) if x <= 0.5 else 0, ACC, "área 0.29", .42, .4)],
    marks=[(7 / 12, b86, "MAP 7/12", ACC, "ur")]) + mc(
    r"Os intervalos de 50% e 90% contêm valores abaixo de 0.5, e \(P(\theta \le 0.5) \approx 0.29\). Jerry tem um caso forte?",
    [("Não: sobra 29% de chance de a maioria ser frequentista", True,
      "Isso. O MEX2G conclui o mesmo: os dois intervalos cobrem valores abaixo de 0.5, e \"there is still a 29% posterior probability that the majority prefers frequentist statistics.\""),
     ("Sim: o MAP fica acima de 0.5, e o MAP é a melhor estimativa", False,
      "O MAP é só o pico. Ele não diz quanta área está do outro lado de 0.5, e aqui essa área é 0.29."),
     ("Sim: 71% de chance já é uma maioria das probabilidades", False,
      "71% é a posterior de θ > 0.5. Uma afirmação com 29% de chance de ser falsa não é um caso forte.")])

# ---------------------------------------------------------------- MAP e MLE
mapmle = r"""
<p>Até aqui a prior foi dada. O MIT16 começa pela pergunta seguinte: e quando não há informação para escolher a prior?</p>
""" + quote(r"""<p>Suppose we have no idea what the distribution of dice in the drawer might be. In this case it’s reasonable to use a flat prior.</p>""",
            src("<i>Choosing priors</i>, §3.1")) + r"""
<p>Uma prior <b>plana</b> dá o mesmo valor a todas as hipóteses. "Plana" e "uniforme" são dois nomes para a mesma prior (o MIT16 diz
<i>flat</i> ou <i>uniform</i>; a P2 diz Uniforme). Com \(\theta\) em \([0, 1]\), ela é \(f(\theta) = 1\).</p>
<p>O exemplo: uma gaveta com dados de 4, 6, 8, 12 e 20 lados, em proporção desconhecida. Tira-se um dado ao acaso, e o primeiro lançamento
dá 4. Com a prior plana, cada hipótese tem prior 1/5, e a tabela de Bayes fica assim:</p>
<table>
<tr><th>hipótese</th><th class="num">prior \(P(H)\)</th><th class="num">likelihood \(P(4 \mid H)\)</th><th class="num">posterior \(P(H \mid 4)\)</th></tr>
<tr><td>4 lados</td><td class="num">1/5</td><td class="num">1/4</td><td class="num">0.370</td></tr>
<tr><td>6 lados</td><td class="num">1/5</td><td class="num">1/6</td><td class="num">0.247</td></tr>
<tr><td>8 lados</td><td class="num">1/5</td><td class="num">1/8</td><td class="num">0.185</td></tr>
<tr><td>12 lados</td><td class="num">1/5</td><td class="num">1/12</td><td class="num">0.123</td></tr>
<tr><td>20 lados</td><td class="num">1/5</td><td class="num">1/20</td><td class="num">0.074</td></tr>
</table>
<p>A posterior é a likelihood dividida pela soma dela. Por exemplo, \(\frac{1/4}{1/4 + 1/6 + 1/8 + 1/12 + 1/20} \approx 0.370\). O 1/5 da prior
aparece em todas as linhas e se cancela na normalização. É a regra do MIT16, "posterior \(\propto\) likelihood \(\cdot\) prior", com uma prior
que não muda de linha para linha:</p>
$$\text{posterior} \propto \text{likelihood} \cdot \underbrace{\text{prior}}_{\text{constante}} \quad\Longrightarrow\quad \text{posterior} \propto \text{likelihood}$$
<p>Se a posterior é a likelihood multiplicada por uma constante, as duas têm o pico no mesmo lugar. O pico da posterior é o MAP; o pico da
likelihood é o MLE. Na tabela, os dois são o dado de 4 lados.</p>
<p>Com \(\theta\) contínuo vale o mesmo. Para ver, volte ao problema de Peter e Jerry da <a href="#objetivo">seção anterior</a>
(MEX2 13): \(\theta\) é a fração dos alunos que preferem Bayes, e na amostra de 10 alunos, 6 preferem Bayes e 4 não. A likelihood é</p>
$$P(\text{dados} \mid \theta) = \binom{10}{6}\,\theta^6(1-\theta)^4$$
<p>O pico dela, o MLE, fica em \(6/10\) (<a href="#recordacao">item 3 da recordação</a>). Agora compare duas priors.</p>
<p>Com a prior plana, \(f(\theta) = 1\) em \([0, 1]\), a prior não muda nada na multiplicação:</p>
$$\text{posterior} \propto \underbrace{1}_{\text{prior}} \cdot \underbrace{\theta^6(1-\theta)^4}_{\text{likelihood sem a constante}} = \theta^6(1-\theta)^4$$
<p>A posterior tem a mesma forma da likelihood, então o pico é o mesmo: MAP \(= 6/10 =\) MLE.</p>
<p>Agora com a prior que Peter e Jerry combinaram, Beta(2, 2). A pdf dela é \(f(\theta) = 6\,\theta(1-\theta)\): a forma é
\(\theta^{a-1}(1-\theta)^{b-1}\) com \(a = b = 2\), e o 6 é a constante da Beta, \(\frac{3!}{1!\,1!}\). Diferente da prior plana, ela muda com \(\theta\):</p>
$$\text{posterior} \propto \underbrace{\theta(1-\theta)}_{\text{prior sem a constante}} \cdot \theta^6(1-\theta)^4 = \theta^7(1-\theta)^5$$
<p>Os expoentes mudaram, e o pico vai para \(7/12 \approx 0.583\) (<a href="#recordacao">item 2 da recordação</a>). A prior Beta(2, 2) é mais alta perto de 0.5,
então puxa o pico de 0.6 para perto de 0.5. Com uma prior que não é constante, o MAP e o MLE ficam diferentes.</p>
""" + pdf_plot(
    [("Beta(7, 5), prior plana", b75, MUT, True, .0, 3.3), ("Beta(8, 6), prior Beta(2, 2)", b86, ACC, False, .0, 2.9)],
    "Mesmos dados (6 sim, 4 não): com prior plana o pico fica em 0.6, o MLE; com prior Beta(2, 2) ele vai para 7/12, mais perto de 0.5.",
    ymax=3.6, marks=[(0.6, lambda x: 0.7, "0.6", MUT), (7 / 12, b86, "7/12", ACC)]) + quote(
    r"""<p>Os estimadores maximum a posteriori (MAP) e maximum likelihood (ML) de um parâmetro θ são iguais se a prior de θ segue uma distribuição
Uniforme.</p>""", f'<a href="{P2}">P2-23.2</a>, questão 4.6', lang="pt-BR") + mc(
    "Verdadeira ou falsa? Qual é a justificativa?",
    [("Verdadeira: com prior uniforme, a posterior é proporcional à likelihood", True,
      "Isso. O gabarito é Verdadeira. A prior uniforme dá o mesmo número a todo θ, então a posterior é a likelihood vezes esse número, e as duas têm o mesmo pico."),
     ("Falsa: a likelihood não depende da prior, então os dois não se relacionam", False,
      "A likelihood não depende da prior, mas a posterior depende das duas. Com prior uniforme, a posterior é proporcional à likelihood."),
     ("Falsa: o MAP usa a posterior e o MLE usa a likelihood, que são diferentes", False,
      "São funções diferentes, mas com prior uniforme uma é a outra vezes um número fixo, e multiplicar por um número fixo não move o pico.")]) + r"""
<p>Um cuidado que o MIT16 mostra com as priors rígidas: "No matter what the data, a hypothesis with prior probability 0 will have posterior
probability 0." Se a prior for Uniforme num trecho que não contém o MLE (por exemplo, Uniforme em \([0, 0.5]\) com MLE 0.6), a posterior é zero
no MLE, e o MAP fica na borda, em 0.5. A afirmação da prova vale para a Uniforme em todo o intervalo possível de \(\theta\), como \([0, 1]\).</p>
"""

# ---------------------------------------------------------------- receita
receita = r"""
<div class="callout"><p>Intervalos e afirmações sobre \(\theta\), a partir da posterior:</p>
<ol class="spaced">
<li>Intervalo de probabilidade \(p\): \([a, b]\) com \(P(a \le \theta \le b) = p\). Com pmf, some; com pdf, integre.</li>
<li>Simétrico: \([q_{(1-p)/2},\ q_{(1+p)/2}]\). 50% é \([q_{0.25}, q_{0.75}]\); 90% é \([q_{0.05}, q_{0.95}]\).</li>
<li>Quantil \(q_s\): resolva \(P(\theta \le q) = s\). Se a integral for simples (como \(2\theta\)), faça à mão; numa Beta grande, use os valores dados.</li>
<li>Para "\(\theta > c\)": calcule \(P(\theta > c) = 1 - P(\theta \le c)\). O MAP acima de \(c\) não basta.</li>
<li>Prior plana (Uniforme em todo o intervalo de \(\theta\)): posterior \(\propto\) likelihood, então MAP = MLE.</li>
</ol></div>
"""

# ---------------------------------------------------------------- fontes
fontes = rf"""
<p>O arquivo do <a href="{MIT16}">MIT16</a> tem duas notas, <i>Choosing priors</i> e <i>Probability intervals</i>, e os problemas de aula.
Esta lição usou a definição de intervalo e os quantis (<i>Probability intervals</i> §2 e §3.1), a soma da posterior numa região (malária,
§4.1), a prior plana do dado (§3.1) e a prior rígida (§3.3). O que ficou de fora:</p>
<table>
<tr><th>trecho</th><th>faz falta na P2?</th><th>por que ficou de fora</th></tr>
<tr><td><i>Choosing priors</i> §3.2: o mesmo dado com prior 10× e 100× no de 20 lados</td><td>não</td><td>a conta é a tabela da lição 0001; a lição é que dados bons reduzem o peso da prior</td></tr>
<tr><td>§4: a malária inteira (tabela 6 × 6, prior informada, gráfico PDALX)</td><td>não</td><td>usamos só a soma da região; a tabela de duas dimensões é a da lição 0001 com mais linhas</td></tr>
<tr><td><i>Probability intervals</i> §4: montar uma prior Beta a partir de intervalos (eleição Sanford)</td><td>não</td><td>nenhuma lista cobra; precisa de software para ajustar a Beta</td></tr>
<tr><td>Problema de aula 1: ECMO × CVT (tabela 4 × 4)</td><td>não</td><td>mesma conta da malária; vale como treino da soma por região</td></tr>
<tr><td>A diferença entre intervalo de probabilidade e intervalo de confiança</td><td>sim, mais adiante</td><td>o intervalo de confiança é frequentista (MIT22, L05) e terá lição própria</td></tr>
</table>
<div class="callout">Se ficou alguma dúvida, pergunte ao seu professor, que é o agente nesta conversa. Vale um passo da conta, um termo ou "por que isso funciona?".</div>
<p style="font-size:.8rem;color:var(--muted)">As citações em inglês são de J. Orloff e J. Bloom, <i>18.05 Introduction to Probability and Statistics</i>,
Spring 2022, MIT OpenCourseWare, licença CC BY-NC-SA 4.0, e da prova da Profª Rosa Leão (COE241). Trechos omitidos aparecem como […]. Os quantis
da Beta(8, 6) foram calculados com software e batem com o MEX2G.</p>
"""

SPEC = {
    "title": "0006 · Intervalos de probabilidade",
    "subtitle": "Lição 0006 · COE241 P2 · MIT16 · intervalos de probabilidade e prior plana · meta: MEX2 13(c–d) e P2-23.2 Q4.6",
    "sections": [
        {"id": "recordacao", "heading": "Recordação: Beta, MAP e MLE", "html": recordacao},
        {"id": "intervalo", "heading": "Intervalos de probabilidade", "html": intervalo},
        {"id": "regiao", "heading": "A probabilidade de uma afirmação", "html": regiao},
        {"id": "objetivo", "heading": "O objetivo: MEX2 13(c–d)", "html": objetivo},
        {"id": "map-mle", "heading": "Prior plana: MAP = MLE (P2-23.2 Q4.6)", "html": mapmle},
        {"id": "receita", "heading": "Como resolver", "html": receita},
        {"id": "fontes", "heading": "O que ficou de fora do MIT16", "html": fontes},
    ],
    "quiz": [
        {"question": r"Numa posterior, \(q_{0.1} = 0.2\) e \(q_{0.7} = 0.6\). Qual é a probabilidade de \(0.2 \le \theta \le 0.6\)?",
         "ref": [("intervalo", "Intervalos de probabilidade")],
         "options": [
             {"text": "0.6", "correct": True, "feedback": r"Isso: entre \(q_{0.1}\) e \(q_{0.7}\) fica \(0.7 - 0.1 = 0.6\)."},
             {"text": "0.4", "correct": False, "feedback": r"Essa é a largura do intervalo, \(0.6 - 0.2\). A probabilidade é a diferença dos índices: \(0.7 - 0.1 = 0.6\)."},
             {"text": "0.7", "correct": False, "feedback": r"0.7 é a área à esquerda de \(q_{0.7}\). Falta tirar os 0.1 à esquerda de \(q_{0.1}\): \(0.7 - 0.1 = 0.6\)."}]},
        {"question": r"Qual é o intervalo simétrico de probabilidade 0.8?",
         "ref": [("intervalo", "Intervalos de probabilidade")],
         "options": [
             {"text": r"\([q_{0.1},\ q_{0.9}]\)", "correct": True, "feedback": r"Isso: sobra \(0.2\), e metade (0.1) fica de cada lado."},
             {"text": r"\([q_{0.2},\ q_{0.8}]\)", "correct": False, "feedback": r"Esse tem probabilidade \(0.8 - 0.2 = 0.6\). Para 0.8, sobra 0.1 de cada lado: \([q_{0.1}, q_{0.9}]\)."},
             {"text": r"\([q_{0.0},\ q_{0.8}]\)", "correct": False, "feedback": r"Tem probabilidade 0.8, mas toda a sobra fica à direita. O simétrico divide a sobra: \([q_{0.1}, q_{0.9}]\)."}]},
        {"question": r"A posterior de \(\theta\) é \(2\theta\) em \([0, 1]\). Qual é \(P(\theta > 0.6)\)?",
         "ref": [("regiao", "A probabilidade de uma afirmação")],
         "options": [
             {"text": "0.64", "correct": True, "feedback": r"Isso. A área à esquerda de 0.6 é a integral da posterior: \(P(\theta \le 0.6) = \int_0^{0.6} 2\theta\,d\theta = \big[\theta^2\big]_0^{0.6} = 0.36\). A área à direita é o resto: \(1 - 0.36 = 0.64\)."},
             {"text": "0.36", "correct": False, "feedback": r"Essa é a área à esquerda, \(\int_0^{0.6} 2\theta\,d\theta = 0.6^2 = 0.36\). A pergunta é a área à direita, o resto: \(1 - 0.36 = 0.64\)."},
             {"text": "0.40", "correct": False, "feedback": r"Essa seria a área à direita se a posterior fosse plana, \(f(\theta) = 1\). Com \(2\theta\): \(1 - \int_0^{0.6} 2\theta\,d\theta = 1 - 0.36 = 0.64\)."}]},
        {"question": r"Prior plana em \([0, 1]\) e 3 caras em 12 lançamentos. Qual é o MAP de \(\theta\)?",
         "ref": [("map-mle", "Prior plana: MAP = MLE (P2-23.2 Q4.6)")],
         "options": [
             {"text": "1/4", "correct": True, "feedback": r"Isso: com prior plana, MAP = MLE = \(3/12\)."},
             {"text": "1/2", "correct": False, "feedback": r"0.5 é o centro da prior plana, mas ela não puxa para lugar nenhum. O pico é o da likelihood, \(3/12\)."},
             {"text": "2/7", "correct": False, "feedback": r"Aqui somou 1 a cada contagem, como numa prior Beta(2, 2). Com prior plana, o pico é \(3/12\)."}]},
    ],
}

if __name__ == "__main__":
    build(SPEC, ROOT / "lessons" / "0006-intervalos-de-probabilidade.html")
