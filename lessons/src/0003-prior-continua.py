"""Lesson 0003 source. Build: python lessons/src/0003-prior-continua.py

Quotes from MIT13 (and one from MIT11) are verbatim from the PDF text (MIT OCW 18.05 Spring 2022,
CC BY-NC-SA 4.0). The extracted text of MIT13 kept the prose clean but garbled the math symbols
(theta, f, p, d-theta came out as one placeholder glyph), so the prose is quoted word for word and
the symbols and formulas are restored in LaTeX from context. Obvious typos are fixed silently.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "assets"))
from build import build, mc, quote, pdf_plot  # noqa: E402

MIT11 = "https://drive.google.com/file/d/1-IfPV-srvMrLhYy4SMKkywMwIcA2ibZs/view"
MIT13 = "https://drive.google.com/file/d/1JZzKI6Iad26Wgm2oNSGRJQ4Eex-6gPiP/view"
MIT15 = "https://drive.google.com/file/d/1nkNUeimH00v3suIbVcsD3XPl-17bW-TV/view"
L03 = "https://drive.google.com/file/d/1Nb8V3KKsByciabbw_dcDfaQ2bYXCVeQm/view"
L03G = "https://drive.google.com/file/d/1w1zevZpR8_RlVbkCjUJtHLfsXRE9wRxI/view"
LESSON1 = "https://claude.ai/artifact/XWsvKr4dXaFPnc1BAz6Wxa"
LESSON2 = "https://claude.ai/artifact/PDFMi8VTuLgeRxHe39qE3Z"

ACC, MUT, FG = "var(--accent)", "var(--muted)", "var(--fg)"


def src(where, doc="MIT13"):
    url = {"MIT13": MIT13, "MIT11": MIT11, "MIT15": MIT15}[doc]
    return f'<a href="{url}">{doc}</a>, {where}'


def num(answer, tol="0.002", width=None):
    w = f' style="width:{width}"' if width else ""
    return f'<input data-answer="{answer}" data-tol="{tol}"{w}>'


def uso(text):
    """Short pointer from an explanation to the formula the student actually uses (the summary box #receita)."""
    return f'<p class="uso"><b>Na prova:</b> {text} (<a href="#receita">as 5 fórmulas</a>)</p>'


def check(body, ok):
    return (f'<div class="check-group" data-ok="{ok}">{body}'
            f'<button class="check">Verificar</button><div class="feedback"></div></div>')


# ---------------------------------------------------------------- recordação
recordacao = f"""
<p>Duas perguntas da <a href="{LESSON2}">lição 0002</a>, de cabeça, antes de começar.</p>
""" + mc(
    "A prior predictive e a posterior predictive de um mesmo resultado (por exemplo, \"sair cara\") são as duas uma média das likelihoods P(cara | H). O que muda de uma para a outra?",
    [("Os pesos: prior numa, posterior na outra", True, "Isso. A likelihood de cada hipótese é a mesma; muda a crença em cada hipótese."),
     ("As likelihoods: dependem do 1º resultado", False, "Sabendo a hipótese, o primeiro resultado não muda a chance do próximo (independência condicional). O que muda são os pesos."),
     ("Nada: as duas dão sempre o mesmo número", False, "Na gaveta de moedas da lição 0002 a prior predictive de cara era 0.625 e a posterior predictive, 0.668.")]) + check(
    r"""<p><b>Moedas A, B e C dão cara com probabilidade 0.5, 0.6 e 0.9. Depois de uma cara, as posteriores são 0.4, 0.24 e 0.36.
Qual a chance de o próximo lançamento dar <em>coroa</em>?</b> """ + num("0.332", "0.002") + "</p>",
    "Isso: 0.5 · 0.4 + 0.4 · 0.24 + 0.1 · 0.36 = 0.332. Nesta lição, a mesma soma ponderada vira uma integral.")

# ---------------------------------------------------------------- revisão da P1
revisao = r"""
<p>A lição usa duas ferramentas da P1. Vale revê-las agora, porque tudo aqui é montado com as duas: a likelihood é uma Binomial, e a prior é uma pdf.</p>

<h3 id="binomial">Binomial: contar caras em \(n\) lançamentos</h3>
<p>Uma moeda dá cara com probabilidade \(\theta\). Jogamos 3 vezes. Qual a chance de sair exatamente 2 caras, com \(\theta = 0.6\)?</p>
<ul>
<li>Uma sequência específica com 2 caras, por exemplo HHT (H de <em>heads</em>, cara; T de <em>tails</em>, coroa), tem probabilidade \(0.6 \cdot 0.6 \cdot 0.4 = 0.144\), porque os lançamentos são independentes.</li>
<li>Há 3 sequências com 2 caras: HHT, HTH e THH. Todas têm a mesma probabilidade 0.144.</li>
<li>Logo \(P(2 \text{ caras}) = 3 \cdot 0.144 = 0.432\).</li>
</ul>
<p>O 3 é o <b>coeficiente binomial</b> \(\binom{3}{2}\), que se lê "3 escolhe 2": o número de maneiras de escolher em quais 2 dos 3 lançamentos
saem as caras. Em geral:</p>
$$\binom{n}{k} = \frac{n!}{k!\,(n-k)!}, \qquad \binom{3}{2} = \frac{3!}{2!\,1!} = \frac{6}{2} = 3.$$
<p>Juntando as duas partes, a <b>pmf</b> (função de probabilidade de massa: a função que dá \(P(X = k)\) para cada valor \(k\) de uma variável
aleatória discreta) da <b>Binomial(\(n, \theta\))</b>, o número de caras em \(n\) lançamentos independentes, é:</p>
$$P(X = k) = \binom{n}{k}\,\theta^{k}(1-\theta)^{n-k}, \qquad k = 0, 1, \dots, n.$$
<p>Com as partes nomeadas:</p>
$$P(X = k) = \underbrace{\binom{n}{k}}_{\text{quantas sequências}} \cdot \underbrace{\theta^{k}(1-\theta)^{n-k}}_{\text{probabilidade de cada uma}}, \qquad k = 0, 1, \dots, n.$$
""" + uso("esta é a fórmula 1.") + r"""
""" + check(
    r"""<p><b>10 pessoas, cada uma prefere comédia com probabilidade \(\theta = 0.5\), independentemente. Calcule:</b></p>
<p>\(\binom{10}{6}\) = """ + num("210", "0.01") + r""" &nbsp;&nbsp; \(P(\text{exatamente 6 preferem comédia})\) = """ + num("0.2051", "0.0005") + "</p>"
    + r"""<details><summary>Dica</summary><p>\(\binom{10}{6} = \frac{10 \cdot 9 \cdot 8 \cdot 7}{4 \cdot 3 \cdot 2 \cdot 1}\) (os outros fatores se cancelam). Com \(\theta = 0.5\), cada sequência tem probabilidade \(0.5^{10} = 1/1024\).</p></details>""",
    "Isso: 210 sequências, cada uma com probabilidade 1/1024, total 210/1024 ≈ 0.2051. É a likelihood da L03 Q2 avaliada em θ = 0.5.") + r"""

<h3 id="pdf">Densidade (pdf) de uma variável contínua</h3>
<p>Uma variável aleatória <b>contínua</b> pode assumir qualquer valor num intervalo, e a chance de um valor exato é 0. Por isso ela não tem pmf;
tem uma <b>pdf</b> (função densidade de probabilidade) \(f(x)\), em que probabilidade é <em>área</em> sob a curva. O MIT13 faz essa revisão antes
de usar a pdf:</p>
""" + quote(r"""<p>Suppose \(X\) is a random variable with pdf \(f(x)\). Recall \(f(x)\) is a density; its units are probability/(units of \(x\)). […]</p>
<p>The probability that the value of \(X\) is in \([c, d]\) is given by</p>
$$\int_c^d f(x)\,dx.$$
<p>The probability that \(X\) is in an infinitesimal range \(dx\) around \(x\) is \(f(x)\,dx\). In fact, the integral formula is just the
‘sum’ of these infinitesimal probabilities. We can visualize these probabilities by viewing the integral as area under the graph of \(f(x)\).</p>
<p>In order to manipulate probabilities instead of densities in what follows, we will make frequent use of the notion that \(f(x)\,dx\) is
the probability that \(X\) is in an infinitesimal range around \(x\) of width \(dx\). Please make sure that you fully understand this notion.</p>""",
    src("§5")) + r"""
<p>Um exemplo com números: \(X\) tem pdf \(f(x) = 2x\) em \([0, 1]\). O gráfico mostra as duas ideias da citação.</p>
""" + pdf_plot(
    [("f(x) = 2x", lambda x: 2 * x, FG, False, 0.6, 1.75)],
    xlabel="x",
    shade=(0.5, 1, lambda x: 2 * x, "área = 0.75"),
    strip=(0.25, 0.03, lambda x: 2 * x, "f(0.25) dx"),
    ymax=2.3,
    caption="A área sombreada é \\(P(0.5 \\le X \\le 1) = \\int_{0.5}^{1} 2x\\,dx = 1 - 0.25 = 0.75\\). "
            "A tira fina perto de 0.25 tem altura \\(f(0.25) = 0.5\\) e largura \\(dx\\): sua área \\(f(0.25)\\,dx\\) é a probabilidade de "
            "\\(X\\) cair nessa tira. Somar todas as tiras (integrar) dá a área total, 1.") + r"""
<p>Três fatos que a lição vai usar:</p>
<ul>
<li>a área total é 1: \(\int_0^1 2x\,dx = \big[x^2\big]_0^1 = 1\);</li>
<li>a altura \(f(x)\) não é probabilidade e pode passar de 1: aqui \(f(1) = 2\);</li>
<li>uma <b>tira</b> é um intervalo muito estreito, de largura \(dx\), em volta de \(x\) (a barrinha do gráfico). Só \(f(x)\,dx\), a área de uma tira, é probabilidade: a chance de \(X\) cair nesse intervalo minúsculo. É por isso que o \(dx\) aparece em todas as tabelas desta lição.</li>
</ul>
""" + check(
    r"""<p><b>Com a mesma pdf \(f(x) = 2x\) em \([0, 1]\): \(P(X \le 0.5)\) = </b>""" + num("0.25", "0.002") + "</p>",
    "Isso: ∫₀^0.5 2x dx = 0.5² = 0.25. Confere com o gráfico: 1 − 0.75 = 0.25.")

# ---------------------------------------------------------------- hipóteses contínuas
continuas = r"""
<p>Até aqui as hipóteses eram poucas: três moedas, cinco dados. O MIT13 abre com o caso em que elas formam um contínuo:</p>
""" + quote(r"""<p>Up to now we have only done Bayesian updating when we had a finite number of hypotheses, e.g. our dice example had five hypotheses
(4, 6, 8, 12 or 20 sides). Now we will study Bayesian updating when there is a continuous range of hypotheses. The Bayesian update process
will be essentially the same as in the discrete case. As usual when moving from discrete to continuous we will need to replace the
probability mass function by a probability density function, and sums by integrals.</p>""", src("§2")) + quote(
    r"""<p><b>Example 1.</b> Suppose you have a system that can succeed or fail with probability \(p\). Then we can hypothesize that \(p\) is anywhere
in the range \([0, 1]\). That is, we have a continuous range of hypotheses. We will often model this example with a ‘bent’ coin with unknown
probability \(p\) of heads. […]</p>
<p>In all of these examples we modeled the random process giving rise to the data by a distribution with parameters –called a parametrized
distribution. Every possible choice of the parameter(s) is a hypothesis, e.g. we can hypothesize that the probability of success in Example 1
is \(p = 0.7313\). We have a continuous set of hypotheses because we could take any value between 0 and 1.</p>""", src("§3")) + r"""
<p>Um <b>parâmetro</b> é o número que fixa uma distribuição: o \(\theta\) da Binomial(\(n, \theta\)), por exemplo. Cada valor possível do parâmetro é
uma hipótese. Na L03 Q2, \(\theta\) é a fração do grupo que prefere comédia, e qualquer valor em \([0, 1]\) é uma hipótese.</p>
<p>Uma imagem ajuda. Na lição 0002, a gaveta tinha três tipos de moeda, e as hipóteses eram "\(\theta = 0.5\)", "\(\theta = 0.6\)" e "\(\theta = 0.9\)".
Agora imagine uma fábrica de moedas tortas em que cada moeda sai com uma chance de cara diferente: 0.31, 0.7313, 0.9… Qualquer número entre
0 e 1 é possível. Você pega uma moeda ao acaso e pergunta "qual é o \(\theta\) desta moeda?". A pergunta é a mesma de antes, mas agora há
infinitas respostas possíveis.</p>
<p>A partir daqui o MIT13 chama o parâmetro de \(\theta\) e usa letras pequenas:</p>
<ul>
<li><b>prior</b> \(f(\theta)\): agora uma <b>pdf</b> sobre as hipóteses;</li>
<li><b>likelihood</b> \(p(x \mid \theta)\): continua uma <b>pmf</b>, porque o dado \(x\) é discreto (cara ou coroa, número de pessoas).</li>
</ul>
<div class="callout" id="letras"><p><b>Qual letra usar.</b> São quatro, e cada uma tem um papel:</p>
<ul class="spaced">
<li>\(P(\ldots)\), maiúscula: probabilidade de um <b>evento</b>, algo que acontece ou não. Entre os parênteses vai uma afirmação:
\(P(H)\), \(P(D \mid H)\), \(P(\theta > 0.5)\). O valor fica sempre entre 0 e 1.</li>
<li>\(p(x)\), minúscula: a <b>pmf</b> de uma variável <b>discreta</b>, \(p(x) = P(X = x)\). Entre os parênteses vai um valor. Continua sendo
uma probabilidade, entre 0 e 1. Exemplo: a likelihood \(p(x \mid \theta)\) de cara ou coroa.</li>
<li>\(f(x)\): a <b>pdf</b> de uma variável <b>contínua</b>. É densidade, não probabilidade, e pode passar de 1: a prior \(2\theta\) vale 1.8 em
\(\theta = 0.9\). Probabilidade é a área, \(\int_c^d f(x)\,dx\), ou \(f(x)\,dx\) numa tira.</li>
<li>\(F(x)\), maiúscula: a <b>cdf</b> (função de distribuição acumulada), \(F(x) = P(X \le x)\). Vale para discreta e contínua; na contínua,
\(F(x) = \int_{-\infty}^{x} f(t)\,dt\). Ainda não apareceu nas lições, mas resolve contas como a da prior \(2\theta\): \(F(\theta) = \theta^2\),
então \(P(\theta > 0.5) = 1 - F(0.5) = 0.75\).</li>
</ul>
<p>Para decidir: se entre os parênteses vai uma afirmação, é \(P\). Se vai um valor, é \(p\) (discreta) ou \(f\) (contínua). Se a pergunta é
"até tal valor", é \(F\).</p></div>
<p>O exemplo que atravessa a nota inteira:</p>
""" + quote(r"""<p><b>Example 4.</b> Suppose we have a bent coin with unknown probability \(\theta\) of heads. […] The value of \(\theta\) is random and
could be anywhere between 0 and 1. For this and the examples that follow we’ll suppose that the value of \(\theta\) follows a distribution with
continuous prior probability density \(f(\theta) = 2\theta\). We have a discrete likelihood because tossing a coin has only two outcomes,
\(x = 1\) for heads and \(x = 0\) for tails.</p>
$$p(x = 1 \mid \theta) = \theta, \qquad p(x = 0 \mid \theta) = 1 - \theta.$$
<p><b>Think:</b> This can be tricky to wrap your mind around. We have a continuous range of types of coins –we identify the type by the value of
the parameter \(\theta\). We are able to choose a coin at random and the type chosen has a probability density \(f(\theta)\).</p>
<p>It may help to see that the discrete examples we did in previous classes are similar. In one example, we had three types of coin with
probability of heads 0.5, 0.6, or 0.9. So, we called our hypotheses \(H_{0.5}\), \(H_{0.6}\), \(H_{0.9}\) and these had prior probabilities
\(P(H_{0.5})\) etc. In other words, we had a type of coin with an unknown probability of heads, we had hypotheses about that probability and
each of these hypotheses had a prior probability.</p>""", src("§6")) + r"""
<p>Por que a prior vira uma pdf? Com 3 hipóteses, ela era uma lista de 3 probabilidades que somam 1. Com infinitas hipóteses, se cada valor
exato de \(\theta\) tivesse probabilidade positiva, a soma passaria de 1. Então a chance de \(\theta\) ser <em>exatamente</em> 0.7313 é 0. O que tem
probabilidade positiva é um intervalo, e essa probabilidade é uma área sob a pdf, como na <a href="#pdf">revisão</a>.</p>
<p>A prior \(f(\theta) = 2\theta\) é a mesma pdf do gráfico da revisão, com \(\theta\) no lugar de \(x\). Ela diz que a fábrica produz mais
moedas com tendência a cara: \(P(\theta > 0.5) = \int_{0.5}^1 2\theta\,d\theta = 0.75\), a mesma conta que o quadro <a href="#letras">Qual letra usar</a> fez com \(F\). Ou seja, 75% das moedas da fábrica dão cara com
mais frequência que coroa, e, antes de jogar, a chance de a moeda escolhida ser uma delas é 0.75.</p>

<p>A likelihood não muda de natureza: o dado continua discreto (cara ou coroa), então ela continua uma probabilidade comum, só que escrita
como fórmula, \(p(\text{cara} \mid \theta) = \theta\).</p>
""" + mc("O MIT13 pergunta: X ~ Bernoulli(θ) (um lançamento: 1 com probabilidade θ, 0 senão), com θ desconhecido. Qual frase é verdadeira?",
         [("Dado discreto, hipóteses num contínuo", True, "Isso: x vale 0 ou 1, e θ pode ser qualquer número em [0, 1]. É o caso do MIT13 inteiro."),
          ("Dado contínuo, hipóteses discretas", False, "É o contrário: x só vale 0 ou 1; θ é que varia num contínuo."),
          ("Dado contínuo, hipóteses num contínuo", False, "θ é contínuo, mas x só vale 0 ou 1. Dado contínuo é o assunto do MIT14.")])

# ---------------------------------------------------------------- probabilidade total
total = r"""
<p>Na lição 0001, \(P(D) = \sum_H P(D \mid H)\,P(H)\) era a soma da coluna dos numeradores. Com hipóteses contínuas, a soma vira integral:</p>
""" + quote(r"""<p><b>Theorem. Law of total probability.</b> Suppose we have a continuous parameter \(\theta\) in the range \([a, b]\), and discrete
random data \(x\). Assume \(\theta\) is itself random with density \(f(\theta)\) and that \(x\) and \(\theta\) have likelihood \(p(x \mid \theta)\).
In this case, the total probability of \(x\) is given by the formula.</p>
$$p(x) = \int_a^b p(x \mid \theta)\,f(\theta)\,d\theta$$
<p><b>Proof.</b> Our proof will be by analogy to the discrete version: The probability term \(p(x \mid \theta)\,f(\theta)\,d\theta\) is perfectly
analogous to the term \(p(x \mid \theta_i)\,p(\theta_i)\) […]. Continuing the analogy: the sum […] becomes the integral […]</p>
<p>As in the discrete case, when we think of \(\theta\) as a hypothesis explaining the probability of the data we call \(p(x)\) the prior
predictive probability for \(x\).</p>""", src("§7")) + r"""
<p>Cada termo \(p(x \mid \theta)\,f(\theta)\,d\theta\) é uma likelihood vezes a probabilidade prior de uma tira de largura \(d\theta\), exatamente
como \(P(D \mid H)\,P(H)\) era na tabela discreta. O exemplo do MIT13:</p>
""" + quote(r"""<p><b>Example 5.</b> […] We have a bent coin with probability \(\theta\) of heads. The value of \(\theta\) is random with prior pdf
\(f(\theta) = 2\theta\) on \([0, 1]\). Suppose I am about to flip the coin. What is the total probability of heads, i.e what is the prior
predictive probability of heads?</p>
<p><b>Solution:</b> In Example 4 we noted that the likelihoods are \(p(x = 1 \mid \theta) = \theta\) and \(p(x = 0 \mid \theta) = 1 - \theta\).
So the total probability of \(x = 1\) is</p>
$$p(x = 1) = \int_0^1 p(x = 1 \mid \theta)\,f(\theta)\,d\theta = \int_0^1 \theta \cdot 2\theta\,d\theta = \int_0^1 2\theta^2\,d\theta = \frac{2}{3}.$$
<p>Since the prior is weighted towards higher probabilities of heads, so is the total probability of heads.</p>""", src("§7")) + r"""
<p>A última integral, passo a passo: \(\int_0^1 2\theta^2\,d\theta = \big[\tfrac{2\theta^3}{3}\big]_0^1 = \tfrac{2}{3}\). Toda integral desta lição
é desse tipo, um polinômio em \(\theta\) de 0 a 1, e sai com a regra \(\int_0^1 \theta^k\,d\theta = \frac{1}{k+1}\). Quando o integrando tem a forma \(\theta^m(1-\theta)^n\), há um
atalho que dispensa expandir: a <a href="#integral-beta">integral da Beta</a>, mais adiante.</p>
""" + uso("esta integral volta na fórmula 5, a da previsão. Para normalizar a posterior, a fórmula 3 dispensa a integral quando a posterior tem forma de Beta.") + r"""
<p id="hipotese-resultado">Repare que há dois números parecidos sobre a mesma prior \(2\theta\), e eles medem coisas diferentes:</p>
<table>
<tr><th>pergunta</th><th>tipo</th><th class="num">valor</th></tr>
<tr><td>Qual a chance de a moeda ser do tipo que favorece cara? \(P(\theta > 0.5)\)</td><td>prior, sobre a <b>hipótese</b></td><td class="num">0.75</td></tr>
<tr><td>Qual a chance de sair cara no primeiro lançamento? \(p(x = 1)\)</td><td>prior predictive, sobre o <b>resultado</b></td><td class="num">0.667</td></tr>
</table>
<p>O segundo é menor porque "a moeda favorece cara" não garante cara: uma moeda com \(\theta = 0.55\) ainda dá coroa 45% das vezes, e as
moedas com \(\theta < 0.5\) ainda dão alguma cara. É a distinção da lição 0002: prior e posterior são sobre hipóteses (qual moeda é);
as predictive são sobre resultados (o que sai no lançamento).</p>
<p>Agora o problema 1 em sala do MIT13, com outra prior:</p>
""" + quote(r"""<p><b>Problem 1. Total probability</b> (a) A coin has unknown probability of heads \(\theta\) with prior pdf, for the value of \(\theta\),
\(f(\theta) = 3\theta^2\). Find the probability of throwing tails on the first toss.</p>""", src("problemas em sala")) + check(
    r"""<p>\(p(x = 0) = \int_0^1 (1-\theta)\,3\theta^2\,d\theta\) = """ + num("1/4", "0.002") + "</p>"
    + r"""<details><summary>Dica</summary><p>Expanda: \((1-\theta)\,3\theta^2 = 3\theta^2 - 3\theta^3\). Integre cada termo com \(\int_0^1 \theta^k\,d\theta = \frac{1}{k+1}\).</p></details>""",
    "Isso: 3 · 1/3 − 3 · 1/4 = 1 − 3/4 = 1/4. A prior 3θ² favorece moedas que dão muita cara, então coroa fica pouco provável.")

# ---------------------------------------------------------------- tabela contínua
tabela = r"""
<p>Bayes contínuo é a mesma fórmula da lição 0001, com \(d\theta\) para que tudo continue sendo probabilidade:</p>
$$f(\theta \mid x)\,d\theta = \frac{p(x \mid \theta)\,f(\theta)\,d\theta}{\int_a^b p(x \mid \theta)\,f(\theta)\,d\theta}$$
<p>Com as partes nomeadas. A <b>tira</b> é a mesma da <a href="#pdf">revisão de pdf</a>: um intervalo minúsculo, de largura \(d\theta\), em
volta de \(\theta\). "Prior da tira" é a chance de \(\theta\) cair nele antes do dado; "posterior da tira", depois.</p>
$$\underbrace{f(\theta \mid x)\,d\theta}_{\text{posterior da tira}} \;=\; \frac{\overbrace{p(x \mid \theta)}^{\text{likelihood}}\;\overbrace{f(\theta)\,d\theta}^{\text{prior da tira}}}{\underbrace{\int_a^b p(x \mid \theta)\,f(\theta)\,d\theta}_{p(x),\ \text{probabilidade total}}}$$
<p>Como \(d\theta\) aparece dos dois lados, pode ser cancelado, e sobra a versão só com densidades:</p>
$$f(\theta \mid x) = \frac{p(x \mid \theta)\,f(\theta)}{\int_a^b p(x \mid \theta)\,f(\theta)\,d\theta}$$
<div class="callout"><b>Na prática, escreva sem o \(d\theta\).</b> É essa forma que vai nas listas e na prova: a resposta da L03 Q2, por exemplo,
é a densidade \(f(\theta \mid x_1 = 6)\), sem \(d\theta\). Só o \(d\theta\) de dentro da integral é obrigatório. Guarde a ideia que ele carrega:
a altura da pdf não é probabilidade (a posterior \(20\theta^3(1-\theta)\) do exemplo abaixo vale 2.11 em \(\theta = 0.75\)), e só a área de
uma tira, \(f(\theta)\,d\theta\), é.</div>
<p id="paralelo">Lado a lado com a regra de Bayes da lição 0001:</p>
$$\begin{aligned} \text{discreto:} \quad P(H \mid D) &= \frac{P(D \mid H)\,P(H)}{\sum_H P(D \mid H)\,P(H)} \\[22pt] \text{contínuo:} \quad f(\theta \mid x) &= \frac{p(x \mid \theta)\,f(\theta)}{\int_a^b p(x \mid \theta)\,f(\theta)\,d\theta} \end{aligned}$$
<p>Os passos são os mesmos: numerador = likelihood × prior; total = somar (ou integrar) os numeradores; posterior = numerador ÷ total.
Mudam só duas coisas: probabilidade vira densidade, e soma vira integral.</p>
""" + uso('a tabela desta seção se resume à fórmula 2 (o numerador) e à fórmula 3 (a constante, que a seção da <a href="#beta">família Beta</a> ensina a achar sem integral). O resto da seção mostra por que elas funcionam.') + r"""
<h3 id="hht">Exemplo: cara, cara, coroa</h3>
<p>A moeda é a mesma das seções anteriores: a chance de cara \(\theta\) é desconhecida, e a prior é \(2\theta\) (a
<a href="#continuas">fábrica</a> faz mais moedas com tendência a cara). Agora ela é jogada três vezes e sai cara, cara, coroa (HHT).
A pergunta é o que esses três lançamentos dizem sobre \(\theta\).</p>
<p>O MIT13 escreve esse dado como \(x = 1, 1, 0\) (1 = cara, 0 = coroa). A likelihood é a chance de sair H, H, T com uma moeda de
tipo \(\theta\): \(p(x = 1,1,0 \mid \theta) = \theta \cdot \theta \cdot (1-\theta)\).</p>
<p>A resposta é uma curva nova, a <b>posterior</b>, que mostra quais valores de \(\theta\) ficaram mais plausíveis e quais ficaram menos.
Na lição 0001, a posterior eram três números, um para cada tipo de moeda. Aqui ela é uma curva, porque \(\theta\) pode ser qualquer número
entre 0 e 1. Os passos até ela são os mesmos da lição 0001: prior, likelihood, numerador, total e posterior. A tabela do MIT13 faz exatamente isso:</p>
""" + quote(r"""<p>1. The table for continuous priors is very simple: since we cannot have a row for each of an infinite number of hypotheses we’ll
have just one row which uses a variable to stand for all hypotheses \(H_\theta\).</p>
<p>2. By including \(d\theta\), all the entries in the table are probabilities and all our usual probability rules apply.</p>
<p><b>Example 6. (Bayesian updating.)</b> Continuing Examples 4 and 5. We have a bent coin with unknown probability \(\theta\) of heads. The value
of \(\theta\) is random with prior pdf \(f(\theta) = 2\theta\). Suppose we flip the coin three times and get the sequence \(HHT\). Compute the
posterior pdf for \(\theta\).</p>
<p><b>Solution:</b> We make the usual update table, with an added column giving the range of values that \(\theta\) can take. We make the first row an abstract version of Bayesian updating and the second row is Bayesian
updating for this particular example. In later examples we will skip that abstract version.</p>
<table>
<tr><th>hypothesis</th><th>range</th><th>prior</th><th>likelihood</th><th>Bayes numerator</th><th>posterior</th></tr>
<tr><td>\(H_\theta\)</td><td>\(\theta\) range</td><td>\(f(\theta)\,d\theta\)</td><td>\(p(x = 1,1,0 \mid \theta)\)</td><td>\(p(x = 1,1,0 \mid \theta)\,f(\theta)\,d\theta\)</td><td>\(f(\theta \mid x = 1,1,0)\,d\theta\)</td></tr>
<tr><td>\(H_\theta\)</td><td>\([0, 1]\)</td><td>\(2\theta\,d\theta\)</td><td>\(\theta^2(1-\theta)\)</td><td>\(2\theta^3(1-\theta)\,d\theta\)</td><td>\(20\theta^3(1-\theta)\,d\theta\)</td></tr>
<tr><td>total</td><td>\([0, 1]\)</td><td>\(\int_a^b f(\theta)\,d\theta\)<br>\(= 1\)</td><td>no sum</td><td>\(p(x = 1,1,0)\)<br>\(= \int_0^1 2\theta^3(1-\theta)\,d\theta\)<br>\(= 1/10\)</td><td>1</td></tr>
</table>
<p>Therefore the posterior pdf (after seeing HHT) is \(f(\theta \mid x) = 20\theta^3(1-\theta)\).</p>""", src("§9")) + r"""
<p>A primeira linha funciona como um cabeçalho: diz o que vai em cada coluna. A segunda é uma fórmula que gera qualquer linha: troque
\(\theta\) por um número e sai a linha daquela moeda, como na tabela da lição 0001. Com \(\theta = 0.75\), por exemplo, a prior vale 1.5, a
likelihood 0.141, o numerador 0.211 e a posterior 2.11, que é o numerador × 10, porque o total é 1/10. Na prova, a linha abstrata e as linhas
com números não aparecem: você escreve só a linha da fórmula (prior × likelihood = numerador) e segue com as fórmulas 2 e 3 da
<a href="#receita">receita</a>.</p>
<p>Os números da tabela, um a um:</p>
<ul class="spaced">
<li><b>likelihood</b> \(p(x = 1,1,0 \mid \theta) = \theta^2(1-\theta)\): a chance da sequência HHT para uma moeda de tipo \(\theta\) (duas caras, uma coroa). É uma sequência
específica, então não há coeficiente binomial;</li>
<li><b>numerador</b> \(p(x \mid \theta)\,f(\theta)\): likelihood × prior, \(\theta^2(1-\theta) \cdot 2\theta = 2\theta^3(1-\theta) = 2\theta^3 - 2\theta^4\);</li>
<li><b>total</b> \(p(x)\): a integral do numerador, \(\int_0^1 (2\theta^3 - 2\theta^4)\,d\theta = \frac{2}{4} - \frac{2}{5} = \frac{1}{10}\);</li>
<li><b>posterior</b> \(f(\theta \mid x)\): numerador ÷ total, \(2\theta^3(1-\theta) / (1/10) = 20\theta^3(1-\theta)\). Dividir pelo total é o que garante área 1
(<b>normalizar</b>), como dividir por \(P(D)\) garantia soma 1 na lição 0001;</li>
<li><b>linha total</b>: na prior, a área da pdf é 1 (as priors somavam 1); a likelihood não se soma ("no sum"), igual à lição 0001; e na
posterior, a área volta a ser 1.</li>
</ul>
""" + pdf_plot(
    [("prior 2θ", lambda t: 2 * t, MUT, True, 0.03, 1.55),
     ("posterior 20θ³(1−θ)", lambda t: 20 * t**3 * (1 - t), ACC, False, 0.03, 2.0)],
    marks=[(0.75, lambda t: 20 * t**3 * (1 - t), "pico em 0.75", ACC)],
    ymax=2.4,
    caption="A coroa no fim de HHT multiplica a prior por \\((1-\\theta)\\), que zera em \\(\\theta = 1\\): a moeda que só dá cara fica impossível. "
            "As duas caras multiplicam por \\(\\theta^2\\), que zera perto de 0. O que sobra é um morro com pico (ponto de máximo) em 0.75, que a <a href='#map'>seção do MAP</a> ensina a achar, um pouco acima da fração de caras observada (2/3), porque a prior 2θ favorece valores altos.") + r"""
<p>Uma observação do MIT13 sobre a tabela:</p>
""" + quote(r"""<p>[…] 5. Regarding both sides as functions of \(\theta\), we can again express Bayes’ theorem in the form:
\(f(\theta \mid x) \propto p(x \mid \theta) \cdot f(\theta)\)</p>
<p>posterior \(\propto\) likelihood × prior.</p>""", src("§9, comentários")) + r"""
<p>O símbolo \(\propto\) ("proporcional a") quer dizer "igual, a menos de uma constante que não depende de \(\theta\)". Aqui a constante é
\(1/p(x) = 10\). Essa forma vai ser a chave do <a href="#map">MAP</a>.</p>

<h3 id="flat">Prior plana</h3>
""" + quote(r"""<p>One important prior is called a flat or uniform prior. A flat prior assumes that every hypothesis is equally probable. For example,
if \(\theta\) has range \([0, 1]\) then \(f(\theta) = 1\) is a flat prior.</p>
<p><b>Example 7. (Flat priors.)</b> We have a bent coin with unknown probability \(\theta\) of heads. Suppose we toss it once and get heads.
Assume a flat prior and find the posterior probability for \(\theta\).</p>""", src("§9.1")) + r"""
<p>Pela tabela de uma linha:</p>
<ul>
<li><b>prior</b> \(f(\theta)\,d\theta = 1 \cdot d\theta\)</li>
<li><b>likelihood</b> de uma cara: \(p(x = 1 \mid \theta) = \theta\)</li>
<li><b>numerador</b> \(p(x = 1 \mid \theta)\,f(\theta)\,d\theta = \theta \cdot 1\,d\theta = \theta\,d\theta\)</li>
<li><b>total</b> \(p(x = 1) = \int_0^1 \theta\,d\theta = 1/2\)</li>
<li><b>posterior</b> \(f(\theta \mid x = 1)\,d\theta = \frac{\theta}{1/2}\,d\theta = 2\theta\,d\theta\)</li>
</ul>
<p>Uma cara, partindo da prior plana, dá exatamente a prior \(2\theta\) dos exemplos anteriores. Repare que, com prior plana, o numerador é a
própria likelihood; a seção do <a href="#map">MAP</a> volta a esse ponto.</p>

<h3 id="pratica-tabela">Prática: duas atualizações seguidas</h3>
""" + quote(r"""<p><b>Problem 2. Bent coin 1</b> We have a ‘bent’ coin with an unknown probability \(\theta\) of heads. Assume the following:</p>
<ul><li>Prior for the value of \(\theta\): \(f(\theta) = 2\theta\) on \([0, 1]\).</li><li>Data: toss once and get heads.</li></ul>
<p>(a) Find the posterior pdf to this data.</p>
<p>(b) Suppose you toss again and get tails. Update your posterior from part (a) using this data.</p>""", src("problemas em sala")) + r"""
<p>Monte a tabela de uma linha. Na (b), a posterior da (a) vira a prior, como nas atualizações repetidas da lição 0001.</p>
""" + check(
    r"""<table>
<tr><th>item</th><th>prior<br>\(f(\theta)\,d\theta\)</th><th>likelihood<br>\(p(x \mid \theta)\)</th><th>numerador<br>\(p(x \mid \theta)\,f(\theta)\,d\theta\)</th><th>total<br>\(p(x)\)</th><th>posterior<br>\(f(\theta \mid x)\,d\theta\)</th></tr>
<tr><td>(a) cara</td><td>\(2\theta\,d\theta\)</td><td>\(\theta\)</td><td>\(2\theta^2\,d\theta\)</td><td>""" + num("2/3", "0.002", "4.5rem") + r"""</td>
<td><input data-answer="3" data-tol="0.01" data-name="c" style="width:3rem"> \(\theta^2\,d\theta\)</td></tr>
<tr><td>(b) coroa</td><td><span data-show="c">c</span>\(\,\theta^2\,d\theta\)</td><td>\(1-\theta\)</td><td><span data-show="c">c</span>\(\,\theta^2(1-\theta)\,d\theta\)</td><td>""" + num("1/4", "0.002", "4.5rem") + r"""</td>
<td>""" + num("12", "0.01", "3rem") + r""" \(\theta^2(1-\theta)\,d\theta\)</td></tr>
</table>
<p style="font-size:.9rem;color:var(--muted)">Na (b), a prior é a posterior da (a), \(c\,\theta^2\). O \(c\) é o número da última coluna da
linha (a): quando você acerta esse número, ele aparece sozinho no lugar do \(c\).</p>""",
    "Isso. (a) ∫2θ² = 2/3, posterior 2θ²/(2/3) = 3θ². (b) ∫3θ²(1−θ) = 3(1/3 − 1/4) = 1/4, posterior 3θ²(1−θ)/(1/4) = 12θ²(1−θ).")

# ---------------------------------------------------------------- preditiva
preditiva = r"""
<p>A probabilidade preditiva da lição 0002 também vira integral: a média das likelihoods, agora com a pdf como peso.</p>
""" + quote(r"""<p><b>Example 9. (Prior and posterior prediction.)</b> Continuing Examples 4, 5, 6: we have a coin with unknown probability \(\theta\) of heads
and the value of \(\theta\) has prior pdf \(f(\theta) = 2\theta\). Find the prior predictive probability of heads. Then suppose the first flip
was heads and find the posterior predictive probabilities of both heads and tails on the second flip.</p>
<p><b>Solution:</b> For notation let \(x_1\) be the result of the first flip and let \(x_2\) be the result of the second flip. The prior
predictive probability is exactly the total probability computed in Examples 5 and 6.</p>
$$p(x_1 = 1) = \int_0^1 p(x_1 = 1 \mid \theta)\,f(\theta)\,d\theta = \int_0^1 2\theta^2\,d\theta = \frac{2}{3}.$$
<p>The posterior predictive probabilities are the total probabilities computed using the posterior pdf. From Example 6 we know the posterior pdf
is \(f(\theta \mid x_1 = 1) = 3\theta^2\). So the posterior predictive probabilities are</p>
$$\begin{aligned} p(x_2 = 1 \mid x_1 = 1) &= \int_0^1 p(x_2 = 1 \mid \theta, x_1 = 1)\,f(\theta \mid x_1 = 1)\,d\theta \\ &= \int_0^1 \theta \cdot 3\theta^2\,d\theta = \frac{3}{4} \end{aligned}$$
$$\begin{aligned} p(x_2 = 0 \mid x_1 = 1) &= \int_0^1 p(x_2 = 0 \mid \theta, x_1 = 1)\,f(\theta \mid x_1 = 1)\,d\theta \\ &= \int_0^1 (1-\theta) \cdot 3\theta^2\,d\theta = \frac{1}{4} \end{aligned}$$
<p>(More simply, we could have computed \(p(x_2 = 0 \mid x_1 = 1) = 1 - p(x_2 = 1 \mid x_1 = 1) = 1/4\).)</p>""", src("§10")) + r"""
<p>A posterior \(3\theta^2\) depois de uma cara é a que você calculou na <a href="#pratica-tabela">prática (a)</a>. O "Example 6" citado pelo MIT13
aqui é o da cara única, não o de HHT. Como na lição 0002, \(p(x_2 = 1 \mid \theta, x_1 = 1)\) vira \(\theta\) porque, sabendo a moeda, o primeiro
lançamento não diz nada sobre o segundo. A receita, lado a lado com a da lição 0002:</p>
$$\sum_H P(D_2 \mid H)\,P(H \mid D_1) \quad\longrightarrow\quad \int_a^b p(x_2 \mid \theta)\,f(\theta \mid x_1)\,d\theta$$
<p>Com as partes nomeadas:</p>
$$\underbrace{\sum_H P(D_2 \mid H)\,P(H \mid D_1)}_{\text{hipóteses discretas (lição 0002)}} \quad\longrightarrow\quad \underbrace{\int_a^b p(x_2 \mid \theta)\,f(\theta \mid x_1)\,d\theta}_{\text{hipóteses contínuas}}$$
""" + uso("esta é a fórmula 5.") + check(
    r"""<p><b>Depois de HHT, a posterior é \(20\theta^3(1-\theta)\). Qual a chance de o próximo lançamento dar cara?</b> """ + num("2/3", "0.002") + "</p>"
    + r"""<details><summary>Dica</summary><p>\(\int_0^1 \theta \cdot 20\theta^3(1-\theta)\,d\theta = 20\int_0^1 (\theta^4 - \theta^5)\,d\theta\). Ou, sem expandir:
\(\theta^4(1-\theta)\) é a forma da Beta(5, 2), então a integral é \(\frac{4!\,1!}{6!} = \frac{1}{30}\) (<a href="#integral-beta">integral da Beta</a>).</p></details>""",
    "Isso: 20 (1/5 − 1/6) = 20/30 = 2/3. É menor que os 3/4 depois de uma cara só, porque a coroa puxou θ para baixo.")

# ---------------------------------------------------------------- MAP
map_ = r"""
<p>A posterior é uma curva inteira. Muitas vezes se quer um número só: o valor de \(\theta\) mais plausível depois dos dados. O candidato
natural é o <b>máximo a posteriori</b> (MAP): o valor de \(\theta\) com a maior densidade posterior, ou seja, o ponto de máximo da
curva posterior. Nesta lição, "pico" quer dizer esse ponto de máximo.
No gráfico de HHT acima, o MAP é 0.75. O MIT13 não usa esse nome, mas o MIT11 já tinha registrado a ideia que o torna barato:</p>
""" + quote(r"""<p>4. If all we care about is finding the most likely hypothesis, the Bayes numerator works as well as the normalized posterior.</p>""",
            src("§3.1, “Important things to notice”", "MIT11")) + r"""
<p><b>Como achar o MAP: o pico do numerador.</b> A posterior é o numerador dividido por \(p(x)\), um número fixo. Dividir por uma
constante muda a altura da curva, não o lugar do pico. Então não é preciso normalizar: basta achar o pico do numerador
\(p(x \mid \theta)\,f(\theta)\). Onde fica esse pico:</p>
<ul>
<li><b>hipóteses discretas</b> (lição 0001): a hipótese com o maior numerador. Basta olhar a coluna;</li>
<li><b>hipóteses contínuas</b>: onde a derivada do numerador zera, ou numa borda do intervalo de \(\theta\).</li>
</ul>
<p>Nesta lição o numerador tem sempre a forma \(\theta^m(1-\theta)^n\) (vezes uma constante, que também não muda o pico), e a derivada já
foi feita uma vez por todas. O pico dessa forma é:</p>
$$\theta_{\text{MAP}} = \frac{m}{m+n}, \qquad m = \text{expoente de } \theta, \quad n = \text{expoente de } (1-\theta).$$
""" + uso("esta é a fórmula 4.") + r"""
<p>Para HHT:</p>
<ul>
<li><b>numerador</b> \(p(x \mid \theta)\,f(\theta) = 2\theta^3(1-\theta)\), então \(m = 3\) e \(n = 1\);</li>
<li><b>MAP:</b> \(\frac{3}{3+1} = \frac{3}{4}\).</li>
</ul>
<details><summary>De onde vem \(m/(m+n)\)</summary><p>O logaritmo tem o pico no mesmo lugar (log é crescente), e a derivada do log zera no pico:
\(\frac{d}{d\theta}\big[m\ln\theta + n\ln(1-\theta)\big] = \frac{m}{\theta} - \frac{n}{1-\theta} = 0\), o que dá \(\theta = \frac{m}{m+n}\).</p></details>
<p>A fórmula vale quando os dois expoentes são positivos. Se um deles é 0, o pico fica na borda: a posterior \(2\theta\), depois de uma cara
com prior plana, tem MAP em \(\theta = 1\).</p>
""" + check(
    r"""<p><b>MAP de cada posterior:</b></p>
<p>\(12\theta^2(1-\theta)\) (prática (b): cara e depois coroa, prior \(2\theta\)): """ + num("2/3", "0.002") + r"""</p>
<p>\(3\theta^2\) (uma cara, prior \(2\theta\)): """ + num("1", "0.002") + "</p>",
    "Isso. 12θ²(1−θ): m = 2, n = 1, pico em 2/3. 3θ² só cresce em [0, 1], então o pico fica na borda, θ = 1.") + r"""
<p>Compare com o <b>MLE</b> (estimativa de máxima verossimilhança): o valor de \(\theta\) que maximiza só a likelihood \(p(x \mid \theta)\),
sem a prior. Para HHT, a likelihood \(\theta^2(1-\theta)\) tem pico em \(2/3\), a fração de caras; o MAP 0.75 ficou acima porque a prior
\(2\theta\) favorece valores altos. O MLE tem lição própria: a <a href="https://claude.ai/artifact/MRMXzP4WVzLVFtDM72Fzks">lição 0000</a>.</p>
""" + mc(
    "Com prior plana f(θ) = 1, o numerador é a própria likelihood. O que isso diz sobre o MAP?",
    [("Coincide com o MLE, o pico da likelihood", True, "Isso: posterior ∝ likelihood × 1. Uma prior não plana desloca o MAP para onde ela põe mais peso."),
     ("Fica em 0.5, o centro da prior plana", False, "A prior plana não tem pico; quem decide o pico é a likelihood."),
     ("Não existe: a prior plana não tem pico", False, "A posterior tem pico mesmo assim: o da likelihood.")])

# ---------------------------------------------------------------- beta
beta = r"""
<p>Escrever uma prior em \([0, 1]\) por extenso dá trabalho. Em geral ela vem só com um nome e dois números, como Beta(2,2). O nome é de uma família de pdfs que o MIT15 define assim:</p>
""" + quote(r"""<p>The beta distribution \(\text{Beta}(a, b)\) is a two-parameter distribution with range \([0, 1]\) and pdf</p>
$$f(\theta) = \frac{(a+b-1)!}{(a-1)!\,(b-1)!}\,\theta^{a-1}(1-\theta)^{b-1}$$
<p>[…] In 18.05 we will stick to integers \(a\) and \(b\) […]</p>""", src("§3", "MIT15")) + r"""
<p>Com as partes nomeadas:</p>
$$f(\theta) = \underbrace{\frac{(a+b-1)!}{(a-1)!\,(b-1)!}}_{\text{constante: faz a área dar 1}}\;\underbrace{\theta^{a-1}(1-\theta)^{b-1}}_{\text{a forma da curva}}$$
<p>\(a\) e \(b\) são dois inteiros positivos que escolhem a forma; a fração na frente só normaliza. Para a <b>Beta(2,2)</b>:</p>
<ul>
<li><b>constante:</b> \(\frac{(2+2-1)!}{(2-1)!\,(2-1)!} = \frac{3!}{1!\,1!} = 6\);</li>
<li><b>forma:</b> \(\theta^{2-1}(1-\theta)^{2-1} = \theta(1-\theta)\);</li>
<li><b>pdf:</b> \(f(\theta) = 6\theta(1-\theta)\). Conferindo a área: \(\int_0^1 (6\theta - 6\theta^2)\,d\theta = 3 - 2 = 1\).</li>
</ul>
<p>Você já viu várias Betas nesta lição, sem o nome:</p>
<table>
<tr><th>na lição</th><th class="num">\(a\)</th><th class="num">\(b\)</th><th>conferindo a constante</th></tr>
<tr><td>prior plana \(1\)</td><td class="num">1</td><td class="num">1</td><td>\(\frac{1!}{0!\,0!} = 1\)</td></tr>
<tr><td>prior \(2\theta\)</td><td class="num">2</td><td class="num">1</td><td>\(\frac{2!}{1!\,0!} = 2\)</td></tr>
<tr><td>\(3\theta^2\), depois de uma cara</td><td class="num">3</td><td class="num">1</td><td>\(\frac{3!}{2!\,0!} = 3\)</td></tr>
<tr><td>\(12\theta^2(1-\theta)\), cara e depois coroa</td><td class="num">3</td><td class="num">2</td><td>\(\frac{4!}{2!\,1!} = 12\)</td></tr>
<tr><td>\(20\theta^3(1-\theta)\), depois de HHT</td><td class="num">4</td><td class="num">2</td><td>\(\frac{5!}{3!\,1!} = 20\)</td></tr>
</table>
<p>Daí sai uma regra que dispensa a integral do total:</p>
""" + quote(r"""<p>If a pdf \(f(\theta)\) with range \([0, 1]\) has the form \(c\,\theta^{a-1}(1-\theta)^{b-1}\) then \(f(\theta)\) is a \(\text{Beta}(a, b)\)
distribution and the normalizing constant must be</p>
$$c = \frac{(a+b-1)!}{(a-1)!\,(b-1)!}.$$
<p>This follows because the constant \(c\) must normalize the pdf to have total probability 1. There is only one such constant and it is given in
the formula for the beta distribution.</p>""", src("§3.1", "MIT15")) + r"""
<p>Ou seja: basta olhar os expoentes. Expoente de \(\theta\) igual a \(a - 1\), expoente de \((1-\theta)\) igual a \(b - 1\), e a constante sai da fórmula.</p>
""" + uso("esta é a fórmula 3.") + r"""
""" + check(
    r"""<p><b>Beta(3,3):</b> \(f(\theta)\) = """ + num("30", "0.01", "3.5rem") + r""" \(\theta\)<sup>""" + num("2", "0.01", "2.6rem")
    + r"""</sup> \((1-\theta)\)<sup>""" + num("2", "0.01", "2.6rem") + r"""</sup></p>
<p><b>Uma pdf da forma \(c\,\theta^4(1-\theta)^2\):</b> é Beta(""" + num("5", "0.01", "2.6rem") + ", " + num("3", "0.01", "2.6rem")
    + r"""), com \(c\) = """ + num("105", "0.01", "3.5rem") + "</p>",
    "Isso. Beta(3,3): 5!/(2!·2!) = 120/4 = 30, forma θ²(1−θ)². E θ⁴(1−θ)² tem a − 1 = 4 e b − 1 = 2, então é Beta(5,3), com c = 7!/(4!·2!) = 5040/48 = 105.") + r"""
<p id="integral-beta"><b>A mesma regra, ao contrário: uma integral sem integrar.</b> Como a área de uma Beta é 1, a constante vezes a integral da forma dá 1:</p>
$$\frac{(a+b-1)!}{(a-1)!\,(b-1)!}\int_0^1 \theta^{a-1}(1-\theta)^{b-1}\,d\theta = 1$$
<p>Passando a constante para o outro lado:</p>
$$\int_0^1 \theta^{a-1}(1-\theta)^{b-1}\,d\theta = \frac{(a-1)!\,(b-1)!}{(a+b-1)!}$$
<p>Ou seja, <b>a integral da forma é o inverso da constante.</b> Exemplo: a tabela acima diz que \(12\theta^2(1-\theta)\) é uma Beta(3,2). Então
\(\int_0^1 \theta^2(1-\theta)\,d\theta = 1/12\), sem fazer conta.</p>
<p>Isso serve em dois lugares:</p>
<ul class="spaced">
<li><b>o total da tabela de Bayes</b>, quando a questão pede \(p(x)\) explicitamente. O numerador quase sempre tem a forma constante × \(\theta^m(1-\theta)^n\);</li>
<li><b>a previsão do próximo dado (fórmula 5).</b> A integral de likelihood × posterior vira um número vezes \(\theta^m(1-\theta)^n\), e essa integral sai daqui.
A <a href="#q23">L03 Q2.3</a> é exatamente isso.</li>
</ul>
<p>O jeito de usar é igual ao da fórmula 3: leia os expoentes, ache \(a\) e \(b\) (expoente + 1) e calcule com os fatoriais. A diferença é que na
fórmula 3 você <b>multiplica</b> pela constante, porque quer a pdf, e aqui você <b>divide</b> por ela, porque quer a área.</p>
"""

# ---------------------------------------------------------------- receita
receita = r"""
<p><b>Passo zero: ler o enunciado.</b> Antes de qualquer fórmula, responda quatro perguntas:</p>
<ol>
<li><b>O que eu não sei?</b> É a <b>hipótese</b>, o \(\theta\).</li>
<li><b>O que eu observei?</b> É o <b>dado</b>.</li>
<li><b>O que eu achava de \(\theta\) antes de observar?</b> É a <b>prior</b>. O enunciado quase sempre diz explicitamente.</li>
<li><b>Se eu já soubesse \(\theta\), qual seria a chance de ver exatamente esse dado?</b> É a <b>likelihood</b>, \(p(\text{dado} \mid \theta)\). Ela vem do
modelo de como o dado é gerado.</li>
</ol>
<p>As quatro questões da L03 seguem esse padrão:</p>
<table>
<tr><th></th><th>o que não sei (\(\theta\))</th><th>o que observei</th><th>prior</th><th>likelihood: "se soubesse \(\theta\)…"</th></tr>
<tr><td><b>Q1</b></td><td>qual dado foi escolhido</td><td>dois 5</td><td>proporção 1:2:10:2:1</td><td>\((1/n)^2\) se o dado tem \(n \ge 5\) faces, senão 0</td></tr>
<tr><td><b>Q2</b></td><td>a fração \(\theta\) que prefere comédia</td><td>6 de 10 preferem</td><td>Beta(2,2)</td><td>Binomial: \(\binom{10}{6}\theta^6(1-\theta)^4\)</td></tr>
<tr><td><b>Q3</b></td><td>o atraso máximo \(\theta\) (1/4 ou 3/4 h)</td><td>atraso de 10 min</td><td>1/2 para cada</td><td>Uniforme[0, \(\theta\)]: \(1/\theta\) se o atraso \(\le \theta\), senão 0</td></tr>
<tr><td><b>Q4</b></td><td>o comprimento \(\theta\) do cabo</td><td>medição \(x = 10\)</td><td>Normal(9, 1)</td><td>Normal(\(\theta\), \(10^{-4}\))</td></tr>
</table>
<p>A Q3 e a Q4 têm dado contínuo; a Q3 vem na lição 0004 (MIT14) e a Q4 na lição 0005 (MIT15). A pista mais segura é a pergunta 4: a likelihood é sempre a chance do
dado <em>fingindo que você já sabe \(\theta\)</em>.</p>
<p>Depois do passo zero, as fórmulas:</p>
<div class="callout"><p>Todo o resto da lição explica por que estas fórmulas funcionam; para resolver as questões, basta isto:</p>
<table>
<tr><th>#</th><th>para quê</th><th>fórmula</th></tr>
<tr><td>1</td><td>likelihood de uma contagem (\(k\) sucessos em \(n\))</td><td>\(p(k \mid \theta) = \binom{n}{k}\theta^k(1-\theta)^{n-k}\)</td></tr>
<tr><td>2</td><td>posterior, a menos da constante</td><td>\(f(\theta \mid x) \propto p(x \mid \theta)\,f(\theta)\): multiplique e some os expoentes</td></tr>
<tr><td>3</td><td>a constante</td><td>se \(f = c\,\theta^{a-1}(1-\theta)^{b-1}\), é Beta(\(a, b\)) e \(c = \frac{(a+b-1)!}{(a-1)!\,(b-1)!}\)<br>(sem essa forma: divida o numerador pela sua integral)</td></tr>
<tr><td>4</td><td>MAP</td><td>ponto de máximo de \(\theta^m(1-\theta)^n\): \(\frac{m}{m+n}\)<br>(discreto: a hipótese com o maior numerador)</td></tr>
<tr><td>5</td><td>previsão do próximo dado</td><td>\(p(x_2 \mid x_1) = \int p(x_2 \mid \theta)\,f(\theta \mid x_1)\,d\theta\)<br>(a integral sai pelo <a href="#integral-beta">inverso da constante da Beta</a>)</td></tr>
</table></div>
<p id="intervalo"><b>Quando a pergunta é um intervalo</b> ("a maioria", "pelo menos 6", \(x_2 \ge 6\)): a fórmula 5 dá a chance de <b>um valor de
cada vez</b>. Então:</p>
<ol class="spaced">
<li><b>liste os valores que contam.</b> "Maioria de 10" é 6, 7, 8, 9 e 10, porque 5 é empate;</li>
<li><b>faça a fórmula 5 para cada um.</b> A posterior é a mesma em todas as contas, e só a likelihood muda com \(k\). Os dois expoentes se movem
juntos: um sobe 1 e o outro desce 1, então o \(a + b - 1\) do fatorial de cima não muda. A integral de cada conta sai pela
<a href="#integral-beta">integral da Beta</a>;</li>
<li><b>some.</b></li>
</ol>
<p>Se o intervalo tiver mais valores do que o lado de fora, use o complemento: \(P(x_2 \ge 6) = 1 - P(x_2 \le 5)\). Faça a conta no lado com menos termos.</p>
"""

# ---------------------------------------------------------------- objetivo
prior_q2 = lambda t: 6 * t * (1 - t)  # noqa: E731
lik_q2 = lambda t: 2310 * t**6 * (1 - t)**4  # noqa: E731  (likelihood rescaled to area 1, for the plot only)
post_q2 = lambda t: 10296 * t**7 * (1 - t)**5  # noqa: E731

objetivo = quote(r"""<p>Foi realizada uma pesquisa com o objetivo de verificar a preferência de um grupo de pessoas com relação ao tipo de filme: ação ou
comédia. Foi escolhida uma amostra aleatória de 10 pessoas desse grupo. Inicialmente, será considerada uma prior \(f(\theta)\) com distribuição
Beta(2,2), onde \(\theta\) é a porcentagem das pessoas que preferem comédia.</p>
<p>1. Seja \(x_1\) o número de pessoas na amostra que preferem comédia. Qual a função probabilidade massa de \(x_1\)?</p>
<p>2. Calcule a posterior de \(\theta\) dado que \(x_1 = 6\). Qual o máximo a posteriori (MAP) de \(\theta\)?</p>
<p>3. É feita uma nova pesquisa com mais dez pessoas. Calcule a posterior predictive probability de que a maioria das pessoas da segunda amostra
prefira comédia.</p>""", f'<a href="{L03}">L03</a>, questão 2', lang="pt-BR") + r"""
<p>Esta lição resolve as três partes. A Q2.1 usa a fórmula 1; a Q2.2 usa as fórmulas 2, 3 e 4; a Q2.3 usa a fórmula 5, com a
<a href="#integral-beta">integral da Beta</a> e a dica de <a href="#intervalo">intervalos</a>.</p>
<p><b>A prior.</b> Pela <a href="#beta">seção anterior</a>, Beta(2,2) é \(6\theta(1-\theta)\): um morro simétrico com pico em 0.5. Antes da
pesquisa, a crença é que o grupo provavelmente está dividido, sem certeza.</p>
<h3 id="q21">Q2.1: a pmf de \(x_1\)</h3>
<p>Cada uma das 10 pessoas prefere comédia com probabilidade \(\theta\), independentemente das outras. Então \(x_1\), o número de pessoas que
preferem comédia, é o número de "sucessos" em 10 tentativas: é <b>Binomial(10, \(\theta\))</b>, como na <a href="#binomial">revisão</a>.
A resposta da Q2.1 é a fórmula 1 com \(n = 10\):</p>
$$p(x_1 \mid \theta) = \binom{10}{x_1}\,\theta^{x_1}(1-\theta)^{10-x_1}, \qquad x_1 = 0, 1, \dots, 10.$$
<p>Ela é a likelihood que a Q2.2 vai usar. Para o dado da Q2.2, \(x_1 = 6\):</p>
""" + check(
    r"""<p>\(p(x_1 = 6 \mid \theta)\) = """ + num("210", "0.01", "4rem") + r""" \(\theta\)<sup>""" + num("6", "0.01", "2.6rem")
    + r"""</sup> \((1-\theta)\)<sup>""" + num("4", "0.01", "2.6rem") + r"""</sup></p>
<p style="font-size:.9rem;color:var(--muted)">As caixas ao lado de \(\theta\) e de \((1-\theta)\) são os expoentes.</p>""",
    "Isso: C(10,6) = 210, com 6 pessoas que preferem comédia e 4 que preferem ação. Repare que, ao contrário de HHT, aqui há coeficiente binomial: o dado é a contagem, não uma sequência específica.") + r"""

<h3 id="q22">Q2.2: a posterior e o MAP</h3>
<p>Agora a tabela de uma linha, com a prior Beta(2,2) e a likelihood da Q2.1. Os passos são os de sempre:</p>
<ul>
<li><b>prior</b> \(f(\theta) = 6\theta(1-\theta)\);</li>
<li><b>likelihood</b> \(p(x_1 = 6 \mid \theta) = 210\,\theta^6(1-\theta)^4\), da Q2.1;</li>
<li><b>numerador</b> \(p(x_1 = 6 \mid \theta)\,f(\theta)\) (fórmula 2): likelihood × prior. Multiplique os números e some os expoentes;</li>
<li><b>posterior</b> \(f(\theta \mid x_1 = 6)\) (fórmula 3): posterior = numerador ÷ total, como na lição 0001. Dividir pelo total só faz a área dar 1: a forma
\(\theta^7(1-\theta)^5\) continua a mesma, e muda só a constante na frente. A fórmula 3 dá essa constante sem integral: compare os expoentes do
numerador com \(a - 1\) e \(b - 1\) e use a constante da Beta;</li>
<li><b>MAP</b> (fórmula 4): o pico do numerador, \(\frac{m}{m+n}\), com \(m\) e \(n\) iguais aos expoentes do numerador.</li>
</ul>
""" + check(
    r"""<table>
<tr><th>hipótese</th><th>prior<br>\(f(\theta)\,d\theta\)</th><th>likelihood (Q2.1)<br>\(p(x_1 \mid \theta)\)</th><th>numerador<br>\(p(x_1 \mid \theta)\,f(\theta)\,d\theta\)</th><th>posterior<br>\(f(\theta \mid x_1)\,d\theta\)</th></tr>
<tr><td>\(\theta \in [0, 1]\)</td><td>\(6\theta(1-\theta)\,d\theta\)</td><td>\(210\,\theta^6(1-\theta)^4\)</td>
<td>""" + num("1260", "0.01", "3.6rem") + r""" \(\theta\)<sup>""" + num("7", "0.01", "2.2rem")
    + r"""</sup><br>\((1-\theta)\)<sup>""" + num("5", "0.01", "2.2rem") + r"""</sup> \(d\theta\)</td>
<td>""" + num("10296", "0.5", "4.2rem") + r""" \(\theta^7(1-\theta)^5\,d\theta\)<br>= Beta(""" + num("8", "0.01", "2.2rem") + ", "
    + num("6", "0.01", "2.2rem") + r""")</td></tr>
<tr><td>total</td><td>1</td><td>não se soma</td><td>\(p(x_1 = 6)\): não precisa calcular,<br>a fórmula 3 dá a constante</td><td>1</td></tr>
</table>
<p><b>MAP:</b> \(\theta_{\text{MAP}}\) = """ + num("7/12", "0.002", "4.5rem") + "</p>",
    f"Isso. Numerador = 210 θ⁶(1−θ)⁴ · 6θ(1−θ) = 1260 θ⁷(1−θ)⁵. Os expoentes 7 e 5 são a − 1 e b − 1, então a posterior é Beta(8,6), "
    f"com constante 13!/(7!·5!) = 10296. O MAP é a fórmula 4 com m = 7 e n = 5: 7/12 ≈ 0.583. "
    f"Confira no <a href='{L03G}'>L03G</a>, questão 2: a solução lá é imagem, então compare com o PDF aberto.") + r"""
<p>A resposta escrita da Q2.2:</p>
$$f(\theta \mid x_1 = 6) = 10296\,\theta^7(1-\theta)^5, \text{ ou seja, Beta}(8, 6)$$
$$\theta_{\text{MAP}} = \frac{7}{12} \approx 0.583$$
<p>Por que 0.583, e não 0.6, a fração observada? O gráfico mostra o cabo de guerra entre prior e likelihood.</p>
""" + pdf_plot(
    [("prior 6θ(1−θ)", prior_q2, MUT, True, 0.01, 2.35),
     ("likelihood (pico em 0.6)", lik_q2, FG, True, 0.01, 2.75),
     ("posterior (pico em 7/12)", post_q2, ACC, False, 0.01, 3.15)],
    marks=[(0.5, prior_q2, "0.5", MUT), (7 / 12, post_q2, "MAP 7/12", ACC)],
    ymax=3.5,
    caption="A likelihood foi reescalada para ter área 1 e caber no mesmo gráfico; isso não muda o pico, que é a fração observada 6/10 (o MLE). "
            "A prior puxa para 0.5, e a posterior fica no meio, em 7/12 ≈ 0.583, mais perto da likelihood porque 10 pessoas pesam mais que a prior. "
            "A altura da posterior usa a constante 10296; o pico não depende dela.") + r"""
<p>A prior Beta(2,2) funciona como se já tivéssemos visto 1 pessoa que prefere comédia e 1 que prefere ação: somando essas "pseudo-observações"
aos dados, ficam 7 e 5, e o MAP é \(7/(7+5)\). A lição 0005 transforma essa leitura numa regra geral.</p>

<h3 id="q23">Q2.3: a maioria na segunda pesquisa</h3>
<p>Seja \(x_2\) o número de pessoas da segunda amostra de 10 que preferem comédia. "A maioria" é \(x_2 \ge 6\), uma pergunta de
<a href="#intervalo">intervalo</a>: faça a fórmula 5 para cada \(k = 6, 7, 8, 9, 10\) e some. Os pesos são a posterior da Q2.2, e a
likelihood de cada \(k\) é a Binomial da Q2.1, agora para a segunda amostra:</p>
$$P(x_2 = k \mid x_1 = 6) = \int_0^1 \binom{10}{k}\theta^k(1-\theta)^{10-k} \cdot 10296\,\theta^7(1-\theta)^5\,d\theta
= \binom{10}{k} \cdot 10296 \int_0^1 \theta^{k+7}(1-\theta)^{15-k}\,d\theta$$
<p>A integral é a forma de uma Beta(\(k+8\), \(16-k\)), sem a constante. Pela <a href="#integral-beta">integral da Beta</a>:</p>
$$\int_0^1 \theta^{k+7}(1-\theta)^{15-k}\,d\theta = \frac{(k+7)!\,(15-k)!}{23!}$$
<p>O 6 de \(x_1 = 6\) e o 6 de \(k = 6\) são coisas diferentes: o primeiro é o dado da primeira pesquisa, que já está dentro da posterior; o
segundo é um resultado possível da segunda.</p>
""" + check(
    r"""<table>
<tr><th class="num">\(k\)</th><th class="num">\(\binom{10}{k}\)</th><th>Beta da integral</th><th class="num">\(P(x_2 = k \mid x_1 = 6)\)</th></tr>
<tr><td class="num">6</td><td class="num">210</td><td>(14, 10)</td><td>""" + num("0.1890", "0.0005", "5rem") + r"""</td></tr>
<tr><td class="num">7</td><td class="num">120</td><td>(15, 9)</td><td>""" + num("0.1680", "0.0005", "5rem") + r"""</td></tr>
<tr><td class="num">8</td><td class="num">45</td><td>(16, 8)</td><td>""" + num("0.1181", "0.0005", "5rem") + r"""</td></tr>
<tr><td class="num">9</td><td class="num">10</td><td>(17, 7)</td><td>""" + num("0.0600", "0.0005", "5rem") + r"""</td></tr>
<tr><td class="num">10</td><td class="num">1</td><td>(18, 6)</td><td>""" + num("0.0170", "0.0005", "5rem") + r"""</td></tr>
<tr><th colspan="3">\(P(x_2 \ge 6 \mid x_1 = 6)\)</th><th>""" + num("0.552", "0.002", "5rem") + r"""</th></tr>
</table>
<details><summary>Dica</summary><p>Para \(k = 6\): \(210 \cdot 10296 \cdot \frac{13!\,9!}{23!}\). A constante da Beta(14, 10) é \(\frac{23!}{13!\,9!} = 11\,440\,660\),
então a conta é \(2\,162\,160 / 11\,440\,660 \approx 0.189\).</p></details>""",
    f"Isso. As cinco parcelas somam 8203/14858 ≈ 0.552. Confira no <a href='{L03G}'>L03G</a>, questão 2.") + r"""
<p>A resposta escrita da Q2.3:</p>
$$P(x_2 \ge 6 \mid x_1 = 6) = \sum_{k=6}^{10} \binom{10}{k} \cdot 10296 \cdot \frac{(k+7)!\,(15-k)!}{23!} = \frac{8203}{14858} \approx 0.552$$
<p>Faz sentido: a posterior tem pico em 7/12, um pouco acima da metade, então a chance de a maioria preferir comédia na próxima amostra fica um
pouco acima de 50%.</p>
"""

# ---------------------------------------------------------------- fontes
fontes = rf"""
<p>O arquivo do <a href="{MIT13}">MIT13</a> tem três partes: a nota <em>Bayesian Updating with Continuous Priors</em>, a nota <em>Notational
conventions</em> e os problemas em sala. Esta lição cobre a nota principal até o §10. O que ficou de fora:</p>
<table>
<tr><th>trecho do MIT13</th><th>por que ficou de fora</th><th>faz falta na P2?</th></tr>
<tr><td>§3, exemplos 2 e 3: tempo de vida exponencial e Normal com parâmetros desconhecidos</td><td>são só exemplos de hipóteses contínuas, sem conta</td><td>não; a Normal volta no MIT14/MIT15 (L03 Q4)</td></tr>
<tr><td>§4 e a nota <em>Notational conventions</em>: letras grandes (\(P(H)\), \(P(D \mid H)\)) e pequenas (\(f(\theta)\), \(p(x \mid \theta)\))</td><td>o quadro <a href="#letras">Qual letra usar</a> resume o essencial</td><td>não; é só notação</td></tr>
<tr><td>§11 (opcional): do discreto ao contínuo, cortando \([0, 1]\) em 4, 8 e 20 hipóteses e vendo os histogramas da prior e da posterior convergirem para a pdf</td><td>é intuição, sem conta nova</td><td>não, mas ajuda se o \(d\theta\) ainda parecer estranho</td></tr>
<tr><td>§9.2, Example 8: probabilidade de um intervalo pela posterior, \(P(\theta > 0.5 \mid x = 1) = \int_{0.5}^1 2\theta\,d\theta = 3/4\)</td><td>nenhuma lista nem prova pede probabilidade de intervalo da posterior</td><td>não; é a mesma conta de área da revisão de pdf</td></tr>
<tr><td>Exemplo em sala 1: três moedas (0.25, 0.5, 0.75) na proporção 1:2:1, duas coroas</td><td>é a tabela discreta da lição 0001</td><td>como treino: posterior de 0.25 dá 0.5</td></tr>
<tr><td>Problema 1(b): descrever um experimento que a prior \(3\theta^2\) modela</td><td>pergunta aberta, sem conta</td><td>não</td></tr>
<tr><td>Problema 2(c): esboçar a prior e as duas posteriores do <em>Bent coin 1</em></td><td>o gráfico de HHT mostra o mesmo efeito</td><td>não</td></tr>
<tr><td>Problema "Bent coin 2": prior plana, 15 caras em 27; escrever a posterior com a constante \(T\) sem calculá-la</td><td>é a mesma ideia da Q2.2, que esta lição faz</td><td>como treino: posterior \(\binom{{27}}{{15}}\theta^{{15}}(1-\theta)^{{12}}/T\), MAP 15/27</td></tr>
</table>
<p>Fica para as próximas lições: a L03 Q3, em que o dado é contínuo (lição 0004, MIT14); a regra de atualização da Beta e a L03 Q4 (lição 0005, MIT15).</p>
<div class="callout">Se ficou alguma dúvida, pergunte ao seu professor, que é o agente nesta conversa. Vale um passo da conta, um termo ou "por que isso funciona?".</div>
<p style="font-size:.8rem;color:var(--muted)">As citações em inglês são de J. Orloff e J. Bloom, <i>18.05 Introduction to Probability and Statistics</i>,
Spring 2022, MIT OpenCourseWare, licença CC BY-NC-SA 4.0. Trechos omitidos aparecem como […]. No texto extraído do PDF do MIT13, os símbolos
matemáticos saíram corrompidos; a prosa é literal, e as fórmulas foram reescritas a partir do contexto.</p>
"""

SPEC = {
    "title": "0003 · Prior contínua e MAP",
    "subtitle": "Lição 0003 · COE241 P2 · MIT13 · hipóteses num contínuo · meta: resolver a L03 Q2 (pmf, posterior, MAP e previsão)",
    "crumbs": f'COE241 · P2 · Lição 0003 &nbsp;·&nbsp; anterior: <a href="{LESSON2}">0002, probabilidade preditiva</a>',
    "sections": [
        {"id": "recordacao", "heading": "Recordação da lição 0002", "html": recordacao},
        {"id": "revisao", "heading": "Revisão da P1: Binomial e pdf", "html": revisao},
        {"id": "continuas", "heading": "Hipóteses num contínuo", "html": continuas},
        {"id": "total", "heading": "Probabilidade total vira integral", "html": total},
        {"id": "tabela", "heading": "A tabela de Bayes com uma linha", "html": tabela},
        {"id": "preditiva", "heading": "Probabilidade preditiva com pdf", "html": preditiva},
        {"id": "map", "heading": "MAP: o pico da posterior", "html": map_},
        {"id": "beta", "heading": "A família Beta", "html": beta},
        {"id": "receita", "heading": "Como resolver: passo zero e as 5 fórmulas", "html": receita},
        {"id": "objetivo", "heading": "O objetivo: L03 Q2", "html": objetivo},
        {"id": "fontes", "heading": "O que ficou de fora do MIT13", "html": fontes},
    ],
    "quiz": [
        {"question": r"A pdf de \(\theta\) vale cerca de \(1.8\) em toda a faixa de \(0.89\) a \(0.91\). Quanto vale \(P(0.89 < \theta < 0.91)\)?",
         "ref": [("pdf", "Densidade (pdf) de uma variável contínua")],
         "options": [
             {"text": r"\(0.036\)", "correct": True, "feedback": r"Isso: probabilidade é área, \(f(\theta)\,d\theta = 1.8 \cdot 0.02\). A densidade pode passar de \(1\); a área não."},
             {"text": r"\(1.8\)", "correct": False, "feedback": r"\(1.8\) é a densidade, não a probabilidade. Probabilidade é área: multiplique pela largura da faixa, \(0.02\)."},
             {"text": r"\(0.018\)", "correct": False, "feedback": r"A largura da faixa é \(0.91 - 0.89 = 0.02\), não \(0.01\). A área é \(1.8 \cdot 0.02 = 0.036\)."}]},
        {"question": r"Moeda torta com prior \(f(\theta) = 2\theta\) em \([0, 1]\). Na tabela de Bayes contínua (uma linha só), a coluna 'total' do numerador é \(p(x) = \int p(x \mid \theta)\,f(\theta)\,d\theta\). No caso discreto, o que fazia esse papel?",
         "ref": [("total", "Probabilidade total vira integral"), ("tabela", "A tabela de Bayes com uma linha")],
         "options": [
             {"text": "A soma dos numeradores", "correct": True, "feedback": "Isso: P(D), que era também a prior predictive. A soma virou integral, e o papel é o mesmo, normalizar e prever."},
             {"text": "A soma das likelihoods", "correct": False, "feedback": r"A coluna das likelihoods não se soma (NO SUM). Somam-se os numeradores, likelihood \(\times\) prior."},
             {"text": "A soma das posteriores", "correct": False, "feedback": r"As posteriores somam \(1\) depois de normalizar. O que normaliza é a soma dos numeradores, \(P(D)\)."}]},
        {"question": r"Prior \(2\theta\), dados HHT (cara, cara, coroa). O numerador é \(2\theta^3(1-\theta)\,d\theta\) e a posterior é \(20\,\theta^3(1-\theta)\). De onde vem o \(20\)?",
         "ref": [("tabela", "A tabela de Bayes com uma linha")],
         "options": [
             {"text": r"De \(2\) dividido por \(p(x) = \frac{1}{10}\)", "correct": True, "feedback": r"Isso: \(p(x) = \int_0^1 2\theta^3(1-\theta)\,d\theta = \frac{1}{10}\), e dividir por ela faz a área da posterior dar \(1\)."},
             {"text": r"De \(2\) vezes o binomial \(\binom{5}{2} = 10\)", "correct": False, "feedback": r"A conta dá \(20\), mas por acaso. Os dados são uma sequência (HHT), sem coeficiente binomial; o \(20\) vem de normalizar: \(2 \div \frac{1}{10}\)."},
             {"text": r"Da área do numerador, que vale \(20\)", "correct": False, "feedback": r"A área do numerador é \(p(x) = \frac{1}{10}\), e não \(20\). Dividir por ela é que multiplica por \(10\): \(2 \cdot 10 = 20\)."}]},
        {"question": r"Para achar o MAP de uma posterior contínua, por que não é preciso calcular a integral \(p(x)\)?",
         "ref": [("map", "MAP: o pico da posterior")],
         "options": [
             {"text": r"\(p(x)\) não depende de \(\theta\): só muda a escala", "correct": True, "feedback": r"Isso: dividir por uma constante muda a altura da curva, não o lugar do pico. Maximize o numerador likelihood \(\times\) prior."},
             {"text": r"\(p(x)\) vale \(1\), pois a posterior integra \(1\)", "correct": False, "feedback": r"Quem integra \(1\) é a posterior, justamente por dividir por \(p(x)\). No exemplo de HHT, \(p(x) = \frac{1}{10}\)."},
             {"text": r"\(p(x)\) é desprezível perto do numerador", "correct": False, "feedback": r"Não é desprezível (no exemplo de HHT, \(\frac{1}{10}\)). Ela é dispensável por outro motivo: não depende de \(\theta\)."}]},
        {"question": r"Na L03 Q2, a prior Beta(2,2) tem pico em \(0.5\), e na amostra \(6\) de \(10\) pessoas preferem comédia, uma fração de \(0.6\). O MAP da posterior é \(\frac{7}{12} \approx 0.583\). Por que ele fica entre \(0.5\) e \(0.6\)?",
         "ref": [("objetivo", "O objetivo: L03 Q2")],
         "options": [
             {"text": r"A prior puxa a \(0.5\); os dados, a \(0.6\)", "correct": True, "feedback": "Isso: a posterior é o produto das duas, e o pico do produto fica entre os dois picos. Com mais dados, o MAP se aproximaria da fração observada."},
             {"text": r"É a média simples de \(0.5\) e \(0.6\)", "correct": False, "feedback": r"A média seria \(0.55\). O MAP \(\frac{7}{12}\) pesa mais os dados (\(10\) pessoas) que a prior (equivale a \(2\))."},
             {"text": "A posterior soma prior e likelihood", "correct": False, "feedback": r"A posterior é o produto, não a soma: \(\theta(1-\theta) \cdot \theta^6(1-\theta)^4 = \theta^7(1-\theta)^5\)."}]},
        {"question": r"Quanto vale \(\int_0^1 \theta^3(1-\theta)^2\,d\theta\), sem expandir o polinômio?",
         "ref": [("integral-beta", "A mesma regra, ao contrário: uma integral sem integrar")],
         "options": [
             {"text": r"\(\frac{3!\,2!}{6!} = \frac{1}{60}\)", "correct": True, "feedback": r"Isso: é a forma da Beta(4, 3), cuja constante é \(\frac{6!}{3!\,2!} = 60\). A integral é o inverso dela."},
             {"text": r"\(\frac{6!}{3!\,2!} = 60\)", "correct": False, "feedback": r"Essa é a constante da Beta(4, 3). A integral da forma é o inverso dela, \(\frac{1}{60}\): a constante vezes a integral dá 1."},
             {"text": r"\(\frac{2!\,1!}{4!} = \frac{1}{12}\)", "correct": False, "feedback": r"Aqui os expoentes foram usados como \(a\) e \(b\). Os expoentes são \(a - 1\) e \(b - 1\): \(a = 4\), \(b = 3\), e a integral é \(\frac{3!\,2!}{6!} = \frac{1}{60}\)."}]},
        {"question": r"L03 Q2.3: numa nova amostra de \(10\) pessoas, quais valores de \(x_2\) contam como 'a maioria prefere comédia'?",
         "ref": [("q23", "Q2.3: a maioria na segunda pesquisa")],
         "options": [
             {"text": r"De \(6\) a \(10\)", "correct": True, "feedback": r"Isso: \(5\) de \(10\) é empate. Faça a fórmula 5 para cada valor de \(6\) a \(10\) e some."},
             {"text": r"De \(5\) a \(10\)", "correct": False, "feedback": r"Com \(5\), metade prefere comédia e metade ação: é empate, não maioria."},
             {"text": r"Só \(x_2 = 6\)", "correct": False, "feedback": r"O \(6\) é o dado da primeira pesquisa. 'A maioria' inclui todos os valores de \(6\) a \(10\), e as cinco chances se somam."}]},
    ],
}

if __name__ == "__main__":
    build(SPEC, ROOT / "lessons" / "0003-prior-continua.html")
