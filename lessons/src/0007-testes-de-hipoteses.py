"""Lesson 0007 source. Build: python lessons/src/0007-testes-de-hipoteses.py

Quotes from MIT17 are verbatim from the PDF text extracted with pymupdf (MIT OCW 18.05 Spring 2022, CC BY-NC-SA 4.0);
the symbols came out clean and are written in LaTeX only for rendering.
Numbers checked with scipy against MIT17 and the MPS08G solution: radar threshold 45.054, power 0.493, n = 10.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "assets"))
from build import build, mc, quote, pdf_plot  # noqa: E402

MIT17 = "https://drive.google.com/file/d/1sRg8Yf5wrXdysgxLNEd6xfCIRCrzq08I/view"
MPS08 = "https://drive.google.com/file/d/1yNr5VOHwgkVbtbKLts3g1KILiA0iKNZs/view"
MPS08G = "https://drive.google.com/file/d/1LS6IxX5KEmC76W62T4g2QaHNE5UskswE/view"
P2 = "https://drive.google.com/file/d/1UC2kRa6K_6zXryQe7irAKbvfMTQh12um/view"
LESSON0, LESSON1, LESSON6 = "0000-mle.html", "0001-tabela-de-atualizacao-bayesiana.html", "0006-intervalos-de-probabilidade.html"

ACC, MUT = "var(--accent)", "var(--muted)"


def src(where):
    return f'<a href="{MIT17}">MIT17</a>, {where}'


def num(answer, tol="0.002", width=None):
    w = f' style="width:{width}"' if width else ""
    return f'<input data-answer="{answer}" data-tol="{tol}"{w}>'


def check(body, ok):
    return (f'<div class="check-group" data-ok="{ok}">{body}'
            f'<button class="check">Verificar</button><div class="feedback"></div></div>')


def Phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def normal(m, s, lo, hi):
    """N(m, s²) drawn on [lo, hi]: pdf_plot works on [0, 1], so u in [0, 1] is mapped to x = lo + u (hi − lo)."""
    return lambda u: math.exp(-((lo + u * (hi - lo) - m) / s) ** 2 / 2) / (s * math.sqrt(2 * math.pi))


def right_of(fn, a):
    return lambda u: fn(u) if u >= a else 0


def U(x, lo, hi):
    return (x - lo) / (hi - lo)


# ---------------------------------------------------------------- numbers (asserted against MIT17 / MPS08G)
def binom_row(t):
    return [math.comb(10, k) * t ** k * (1 - t) ** (10 - k) for k in range(11)]


ROWS = {t: binom_row(t) for t in (.5, .6, .7)}
REJ, REJ05 = {0, 1, 2, 8, 9, 10}, {0, 1, 9, 10}
alpha = sum(ROWS[.5][k] for k in REJ)
pow6, pow7 = (sum(ROWS[t][k] for k in REJ) for t in (.6, .7))
alpha05, pow7_05 = sum(ROWS[.5][k] for k in REJ05), sum(ROWS[.7][k] for k in REJ05)
assert round(alpha, 2) == .11 and round(pow6, 3) == .180 and round(pow7, 3) == .384  # MIT17 §4.3

Z05, Z04, Z10 = 1.645, 1.751, 1.2816          # read from the Φ table below
C10 = 100 + Z05 * 15                          # MIT17 Ex. 10: 124.7
C9 = 100 + Z05 * 5                            # IQ, 9 students: x̄ ~ N(100, 5²)
POW110 = 1 - Phi((C9 - 110) / 5)
N105 = ((Z05 + Z10) * 15 / 5) ** 2            # n for power 0.9 at μ = 105
SD3 = 5 / math.sqrt(3)
RADAR_C = 40 + Z04 * SD3
RADAR_POW = 1 - Phi((RADAR_C - 45) / SD3)
RADAR_N = ((Z04 + Z10) * 5 / 5) ** 2
assert round(C10, 1) == 124.7 and abs(POW110 - .639) < .002 and math.ceil(N105) == 78
assert abs(RADAR_C - 45.054) < .002 and abs(RADAR_POW - .493) < .002 and math.ceil(RADAR_N) == 10  # MPS08G


def binom_table(rows, rej, caption):
    """Probability table of x heads in 10 tosses, one row per θ; rejection-region cells shaded."""
    shade = ' style="background:var(--callout-bg);font-weight:600"'
    head = "".join(f'<th class="num"{shade if k in rej else ""}>{k}</th>' for k in range(11))
    body = "".join(f'<tr><th>\\(p(x \\mid \\theta = {t:g})\\)</th>'
                   + "".join(f'<td class="num"{shade if k in rej else ""}>{ROWS[t][k]:.3f}</td>' for k in range(11)) + "</tr>"
                   for t in rows)
    return (f'<table style="table-layout:fixed"><tr><th>\\(x\\)</th>{head}</tr>{body}</table>'
            f'<p style="font-size:.85rem;color:var(--muted)">{caption}</p>')


def phi_table(zs):
    cells = "".join(f'<tr><td class="num">{z:.2f}</td><td class="num">{Phi(z):.4f}</td></tr>' for z in zs)
    return f'<table style="width:auto"><tr><th>\\(z\\)</th><th>\\(\\Phi(z) = P(Z \\le z)\\)</th></tr>{cells}</table>'


# ---------------------------------------------------------------- recordação
recordacao = rf"""
<p>Esta lição usa três coisas das lições anteriores: a taxa-base (<a href="{LESSON1}">0001</a>), a área à direita de um ponto
(<a href="{LESSON6}">0006</a>) e a likelihood da Binomial (<a href="{LESSON0}">0000</a>). Tente sem voltar lá.</p>
""" + check(
    r"""<p>1. Numa cidade, 1% das pessoas tem uma doença. O exame dá positivo em 90% dos doentes e em 4% dos sãos. Uma pessoa testou
positivo. \(P(\text{são} \mid \text{positivo})\) = """ + num("0.0396/0.0486", "0.003", "4rem") + r"""</p>
<p>2. Uma pdf é \(f(x) = 2x\) em \([0, 1]\). O ponto \(c\) que deixa área 0.19 à direita é \(c\) = """ + num("0.9", "0.002", "4rem") + r"""</p>
<p>3. Uma moeda com \(\theta = 0.5\) (probabilidade de cara) é lançada 10 vezes. A probabilidade de sair exatamente 6 caras é """
    + num("210/1024", "0.002", "4rem") + "</p>",
    "Isso. 1: numeradores 0.99 × 0.04 = 0.0396 (são) e 0.01 × 0.9 = 0.009 (doente); 0.0396/(0.0396 + 0.009) ≈ 0.815. "
    "2: a área à esquerda de c é ∫₀ᶜ 2x dx = c², e ela vale 1 − 0.19 = 0.81, então c = 0.9. "
    "3: C(10, 6) · 0.5⁶ · 0.5⁴ = 210/1024 ≈ 0.205.")

# ---------------------------------------------------------------- frequentista
frequentista = r"""
<p>Até aqui, toda conta começou por uma prior. Na moeda, no dado tirado da gaveta, na doença com taxa-base conhecida, a prior vinha no enunciado.
E quando duas pessoas discordam da prior, ou ninguém sabe qual usar? O MIT17 abre com essa pergunta:</p>
""" + quote(r"""<p>When the prior is known exactly, all statisticians will use Bayes’ formula. […] In practice we saw that there is usually no universally
accepted prior – different people will have different a priori beliefs – but we would still like to make useful inferences from data.</p>""",
            src("<i>The Frequentist School of Statistics</i>, §2.1")) + r"""
<p>Daí saem dois caminhos. Os dois partem da fórmula de Bayes e da likelihood \(P(D \mid H)\):</p>
<div class="flow">
<div class="box"><small>caminho bayesiano</small>sem prior conhecida, escolhe uma prior com a melhor informação disponível e calcula a posterior</div>
<div class="box plain"><small>caminho frequentista</small>sem prior conhecida, tira conclusões só da likelihood, sem prior e sem posterior</div>
</div>
<p>A diferença vem do que cada escola aceita chamar de probabilidade. Para o <b>frequentista</b>, probabilidade é frequência de longo prazo
de um experimento que se repete: "a moeda tem probabilidade 1/2 de cara" quer dizer que a fração de caras vai para 1/2 quando o número de
lançamentos cresce. Um parâmetro como o \(\theta\) da moeda tem um valor fixo, mesmo que desconhecido, e não se repete; por isso o frequentista
não põe pdf nele.</p>
""" + quote(r"""<p>In short, Bayesians put probability distributions on everything (hypotheses and data), while frequentists put probability distributions
on (random, repeatable, experimental) data given a hypothesis. For the frequentist when dealing with data from an unknown distribution only the
likelihood has meaning. The prior and posterior do not.</p>""", src("<i>The Frequentist School of Statistics</i>, §2.2")) + mc(
    r"Um atraso \(x\) segue uma Uniforme\((0, \theta)\), com \(\theta\) desconhecido. Jon escolhe uma prior \(f(\theta)\), calcula a likelihood "
    r"\(\phi(x \mid \theta)\) e a posterior \(f(\theta \mid x)\). Qual dessas contas um frequentista aceita?",
    [("só a likelihood, a probabilidade do dado dado θ", True,
      "Isso. É a resposta do MIT17 (problema de aula, concept question 1): a likelihood é a probabilidade de um dado que se repete, com θ fixado. "
      "Prior e posterior são distribuições sobre valores de θ, e o frequentista não as aceita."),
     ("a prior e a posterior, que descrevem o θ", False,
      "É o contrário. Prior e posterior são probabilidades sobre θ, um valor fixo; o frequentista só aceita probabilidade de dado que se repete."),
     ("as três, porque todas saem da fórmula de Bayes", False,
      "Todo mundo aceita a fórmula de Bayes quando a prior é conhecida. Aqui ela é uma crença do Jon, e o frequentista fica só com a likelihood.")]) + r"""
<h3>Estatística</h3>
<p>Sem posterior, as conclusões do frequentista saem de números calculados a partir dos dados:</p>
""" + quote(r"""<p>Statistic. A statistic is anything that can be computed from data and known values. […] But it does not include anything that requires
we know the true value of a model parameter with unknown value.</p>""", src("<i>The Frequentist School of Statistics</i>, §3")) + r"""
<p>Uma <b>estatística</b> é uma conta feita só com os dados e com valores conhecidos. A média \(\bar x = \frac{x_1 + \cdots + x_n}{n}\) dos
dados \(x_1, \dots, x_n\) é uma estatística. A distância \(\bar x - \mu\) até a média verdadeira \(\mu\), desconhecida, não é. Como os dados são
aleatórios, uma estatística também é uma variável aleatória, com distribuição própria:</p>
""" + quote(r"""<p>It’s important to remember that a statistic is itself a random variable since it is computed from random data. For example, if data is
drawn from \(N(\mu, \sigma^2)\) then the mean of \(n\) data points follows the distribution \(N(\mu, \sigma^2/n)\).</p>""",
            src("<i>The Frequentist School of Statistics</i>, §3")) + r"""
<p>Por exemplo, se o QI de uma pessoa segue \(N(100, 15^2)\), a média do QI de 9 pessoas segue \(N(100, 15^2/9) = N(100, 5^2)\): a mesma média,
com desvio padrão 3 vezes menor (\(\sqrt{9} = 3\)).</p>
"""

# ---------------------------------------------------------------- ingredientes
ingredientes = r"""
<p>Sem prior, como decidir se uma moeda é honesta? Se ela der 85 caras em 100 lançamentos, quase todo mundo desconfia; com 52 caras, ninguém;
com 60, a resposta não é clara. O <b>teste de hipóteses</b> (NHST, <i>null hypothesis significance testing</i>) transforma essa intuição em
conta. A ideia: supor que nada de especial acontece e ver se os dados ficariam muito longe do esperado nesse caso. Os ingredientes:</p>
""" + quote(r"""<ul>
<li>\(H_0\): the null hypothesis. This is the default assumption for the model generating the data.</li>
<li>\(H_A\): the alternative hypothesis. If we reject the null hypothesis we accept this alternative as the best explanation for the data.</li>
<li>\(X\): the test statistic. We compute this from the data. It is a random variable, because it is computed from random data.</li>
<li>Null distribution: the probability distribution of \(X\) assuming \(H_0\).</li>
<li>Rejection region: if \(X\) is in the rejection region we reject \(H_0\) in favor of \(H_A\).</li>
<li>Non-rejection region: the complement to the rejection region. If \(X\) is in this region we do not reject \(H_0\). Note that we say ‘do not
reject’ rather than ‘accept’ because usually the best we can say is that the data does not support rejecting \(H_0\).</li>
</ul>""", src("<i>Null Hypothesis Significance Testing I</i>, §3.1")) + r"""
<p>Em português: a <b>hipótese nula</b> \(H_0\) é o padrão, "nada de especial"; a <b>hipótese alternativa</b> \(H_A\) (a P2 escreve \(H_1\)) é
o que se conclui se \(H_0\) cair. A <b>estatística de teste</b> \(X\) é a conta feita com os dados. A <b>distribuição nula</b> é a
distribuição de \(X\) supondo \(H_0\). Se \(X\) cair na <b>região de rejeição</b>, rejeita-se \(H_0\); se cair fora, na região de não rejeição,
diz-se que os dados não sustentam rejeitar \(H_0\). Nunca se diz que \(H_0\) foi provada.</p>
<h3>Exemplo: a moeda lançada 10 vezes</h3>
<p>O exemplo do MIT17 (§4, Example 3): para testar se uma moeda é honesta, ela é lançada 10 vezes. \(\theta\) é a probabilidade de cara.</p>
<ol class="spaced">
<li>Hipótese nula: a moeda é honesta, \(H_0: \theta = 0.5\).</li>
<li>Hipótese alternativa: a moeda não é honesta, \(H_A: \theta \ne 0.5\).</li>
<li>Estatística de teste: \(X\) = número de caras nos 10 lançamentos.</li>
<li>Distribuição nula: supondo \(H_0\), \(X\) é Binomial(10, 0.5). Cada \(p(x \mid \theta = 0.5) = \binom{10}{x}\,0.5^{10}\) é a likelihood de
\(\theta = 0.5\) para o dado \(x\), a mesma conta do item 3 da recordação.</li>
<li>Região de rejeição: com \(H_0\), espera-se umas 5 caras. Rejeita-se \(H_0\) se o número de caras ficar longe de 5: \(\{0, 1, 2, 8, 9, 10\}\).</li>
</ol>
""" + binom_table([.5], REJ, "Distribuição nula Binomial(10, 0.5). Casas pintadas: a região de rejeição {0, 1, 2, 8, 9, 10}.") + r"""
<p>Se a moeda for honesta, qual é a chance de o teste dizer, por engano, que ela não é? É a chance de \(X\) cair na região de rejeição com
\(H_0\) verdadeira: a soma das casas pintadas.</p>
$$P(\text{rejeitar } H_0 \mid H_0) = 0.001 + 0.010 + 0.044 + 0.044 + 0.010 + 0.001 = 0.110$$
<p>Se der 3 caras, \(X\) fica fora da região de rejeição, e a conclusão é "os dados não sustentam rejeitar \(H_0\)". Mesmo com 5 caras, o
teste não prova que a moeda é honesta.</p>
<h3>Hipótese simples e composta</h3>
""" + quote(r"""<p>Definition: simple hypothesis: A simple hypothesis is one for which we can specify its distribution completely. A typical simple
hypothesis is that a parameter of interest takes a specific value.</p>
<p>Definition: composite hypotheses: If its distribution cannot be fully specified, we say that the hypothesis is composite. A typical composite
hypothesis is that a parameter of interest lies in a range of values.</p>""", src("<i>Null Hypothesis Significance Testing I</i>, §4.1")) + r"""
<p>Uma hipótese é <b>simples</b> quando fixa a distribuição inteira (em geral, um valor só para o parâmetro) e <b>composta</b> quando deixa
uma faixa de valores. Na moeda, \(H_0: \theta = 0.5\) dá a Binomial(10, 0.5) inteira: é simples. \(H_A: \theta \ne 0.5\) junta 0.51, 0.7,
0.99 e todos os outros valores: é composta.</p>
""" + mc(
    r"Para testar se uma pessoa adivinha o naipe de cartas acima do acaso, \(T\) conta os acertos em 100 cartas. "
    r"\(H_0\): \(T\) é Binomial(100, 0.25). \(H_A\): \(T\) é Binomial(100, \(p\)) com \(p > 0.25\). Como são as hipóteses?",
    [(r"\(H_0\) é simples e \(H_A\) é composta", True,
      "Isso (MIT17, §4.1, Example 6): H₀ fixa p = 0.25, e H_A deixa p em toda a faixa acima de 0.25."),
     (r"\(H_0\) é composta e \(H_A\) é simples", False,
      "Está trocado. H₀ fixa um valor só, p = 0.25, então é simples; H_A deixa uma faixa, p > 0.25, então é composta."),
     ("as duas hipóteses são simples", False,
      "Dar a família não basta: H_A não diz qual p, então a Binomial dela não fica inteira. Ela é composta.")])

# ---------------------------------------------------------------- erros
erros = r"""
<p>O teste pode errar de dois jeitos: rejeitar \(H_0\) quando ela é verdadeira, ou não rejeitar quando ela é falsa.</p>
<table>
<tr><th>decisão</th><th>\(H_0\) verdadeira</th><th>\(H_A\) verdadeira</th></tr>
<tr><td>rejeitar \(H_0\)</td><td>erro tipo I</td><td>decisão certa</td></tr>
<tr><td>não rejeitar \(H_0\)</td><td>decisão certa</td><td>erro tipo II</td></tr>
</table>
<p>As duas probabilidades que medem a qualidade do teste:</p>
""" + quote(r"""<p>Significance level \(= P(\text{reject } H_0 \mid H_0)\) = probability we incorrectly reject \(H_0\) = \(P\)(type I error).</p>
<p>Power = probability we correctly reject \(H_0\) = \(P(\text{reject } H_0 \mid H_A)\) = 1 − \(P\)(type II error).</p>""",
            src("<i>Null Hypothesis Significance Testing I</i>, §4.3")) + r"""
<p>O <b>nível de significância</b> \(\alpha\) é a probabilidade do erro tipo I. A <b>potência</b> (<i>power</i>) é a probabilidade de
rejeitar \(H_0\) quando \(H_A\) é verdadeira. Com \(\beta = P(\text{erro tipo II})\), como escreve a P2, a potência é \(1 - \beta\).
Um bom teste tem \(\alpha\) perto de 0 e potência perto de 1. Na moeda, \(\alpha = 0.11\), a conta da seção anterior.</p>
<p>Repare na ordem da condicional: \(\alpha = P(\text{rejeitar} \mid H_0)\), e não \(P(H_0 \mid \text{rejeitou})\). No exame do item 1 da
recordação, \(P(\text{positivo} \mid \text{são}) = 0.04\), mas \(P(\text{são} \mid \text{positivo}) \approx 0.815\). A segunda precisou da
taxa-base, que é uma prior, e o frequentista não tem prior.</p>
<h3>Potência com \(H_A\) composta</h3>
<p>Na moeda, \(H_A: \theta \ne 0.5\) é composta, então a potência muda com o \(\theta\) verdadeiro. Para cada \(\theta\), a potência é a
probabilidade de \(X\) cair na região de rejeição: a soma das casas pintadas na linha daquele \(\theta\).</p>
""" + binom_table([.5, .6, .7], REJ, "Cada linha é a Binomial(10, θ). Casas pintadas: a região de rejeição {0, 1, 2, 8, 9, 10}, a mesma nas três linhas.") + r"""
<p>Com \(\theta = 0.6\):</p>
$$\text{potência}(0.6) = P(X \in \{0, 1, 2, 8, 9, 10\} \mid \theta = 0.6) = 0.000 + 0.002 + 0.011 + 0.121 + 0.040 + 0.006 = 0.180$$
""" + check(
    r"""<p>Potência com \(\theta = 0.7\): """ + num(f"{pow7:.4f}", "0.002", "4rem") + "</p>",
    f"Isso: 0.000 + 0.000 + 0.001 + 0.233 + 0.121 + 0.028 ≈ 0.383 com as casas arredondadas; sem arredondar, {pow7:.3f} (o valor do MIT17). "
    "A potência é maior com θ = 0.7: uma moeda mais longe de 0.5 é mais fácil de pegar.") + r"""
<p>E se \(H_0\) também for composta, como \(\theta \le 0.5\)? Aí o erro tipo I depende de qual valor de \(H_0\) é o verdadeiro, e o MIT17
fica com o pior caso:</p>
""" + quote(r"""<p>Significance for a composite null hypothesis. If \(H_0\) is composite then P(type I error) depends on which member of \(H_0\) is true.
In this case the significance level is defined as the maximum of these probabilities.</p>""",
            src("<i>Null Hypothesis Significance Testing I</i>, §5")) + r"""
<h3>Escolher \(\alpha\) e a região de rejeição</h3>
<p>Na prática, a ordem é outra: primeiro se escolhe \(\alpha\), e a região de rejeição sai dele. Valores comuns de \(\alpha\) são 0.1, 0.05 e 0.01.
A região de rejeição fica nas pontas da distribuição nula, e a probabilidade dela, supondo \(H_0\), não pode passar de \(\alpha\).</p>
<p>Antes, decida o lado. \(H_A: \theta \ne 0.5\) é <b>bilateral</b>: a moeda pode puxar para cara ou para coroa, então a região de rejeição
fica nas duas pontas. Se só interessa "puxa para cara", \(H_A: \theta > 0.5\) é <b>unilateral</b>, e a região fica só na ponta direita,
porque poucas caras não falam a favor de \(H_A\).</p>
<p>Com \(\alpha = 0.05\) e o teste bilateral: tirando as casas das pontas para dentro, \(\{0, 10\}\) tem 0.002 e \(\{0, 1, 9, 10\}\) tem 0.022.
Acrescentar 2 e 8 daria \(0.022 + 0.044 + 0.044 = 0.110\), acima de 0.05. A região é \(\{0, 1, 9, 10\}\).</p>
""" + check(
    r"""<p>Teste unilateral \(H_A: \theta > 0.5\) com \(\alpha = 0.05\). A região de rejeição é \(\{\)""" + num("9", "0.01", "2.6rem")
    + r""", \(10\}\), e a probabilidade dela com \(H_0\) é """ + num("0.011", "0.002", "4rem") + "</p>",
    "Isso: {10} tem 0.001, {9, 10} tem 0.011, e {8, 9, 10} teria 0.055, acima de 0.05.") + r"""
<p>Diminuir \(\alpha\) encolhe a região de rejeição, e isso também derruba a potência, porque a potência é a probabilidade da mesma região
com \(H_A\). Compare as duas regiões bilaterais na linha \(\theta = 0.7\) da tabela:</p>
""" + check(
    r"""<p>Com a região \(\{0, 1, 9, 10\}\): \(\alpha\) = """ + num(f"{alpha05:.4f}", "0.002", "4rem")
    + r""" e a potência com \(\theta = 0.7\) é """ + num(f"{pow7_05:.4f}", "0.002", "4rem") + "</p>",
    f"Isso: α = 0.001 + 0.010 + 0.010 + 0.001 ≈ 0.02 e potência = 0.000 + 0.000 + 0.121 + 0.028 = 0.149. "
    f"Com a região maior, era α = 0.11 e potência {pow7:.3f}: α menor, potência menor.")

# ---------------------------------------------------------------- revisão da Normal
lo_q, hi_q = 40, 160
nq = normal(100, 15, lo_q, hi_q)
revisao = r"""
<p>Os testes com dados contínuos usam a Normal da P1. Uma variável \(X\) com distribuição \(N(\mu, \sigma^2)\) tem média \(\mu\) e desvio padrão
\(\sigma\). <b>Padronizar</b> é medir a distância até a média em desvios padrão:</p>
$$Z = \frac{X - \mu}{\sigma} \sim N(0, 1)$$
<p>\(Z\) é a Normal padrão, e a tabela da prova dá \(\Phi(z) = P(Z \le z)\), a área à esquerda de \(z\). A área à direita é o resto,
\(1 - \Phi(z)\). Algumas linhas da tabela:</p>
""" + phi_table([0.02, 0.35, 0.36, 1.00, 1.28, 1.29, 1.64, 1.65, 1.75, 1.76, 1.96, 2.00, 2.40]) + r"""
<p>Por exemplo, com \(X \sim N(100, 15^2)\), a probabilidade de \(X > 130\):</p>
$$\begin{aligned}
z &= \frac{130 - 100}{15} = 2 \\
P(X > 130) &= 1 - \Phi(2) = 1 - 0.9772 = 0.0228
\end{aligned}$$
<p>A tabela também se lê ao contrário: para achar o ponto com área 0.05 à direita, procure 0.95 dentro da coluna de \(\Phi\). Ele fica entre
\(\Phi(1.64) = 0.9495\) e \(\Phi(1.65) = 0.9505\), no meio, então \(z = 1.645\). É o quantil \(q_{0.95}\) da Normal padrão
(<a href="{LESSON6}">lição 0006</a>: \(q_s\) deixa \(s\) à esquerda).</p>
""".replace("{LESSON6}", LESSON6) + check(
    r"""<p>Com \(X \sim N(100, 15^2)\): \(P(X \le 115)\) = """ + num(f"{Phi(1):.4f}", "0.002", "4rem")
    + r"""</p><p>O \(z\) com área 0.1 à direita: \(z\) = """ + num("1.2816", "0.006", "4rem") + "</p>",
    "Isso. (115 − 100)/15 = 1, e Φ(1) = 0.8413. Para área 0.1 à direita, Φ(z) = 0.9: entre Φ(1.28) = 0.8997 e Φ(1.29) = 0.9015, "
    "mais perto de 1.28; interpolando, z ≈ 1.2816.")

# ---------------------------------------------------------------- valor crítico e potência
lo9, hi9 = 75, 135
n0, nA = normal(100, 5, lo9, hi9), normal(110, 5, lo9, hi9)
critico = r"""
<p>Com dados contínuos, a região de rejeição é uma ponta da distribuição nula, e o ponto onde ela começa tem nome:</p>
""" + quote(r"""<p>Critical values are like quantiles except they refer to the probability to the right of the value instead of the left.</p>""",
            src("<i>Null Hypothesis Significance Testing I</i>, §6")) + r"""
<p>O <b>valor crítico</b> \(x_\alpha\) deixa a probabilidade \(\alpha\) à direita. Ele é o quantil \(q_{1-\alpha}\): na Normal padrão,
\(z_{0.05} = q_{0.95} = 1.645\). O exemplo do MIT17:</p>
""" + quote(r"""<p>Example 10. Critical values and rejection regions. Suppose our test statistic \(x\) has null distribution \(N(100, 15^2)\), i.e.
\(\phi(x \mid H_0) \sim N(100, 15^2)\). Suppose also that our rejection region is right-sided and we have a significance level of 0.05. Find the
critical value and sketch the null distribution and rejection region.</p>""", src("<i>Null Hypothesis Significance Testing I</i>, §6")) + rf"""
<p>A região de rejeição é a ponta direita com área 0.05. O ponto onde ela começa está 1.645 desvios padrão acima da média (o \(z\) com
área 0.05 à direita, da revisão). Desfazendo a padronização:</p>
$$x_{{0.05}} = \mu + z_{{0.05}}\,\sigma = 100 + 1.645 \cdot 15 = {C10:.1f}$$
<p>\(\mu = 100\) e \(\sigma = 15\) são a média e o desvio padrão da distribuição nula. Rejeita-se \(H_0\) se \(x \ge {C10:.1f}\).</p>
""" + pdf_plot(
    [("N(100, 15²)", nq, ACC, False, .62)],
    "Distribuição nula N(100, 15²). A área pintada, à direita de 124.7, é α = 0.05: a região de rejeição.",
    xlabel="x", xlo=lo_q, xscale=hi_q - lo_q,
    fills=[(right_of(nq, U(C10, lo_q, hi_q)), ACC, "α = 0.05", U(148, lo_q, hi_q), .0025)],
    marks=[(U(C10, lo_q, hi_q), nq, f"x₀.₀₅ = {C10:.1f}", ACC, "ur")]) + check(
    r"""<p>Mesma distribuição nula, agora com a região de rejeição à esquerda e \(\alpha = 0.05\). Rejeita-se \(H_0\) se \(x \le\) """
    + num(f"{200 - C10:.2f}", "0.1", "4rem") + "</p>",
    f"Isso: a ponta esquerda com área 0.05 começa 1.645 desvios abaixo da média, 100 − 1.645 · 15 = {200 - C10:.1f} (MIT17, Example 11).") + rf"""
<h3>Potência de um teste com a Normal</h3>
<p>O exemplo do QI do MIT17 (§7.1, Example 13): o QI da população segue \(N(100, 15^2)\), e a suspeita é que alunos do MIT têm QI acima da média.
\(H_0\): o QI dos alunos segue \(N(100, 15^2)\), como a população. \(H_A\): a média do QI dos alunos é maior que 100 (unilateral à direita).
A estatística de teste é a média \(\bar x\) do QI de 9 alunos. Com \(H_0\), \(\bar x \sim N(100, 15^2/9) = N(100, 5^2)\) (a média de
\(n\) dados, da <a href="#frequentista">seção da estatística</a>).</p>
<p>Com \(\alpha = 0.05\), o valor crítico é \(100 + 1.645 \cdot 5 = {C9:.2f}\): rejeita-se \(H_0\) se \(\bar x \ge {C9:.2f}\).</p>
<p>Qual é a potência se a média verdadeira dos alunos for 110? É a probabilidade de \(\bar x\) cair na mesma região, \(\bar x \ge {C9:.2f}\),
agora com \(\bar x \sim N(110, 5^2)\). Padronize com a média de \(H_A\):</p>
$$\begin{{aligned}}
z &= \frac{{{C9:.2f} - 110}}{{5}} = {(C9 - 110) / 5:.3f} \\
\text{{potência}} &= P(Z \ge {(C9 - 110) / 5:.3f}) = 1 - \Phi({(C9 - 110) / 5:.3f}) = \Phi({(110 - C9) / 5:.3f}) \approx {POW110:.3f}
\end{{aligned}}$$
<p>(\(1 - \Phi(-a) = \Phi(a)\), porque a Normal padrão é simétrica em torno de 0.) O valor de \(\Phi(0.355)\) fica entre as linhas 0.35 e
0.36 da tabela da revisão.</p>
""" + pdf_plot(
    [("H₀: N(100, 5²)", n0, ACC, False, .02, .075), ("H_A: N(110, 5²)", nA, MUT, True, .74, .075)],
    f"A mesma região de rejeição, x̄ ≥ {C9:.1f}, lida nas duas curvas: a área pintada sob H₀ é α = 0.05; a área hachurada sob H_A é a potência, {POW110:.2f}.",
    xlabel="x̄", xlo=lo9, xscale=hi9 - lo9, ymax=.095,
    fills=[(right_of(n0, U(C9, lo9, hi9)), ACC, "α", U(112.5, lo9, hi9), .006),
           (right_of(nA, U(C9, lo9, hi9)), MUT, f"potência {POW110:.2f}", U(123, lo9, hi9), .035, "hatch")],
    marks=[(U(C9, lo9, hi9), lambda u: .088, f"{C9:.1f}", ACC)]) + rf"""
<p>Quanto mais as duas curvas se sobrepõem, menor a potência, porque menos área de \(H_A\) fica na região de rejeição. Para separar as curvas sem mudar as médias, é preciso estreitá-las, e isso se faz com mais dados:</p>
""" + quote(r"""<p>Typically we can increase the power of a test by increasing the amount of data and thereby decreasing the variance of the null and
alternative distributions. In experimental design it is important to determine ahead of time the number of trials or subjects needed to achieve
a desired power.</p>""", src("<i>Null Hypothesis Significance Testing I</i>, §4.4.2")) + rf"""
<h3>Quantos dados para uma potência desejada?</h3>
<p>Mesmo teste do QI, \(\alpha = 0.05\), mas agora com \(H_A\) em 105, mais perto de 100. Quantos alunos são precisos para a potência chegar a 0.9?</p>
<p>Com \(n\) alunos, \(\bar x \sim N(\mu, 15^2/n)\): o desvio padrão é \(15/\sqrt{{n}}\). O valor crítico e a potência dependem de \(n\):</p>
$$\begin{{aligned}}
c_n &= 100 + 1.645 \cdot \frac{{15}}{{\sqrt{{n}}}} \\
\text{{potência}}(n) &= P(\bar x \ge c_n \mid \mu = 105) = 1 - \Phi\!\left(\frac{{c_n - 105}}{{15/\sqrt{{n}}}}\right)
\end{{aligned}}$$
<p>A primeira forma de achar \(n\) é tentar valores:</p>
<table>
<tr><th>\(n\)</th><th class="num">\(15/\sqrt{{n}}\)</th><th class="num">\(c_n\)</th><th class="num">\(\frac{{c_n - 105}}{{15/\sqrt{{n}}}}\)</th><th class="num">potência</th></tr>
""" + "".join(
    f'<tr><td class="num">{n}</td><td class="num">{15 / math.sqrt(n):.3f}</td><td class="num">{100 + Z05 * 15 / math.sqrt(n):.3f}</td>'
    f'<td class="num">{(100 + Z05 * 15 / math.sqrt(n) - 105) / (15 / math.sqrt(n)):.3f}</td>'
    f'<td class="num">{1 - Phi((100 + Z05 * 15 / math.sqrt(n) - 105) / (15 / math.sqrt(n))):.3f}</td></tr>'
    for n in (9, 49, 77, 78)) + rf"""
</table>
<p>Com 77 alunos a potência fica um pouco abaixo de 0.9, e com 78 passa. A segunda forma é resolver a conta. A potência é 0.9 quando o
\(z\) dentro do \(\Phi\) é o ponto com área 0.9 à direita, \(z_{{0.9}} = -1.2816\) (o simétrico do \(z_{{0.1}} = 1.2816\) da revisão):</p>
$$\begin{{aligned}}
\frac{{c_n - 105}}{{15/\sqrt{{n}}}} &= -1.2816 \\
\frac{{100 - 105}}{{15/\sqrt{{n}}}} + 1.645 &= -1.2816 &&\text{{substituindo }} c_n \\
-\frac{{5\sqrt{{n}}}}{{15}} + 1.645 &= -1.2816 \\
\frac{{5\sqrt{{n}}}}{{15}} &= 1.645 + 1.2816 = 2.9266 \\
\sqrt{{n}} &= 8.780, \qquad n = 77.08
\end{{aligned}}$$
<p>Como \(n\) é inteiro e a potência tem que chegar a 0.9, arredonde para cima: \(n = 78\), como na tabela.</p>
<div class="callout"><p>Atalho da conta acima, para um teste unilateral à direita com a Normal: com \(z_\alpha\) o valor crítico de \(H_0\), \(z_{{0.9}}\) o ponto
com área 0.9 à direita (para outra potência, troque o 0.9), \(\sigma\) o desvio padrão de um dado e \(\mu_A - \mu_0\) a distância entre as médias de \(H_A\) e
\(H_0\),</p>
$$n = \left(\frac{{(z_\alpha - z_{{0.9}})\,\sigma}}{{\mu_A - \mu_0}}\right)^2 = \left(\frac{{(1.645 + 1.2816) \cdot 15}}{{5}}\right)^2 = 77.08$$
<p>É a mesma conta, resolvida com letras. Se esquecer, faça a conta.</p></div>
"""

# ---------------------------------------------------------------- p-valor
lz, hz = -4, 4
nz = normal(0, 1, lz, hz)
pvalor = r"""
<p>O valor crítico compara \(\bar x\) com uma fronteira. Outra forma de decidir, a mais usada na prática, mede quão extremo foi o dado:</p>
""" + quote(r"""<p>Definition. The \(p\)-value is the probability, assuming the null hypothesis, of seeing data at least as extreme as the experimental data.
What ‘at least as extreme’ means depends on the experimental design.</p>
<p>P-test. If the \(p\)-value is less than the significance level \(\alpha\) then we reject \(H_0\). Otherwise we do not reject \(H_0\).</p>""",
            src("<i>Null Hypothesis Significance Testing I</i>, §7")) + rf"""
<p>O <b>p-valor</b> é a probabilidade, supondo \(H_0\), de um dado pelo menos tão extremo quanto o observado. "Extremo" segue o lado do teste:
num teste unilateral à direita, com estatística observada \(x\), o p-valor é \(P(X \ge x \mid H_0)\), a área à direita de \(x\) na
distribuição nula.</p>
<p>No teste do QI, os 9 alunos tiveram média \(\bar x = 112\). Padronizando com \(H_0\) (média 100, desvio padrão \(15/\sqrt9 = 5\)):</p>
$$\begin{{aligned}}
z &= \frac{{112 - 100}}{{15/\sqrt{{9}}}} = \frac{{12}}{{5}} = 2.4 \\
p &= P(Z \ge 2.4) = 1 - \Phi(2.4) = 1 - 0.9918 = 0.0082
\end{{aligned}}$$
<p>Como \(p = 0.008 < \alpha = 0.05\), rejeita-se \(H_0\). O MIT17 escreve a conclusão assim:</p>
""" + quote(r"""<p>We reject the null hypothesis in favor of the alternative hypothesis that MIT students have higher IQs on average. We have done this at
significance level 0.05 with a \(p\)-value of 0.008.</p>""", src("<i>Null Hypothesis Significance Testing I</i>, §7.1")) + r"""
<p>Por que \(p < \alpha\) é o mesmo que cair na região de rejeição? A região de rejeição é a ponta à direita de \(z_{0.05} = 1.645\), com área
0.05. Se \(z = 2.4\) está dentro dela, a área à direita de 2.4 é um pedaço dessa ponta, então é menor que 0.05.</p>
""" + pdf_plot(
    [("N(0, 1)", nz, ACC, False, .6, .33)],
    "Distribuição nula de z. A área pintada, à direita de 1.645, é α = 0.05; a área hachurada, à direita de 2.4, é o p-valor 0.008, um pedaço da pintada.",
    xlabel="z", xlo=lz, xscale=hz - lz,
    fills=[(right_of(nz, U(Z05, lz, hz)), ACC, "α", U(1.0, lz, hz), .03),
           (right_of(nz, U(2.4, lz, hz)), MUT, "p", U(3.4, lz, hz), .045, "hatch")],
    marks=[(U(Z05, lz, hz), nz, "1.645", ACC, "ur"), (U(2.4, lz, hz), nz, "2.4", MUT, "ur")]) + check(
    r"""<p>Teste bilateral (problema de aula 2 do MIT17): \(H_0\): os dados seguem \(N(5, 10^2)\); \(H_A\): seguem \(N(\mu, 10^2)\) com
\(\mu \ne 5\). São 64 dados com média \(\bar x = 6.25\), e \(\alpha = 0.05\).</p>
<p>\(z\) = """ + num("1", "0.005", "4rem") + r"""</p>
<p>Região de rejeição: \(|z| \ge\) """ + num("1.96", "0.005", "4rem") + r"""</p>
<p>p-valor, as duas pontas: \(P(|Z| \ge |z|)\) = """ + num(f"{2 * (1 - Phi(1)):.4f}", "0.003", "4rem") + "</p>"
    + r"""<details><summary>Dica</summary><p>Bilateral: \(\alpha\) se divide em 0.025 em cada ponta, e o p-valor soma as duas pontas, as áreas
abaixo de \(-|z|\) e acima de \(|z|\).</p></details>""",
    "Isso: z = (6.25 − 5)/(10/√64) = 1.25/1.25 = 1. A ponta direita com 0.025 começa em z = 1.96 (Φ(1.96) = 0.975). "
    "p = 2(1 − Φ(1)) = 2 · 0.1587 = 0.317 > 0.05: z fora da região de rejeição e p > α dizem a mesma coisa, não rejeitar H₀.")

# ---------------------------------------------------------------- objetivo: L04 = MPS08 problema 3
lo_r, hi_r = 28, 56
nr = normal(40, SD3, lo_r, hi_r)
objetivo = quote(r"""<p>Problem 3. (25: 10,10,5 pts.) z-test. Suppose three radar guns are set up along a stretch of road to catch people driving over the speed limit of 40 miles
per hour. Each radar gun is known to have a normal measurement error modeled on \(N(0, 5^2)\). For a passing car, let \(\bar x\) be the average of
the three readings. Our default assumption for a car is that it is not speeding.</p>
<p>(a) Describe the above story in the context of NHST. Are the most natural null and alternative hypotheses simple or composite?</p>
<p>(b) The police would like to set a threshold on \(\bar x\) for issuing tickets so that no more than 4% of law abiding, non-speeders are
mistakenly given tickets. You should assume this means that they set the threshold conservatively, so that no more 4% of drivers going exactly
40 mph get a ticket.</p>
<p>(i) Use the NHST description in part (a) to help determine what threshold should they set.</p>
<p>(ii) Sketch a graph illustrating your reasoning in part (i).</p>
<p>(iii) What is the probability that a person getting a ticket was not speeding?</p>
<p>(iv) Suppose word gets out about the speed trap and no one speeds along it anymore. What percentage of tickets are given in error?</p>
<p>(c) What is the power of this test with the alternative hypothesis that the car is traveling at 45 miles per hour? How many cameras are needed
to achieve a power of 0.9 with \(\alpha = 0.04\)?</p>""", f'<a href="{MPS08}">MPS08</a>, problema 3 (L04)') + r"""
<p>Três radares medem a velocidade de um carro, com limite de 40 milhas por hora. Cada leitura é a velocidade verdadeira \(\mu\) mais um erro
\(N(0, 5^2)\), então cada leitura segue \(N(\mu, 5^2)\), e a média \(\bar x\) das três leituras é a estatística de teste.</p>
<h3>(a) As hipóteses</h3>
""" + mc(
    r"A suposição padrão é que o carro não está acima do limite. Quais são \(H_0\) e \(H_A\)?",
    [(r"\(H_0: \mu \le 40\), não corre; \(H_A: \mu > 40\), corre", True,
      "Isso. H₀ é o padrão, \"não está correndo\", e H_A é o que se conclui se H₀ cair. É a solução do MPS08G."),
     (r"\(H_0: \mu > 40\), corre; \(H_A: \mu \le 40\), não corre", False,
      "Está trocado. A hipótese nula é a suposição padrão do enunciado, \"not speeding\", ou seja, μ ≤ 40."),
     (r"\(H_0: \mu = 40\), no limite; \(H_A: \mu \ne 40\), fora", False,
      "Um carro a 30 não está correndo e cairia em H_A. Só interessa um lado, acima do limite: H₀: μ ≤ 40 e H_A: μ > 40.")]) + mc(
    r"\(H_0: \mu \le 40\) e \(H_A: \mu > 40\) são simples ou compostas?",
    [("as duas são compostas, porque deixam uma faixa", True,
      "Isso. Cada uma deixa uma faixa de valores para μ. O MPS08G acrescenta que as contas usam μ = 40, que é simples (item b)."),
     ("as duas são simples, porque fixam o limite 40", False,
      "40 é só a fronteira. H₀ deixa μ em toda a faixa até 40, então a distribuição de x̄ não fica fixada: é composta."),
     ("H₀ é simples e H_A é composta, como na moeda", False,
      "Na moeda, H₀ era θ = 0.5, um valor só. Aqui H₀ é μ ≤ 40, uma faixa, então também é composta.")]) + r"""
<h3>(b)(i) O limiar</h3>
<p>Multar quem não está correndo é rejeitar \(H_0\) com \(H_0\) verdadeira: um erro tipo I. Como \(H_0\) é composta, o nível de significância
é o maior erro tipo I entre os valores de \(H_0\) (a <a href="#erros">citação da seção dos erros</a>). O pior caso é o carro exatamente a 40: com a região de rejeição
à direita, quanto maior \(\mu\), maior a chance de \(\bar x\) passar do limiar, e o maior \(\mu\)
de \(H_0\) é 40. É o "exactly 40 mph" do enunciado.</p>
""" + check(
    r"""<p>Com \(\mu = 40\), \(\bar x\) das 3 leituras segue \(N(40, \sigma^2)\) com desvio padrão \(\sigma\) = """ + num(f"{SD3:.4f}", "0.005", "4rem")
    + r"""</p><p>O \(z\) com área 0.04 à direita: \(z_{0.04}\) = """ + num(f"{Z04}", "0.006", "4rem")
    + r"""</p><p>O limiar: multa se \(\bar x \ge\) """ + num(f"{RADAR_C:.3f}", "0.03", "4rem") + "</p>"
    + r"""<details><summary>Dica</summary><p>A média de \(n\) dados \(N(\mu, 5^2)\) tem desvio padrão \(5/\sqrt n\). Para \(z_{0.04}\), procure
\(\Phi(z) = 0.96\) na tabela da revisão. O limiar é \(40 + z_{0.04}\,\sigma\).</p></details>""",
    f"Isso: σ = 5/√3 ≈ 2.887; Φ(z) = 0.96 fica entre Φ(1.75) = 0.9599 e Φ(1.76) = 0.9608, z₀.₀₄ ≈ 1.751; "
    f"limiar = 40 + 1.751 · 2.887 ≈ 45.05. Confira no <a href='{MPS08G}'>MPS08G</a>: 45.054.") + r"""
<h3>(b)(ii) O esboço</h3>
""" + check(
    r"""<p>O esboço é a curva da distribuição nula N(40, """ + num("25/3", "0.02", "4rem") + r""") (a variância), com a área à
direita do limiar pintada. Essa área vale """ + num("0.04", "0.002", "4rem") + "</p>",
    "Isso: variância 5²/3 = 25/3 ≈ 8.33, e a área pintada é α = 0.04.") + pdf_plot(
    [("N(40, 5²/3)", nr, ACC, False, .5)],
    f"Distribuição nula de x̄ para um carro a 40. A área pintada, à direita de {RADAR_C:.2f}, é α = 0.04: os carros a 40 que recebem multa.",
    xlabel="x̄", xlo=lo_r, xscale=hi_r - lo_r,
    fills=[(right_of(nr, U(RADAR_C, lo_r, hi_r)), ACC, "α = 0.04", U(51, lo_r, hi_r), .02)],
    marks=[(U(RADAR_C, lo_r, hi_r), nr, f"{RADAR_C:.2f}", ACC, "ur")]) + r"""
<h3>(b)(iii) e (iv) Quem foi multado sem correr</h3>
""" + mc(
    r"Qual é a probabilidade de uma pessoa multada não estar correndo, \(P(\text{não corre} \mid \text{multa})\)?",
    [("não dá para saber sem a prior de quem corre", True,
      "Isso. O teste controla P(multa | não corre) ≤ 0.04. A pergunta inverte a condicional, e para isso a fórmula de Bayes precisa da "
      "fração de motoristas que correm, uma prior. O MPS08G: \"To find it out would require a prior probability that a random driver is speeding.\""),
     ("0.04, o nível de significância do teste", False,
      "0.04 é P(multa | não corre). A pergunta é a condicional ao contrário, P(não corre | multa), como no exame do item 1 da recordação."),
     ("0.96, o complemento do nível de significância", False,
      "0.96 é P(sem multa | não corre). A pergunta é P(não corre | multa), e ela depende de quantos motoristas correm, uma prior.")]) + check(
    r"""<p>Ninguém mais corre naquela estrada. A porcentagem de multas dadas por engano é """ + num("100", "0.5", "4rem") + " %</p>",
    "Isso: se ninguém corre, toda multa vai para quem não corre. É a prior \"ninguém corre\" levada ao extremo: P(não corre | multa) = 1.") + rf"""
<h3>(c) A potência e o número de radares</h3>
""" + check(
    r"""<p>Potência com \(H_A: \mu = 45\) e os 3 radares: """ + num(f"{RADAR_POW:.4f}", "0.006", "4rem")
    + r"""</p><p>Número de radares para potência 0.9 com \(\alpha = 0.04\): """ + num("10", "0.01", "3rem") + "</p>"
    + r"""<details><summary>Dica</summary><p>Potência: a probabilidade de \(\bar x \ge 45.05\) com \(\bar x \sim N(45, 5^2/3)\); padronize com a
média 45. Radares: refaça a conta do QI com \(z_{0.04}\) no lugar de 1.645, desvio de um dado 5 e distância entre as médias \(45 - 40\).</p></details>""",
    f"Isso. Potência: z = (45.054 − 45)/2.887 ≈ 0.019, e 1 − Φ(0.019) ≈ 1 − 0.508 = 0.492 (o MPS08G dá 0.493). "
    f"Radares: a mesma conta dá (45 − 40)/(5/√n) = 1.751 + 1.2816, e (45 − 40)/(5/√n) = √n, então √n = 3.032 e n = 9.19; arredondando para cima, n = 10. "
    f"Confira no <a href='{MPS08G}'>MPS08G</a>.") + r"""
<h3>P2-23.2 Q4.4 e Q4.5</h3>
""" + quote(r"""<p>4. A potência (\(power = (1-\beta)\)) do teste de hipótese aumenta com o decréscimo do nível de significância
(\(significance\ level = \alpha\)) do teste.</p>""", f'<a href="{P2}">P2-23.2</a>, questão 4.4', lang="pt-BR") + mc(
    "Verdadeira ou falsa? Qual é a justificativa?",
    [("Falsa: α menor encolhe a região, e a potência cai junto", True,
      "Isso. Na prova corrigida, Falsa está marcada como certa. A potência é a probabilidade da região de rejeição com H_A; diminuir α tira pedaços dessa região. "
      "Na moeda, α passou de 0.11 para 0.02 e a potência com θ = 0.7 caiu de 0.384 para 0.149."),
     ("Verdadeira: α menor erra menos, e o teste fica mais forte", False,
      "α menor erra menos com H₀ verdadeira, mas rejeita menos com H_A também. Na moeda, a potência caiu de 0.384 para 0.149."),
     ("Verdadeira: α e a potência somam 1 em qualquer teste", False,
      "Quem soma 1 com a potência é β, o erro tipo II. α e a potência são áreas da mesma região sob curvas diferentes, e andam juntas.")]) + quote(
    r"""<p>5. O p-valor de um teste é \(P[X > x \mid H_0]\), onde \(x\) é o valor calculado para estatística do teste e \(X\) é a v.a. que
representa a estatística do teste.</p>""", f'<a href="{P2}">P2-23.2</a>, questão 4.5', lang="pt-BR") + mc(
    "Verdadeira ou falsa? Qual é a justificativa?",
    [("Verdadeira: é a chance, com H₀, de um dado mais extremo", True,
      "Isso. Na prova corrigida, Verdadeira está marcada como certa: é a definição do MIT17 para um teste unilateral à direita, em que \"mais extremo\" é \"maior que x\". "
      "Num teste bilateral o p-valor somaria as duas pontas."),
     ("Falsa: o p-valor é a probabilidade de H₀ dado o dado", False,
      "Isso seria P(H₀ | dado), uma posterior, que o frequentista não calcula. O p-valor condiciona em H₀: P(X > x | H₀)."),
     ("Falsa: o p-valor é a probabilidade de errar o teste", False,
      "A probabilidade de erro tipo I é α, fixada antes dos dados. O p-valor depende do x observado: P(X > x | H₀).")])

# ---------------------------------------------------------------- receita
receita = r"""
<div class="callout"><p>Teste de hipóteses, passo a passo:</p>
<ol class="spaced">
<li>Hipóteses: \(H_0\) é o padrão, "nada de especial"; \(H_A\) é o que se quer mostrar. Uma faixa de valores é composta; um valor só é simples.</li>
<li>Lado: \(H_A\) com \(>\) ou \(<\) é unilateral, com a região de rejeição numa ponta; com \(\ne\), bilateral, com \(\alpha/2\) em cada ponta.</li>
<li>Distribuição nula: a da estatística supondo \(H_0\). A média de \(n\) dados \(N(\mu, \sigma^2)\) segue \(N(\mu, \sigma^2/n)\). Com \(H_0\) composta, use o valor da fronteira (o pior caso).</li>
<li>Região de rejeição: discreta, junte as casas das pontas enquanto a soma não passar de \(\alpha\); Normal à direita, comece no valor crítico \(\mu_0 + z_\alpha\,\sigma/\sqrt n\).</li>
<li>Decisão: rejeite \(H_0\) se a estatística cair na região, o mesmo que p-valor \(< \alpha\). Senão, "os dados não sustentam rejeitar \(H_0\)".</li>
<li>Potência: a probabilidade da mesma região com \(H_A\) (padronize com a média de \(H_A\)). \(n\) para uma potência: resolva potência\((n)\) = meta e arredonde para cima.</li>
</ol></div>
"""

# ---------------------------------------------------------------- fontes
fontes = rf"""
<p>O arquivo do <a href="{MIT17}">MIT17</a> tem duas notas, <i>The Frequentist School of Statistics</i> e <i>Null Hypothesis Significance
Testing I</i>, e os problemas de aula. Esta lição usou a escola frequentista e a estatística (§2 e §3 da primeira nota), os ingredientes, os
erros, o nível de significância e a potência (§3 a §5 da segunda, com a moeda do Example 3), os valores críticos (§6), o p-valor e o teste z
(§7) e dois problemas de aula (a concept question 1 e o problema 2). O que ficou de fora:</p>
<table>
<tr><th>trecho</th><th>faz falta na P2?</th><th>por que ficou de fora</th></tr>
<tr><td>§3: estatística de intervalo e de conjunto (como os dados que ainda podem ter dado um lançamento)</td><td>não</td><td>nenhuma lista cobra; a estatística pontual (\(\bar x\)) basta para os testes</td></tr>
<tr><td>§4.1, Examples 4 e 5: hipóteses com Normal e com Poisson</td><td>não</td><td>a mesma definição de simples e composta, com outras distribuições</td></tr>
<tr><td>§4.3 e §5: analogias (o julgamento, o chocolate, as impressões digitais)</td><td>não</td><td>ilustram α e a potência sem conta nova</td></tr>
<tr><td>§6, Example 12: valores críticos bilaterais de \(N(100, 15^2)\)</td><td>não</td><td>a mesma conta do problema de aula 2, feito na seção do p-valor</td></tr>
<tr><td>§8: χ² de aderência (bactérias no leite) e teste t de duas amostras</td><td>sim, mais adiante</td><td>o MIT17 só os mostra; as contas estão no MIT19 e caem na L04 (MEX2 20e) e na P2-23.2 Q3</td></tr>
<tr><td>Problemas de aula: "Is it a statistic", "Picture the significance" e "More coins" (C1 × C2)</td><td>não</td><td>bons treinos; "More coins" mostra que, trocando \(H_0\) e \(H_A\), nenhuma das duas moedas é rejeitada</td></tr>
</table>
<div class="callout">Se ficou alguma dúvida, pergunte ao seu professor, que é o agente nesta conversa. Vale um passo da conta, um termo ou "por que isso funciona?".</div>
<p style="font-size:.8rem;color:var(--muted)">As citações em inglês são de J. Orloff e J. Bloom, <i>18.05 Introduction to Probability and Statistics</i>,
Spring 2022, MIT OpenCourseWare, licença CC BY-NC-SA 4.0, e da prova da Profª Rosa Leão (COE241). Trechos omitidos aparecem como […]. As tabelas
da moeda foram refeitas com as mesmas contas do MIT17, e os valores de \(\Phi\) saem da Normal padrão com 4 casas, como na tabela da prova.</p>
"""

SPEC = {
    "title": "0007 · Testes de hipóteses (NHST)",
    "subtitle": "Lição 0007 · COE241 P2 · MIT17 · escola frequentista, NHST, significância, potência, p-valor · meta: L04 (MPS08 3) e P2-23.2 Q4.4–4.5",
    "sections": [
        {"id": "recordacao", "heading": "Recordação: taxa-base, área à direita e likelihood", "html": recordacao},
        {"id": "frequentista", "heading": "Sem prior: a escola frequentista", "html": frequentista},
        {"id": "ingredientes", "heading": "Os ingredientes de um teste de hipóteses", "html": ingredientes},
        {"id": "erros", "heading": "Erros, nível de significância e potência", "html": erros},
        {"id": "normal", "heading": "Revisão da P1: a Normal e a tabela Φ", "html": revisao},
        {"id": "critico", "heading": "Dados contínuos: valor crítico e potência", "html": critico},
        {"id": "pvalor", "heading": "O p-valor", "html": pvalor},
        {"id": "objetivo", "heading": "O objetivo: L04 (MPS08 problema 3) e P2-23.2 Q4.4–4.5", "html": objetivo},
        {"id": "receita", "heading": "Como resolver", "html": receita},
        {"id": "fontes", "heading": "O que ficou de fora do MIT17", "html": fontes},
    ],
    "quiz": [
        {"question": r"Na moeda lançada 10 vezes, com \(H_0: \theta = 0.5\), a região de rejeição é \(\{0, 10\}\). Qual é o nível de significância?",
         "ref": [("ingredientes", "Os ingredientes de um teste de hipóteses")],
         "options": [
             {"text": "0.002", "correct": True, "feedback": r"Isso: \(p(0 \mid H_0) + p(10 \mid H_0) = 0.001 + 0.001 = 0.002\)."},
             {"text": "0.001", "correct": False, "feedback": r"Essa é uma ponta só. A região tem as duas: \(0.001 + 0.001 = 0.002\)."},
             {"text": "0.998", "correct": False, "feedback": r"Essa é a probabilidade de não rejeitar com \(H_0\). α é a da região: \(0.001 + 0.001 = 0.002\)."}]},
        {"question": r"Qual é o valor crítico \(z_{0.1}\) da Normal padrão (área 0.1 à direita)?",
         "ref": [("normal", "Revisão da P1: a Normal e a tabela Φ")],
         "options": [
             {"text": "1.28", "correct": True, "feedback": r"Isso: \(\Phi(1.28) \approx 0.90\), então sobra 0.1 à direita."},
             {"text": "−1.28", "correct": False, "feedback": r"Esse deixa 0.1 à esquerda (é \(z_{0.9}\)). Com 0.1 à direita, \(\Phi(z) = 0.9\): \(z = 1.28\)."},
             {"text": "1.645", "correct": False, "feedback": r"Esse é \(z_{0.05}\), com 0.05 à direita. Para 0.1, \(\Phi(z) = 0.9\): \(z = 1.28\)."}]},
        {"question": r"Um teste com \(\alpha = 0.05\) deu p-valor 0.03. Qual é a decisão?",
         "ref": [("pvalor", "O p-valor")],
         "options": [
             {"text": r"rejeitar \(H_0\), porque \(p < \alpha\)", "correct": True, "feedback": r"Isso: \(p = 0.03 < 0.05\), então a estatística caiu na região de rejeição."},
             {"text": r"não rejeitar \(H_0\), porque \(p > 0\)", "correct": False, "feedback": r"O p-valor se compara com α, e não com 0. \(0.03 < 0.05\): rejeita-se \(H_0\)."},
             {"text": r"aceitar \(H_0\), porque \(p\) é pequeno", "correct": False, "feedback": r"p pequeno é evidência contra \(H_0\): \(0.03 < 0.05\), rejeita-se. E o teste nunca \"aceita\" \(H_0\)."}]},
        {"question": r"Com o mesmo \(\alpha\) e a mesma \(H_A\), o número de dados passa de 9 para 36. O que acontece com a potência?",
         "ref": [("critico", "Dados contínuos: valor crítico e potência")],
         "options": [
             {"text": "aumenta, porque as curvas ficam mais estreitas", "correct": True, "feedback": r"Isso: o desvio padrão de \(\bar x\) cai de \(\sigma/3\) para \(\sigma/6\), as curvas de \(H_0\) e \(H_A\) se sobrepõem menos, e a potência sobe."},
             {"text": "diminui, porque o valor crítico fica mais perto", "correct": False, "feedback": r"O valor crítico chega mais perto de \(\mu_0\), e isso aumenta a região de rejeição. A potência sobe."},
             {"text": "não muda, porque α e a hipótese são os mesmos", "correct": False, "feedback": r"α fica igual, mas a curva de \(H_A\) fica mais estreita e põe mais área na região de rejeição. A potência sobe."}]},
    ],
}

if __name__ == "__main__":
    build(SPEC, ROOT / "lessons" / "0007-testes-de-hipoteses.html")
