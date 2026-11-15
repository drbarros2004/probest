"""Lesson 0000 source. Build: python lessons/src/0000-mle.py

Quotes from MIT10 (Maximum Likelihood Estimates) are verbatim from the PDF text (MIT OCW 18.05 Spring 2022,
CC BY-NC-SA 4.0). The extracted text kept the prose clean but garbled the math symbols, so the prose is
quoted word for word and the formulas are restored in LaTeX from context. The LMLE problems are quoted from
the list PDF (an image; transcribed by hand). Answers checked against LMLEG and MEX2G problems 5 to 9.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "assets"))
from build import build, mc, quote, pdf_plot  # noqa: E402

MIT10 = "https://drive.google.com/file/d/1KlxN6zAnv-MLnhpaTUvTBKVZ5aame8yM/view"
LMLE = "https://drive.google.com/file/d/17yRyo--qjCsMfsi2MPj322gUagn193bd/view"
LMLEG = "https://drive.google.com/file/d/1ZyJsivcY8yYgSM0Ull_rAWnWQEcg6D7X/view"
LESSON1 = "https://claude.ai/artifact/XWsvKr4dXaFPnc1BAz6Wxa"
LESSON3 = "https://claude.ai/artifact/Mg37Am6eQ3TsQEvzxY98BT"

ACC, MUT, FG = "var(--accent)", "var(--muted)", "var(--fg)"


def src(where):
    return f'<a href="{MIT10}">MIT10</a>, {where}'


def lmle(n):
    return f'<a href="{LMLE}">LMLE</a>, problema {n}'


def num(answer, tol="0.002", width=None):
    w = f' style="width:{width}"' if width else ""
    return f'<input data-answer="{answer}" data-tol="{tol}"{w}>'


def uso(text):
    return f'<p class="uso"><b>Na prova:</b> {text} (<a href="#receita">as 4 fórmulas</a>)</p>'


def check(body, ok):
    return (f'<div class="check-group" data-ok="{ok}">{body}'
            f'<button class="check">Verificar</button><div class="feedback"></div></div>')


# ---------------------------------------------------------------- diagnóstico
diagnostico = r"""
<p>Antes de qualquer explicação, tente dois problemas da LMLE <b>sem consultar nada</b>, no papel. Não importa acertar: o objetivo é
descobrir em que passo você trava, para ler só a parte da lição que cobre esse passo.</p>
""" + quote(r"""<p><b>6. (a)</b> A coin is tossed 100 times and lands heads 62 times. What is the maximum likelihood estimate for \(\theta\) the
probability of heads.</p>
<p><b>(b)</b> A coin is tossed \(n\) times and lands heads \(k\) times. What is the maximum likelihood estimate for \(\theta\) the probability of
heads.</p>
<p><b>8.</b> Suppose data \(x_1, \dots, x_n\) is drawn from an exponential distribution \(\exp(\lambda)\). Find the maximum likelihood for \(\lambda\).</p>""",
            f'<a href="{LMLE}">LMLE</a>, problemas 6 e 8') + r"""
<p>Em cada problema, tente três passos:</p>
<ol>
<li>escrever a <b>likelihood</b>, a chance dos dados como função do parâmetro;</li>
<li>tirar o <b>log</b> dela;</li>
<li><b>derivar</b>, igualar a zero e isolar o parâmetro.</li>
</ol>
<p>Depois confira:</p>
""" + check(r"""<p><b>6 (a):</b> \(\hat\theta\) = """ + num("0.62", "0.002") + "</p>",
            "Isso: 62/100. A seção do MLE mostra por que a resposta é a fração de caras.") + mc(
    "6 (b): qual é o MLE de θ com k caras em n lançamentos?",
    [("θ̂ = k / n", True, "Isso: a fração de caras, como na (a)."),
     ("θ̂ = n / k", False, "Isso passa de 1 (n ≥ k), e θ é uma probabilidade. Veja a seção do MLE."),
     ("θ̂ = 1 / k", False, "Com mais caras, θ̂ deveria subir, não descer. Veja a seção do MLE.")]) + mc(
    "8: qual é o MLE de λ para n dados de uma exp(λ)? (x̄ é a média dos dados.)",
    [("λ̂ = 1 / x̄", True, "Isso: n / (x₁ + … + xₙ), o inverso da média dos dados."),
     ("λ̂ = n / x̄", False, "Sobra um n: a derivada do log dá n/λ = n·x̄. Veja a seção de dados independentes."),
     ("λ̂ = x̄ / n", False, "Veja a seção de dados independentes: a derivada do log dá n/λ − (x₁ + … + xₙ) = 0.")]) + r"""
<p>Onde você travou decide o que ler:</p>
<table>
<tr><th>travei em…</th><th>leia</th></tr>
<tr><td>escrever a likelihood da 6 (o que é, de que é função)</td><td><a href="#mle">O MLE</a></td></tr>
<tr><td>a pdf da exponencial, ou regras de log e derivada</td><td><a href="#revisao">Revisão da P1</a></td></tr>
<tr><td>juntar \(x_1, \dots, x_n\) numa likelihood só, na 8</td><td><a href="#iid">Dados independentes</a></td></tr>
<tr><td>nada: acertei os três</td><td>pule para <a href="#borda">Sem derivada</a>, o que a 6 e a 8 não testam</td></tr>
</table>
"""

# ---------------------------------------------------------------- MLE
L55 = math.lgamma(102) - math.lgamma(56) - math.lgamma(46)  # log of the constant that gives theta^55 (1-theta)^45 area 1


def lik55(t):
    if t <= 0 or t >= 1:
        return 0.0
    return math.exp(L55 + 55 * math.log(t) + 45 * math.log(1 - t))


mle = r"""
<p>Um <b>parâmetro</b> é o número que fixa uma distribuição: a chance de cara \(\theta\) de uma moeda, por exemplo. Na estatística, os dados
são conhecidos e o parâmetro não. O MIT10 propõe um jeito de estimar o parâmetro a partir dos dados:</p>
""" + quote(r"""<p>There are many methods for estimating unknown parameters from data. We will first consider the maximum likelihood estimate
(MLE), which answers the question:</p>
<p>For which parameter value does the observed data have the biggest probability?</p>""", src("§3")) + quote(
    r"""<p><b>Example 1.</b> A coin is flipped 100 times. Given that there were 55 heads, find the maximum likelihood estimate for the
probability \(p\) of heads on a single toss.</p>
<p>[…] For a given value of \(p\), the probability of getting 55 heads in this experiment is the binomial probability</p>
$$P(55 \text{ heads}) = \binom{100}{55} p^{55}(1-p)^{45}.$$
<p>The probability of getting 55 heads depends on the value of \(p\), so let’s include \(p\) in by using the notation of conditional
probability:</p>
$$P(55 \text{ heads} \mid p) = \binom{100}{55} p^{55}(1-p)^{45}.$$
<p>[…] <b>Likelihood</b>, or likelihood function: this is \(P(\text{data} \mid p)\). Note it is a function of both the data and the
parameter \(p\). […]</p>
<p><b>Definition:</b> Given data the maximum likelihood estimate (MLE) for the parameter \(p\) is the value of \(p\) that maximizes the
likelihood \(P(\text{data} \mid p)\). That is, the MLE is the value of \(p\) for which the data is most likely.</p>""", src("§3, Example 1")) + r"""
<p>O MIT10 chama de \(p\) o que a LMLE chama de \(\theta\); daqui em diante, \(\theta\). A fórmula da likelihood é a pmf da Binomial
(<a href="#dists">revisão</a>, se precisar). O que muda é a leitura: os dados (55 caras) ficam <em>fixos</em> e \(\theta\) varia. Avaliando em
alguns valores:</p>
<ul>
<li>\(\theta = 0.5\): \(P(55 \text{ caras} \mid 0.5) = \binom{100}{55}0.5^{100} \approx 0.0485\);</li>
<li>\(\theta = 0.55\): \(P(55 \text{ caras} \mid 0.55) \approx 0.0800\);</li>
<li>\(\theta = 0.7\): \(P(55 \text{ caras} \mid 0.7) \approx 0.0006\).</li>
</ul>
<p>O MLE, escrito \(\hat\theta\), é o \(\theta\) em que essa função chega ao máximo:</p>
""" + pdf_plot(
    [("likelihood θ⁵⁵(1−θ)⁴⁵ (reescalada)", lik55, ACC, False, 0.62, 6.5)],
    marks=[(0.55, lik55, "máximo em 0.55", ACC)],
    caption="A likelihood de 55 caras em 100, como função de θ. Ela foi multiplicada por uma constante para caber no gráfico; "
            "isso muda a altura, não o lugar do máximo. Ela vale 0 em θ = 0 e em θ = 1 (com θ = 0 nunca sai cara; com θ = 1 nunca sai coroa).") + r"""
<p><b>Como achar o máximo.</b> Onde a curva tem um pico liso, a derivada é zero. Derivar \(\theta^{55}(1-\theta)^{45}\) direto exige a regra do
produto; o MIT10 mostra um atalho:</p>
""" + quote(r"""<p>It is often easier to work with the natural log of the likelihood function. For short this is simply called the log likelihood.
Since \(\ln(x)\) is an increasing function, the maxima of the likelihood and log likelihood coincide.</p>""", src("§3.1")) + r"""
<p>"Crescente" quer dizer que, se \(a > b\), então \(\ln a > \ln b\): o \(\theta\) que dá a maior likelihood dá também o maior log. E o log
troca produtos e potências por somas, que são fáceis de derivar. Os passos para 55 caras:</p>
<ul>
<li><b>likelihood</b> \(L(\theta) = \binom{100}{55}\theta^{55}(1-\theta)^{45}\);</li>
<li><b>log</b> \(\ln L(\theta) = \ln\binom{100}{55} + 55\ln\theta + 45\ln(1-\theta)\);</li>
<li><b>derivada</b> \(\frac{d}{d\theta}\ln L = \frac{55}{\theta} - \frac{45}{1-\theta}\) (a constante \(\ln\binom{100}{55}\) some ao derivar);</li>
<li><b>igualar a zero:</b> \(\frac{55}{\theta} = \frac{45}{1-\theta}\), então \(55(1-\theta) = 45\theta\), então \(55 = 100\theta\), e \(\hat\theta = 0.55\).</li>
</ul>
<p><b>Conferir que é máximo.</b> A derivada zero pode ser um mínimo. O MIT10 sugere olhar as bordas:</p>
""" + quote(r"""<p>Officially we need to check that this critical point is actually the maximum. We could use the second derivative test. Another way
is to notice that we are interested only in \(0 \le p \le 1\); that the probability is bigger than zero for \(0 < p < 1\); and that the
probability is equal to zero for \(p = 0\) and for \(p = 1\). From these facts it follows that the critical point must be the unique
maximum.</p>""", src("§3, Note 3")) + r"""
<p>Ou seja: a função começa em 0, fica positiva, volta a 0. Se a derivada só zera num ponto, esse ponto é o topo.</p>
""" + uso("os passos são as fórmulas 1 a 3. Na prova, escreva likelihood, log, derivada = 0 e uma frase sobre as bordas.") + check(
    r"""<p><b>A moeda foi lançada 80 vezes e deu 49 caras.</b></p>
<p>\(\ln L(\theta) = \ln\binom{80}{49}\) + """ + num("49", "0.01", "3rem") + r""" \(\ln\theta\) + """ + num("31", "0.01", "3rem")
    + r""" \(\ln(1-\theta)\) &nbsp;&nbsp; \(\hat\theta\) = """ + num("49/80", "0.002", "4.5rem") + "</p>",
    "Isso: 49/θ − 31/(1−θ) = 0 dá 49(1−θ) = 31θ, θ̂ = 49/80 ≈ 0.6125. Com k caras em n, o mesmo cálculo dá k/n: é a 6 (b).")

# ---------------------------------------------------------------- revisão P1
revisao = r"""
<p>Ferramentas da P1 que aparecem nas contas de MLE. Leia só o que estiver enferrujado.</p>
<h3 id="dists">As quatro distribuições desta lição</h3>
<p>Uma <b>pmf</b> (função de massa) dá \(P(X = x)\) para uma variável discreta. Uma <b>pdf</b> (densidade) \(f(x)\) faz o mesmo papel para
uma variável contínua, mas \(f(x)\) não é probabilidade: probabilidade é área sob a curva.</p>
<table>
<tr><th>distribuição</th><th>o que conta</th><th>pmf ou pdf</th><th>exemplo</th></tr>
<tr><td>Binomial(\(n, \theta\))</td><td>caras em \(n\) lançamentos</td><td>\(\binom{n}{k}\theta^k(1-\theta)^{n-k}\)</td><td>2 caras em 3, \(\theta = 0.6\): \(3 \cdot 0.6^2 \cdot 0.4 = 0.432\)</td></tr>
<tr><td>Geométrica(\(p\))</td><td>tentativas até o 1º sucesso, contando ele</td><td>\((1-p)^{x-1}\,p\), \(x = 1, 2, \dots\)</td><td>FFFFS: \(x = 5\), \((1-p)^4 p\)</td></tr>
<tr><td>Uniforme discreta 1..\(N\)</td><td>um inteiro sorteado de 1 a \(N\)</td><td>\(1/N\) se \(1 \le x \le N\), senão 0</td><td>\(N = 6\) (um dado): \(P(4) = 1/6\), \(P(9) = 0\)</td></tr>
<tr><td>Exponencial(\(\lambda\))</td><td>tempo de espera, \(x \ge 0\)</td><td>pdf \(\lambda e^{-\lambda x}\); média \(1/\lambda\)</td><td>\(\lambda = 0.5\): \(f(2) = 0.5\,e^{-1} \approx 0.184\)</td></tr>
</table>
<p>Na Geométrica, as \(x - 1\) falhas (F) vêm antes do sucesso (S), e cada uma tem chance \(1 - p\). O \(\binom{n}{k}\) da Binomial ("\(n\) escolhe
\(k\)") é o número de jeitos de escolher \(k\) itens entre \(n\): \(\binom{n}{k} = \frac{n!}{k!\,(n-k)!}\), por exemplo \(\binom{3}{2} = 3\).</p>

<h3 id="logs">Regras de log e de derivada</h3>
<p>\(\ln\) é o log natural (base \(e\)). As regras usadas nas derivadas abaixo:</p>
<ul>
<li>\(\ln(ab) = \ln a + \ln b\): produto vira soma;</li>
<li>\(\ln(a^k) = k\ln a\): o expoente desce, por exemplo \(\ln\theta^{55} = 55\ln\theta\);</li>
<li>\(\ln(e^{u}) = u\), por exemplo \(\ln e^{-13\lambda} = -13\lambda\);</li>
<li>\(\frac{d}{d\theta}\ln\theta = \frac{1}{\theta}\) e \(\frac{d}{d\theta}\ln(1-\theta) = -\frac{1}{1-\theta}\) (o sinal vem da derivada de dentro, \(-1\));</li>
<li>a derivada de uma constante é 0, e a de \(c\,\lambda\) é \(c\).</li>
</ul>
""" + check(
    r"""<p>\(\ln\big(\theta^3(1-\theta)^2\big) = \) """ + num("3", "0.01", "3rem") + r""" \(\ln\theta \;+\) """ + num("2", "0.01", "3rem")
    + r""" \(\ln(1-\theta)\) &nbsp;&nbsp; a derivada \(\frac{3}{\theta} - \frac{2}{1-\theta}\) zera em \(\theta\) = """ + num("3/5", "0.002", "4.5rem") + "</p>",
    "Isso: 3(1−θ) = 2θ dá θ = 3/5. Repare no sinal de menos que vem de ln(1−θ).")

# ---------------------------------------------------------------- iid
iid = r"""
<p>Na 6, o dado é uma contagem só. Na 8, são \(n\) números \(x_1, \dots, x_n\), cada um de uma exponencial. Dados <b>i.i.d.</b>
(independentes e identicamente distribuídos) são observações que não influenciam umas às outras e vêm da mesma distribuição.
Para eles, o MIT10 dá a regra:</p>
""" + quote(r"""<p>For multiple independent data points, the likelihood is the product of the individual likelihoods.</p>""",
            src("problemas em sala, Problem 2")) + r"""
<p>É a regra da P1 para eventos independentes, \(P(A \cap B) = P(A)\,P(B)\). Com dados contínuos, entra a pdf no lugar da pmf:</p>
""" + quote(r"""<p>For continuous distributions, we use the probability density function to define the likelihood.</p>
<p><b>Example 3. Light bulbs</b> Suppose that the lifetime of Badger brand light bulbs is modeled by an exponential distribution with
(unknown) parameter \(\lambda\). We test 5 bulbs and find they have lifetimes of 2, 3, 1, 3, and 4 years, respectively. What is the MLE for
\(\lambda\)?</p>""", src("§3.2")) + r"""
<p>A solução, nos mesmos passos da seção do MLE:</p>
<ul>
<li><b>likelihood de uma lâmpada</b> \(f(x_i \mid \lambda) = \lambda e^{-\lambda x_i}\);</li>
<li><b>likelihood das cinco</b> (produto): \(L(\lambda) = \lambda e^{-2\lambda} \cdot \lambda e^{-3\lambda} \cdot \lambda e^{-1\lambda} \cdot \lambda e^{-3\lambda} \cdot \lambda e^{-4\lambda} = \lambda^5 e^{-13\lambda}\).
Os cinco \(\lambda\) viram \(\lambda^5\); os expoentes de \(e\) se somam, e \(2 + 3 + 1 + 3 + 4 = 13\);</li>
<li><b>log</b> \(\ln L = 5\ln\lambda - 13\lambda\);</li>
<li><b>derivada = 0:</b> \(\frac{5}{\lambda} - 13 = 0\), então \(\hat\lambda = \frac{5}{13} \approx 0.385\).</li>
</ul>
<p>O \(\hat\lambda\) é o inverso da média dos dados, \(13/5 = 2.6\) anos: a média de uma exp(\(\lambda\)) é \(1/\lambda\), e o MLE escolhe a
exponencial cuja média é a média observada. Conferir as bordas: com \(\lambda \to 0\), \(\lambda^5 \to 0\); com \(\lambda\) grande,
\(e^{-13\lambda} \to 0\). A likelihood começa e termina em 0, então o ponto da derivada zero é o máximo.</p>
<p><b>Por que a pdf, se ela não é probabilidade?</b> A chance de uma lâmpada durar perto de \(x\) é \(f(x)\,dx\), com \(dx\) uma largura minúscula
(a precisão da medida). A chance dos dados seria \(L(\lambda)\,dx_1 \cdots dx_5\), e os \(dx\) não dependem de \(\lambda\): não mudam onde fica
o máximo. Por isso o MIT10 (§4) os descarta e usa só a pdf.</p>
""" + uso("é a fórmula 1 (produto) seguida da 2 (log vira soma).") + r"""
<p>Com \(n\) dados genéricos, a soma \(2 + 3 + 1 + 3 + 4\) vira \(x_1 + \dots + x_n\), que se escreve \(\sum x_i\). A média dos dados é
\(\bar x = \frac{\sum x_i}{n}\), e por isso \(\sum x_i = n\bar x\).</p>
<p><b>A 8, com \(n\) dados.</b> Os mesmos passos, com letras:</p>
<ul>
<li><b>likelihood</b> \(L(\lambda) = \lambda e^{-\lambda x_1} \cdots \lambda e^{-\lambda x_n} = \lambda^n e^{-\lambda \sum x_i}\);</li>
<li><b>log</b> \(\ln L = n\ln\lambda - \lambda\sum x_i\);</li>
<li><b>derivada = 0:</b> \(\frac{n}{\lambda} - \sum x_i = 0\), então \(\hat\lambda = \frac{n}{\sum x_i} = \frac{1}{\bar x}\).</li>
</ul>
"""

# ---------------------------------------------------------------- sem derivada
borda = r"""
<p>Até aqui o caminho foi sempre o mesmo: escrever a likelihood, derivar e igualar a zero. Isso só funciona se o parâmetro puder variar
continuamente. E se ele for inteiro, como o \(N\) de um sorteio entre 1 e \(N\)? Não existe derivada em \(N\). Além disso, a likelihood vale
zero para todo \(N\) menor que o maior dado, então nem há um pico liso para procurar. O MIT10 resolve um caso parecido, com a Uniforme
contínua \(U(a, b)\):</p>
""" + quote(r"""<p><b>Example 5. Uniform distributions</b> Suppose our data \(x_1, \dots, x_n\) are independently drawn from a uniform distribution
\(U(a, b)\). Find the MLE for \(a\) and \(b\).</p>
<p><b>Solution:</b> This example is different from the previous ones in that we won’t use calculus to find the MLE. The density for
\(U(a, b)\) is \(\frac{1}{b-a}\) on \([a, b]\). Therefore our likelihood function is</p>
$$f(x_1, \dots, x_n \mid a, b) = \begin{cases} \left(\frac{1}{b-a}\right)^n & \text{if all } x_i \text{ are in the interval } [a, b] \\ 0 & \text{otherwise.} \end{cases}$$
<p>This is maximized by making \(b - a\) as small as possible. The only restriction is that the interval \([a, b]\) must include all the data.
Thus the MLE for the pair \((a, b)\) is</p>
$$\hat a = \min(x_1, \dots, x_n), \qquad \hat b = \max(x_1, \dots, x_n).$$""", src("§3.2, Example 5")) + r"""
<p>A ideia, para a Uniforme 1..\(N\): com dados 1, 3, 7, a likelihood é \((1/N)^3\) se \(N \ge 7\), e 0 se \(N < 7\) (com \(N = 6\), tirar
um 7 é impossível). Avaliando:</p>
<table>
<tr><th class="num">\(N\)</th><th class="num">likelihood \(L(N)\)</th><th>por quê</th></tr>
<tr><td class="num">6</td><td class="num">0</td><td>o 7 não cabe em 1..6</td></tr>
<tr><td class="num">7</td><td class="num">\(1/343 \approx 0.00292\)</td><td>\((1/7)^3\), o maior valor</td></tr>
<tr><td class="num">8</td><td class="num">\(1/512 \approx 0.00195\)</td><td>\((1/8)^3\)</td></tr>
<tr><td class="num">9</td><td class="num">\(1/729 \approx 0.00137\)</td><td>\((1/9)^3\)</td></tr>
</table>
<p>Onde a likelihood é positiva, ela só diminui com \(N\). Então o máximo fica no <b>menor \(N\) permitido</b>, que é o maior dado:
\(\hat N = \max(x_i)\). Com qualquer \(N\) acima disso, cada dado fica "diluído" entre mais valores possíveis.</p>
""" + uso("é a fórmula 4.") + check(
    r"""<p><b>Dados 4, 9, 2 de uma Uniforme 1..\(N\):</b> \(L(9)\) = """ + num("1/729", "0.00005", "5rem")
    + r""" &nbsp;&nbsp; \(L(8)\) = """ + num("0", "0.00001", "3rem") + r""" &nbsp;&nbsp; \(\hat N\) = """ + num("9", "0.01", "3rem") + "</p>",
    "Isso: (1/9)³ = 1/729; com N = 8 o 9 é impossível; o máximo fica em N = 9.")

# ---------------------------------------------------------------- receita
receita = r"""
<div class="callout"><p>Para resolver a LMLE, basta isto:</p>
<table>
<tr><th>#</th><th>passo</th><th>fórmula</th></tr>
<tr><td>1</td><td>likelihood de dados independentes</td><td>\(L(\theta) = p(x_1 \mid \theta) \cdots p(x_n \mid \theta)\)<br>(pmf se o dado é discreto, pdf se é contínuo)</td></tr>
<tr><td>2</td><td>log</td><td>\(\ln L(\theta) = \ln p(x_1 \mid \theta) + \dots + \ln p(x_n \mid \theta)\)</td></tr>
<tr><td>3</td><td>parâmetro contínuo</td><td>\(\frac{d}{d\theta}\ln L = 0\), isole \(\theta\);<br>confira que \(L\) cai a 0 (ou diminui) nas bordas</td></tr>
<tr><td>4</td><td>sem derivada (inteiro, ou \(L = 0\) numa faixa)</td><td>tabele \(L\) em alguns valores e veja para onde cresce;<br>Uniforme: menor valor permitido, \(\max(x_i)\)</td></tr>
</table></div>
<p>As pmfs e a pdf estão na <a href="#dists">tabela da revisão</a>.</p>
"""

# ---------------------------------------------------------------- objetivo
objetivo = r"""
<p>A 6 e a 8 estão resolvidas no <a href="#mle">MLE</a> e em <a href="#iid">dados independentes</a>. Faltam três. Tente cada uma antes de abrir a
solução.</p>
<h3 id="p7">Problema 7: Uniforme discreta</h3>
""" + quote(r"""<p><b>7.</b> Suppose the data set \(y_1, \dots, y_n\) is a drawn from a random sample consisting of i.i.d. discrete uniform distributions
with range 1 to \(N\). Find the maximum likelihood estimate of \(N\).</p>""", lmle(7)) + mc(
    "Qual é o MLE de N?",
    [("N̂ = max(yᵢ)", True, "Isso: é a fórmula 4. L(N) = (1/N)ⁿ se N ≥ max(yᵢ), e 0 se N < max(yᵢ)."),
     ("N̂ = min(yᵢ)", False, "Com N = min(yᵢ), os dados maiores seriam impossíveis: L = 0."),
     ("N̂ = Σ yᵢ", False, "Com N = Σyᵢ a likelihood é positiva, mas (1/N)ⁿ é maior com um N menor.")]) + r"""
<details><summary>Solução escrita</summary>
<ul>
<li><b>likelihood</b> (fórmula 1): cada \(y_i\) tem chance \(1/N\) se \(y_i \le N\), então \(L(N) = (1/N)^n\) se \(N \ge \max(y_i)\), e \(L(N) = 0\) se \(N < \max(y_i)\);</li>
<li><b>máximo</b> (fórmula 4): \((1/N)^n\) diminui com \(N\), então o máximo fica no menor \(N\) permitido: \(\hat N = \max(y_i)\).</li>
</ul></details>

<h3 id="p9">Problema 9: Geométrica</h3>
""" + quote(r"""<p><b>9.</b> Suppose \(x_1, \dots, x_n\) is a data set drawn from a geometric(\(1/a\)) distribution. Find the maximum likelihood estimate
of \(a\). Here, geometric(\(p\)) means the probability of success is \(p\) and we run trials until the first success and report the total
number of trials, including the success. For example, the sequence \(FFFFS\) is 4 failures followed by a success, which produces
\(x = 5\).</p>""", lmle(9)) + r"""
<p>Com \(p = 1/a\), a pmf da <a href="#dists">revisão</a> fica \(p(x_i \mid a) = \left(1 - \frac{1}{a}\right)^{x_i - 1}\frac{1}{a} = \left(\frac{a-1}{a}\right)^{x_i-1}\frac{1}{a}\).
Monte a likelihood dos \(n\) dados, tire o log e derive. Para conferir sem ver a solução, aplique o seu resultado a três dados:</p>
""" + check(
    r"""<p><b>Dados 2, 5, 3 de uma geometric(\(1/a\)):</b> \(\sum x_i - n\) = """ + num("7", "0.01", "3rem")
    + r""" &nbsp;&nbsp; \(\hat a\) = """ + num("10/3", "0.002", "4.5rem") + "</p>",
    "Isso: 10 − 3 = 7, e â = 10/3 ≈ 3.33, a média dos dados.") + r"""
<details><summary>Solução escrita</summary>
<ul>
<li><b>likelihood</b> (fórmula 1): multiplicando as \(n\) pmfs, os expoentes \(x_i - 1\) se somam em \(\sum x_i - n\), e os \(n\) fatores \(1/a\) viram \((1/a)^n\):
$$L(a) = \left(\frac{a-1}{a}\right)^{\sum x_i - n}\left(\frac{1}{a}\right)^n$$</li>
<li><b>log</b> (fórmula 2): \(\ln L = \left(\sum x_i - n\right)\big(\ln(a-1) - \ln a\big) - n\ln a\);</li>
<li><b>derivada</b> (fórmula 3): \(\frac{d}{da}\ln L = \left(\sum x_i - n\right)\left(\frac{1}{a-1} - \frac{1}{a}\right) - \frac{n}{a}\);</li>
<li><b>simplificar:</b> \(\frac{1}{a-1} - \frac{1}{a} = \frac{a - (a-1)}{a(a-1)} = \frac{1}{a(a-1)}\);</li>
<li><b>igualar a zero:</b> \(\frac{\sum x_i - n}{a(a-1)} = \frac{n}{a}\). Multiplicando por \(a(a-1)\): \(\sum x_i - n = n(a-1) = na - n\), então \(\sum x_i = na\) e \(\hat a = \frac{\sum x_i}{n} = \bar x\).</li>
</ul>
<p>Faz sentido: a média de uma Geométrica(\(p\)) é \(1/p = a\), e o MLE escolhe \(a\) igual à média observada.</p></details>

<h3 id="p10">Problema 10: o tamanho da turma</h3>
""" + quote(r"""<p><b>10.</b> You want to estimate the size of an MIT class that is closed to visitors. You know that the students are numbered from 1
to \(n\), where \(n\) is the number of students. You call three random students out of the classroom and ask for their numbers, which turn out
to be 1, 3, 7. Find the maximum likelihood estimate for \(n\). (Hint: the student #’s are drawn from a discrete uniform distribution.)</p>""",
                   lmle(10)) + r"""
<p>Aqui \(n\) é o parâmetro (o tamanho da turma), não o número de dados. Três alunos <em>diferentes</em> saem da sala, então o sorteio é sem
reposição: há \(\binom{n}{3}\) trios possíveis, todos com a mesma chance. O trio {1, 3, 7} é um deles se \(n \ge 7\).</p>
""" + check(
    r"""<table>
<tr><th class="num">\(n\)</th><th class="num">\(\binom{n}{3}\)</th><th class="num">likelihood \(L(n)\)</th></tr>
<tr><td class="num">6</td><td class="num">20</td><td>""" + num("0", "0.00001", "4.5rem") + r"""</td></tr>
<tr><td class="num">7</td><td>""" + num("35", "0.01", "4.5rem") + r"""</td><td>""" + num("1/35", "0.0005", "4.5rem") + r"""</td></tr>
<tr><td class="num">8</td><td>""" + num("56", "0.01", "4.5rem") + r"""</td><td>""" + num("1/56", "0.0005", "4.5rem") + r"""</td></tr>
</table>
<p><b>MLE:</b> \(\hat n\) = """ + num("7", "0.01", "3rem") + "</p>",
    "Isso. Com n = 6 o aluno 7 não existe; de 7 em diante L(n) = 1/C(n,3) só diminui, então n̂ = 7 (fórmula 4).") + r"""
<p>O LMLEG usa essa likelihood, \(1/\binom{n}{3} = \frac{3!}{n(n-1)(n-2)}\). Se você tratar os três sorteios como independentes e com
reposição, como no problema 7, a likelihood vira \((1/n)^3\), que também só diminui a partir de 7: a resposta é a mesma.</p>
<p>Confira as cinco respostas com o <a href="{LMLEG}">LMLEG</a>: 6 (a) 62/100; 6 (b) \(k/n\); 7 \(\max(y_i)\); 8 \(1/\bar x\); 9 \(\bar x\); 10 \(n = 7\).</p>
""".replace("{LMLEG}", LMLEG)

# ---------------------------------------------------------------- fontes
fontes = rf"""
<p><b>Ligação com a lição 0003.</b> Na <a href="{LESSON3}">lição 0003</a>, o MAP faz o mesmo cálculo com a prior junto: maximiza
likelihood × prior em vez de só a likelihood. Com prior plana, MAP = MLE.</p>
<p>O arquivo do <a href="{MIT10}">MIT10</a> tem duas notas (<em>Introduction to Statistics</em> e <em>Maximum Likelihood Estimates</em>) e os
problemas em sala. Leitura recomendada: a nota do MLE, §3 e §4. O que ficou de fora:</p>
<table>
<tr><th>trecho do MIT10</th><th>faz falta na P2?</th></tr>
<tr><td><em>Introduction to Statistics</em>: fases da estatística, o caso Sally Clark, revisão de Bayes</td><td>só a definição de <b>estatística</b> (§2.4): "anything that can be computed from the collected data". \(\bar x\) é uma estatística; \(\lambda\) não é</td></tr>
<tr><td>Example 4: MLE da Normal, \(\hat\mu = \bar x\) e \(\hat\sigma^2 = \frac{{1}}{{n}}\sum(x_i - \bar x)^2\)</td><td>pode cair; usa derivadas parciais, com os mesmos passos</td></tr>
<tr><td>Example 6 (captura e recaptura) e Example 7 (Hardy-Weinberg)</td><td>não; o 6 é a mesma ideia sem derivada da turma</td></tr>
<tr><td>§4: por que usar a densidade (o \(dx\) que não depende do parâmetro)</td><td>não; está resumido em <a href="#iid">dados independentes</a></td></tr>
<tr><td>§5 apêndice: propriedades do MLE</td><td>não; o próprio MIT10 diz "will not be on any exams"</td></tr>
<tr><td>Problema em sala 1 (a): três moedas (1/3, 1/2, 2/3), 49 caras em 80; MLE entre hipóteses discretas</td><td>como treino: calcule a likelihood de cada moeda e escolha a maior; dá 2/3</td></tr>
</table>
<div class="callout">Se ficou alguma dúvida, pergunte ao seu professor, que é o agente nesta conversa: um passo da conta, um termo ou "por que isso funciona?".</div>
<p style="font-size:.8rem;color:var(--muted)">As citações em inglês são de J. Orloff e J. Bloom, <i>18.05 Introduction to Probability and Statistics</i>,
Spring 2022, MIT OpenCourseWare, licença CC BY-NC-SA 4.0, e da lista de MLE da Profª Rosa Leão (COE241). Trechos omitidos aparecem como […].
No texto extraído do PDF do MIT10, os símbolos matemáticos saíram corrompidos; a prosa é literal, e as fórmulas foram reescritas a partir do contexto.</p>
"""

SPEC = {
    "title": "0000 · Máxima verossimilhança (MLE)",
    "subtitle": "Lição 0000 · COE241 P2 · MIT10 · meta: resolver a LMLE inteira (problemas 6 a 10)",
    "crumbs": f'COE241 · P2 · Lição 0000 &nbsp;·&nbsp; próxima: <a href="{LESSON1}">0001, tabela de atualização bayesiana</a>',
    "sections": [
        {"id": "diagnostico", "heading": "Diagnóstico: tente antes", "html": diagnostico},
        {"id": "mle", "heading": "O MLE: o parâmetro que torna os dados mais prováveis", "html": mle},
        {"id": "revisao", "heading": "Revisão da P1: distribuições, log e derivada", "html": revisao},
        {"id": "iid", "heading": "Dados independentes: produto, e soma no log", "html": iid},
        {"id": "borda", "heading": "Sem derivada: parâmetro inteiro", "html": borda},
        {"id": "receita", "heading": "As 4 fórmulas", "html": receita},
        {"id": "objetivo", "heading": "O objetivo: LMLE 7, 9 e 10", "html": objetivo},
        {"id": "fontes", "heading": "Ligação com a 0003 e o que ficou de fora do MIT10", "html": fontes},
    ],
    "quiz": [
        {"question": r"Uma moeda deu \(49\) caras em \(80\) lançamentos, e o MLE de \(\theta\) é \(\frac{49}{80}\). O que esse valor maximiza?",
         "ref": [("mle", "O MLE")],
         "options": [
             {"text": r"\(p(\text{dados} \mid \theta)\), como função de \(\theta\)", "correct": True, "feedback": r"Isso: os dados ficam fixos e \(\theta\) varia."},
             {"text": r"\(p(\theta \mid \text{dados})\), como função de \(\theta\)", "correct": False, "feedback": "Essa é a posterior, que precisa de uma prior (lição 0003). O MLE usa só a likelihood."},
             {"text": r"\(p(\text{dados})\), somada em todo \(\theta\)", "correct": False, "feedback": r"Essa é a probabilidade total, que nem depende de \(\theta\)."}]},
        {"question": r"Por que se maximiza \(\ln L(\theta)\) em vez de \(L(\theta)\)?",
         "ref": [("mle", "O MLE"), ("logs", "Regras de log")],
         "options": [
             {"text": r"\(\ln\) cresce, e produto vira soma", "correct": True, "feedback": "Isso: o máximo fica no mesmo lugar, e a derivada fica fácil."},
             {"text": r"\(\ln\) muda o máximo para dentro", "correct": False, "feedback": r"Como \(\ln\) é crescente, o máximo não muda de lugar."},
             {"text": r"\(\ln\) deixa a likelihood sempre positiva", "correct": False, "feedback": r"O log de um número entre \(0\) e \(1\) é negativo. O ganho é trocar produto por soma."}]},
        {"question": r"Cinco lâmpadas com vida \(\text{exp}(\lambda)\) duraram \(2\), \(3\), \(1\), \(3\) e \(4\) anos. Qual é o MLE de \(\lambda\)?",
         "ref": [("iid", "Dados independentes")],
         "options": [
             {"text": r"\(\hat\lambda = \frac{5}{13}\)", "correct": True, "feedback": r"Isso: \(L = \lambda^5 e^{-13\lambda}\), e a derivada do log é \(\frac{5}{\lambda} - 13 = 0\)."},
             {"text": r"\(\hat\lambda = \frac{13}{5}\)", "correct": False, "feedback": r"\(\frac{13}{5}\) é a média dos dados; \(\hat\lambda\) é o inverso dela."},
             {"text": r"\(\hat\lambda = \frac{1}{13}\)", "correct": False, "feedback": r"São \(5\) lâmpadas: o expoente de \(\lambda\) é \(5\), e a derivada dá \(\frac{5}{\lambda}\)."}]},
        {"question": r"Dados \(2\), \(9\) e \(4\) de uma Uniforme discreta \(1, \dots, N\). Qual é o MLE de \(N\)?",
         "ref": [("borda", "Sem derivada")],
         "options": [
             {"text": r"\(\hat N = 9\)", "correct": True, "feedback": r"Isso: \(L(N) = \left(\frac{1}{N}\right)^3\) só para \(N \ge 9\), e diminui com \(N\)."},
             {"text": r"\(\hat N = 5\)", "correct": False, "feedback": r"Com \(N = 5\), o \(9\) seria impossível: \(L(5) = 0\)."},
             {"text": r"\(\hat N = 15\)", "correct": False, "feedback": r"\(L(15) = \left(\frac{1}{15}\right)^3\) é positiva, mas menor que \(L(9) = \left(\frac{1}{9}\right)^3\)."}]},
    ],
}

if __name__ == "__main__":
    build(SPEC, ROOT / "lessons" / "0000-mle.html")
