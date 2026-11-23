"""Lesson 0005 source. Build: python lessons/src/0005-priors-conjugadas.py

Quotes from MIT15 and MIT14 are verbatim from the PDF text (MIT OCW 18.05 Spring 2022, CC BY-NC-SA 4.0).
As in MIT13, the extracted text kept the prose clean but garbled the math symbols, so the prose is
quoted word for word and the symbols are restored in LaTeX from context.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "assets"))
from build import build, mc, quote, pdf_plot, slider  # noqa: E402

MIT14 = "https://drive.google.com/file/d/1yuuRlktCwZvKz6AJkkwUYqzc73XvduaC/view"
MIT15 = "https://drive.google.com/file/d/1nkNUeimH00v3suIbVcsD3XPl-17bW-TV/view"
L03 = "https://drive.google.com/file/d/1Nb8V3KKsByciabbw_dcDfaQ2bYXCVeQm/view"
L03G = "https://drive.google.com/file/d/1w1zevZpR8_RlVbkCjUJtHLfsXRE9wRxI/view"
P2 = "https://drive.google.com/file/d/1UC2kRa6K_6zXryQe7irAKbvfMTQh12um/view"
LESSON3 = "https://claude.ai/artifact/Mg37Am6eQ3TsQEvzxY98BT"
LESSON4 = "https://claude.ai/artifact/ULdAerrDUzGftPBWRQvrbC"

ACC, MUT, FG = "var(--accent)", "var(--muted)", "var(--fg)"


def src(where, doc="MIT15"):
    return f'<a href="{ {"MIT14": MIT14, "MIT15": MIT15}[doc] }">{doc}</a>, {where}'


def num(answer, tol="0.002", width=None):
    w = f' style="width:{width}"' if width else ""
    return f'<input data-answer="{answer}" data-tol="{tol}"{w}>'


def check(body, ok):
    return (f'<div class="check-group" data-ok="{ok}">{body}'
            f'<button class="check">Verificar</button><div class="feedback"></div></div>')


def normal(mu, var, scale=8):
    """pdf of N(mu, var) in θ, drawn on the [0, 1] plot axis that shows θ in [0, scale]."""
    return lambda x: math.exp(-(x * scale - mu) ** 2 / (2 * var)) / math.sqrt(2 * math.pi * var)


# ---------------------------------------------------------------- recordação
recordacao = rf"""
<p>Na <a href="{LESSON3}">lição 0003</a> você conheceu a família Beta. Em resumo:</p>
$$\text{{Beta}}(a, b):\quad f(\theta) = \underbrace{{\frac{{(a+b-1)!}}{{(a-1)!\,(b-1)!}}}}_{{\text{{constante}}}}\;\underbrace{{\theta^{{a-1}}(1-\theta)^{{b-1}}}}_{{\text{{forma}}}},\quad 0 \le \theta \le 1$$
<p>E a regra que dispensa a integral: se uma pdf em \([0, 1]\) tem a forma \(c\,\theta^{{a-1}}(1-\theta)^{{b-1}}\), ela é Beta(\(a, b\)), e o \(c\) é a
constante acima. Basta ler os expoentes e somar 1.</p>
""" + check(
    r"""<p>Na L03 Q2.2, a prior era Beta(2,2) e 6 de 10 pessoas preferiram comédia. Prior × likelihood deu o numerador
\(1260\,\theta^7(1-\theta)^5\). Que Beta é a posterior? Beta(""" + num("8", "0.01", "2.6rem")
    + ", " + num("6", "0.01", "2.6rem") + ").</p>",
    "Isso: expoente 7 = a − 1 e expoente 5 = b − 1, então Beta(8, 6). O 1260 não importa: a constante sai da fórmula da Beta.")

# ---------------------------------------------------------------- regra da Beta
regra = r"""
<p>Para chegar à Beta(8, 6) da Q2.2 você multiplicou prior e likelihood, juntou as potências e leu os expoentes. Repare nos números:
\(8 = 2 + 6\) e \(6 = 2 + 4\). O \(a\) da prior ganhou as 6 pessoas que preferem comédia, e o \(b\) ganhou as 4 que preferem ação.
Isso é coincidência?</p>
<p>Não. Faça a conta com letras: prior Beta(\(a, b\)) e \(s\) sucessos e \(f\) fracassos (Binomial). As constantes não importam, porque
a regra da Beta acha a constante no fim:</p>
$$\underbrace{\theta^{a-1}(1-\theta)^{b-1}}_{\text{prior, sem a constante}} \cdot \underbrace{\theta^{s}(1-\theta)^{f}}_{\text{likelihood, sem o }\binom{s+f}{s}}
= \theta^{(a+s)-1}\,(1-\theta)^{(b+f)-1}$$
<p>Os expoentes de potências de mesma base se somam. O resultado tem a forma de uma Beta(\(a + s,\ b + f\)). Como toda posterior
precisa ter área 1, ela é essa Beta. O MIT15 resume assim:</p>
""" + quote(r"""<p>We have seen that if the prior on \(\theta\) is a beta distribution then so is the posterior; only the parameters \(a, b\) of the beta
distribution change!</p>
<table><tr><th>hypothesis</th><th>data</th><th>prior</th><th>likelihood</th><th>posterior</th></tr>
<tr><td>\(\theta\)</td><td>\(x = s, f\)</td><td>Beta(\(a, b\))</td><td>binomial(\(s + f, \theta\))</td><td>Beta(\(a + s, b + f\))</td></tr></table>""",
            src("§3.2")) + r"""
<div class="callout"><p><b>Regra da Beta-Binomial:</b> prior Beta(\(a, b\)) e \(s\) sucessos e \(f\) fracassos dão posterior
Beta(\(a + s,\ b + f\)). <b>Cada sucesso soma 1 em \(a\); cada fracasso soma 1 em \(b\).</b></p></div>
<p>Você já tinha visto isso na tabela da lição 0003: a prior plana é Beta(1, 1), uma cara levou a Beta(2, 1), mais uma cara a Beta(3, 1),
e uma coroa a Beta(3, 2). Era a regra, um dado de cada vez. Por isso dá no mesmo atualizar com tudo junto ou aos poucos: a ordem das somas não importa.</p>
<p>Uma prior é <b>conjugada</b> de uma likelihood quando prior × likelihood dá uma posterior
<b>da mesma família da prior</b>. Aí atualizar vira só trocar os parâmetros, sem integral:</p>
<div class="flow">
<div class="box"><small>prior</small>Beta(\(a, b\))</div><span class="arrow">×</span>
<div class="box plain"><small>likelihood</small>Binomial: \(s\) sucessos, \(f\) fracassos</div><span class="arrow">→</span>
<div class="box"><small>posterior</small>Beta(\(a + s,\ b + f\))</div>
</div>
<div class="flow">
<div class="box"><small>prior</small>Beta(2, 2)</div><span class="arrow">×</span>
<div class="box plain"><small>likelihood</small>6 comédia, 4 ação</div><span class="arrow">→</span>
<div class="box"><small>posterior</small>Beta(8, 6)</div>
</div>
<p class="flow-note">Prior e posterior (borda colorida) são da mesma família, a Beta.</p>
<p>O MIT15 diz o mesmo:</p>
""" + quote(r"""<p>The beta distribution is called a conjugate prior for the binomial distribution. This means that if the likelihood function is binomial,
then a beta prior gives a beta posterior […]</p>
<p>Conjugate priors are useful because they reduce Bayesian updating to modifying the parameters of the prior distribution (so-called
hyperparameters) rather than computing integrals.</p>""", src("§4")) + r"""
<p>(<b>Hiperparâmetros</b> são o \(a\) e o \(b\): os parâmetros da pdf de \(\theta\), "um nível acima" do parâmetro \(\theta\).)</p>
""" + check(
    r"""<p>Depois da Q2.2 (posterior Beta(8, 6)), uma segunda pesquisa encontra 7 de 10 pessoas que preferem comédia. Usando Beta(8, 6) como
prior, a nova posterior é Beta(""" + num("15", "0.01", "2.6rem") + ", " + num("9", "0.01", "2.6rem") + ").</p>",
    "Isso: 8 + 7 = 15 e 6 + 3 = 9. Pelo caminho direto (Beta(2,2) com 13 de 20) dá o mesmo: 2 + 13 = 15 e 2 + 7 = 9.") + r"""
<p>A P2-23.2 cobrou exatamente essa regra:</p>
""" + quote(r"""<p>Seja θ a probabilidade de sair cara para uma moeda defeituosa. Considere a prior de θ a distribuição Beta(6,8). Suponha que você
jogue a moeda 7 vezes, obtendo 2 caras e 5 coroas. Qual a distribuição a posteriori (posterior distribution) f(θ|x)?</p>""",
            f'<a href="{P2}">P2-23.2</a>, questão 4.1', lang="pt-BR") + mc(
    "Qual é a posterior?",
    [("Beta(8, 13)", True, "Isso: 6 + 2 caras = 8 e 8 + 5 coroas = 13."),
     ("Beta(2, 5)", False, "Essa é só a contagem dos dados, sem a prior. A prior Beta(6, 8) entra na soma: Beta(6 + 2, 8 + 5)."),
     ("Beta(11, 10)", False, "Aqui as coroas foram para o a e as caras para o b. Caras (sucessos) somam em a: Beta(6 + 2, 8 + 5).")])

# ---------------------------------------------------------------- revisão da Normal
revisao = r"""
<p>A L03 Q4 troca a Beta pela Normal: a prior e a medição são Normais. Antes, a Normal da P1.</p>
<p>\(X \sim N(\mu, \sigma^2)\) tem pdf</p>
$$f(x) = \underbrace{\frac{1}{\sigma\sqrt{2\pi}}}_{\text{constante: faz a área dar 1}}\;\underbrace{e^{-(x-\mu)^2/(2\sigma^2)}}_{\text{a forma do sino}}$$
<ul class="spaced">
<li>A média \(\mu\) é o centro do sino, onde fica o pico. No expoente, é o número subtraído de \(x\).</li>
<li>A variância \(\sigma^2\) dá a largura. No expoente, o denominador é \(2\sigma^2\), <b>o dobro</b> da variância.</li>
<li>\(N(\mu, \sigma^2)\) leva a variância, e não o desvio padrão \(\sigma\): \(N(2, 9)\) tem desvio padrão 3. Se o enunciado der
o desvio padrão, eleve ao quadrado.</li>
</ul>
<p>Como na Beta, a constante não precisa ser conferida. O MIT15 diz, logo depois da regra da Beta: "A similar observation holds for normal
distributions". Ou seja, toda pdf da forma \(c\,e^{-(\theta-m)^2/k}\) é uma Normal, e média e variância se leem no expoente:</p>
$$c\,e^{-(\theta - m)^2/k} \text{ é } N\!\left(m,\ \tfrac{k}{2}\right) \qquad (\text{porque } k = 2\sigma^2)$$
<p>O MIT14 põe isso entre os objetivos: "Be able to recognize the pdf of a normal distribution and determine its mean and variance."</p>
""" + check(
    r"""<p><b>1.</b> \(f(\theta) = c\,e^{-(\theta-3)^2/8}\): média """ + num("3", "0.01", "3rem") + ", variância " + num("4", "0.01", "3rem") + r"""</p>
<p><b>2.</b> \(f(\theta) = c\,e^{-2(\theta+1)^2}\): média """ + num("-1", "0.01", "3rem") + ", variância " + num("1/4", "0.002", "3rem") + r"""</p>
<details><summary>Dica para o 2</summary><p>Escreva \(2(\theta+1)^2\) como \((\theta-m)^2/k\): \(\theta + 1 = \theta - (-1)\), e multiplicar por 2 é
dividir por \(1/2\). Então \(k = 1/2 = 2\sigma^2\).</p></details>""",
    "Isso. 1: 2σ² = 8, σ² = 4. 2: θ + 1 = θ − (−1), então μ = −1; e 2(θ+1)² = (θ+1)²/(1/2), então 2σ² = 1/2 e σ² = 1/4.")

# ---------------------------------------------------------------- Normal-Normal
ex_prior, ex_post = normal(2, 1), normal(3.5, .5)
nn = r"""
<p>A Beta é conjugada da Binomial. Será que existe uma família assim para medições Normais? Existe, e é a própria Normal:</p>
""" + quote(r"""<p>[…] the normal distribution is its own conjugate prior. In particular, if the likelihood function is normal with known variance, then
a normal prior gives a normal posterior.</p>""", src("§4")) + r"""
<p>"Known variance": a variância \(\sigma^2\) da medição é conhecida; o parâmetro desconhecido \(\theta\) é a média dela. Para ver por que a
posterior é Normal, o MIT14 faz a conta num exemplo:</p>
""" + quote(r"""<p>Suppose we have data \(x = 5\) which was drawn from a normal distribution with unknown mean \(\theta\) and standard deviation 1.
[…] Suppose further, that our prior distribution for the unknown parameter \(\theta\) is \(\theta \sim N(2, 1)\).</p>""", src("§6, exemplo 3", "MIT14")) + r"""
<p>Como na tabela da <a href="{LESSON4}">lição 0004</a>, o numerador é prior × likelihood, agora escrito para um \(\theta\) qualquer. A prior
é a pdf de \(N(2, 1)\) em \(\theta\), e a likelihood é a pdf de \(N(\theta, 1)\) no dado \(x = 5\):</p>
$$\underbrace{\tfrac{1}{\sqrt{2\pi}}\,e^{-(\theta-2)^2/2}}_{\text{prior}} \cdot \underbrace{\tfrac{1}{\sqrt{2\pi}}\,e^{-(5-\theta)^2/2}}_{\text{likelihood}}
= \tfrac{1}{2\pi}\,e^{-\left[(\theta-2)^2 + (5-\theta)^2\right]/2}$$
<p>A pergunta é: <b>esse expoente tem a forma \(-(\theta - m)^2/k\)?</b> Se tiver, é Normal: \(m\) é a média e \(k = 2\sigma^2\), então a variância é \(k/2\). Para
descobrir, <b>completa-se o quadrado</b>, em três passos:</p>
<ol class="spaced">
<li>Expanda os quadrados:
$$\begin{aligned}
(\theta-2)^2 + (5-\theta)^2 &= \theta^2 - 4\theta + 4 + 25 - 10\theta + \theta^2 \\
&= 2\theta^2 - 14\theta + 29
\end{aligned}$$
No expoente, essa soma está dividida por 2:
$$\tfrac{1}{2}\left(2\theta^2 - 14\theta + 29\right) = \theta^2 - 7\theta + \tfrac{29}{2}$$</li>
<li>Complete o quadrado. Para o termo do meio dar \(-7\theta\), \(m = 7/2\):
$$(\theta - m)^2 = \theta^2 - 2m\theta + m^2 \quad\Rightarrow\quad (\theta - \tfrac{7}{2})^2 = \theta^2 - 7\theta + \tfrac{49}{4}$$
Passando o \(\tfrac{49}{4}\) para o outro lado:
$$\theta^2 - 7\theta = (\theta - \tfrac{7}{2})^2 - \tfrac{49}{4}$$
Somando \(\tfrac{29}{2}\) dos dois lados:
$$\begin{aligned}
\theta^2 - 7\theta + \tfrac{29}{2} &= (\theta - \tfrac{7}{2})^2 - \tfrac{49}{4} + \tfrac{29}{2} \\
&= (\theta - \tfrac{7}{2})^2 + \tfrac{9}{4}
\end{aligned}$$</li>
<li>Mande a sobra para a constante:
$$e^{-[(\theta - 7/2)^2 + 9/4]} = e^{-9/4} \cdot e^{-(\theta - 7/2)^2}$$
O \(e^{-9/4}\) não tem \(\theta\): vai para a constante, como o coeficiente binomial na Beta. Sobra
$$\text{numerador} = c\,e^{-(\theta - 7/2)^2} = c\,e^{-(\theta - 7/2)^2/1}$$
Os 4 de \(\tfrac{49}{4}\) e \(\tfrac{9}{4}\) não são denominador do expoente: o \(\tfrac{9}{4}\) foi para a constante.</li>
</ol>
""".replace("{LESSON4}", LESSON4) + mc(
    r"A posterior é \(c\,e^{-(\theta-7/2)^2}\). Qual é a variância dela?",
    [(r"\(1/2\), porque \(2\sigma^2 = 1\)", True, r"Isso: o denominador do expoente é \(1 = 2\sigma^2\), então \(\sigma^2 = 1/2\). A posterior é \(N(7/2, 1/2)\)."),
     (r"\(1\), porque \(\sigma^2 = 1\)", False, r"O denominador do expoente é \(2\sigma^2\), e não \(\sigma^2\). Com \(2\sigma^2 = 1\), \(\sigma^2 = 1/2\)."),
     (r"\(2\), porque \(\sigma^2 = 2 \cdot 1\)", False, r"Aqui o \(2\) multiplicou o denominador, mas o denominador já é \(2\sigma^2\): \(2\sigma^2 = 1\), então \(\sigma^2 = 1/2\).")]) + quote(
    r"""<p>We can see by the form of the posterior pdf that it is a normal distribution. Because the exponential for a normal distribution is
\(e^{-(\theta-\mu)^2/2\sigma^2}\) we have mean \(\mu = 7/2\) and \(2\sigma^2 = 1\), so variance \(\sigma^2 = 1/2\).</p>""", src("§6, exemplo 3", "MIT14")) + pdf_plot(
    [("prior N(2, 1)", ex_prior, MUT, True, .02, .45), ("posterior N(7/2, 1/2)", ex_post, ACC, False, .5, .62)],
    "Prior centrada em 2 e dado x = 5: a posterior fica em 3.5 e é mais estreita que a prior, porque o dado reduziu a incerteza sobre θ.",
    ymax=.7, xscale=8, marks=[(5 / 8, lambda x: .5, "dado x = 5", FG, "ur")]) + quote(
    r"""<p>Note how the data ‘pulls’ the prior […] towards the data. […] After collecting data, we have a new opinion about the mean, and we are more
sure of this new opinion.</p>""", src("§6", "MIT14"))

# ---------------------------------------------------------------- atalho
atalho = r"""
<p>Completar o quadrado sempre funciona, mas é trabalhoso. Como a posterior é sempre Normal, o MIT15 faz a conta uma vez, com letras, e
entrega as fórmulas, que dão o mesmo resultado que completar o quadrado. Para \(n\) medições \(x_1, \dots, x_n\), cada uma \(N(\theta, \sigma^2)\), com média \(\bar{x}\), e prior
\(N(\mu_{\text{prior}}, \sigma^2_{\text{prior}})\):</p>
$$a = \frac{1}{\sigma^2_{\text{prior}}}, \qquad b = \frac{n}{\sigma^2}, \qquad
\mu_{\text{post}} = \frac{a\,\mu_{\text{prior}} + b\,\bar{x}}{a + b}, \qquad \sigma^2_{\text{post}} = \frac{1}{a + b}$$
<p class="uso" style="font-size:.85rem;color:var(--muted)">MIT15 §7.3, fórmulas (4). Com uma medição só, \(n = 1\) e \(\bar{x} = x\) (fórmulas (2) do §7).
Os nomes \(a\) e \(b\) são do MIT15 e não têm relação com os parâmetros da Beta.</p>
<p>Como ler:</p>
<ul class="spaced">
<li>\(a\) e \(b\) são <b>pesos</b>: o inverso de uma variância mede a certeza. Prior estreita → \(a\) grande. Medições precisas ou muitas → \(b\) grande.</li>
<li>\(\mu_{\text{post}}\) é a <b>média ponderada</b> da média da prior e da média dos dados, com esses pesos. Fica sempre entre as duas,
mais perto de quem pesa mais.</li>
<li>\(\sigma^2_{\text{post}}\) é o inverso da soma das certezas. Ela é menor que \(\sigma^2_{\text{prior}}\) e que \(\sigma^2/n\): a posterior sabe
mais que a prior e mais que os dados sozinhos.</li>
</ul>
""" + quote(r"""<ol><li>Lots of data has a big influence on the posterior.</li>
<li>High certainty (low variance) in the prior has a big influence on the posterior.</li></ol>
<p>The actual posterior is a balance of these two influences.</p>""", src("§7.3")) + check(
    r"""<p><b>Confira no exemplo do MIT14</b> (prior \(N(2, 1)\), \(\sigma^2 = 1\), \(x = 5\)):
\(a\) = """ + num("1", "0.01", "3rem") + r", \(b\) = " + num("1", "0.01", "3rem") + r", \(\mu_{\text{post}}\) = " + num("3.5", "0.01", "3.5rem")
    + r", \(\sigma^2_{\text{post}}\) = " + num("0.5", "0.01", "3.5rem") + "</p>",
    "Isso: a = b = 1, então os pesos são iguais e μpost = (2 + 5)/2 = 3.5, σ²post = 1/2. É o N(7/2, 1/2) do quadrado completado.") + r"""
<p>Veja o equilíbrio mudar. Os valores iniciais são os do exemplo do MIT14: prior \(N(2, 1)\), \(\sigma^2 = 1\), uma medição \(x = 5\).</p>
<div class="playground">
<div class="controls">
""" + "\n".join([slider("mp", r"\(\mu_{\text{prior}}\)", 0, 10, 0.5, 2), slider("vp", r"\(\sigma^2_{\text{prior}}\)", 0.25, 4, 0.25, 1),
                 slider("s2", r"\(\sigma^2\)", 0.5, 4, 0.25, 1), slider("n", r"\(n\)", 1, 10, 1, 1),
                 slider("xb", r"\(\bar{x}\)", 0, 10, 0.5, 5)]) + r"""
</div>
<div class="plot-stack">
<svg class="plot" data-legend="posterior|prior" data-xlabel="θ" data-ylabel="densidade f(θ)" data-fn="normal(x, (mp/vp + n*xb/s2)/(1/vp + n/s2), 1/(1/vp + n/s2))" data-x="0 10" data-y="0 2" role="img" aria-label="Posterior Normal"></svg>
<svg class="plot second" data-fn="normal(x, mp, vp)" data-x="0 10" data-y="0 2" aria-hidden="true"></svg>
</div>
</div>
$$a = \frac{1}{\live{vp}} = \live{1/vp}, \qquad b = \frac{\live{n}}{\live{s2}} = \live{n/s2}$$
$$\mu_{\text{post}} = \frac{\live{1/vp} \cdot \live{mp} + \live{n/s2} \cdot \live{xb}}{\live{1/vp + n/s2}} = \live{(mp/vp + n*xb/s2)/(1/vp + n/s2)},
\qquad \sigma^2_{\text{post}} = \frac{1}{\live{1/vp + n/s2}} = \live{1/(1/vp + n/s2)}$$
<div class="stats">
<div class="stat"><div class="stat-label">peso dos dados, \(\frac{b}{a+b}\)</div><div class="stat-value" data-expr="Math.round(100*(n/s2)/(1/vp + n/s2)) + '%'"></div></div>
<div class="stat"><div class="stat-label">\(\sigma^2_{\text{post}}\) vs. \(\sigma^2_{\text{prior}}\)</div><div class="stat-value" data-expr="(1/(1/vp + n/s2)).toFixed(3) + ' < ' + vp"></div></div>
</div>
<p>Aumente o \(n\) ou diminua o \(\sigma^2\): a posterior corre para \(\bar{x}\) e afina. Diminua o \(\sigma^2_{\text{prior}}\): ela fica presa
perto de \(\mu_{\text{prior}}\).</p>
"""

# ---------------------------------------------------------------- objetivo
objetivo = quote(r"""<p>Suponha que você tenha um cabo cujo tamanho exato é θ. Você tem uma régua que possui um erro com distribuição Normal de média 0 e
variância 10<sup>−4</sup>. Usando esta régua, você mede seu cabo, e a medição resultante x tem distribuição Normal com média θ e variância 10<sup>−4</sup>.</p>
<ol><li>Suponha que a sua prior para o comprimento do cabo θ seja uma variável aleatória Normal com média 9 e variância 1. Se você medir e obtiver
x = 10, qual é a posterior de θ?</li>
<li>Com a mesma prior do item anterior, calcule o número total de medições necessárias de modo que a variância da posterior de θ seja menor que
10<sup>−6</sup>.</li></ol>""", f'<a href="{L03}">L03</a>, questão 4', lang="pt-BR") + r"""
<p>A hipótese é o comprimento \(\theta\). A medição é \(x = \theta + \text{erro}\), com erro \(N(0, 10^{-4})\), então
\(x \sim N(\theta, 10^{-4})\): é a likelihood, com variância conhecida \(\sigma^2 = 10^{-4}\). A prior é \(N(9, 1)\). É o caso Normal-Normal.</p>
<h3>Q4.1: uma medição</h3>
<p>A medição é \(x = 10\). Pode digitar frações (por exemplo, 1/3).</p>
""" + check(
    r"""<p>\(a = 1/\sigma^2_{\text{prior}}\) = """ + num("1", "0.001", "4rem") + r""" &nbsp; \(b = 1/\sigma^2\) = """ + num("10000", "0.5", "5rem") + r"""</p>
<p>\(\mu_{\text{post}}\) = """ + num("100009/10001", "0.00005", "7rem") + r""" &nbsp; \(\sigma^2_{\text{post}}\) = """ + num("1/10001", "0.000000001", "7rem") + "</p>",
    f"Isso: b = 1/10⁻⁴ = 10⁴. μpost = (1·9 + 10⁴·10)/(1 + 10⁴) = 100009/10001 ≈ 9.9999; σ²post = 1/10001 ≈ 9.999 × 10⁻⁵. "
    f"Confira no <a href='{L03G}'>L03G</a>, questão 4 (a solução é imagem; compare com o PDF aberto).") + r"""
<p>A resposta escrita:</p>
$$\theta \mid x = 10 \;\sim\; N\!\left(\frac{9 + 10^5}{1 + 10^4},\ \frac{1}{1 + 10^4}\right) \approx N(9.9999,\ 0.9999 \times 10^{-4})$$
<p>A média fica quase em 10 porque a régua pesa \(b/a = 10\,000\) vezes mais que a prior: ela erra uns \(\sigma = 0.01\), enquanto a prior
só dizia "9, mais ou menos 1". A variância fica um pouco abaixo da da régua (\(10^{-4}\)), porque o peso da prior também entra em \(a + b\).</p>
<h3>Q4.2: quantas medições</h3>
<p>Com \(n\) medições, só o \(b\) muda: \(b = n/\sigma^2 = n \cdot 10^4\). A variância da posterior é</p>
$$\sigma^2_{\text{post}} = \frac{1}{1 + n \cdot 10^4}$$
<p>Ela não depende dos valores medidos, só de quantos são. Por isso dá para responder antes de medir.</p>
""" + check(
    r"""<p>Menor \(n\) com \(\sigma^2_{\text{post}} < 10^{-6}\): """ + num("100", "0.01", "4rem") + r"""</p>
<details><summary>Dica</summary><p>\(\frac{1}{1 + n \cdot 10^4} < 10^{-6}\) é o mesmo que \(1 + n \cdot 10^4 > 10^6\). Isole o \(n\) e lembre
que ele é inteiro.</p></details>""",
    f"Isso: n > (10⁶ − 1)/10⁴ = 99.9999, então n = 100 medições no total (a primeira inclusa). Com 99, σ²post = 1/990001, que passa de 10⁻⁶. "
    f"Confira no <a href='{L03G}'>L03G</a>, questão 4.") + r"""
<p>Com isso a L03 está toda feita: Q1 nas lições 0001 e 0002, Q2 na 0003, Q3 na 0004 e Q4 aqui.</p>
"""

# ---------------------------------------------------------------- receita
receita = r"""
<div class="callout"><p>Priors conjugadas: a posterior sai trocando os parâmetros da prior, sem integral.</p>
<ol class="spaced">
<li><b>Beta + Binomial</b> (contagem de sucessos, \(\theta \in [0, 1]\)): prior Beta(\(a, b\)), \(s\) sucessos e \(f\) fracassos.
\[\text{posterior} = \text{Beta}(a + s,\ b + f)\]</li>
<li><b>Normal + Normal</b> (medição com variância \(\sigma^2\) conhecida, \(\theta\) = média): leia \(\mu_{\text{prior}}\), \(\sigma^2_{\text{prior}}\),
\(\sigma^2\), \(n\) e \(\bar{x}\). Depois:
\[a = \frac{1}{\sigma^2_{\text{prior}}}, \qquad b = \frac{n}{\sigma^2}\]
\[\mu_{\text{post}} = \frac{a\,\mu_{\text{prior}} + b\,\bar{x}}{a + b}, \qquad \sigma^2_{\text{post}} = \frac{1}{a + b}\]</li>
<li><b>Variância, e não desvio padrão:</b> \(N(\mu, \sigma^2)\). Se vier \(\sigma\), eleve ao quadrado antes.</li>
<li><b>Sem a fórmula:</b> multiplique prior e likelihood, complete o quadrado no expoente e leia:
\[c\,e^{-(\theta-m)^2/k} \ \text{ é } \ N\!\left(m, \tfrac{k}{2}\right)\]</li>
<li><b>Conferência:</b> \(\mu_{\text{post}}\) fica entre \(\mu_{\text{prior}}\) e \(\bar{x}\).
\(\sigma^2_{\text{post}}\) é menor que \(\sigma^2_{\text{prior}}\) e menor que \(\sigma^2/n\).</li>
</ol></div>
"""

# ---------------------------------------------------------------- fontes
fontes = rf"""
<p>Esta lição usou do <a href="{MIT15}">MIT15</a> a regra da Beta-Binomial (§3.2), a definição de prior conjugada (§4) e as fórmulas Normal-Normal (§7);
do <a href="{MIT14}">MIT14</a>, o exemplo 3 do §6 (completar o quadrado). O que ficou de fora:</p>
<table>
<tr><th>trecho</th><th>faz falta na P2?</th><th>por que ficou de fora</th></tr>
<tr><td>MIT15 §3 e §3.1: a pdf da Beta e a constante</td><td>sim, na lição 0003</td><td>já estão na lição 0003 (só recordados aqui)</td></tr>
<tr><td>MIT15 §5.2: Beta com likelihood Bernoulli</td><td>coberto pela regra</td><td>é a Binomial com \(n = 1\): um sucesso soma 1 em \(a\), um fracasso soma 1 em \(b\)</td></tr>
<tr><td>MIT15 §5.3 e exemplo 3: likelihood Geométrica (Mario e Luigi)</td><td>não</td><td>nenhuma lista usa; a ideia é que likelihoods proporcionais dão a mesma posterior</td></tr>
<tr><td>MIT15 §6: tabela com hipótese e dado contínuos</td><td>não</td><td>é a tabela da lição 0004 com o total virando integral; a conjugação dispensa a integral</td></tr>
<tr><td>MIT15 §7: a prova das fórmulas Normal-Normal</td><td>não</td><td>o MIT deixa para o problem set; é o mesmo completar o quadrado, com letras</td></tr>
<tr><td>MIT15 §7.3, exemplo 7: atualizar uma medição de cada vez</td><td>não</td><td>dá o mesmo que usar \(n\) e \(\bar{{x}}\) de uma vez (fórmulas (4))</td></tr>
<tr><td>MIT15, problemas de aula 1(c, d): previsão com prior Beta</td><td>sim, na lição 0003</td><td>é a fórmula 5 e a integral da Beta da lição 0003 (L03 Q2.3)</td></tr>
<tr><td>MIT14 §6, exemplo 4: o mesmo exemplo com \(x\) genérico</td><td>não</td><td>repete o exemplo 3 com letras</td></tr>
</table>
<div class="callout">Se ficou alguma dúvida, pergunte ao seu professor, que é o agente nesta conversa. Vale um passo da conta, um termo ou "por que isso funciona?".</div>
<p style="font-size:.8rem;color:var(--muted)">As citações em inglês são de J. Orloff e J. Bloom, <i>18.05 Introduction to Probability and Statistics</i>,
Spring 2022, MIT OpenCourseWare, licença CC BY-NC-SA 4.0. Trechos omitidos aparecem como […]. No texto extraído dos PDFs do MIT14 e do MIT15, os
símbolos matemáticos saíram corrompidos; a prosa é literal, e as fórmulas foram reescritas a partir do contexto.</p>
"""

SPEC = {
    "title": "0005 · Priors conjugadas",
    "subtitle": "Lição 0005 · COE241 P2 · MIT15 e MIT14 §6 · Beta-Binomial e Normal-Normal · meta: resolver a L03 Q4",
    "crumbs": f'COE241 · P2 · Lição 0005 &nbsp;·&nbsp; anterior: <a href="{LESSON4}">0004, likelihood contínua</a>',
    "sections": [
        {"id": "recordacao", "heading": "Recordação: a família Beta", "html": recordacao},
        {"id": "regra", "heading": "A regra da Beta: somar caras e coroas", "html": regra},
        {"id": "normal", "heading": "Revisão da P1: a Normal", "html": revisao},
        {"id": "normal-normal", "heading": "Prior Normal e dado Normal: completar o quadrado", "html": nn},
        {"id": "atalho", "heading": "O atalho: média ponderada", "html": atalho},
        {"id": "objetivo", "heading": "O objetivo: L03 Q4", "html": objetivo},
        {"id": "receita", "heading": "Como resolver", "html": receita},
        {"id": "fontes", "heading": "O que ficou de fora do MIT15 e do MIT14", "html": fontes},
    ],
    "quiz": [
        {"question": r"A prior de \(\theta\) é Beta(3, 5). Você joga a moeda 6 vezes e sai 4 caras e 2 coroas. Qual é a posterior?",
         "ref": [("regra", "A regra da Beta: somar caras e coroas")],
         "options": [
             {"text": "Beta(7, 7)", "correct": True, "feedback": r"Isso: \(3 + 4 = 7\) e \(5 + 2 = 7\)."},
             {"text": "Beta(4, 2)", "correct": False, "feedback": r"Essa é só a contagem dos dados. A prior entra na soma: Beta(\(3 + 4,\ 5 + 2\))."},
             {"text": "Beta(6, 6)", "correct": False, "feedback": r"O numerador é \(\theta^6(1-\theta)^6\), mas os expoentes são \(a - 1\) e \(b - 1\): Beta(7, 7)."}]},
        {"question": r"Uma posterior tem a forma \(c\,e^{-(\theta-4)^2/6}\). Qual distribuição é essa?",
         "ref": [("normal", "Revisão da P1: a Normal")],
         "options": [
             {"text": r"\(N(4, 3)\)", "correct": True, "feedback": r"Isso: o denominador é \(2\sigma^2 = 6\), então \(\sigma^2 = 3\)."},
             {"text": r"\(N(4, 6)\)", "correct": False, "feedback": r"O denominador do expoente é \(2\sigma^2\), e não \(\sigma^2\): \(\sigma^2 = 6/2 = 3\)."},
             {"text": r"\(N(4, 12)\)", "correct": False, "feedback": r"É para dividir o denominador por 2, e não multiplicar: \(2\sigma^2 = 6\) dá \(\sigma^2 = 3\)."}]},
        {"question": r"Prior \(N(0, 1)\) e uma medição \(x = 4\) com variância \(\sigma^2 = 1/3\). Qual é a média da posterior?",
         "ref": [("atalho", "O atalho: média ponderada")],
         "options": [
             {"text": r"\(3\)", "correct": True, "feedback": r"Isso: \(a = 1\), \(b = 3\), \(\mu_{\text{post}} = (0 + 3 \cdot 4)/4 = 3\)."},
             {"text": r"\(2\)", "correct": False, "feedback": r"Essa é a média simples de 0 e 4. Os pesos são \(a = 1\) e \(b = 3\): \((0 + 12)/4 = 3\)."},
             {"text": r"\(4\)", "correct": False, "feedback": r"Esse é o dado sozinho. A prior também pesa: \((1 \cdot 0 + 3 \cdot 4)/(1 + 3) = 3\)."}]},
        {"question": r"Na L03 Q4.2, por que dá para calcular o número de medições antes de medir?",
         "ref": [("objetivo", "O objetivo: L03 Q4")],
         "options": [
             {"text": r"\(\sigma^2_{\text{post}}\) não usa os valores medidos", "correct": True, "feedback": r"Isso: \(\sigma^2_{\text{post}} = 1/(a + b)\), e \(b = n/\sigma^2\) só depende de quantas medições."},
             {"text": r"\(\mu_{\text{post}}\) não usa os valores medidos", "correct": False, "feedback": r"A média usa: \(\bar{x}\) está na fórmula. Quem não usa é \(\sigma^2_{\text{post}} = 1/(a + b)\)."},
             {"text": r"\(\sigma^2_{\text{post}}\) é igual a \(\sigma^2\) da régua", "correct": False, "feedback": r"\(\sigma^2_{\text{post}} = 1/(1 + n \cdot 10^4)\), menor que \(10^{-4}\). Ela só não depende dos valores medidos."}]},
    ],
}

if __name__ == "__main__":
    build(SPEC, ROOT / "lessons" / "0005-priors-conjugadas.html")
