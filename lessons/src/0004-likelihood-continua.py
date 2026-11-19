"""Lesson 0004 source. Build: python lessons/src/0004-likelihood-continua.py

Quotes from MIT14 are verbatim from the PDF text (MIT OCW 18.05 Spring 2022, CC BY-NC-SA 4.0).
As in MIT13, the extracted text kept the prose clean but garbled the math symbols, so the prose is
quoted word for word and the symbols are restored in LaTeX from context.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "assets"))
from build import build, mc, quote, pdf_plot, bayes_table, slider  # noqa: E402

MIT14 = "https://drive.google.com/file/d/1yuuRlktCwZvKz6AJkkwUYqzc73XvduaC/view"
L03 = "https://drive.google.com/file/d/1Nb8V3KKsByciabbw_dcDfaQ2bYXCVeQm/view"
L03G = "https://drive.google.com/file/d/1w1zevZpR8_RlVbkCjUJtHLfsXRE9wRxI/view"
LESSON0 = "https://claude.ai/artifact/MRMXzP4WVzLVFtDM72Fzks"
LESSON1 = "https://claude.ai/artifact/XWsvKr4dXaFPnc1BAz6Wxa"
LESSON3 = "https://claude.ai/artifact/Mg37Am6eQ3TsQEvzxY98BT"
LESSON5 = "https://claude.ai/artifact/2WoxChPHPSesBbiDpU4ZJ8"

ACC, MUT = "var(--accent)", "var(--muted)"


def src(where):
    return f'<a href="{MIT14}">MIT14</a>, {where}'


def num(answer, tol="0.002"):
    return f'<input data-answer="{answer}" data-tol="{tol}">'


def check(body, ok):
    return (f'<div class="check-group" data-ok="{ok}">{body}'
            f'<button class="check">Verificar</button><div class="feedback"></div></div>')


def unif(t):
    """pdf of Uniform[0, t]."""
    return lambda x: 1 / t if x <= t else 0


# ---------------------------------------------------------------- recordação
recordacao = rf"""
<p>Duas perguntas de cabeça: uma da <a href="{LESSON1}">lição 0001</a> e uma da P1, que esta lição usa o tempo todo.</p>
""" + mc(
    "Na tabela de Bayes com hipóteses discretas, como se chega à posterior de cada hipótese?",
    [("Prior × likelihood, dividido pela soma", True, "Isso: o numerador de cada linha dividido por P(D), a soma dos numeradores."),
     ("Likelihood dividida pela soma delas", False, "Assim a prior fica de fora. Só dá certo quando a prior é igual para todas (é o caso da Q3, mas não em geral)."),
     ("Prior × likelihood, sem dividir nada", False, "Esse é o numerador de Bayes. Os numeradores não somam 1: falta dividir por P(D).")]) + check(
    r"""<p><b>Revisão da P1.</b> \(X\) é Uniforme em \([0, \theta]\): todo valor entre 0 e \(\theta\) é igualmente provável. A pdf é uma
constante \(c\) em \([0, \theta]\) e 0 fora. Para \(\theta = 0.5\), quanto vale \(c\)?</p>
<p>\(c\) = """ + num("2", "0.01") + "</p>",
    "Isso: a área do retângulo, c · 0.5, tem que dar 1, então c = 2. Em geral, c = 1/θ. A densidade passou de 1, e isso é normal: só a área precisa ser ≤ 1.")

# ---------------------------------------------------------------- ideia
ex = [(r"θ = 1/2", unif(.5), ACC, False, .08, 2.15), (r"θ = 1", unif(1), MUT, True, .8, 1.12)]

ideia = rf"""
<p>Até agora o dado sempre foi uma contagem: um 5 no dado, 6 pessoas em 10. A likelihood era uma probabilidade, \(P(D \mid H)\).
Na L03 Q3 o dado é um <b>tempo</b> (Maria chega com 10 minutos de atraso), e um tempo é contínuo. Aí aparece um problema:
para uma variável contínua, a chance de um valor exato é zero. Se toda likelihood vale 0, todo numerador vale 0, e a tabela não diz nada.</p>
<p>O MIT14 resolve com uma troca só:</p>
""" + quote(r"""<p>When both data and hypotheses are continuous, the only change to the previous example is that the likelihood function uses a
pdf \(\phi(x \mid \theta)\) instead of a pmf \(p(x \mid \theta)\). The general shape of the Bayesian update table is the same.</p>""", src("§4")) + r"""
<p>Ali as hipóteses também são contínuas, mas a troca não depende disso. Com hipóteses discretas, como na Q3, a tabela é a da
lição 0001, com uma coluna diferente: a <b>likelihood passa a ser o valor da pdf do dado</b>, \(\phi(x \mid \theta)\), lido no ponto
observado. (A letra \(\phi\) é um f grego; o MIT14 a usa para a pdf do dado e deixa o \(f\) para a pdf de \(\theta\).)</p>
<p>Por que isso é legítimo, se a pdf não é probabilidade? O MIT14 explica o que o valor da pdf representa:</p>
""" + quote(r"""<ul><li>Likelihood \(\phi(x \mid \theta)\,dx\). This is the (calculated) probability that the data is in a small interval of size \(dx\)
around \(x\), ASSUMING the hypothesis \(\theta\).</li></ul>
<p>[…] To simplify the notation we will sometimes allow ourselves to drop \(dx\) in our tables. This is fine because the data \(x\) is fixed
in each calculation.</p>""", src("§4")) + r"""
<p>Ou seja: a probabilidade de verdade é a de o dado cair numa faixinha de largura \(dx\) em volta de \(x\), e ela vale \(\phi(x \mid \theta)\,dx\).
O \(dx\) é o mesmo em todas as linhas da tabela, porque o dado é o mesmo. Ele multiplica todos os numeradores e também a soma deles, e por isso
se cancela na divisão. Pode-se escrever só \(\phi(x \mid \theta)\).</p>

<h3 id="exemplo">Um exemplo com números</h3>
<p>Um sorteio dá um número uniforme em \([0, \theta]\). Você não sabe se \(\theta = 1/2\) ou \(\theta = 1\) e acha as duas igualmente
prováveis (prior 1/2 para cada). Saiu \(x = 0.4\). A likelihood de cada hipótese é a altura da pdf dela em \(x = 0.4\):</p>
""" + pdf_plot(ex, "As duas pdfs possíveis do dado. As duas áreas valem 1, então a mais estreita (θ = 1/2) é a mais alta. Em x = 0.4, a altura é 2 numa e 1 na outra.",
               ymax=2.5, marks=[(.4, unif(.5), "2", ACC, "ur"), (.4, unif(1), "1", MUT, "ur")], xlabel="x", n=1000,
               fills=[(unif(.5), ACC, "área 1", .25, 1.5), (unif(1), MUT, "área 1", .75, .5, "hatch")]) + r"""
<table>
<tr><th>hipótese</th><th class="num">prior</th><th class="num">likelihood \(\phi(0.4 \mid \theta)\)</th><th class="num">numerador</th><th class="num">posterior</th></tr>
<tr><td>\(\theta = 1/2\)</td><td class="num">1/2</td><td class="num">2</td><td class="num">1</td><td class="num">2/3</td></tr>
<tr><td>\(\theta = 1\)</td><td class="num">1/2</td><td class="num">1</td><td class="num">1/2</td><td class="num">1/3</td></tr>
<tr><th>total</th><th class="num">1</th><th></th><th class="num">3/2</th><th class="num">1</th></tr>
</table>
<p>A soma dos numeradores deu 3/2, maior que 1. Ela é uma <b>densidade</b> (a de \(x\) antes de saber \(\theta\)), e só serve para dividir.
As posteriores somam 1, como sempre.</p>
<p>Por que \(\theta = 1/2\) ganhou? As duas hipóteses explicam o 0.4, mas a pdf de \(\theta = 1/2\) espalha a mesma área 1 numa faixa
mais estreita, então é mais alta em cada ponto. <b>Entre as hipóteses compatíveis com o dado, a mais estreita vence.</b> É o mesmo efeito do
MLE da Uniforme na LMLE 7 (<a href="{LESSON0}">lição 0000</a>): o menor \(\theta\) que ainda cobre os dados.</p>
""".replace("{LESSON0}", LESSON0) + mc(
    r"Se o sorteio tivesse dado \(x = 0.7\), quanto valeria a likelihood de \(\theta = 1/2\)?",
    [(r"\(0\), porque \(0.7\) passa de \(1/2\)", True, r"Isso: com \(\theta = 1/2\), o sorteio nunca passa de \(0.5\). A pdf é 0 em \(0.7\), e a posterior de \(\theta = 1/2\) também."),
     (r"\(2\), porque a pdf vale \(1/\theta\)", False, r"A pdf vale \(1/\theta\) só dentro de \([0, \theta]\). Fora dela vale 0, e \(0.7\) está fora."),
     (r"\(0.7\), o próprio valor sorteado", False, r"A likelihood é a altura da pdf no ponto sorteado, e não o ponto. Aqui a altura é 0, porque \(0.7 > 1/2\).")])

# ---------------------------------------------------------------- prática
pratica = r"""
<p>Um ônibus atrasa \(X\) minutos, com \(X\) Uniforme em \([0, \theta]\). O atraso máximo \(\theta\) é 5, 10 ou 20 minutos, com prior
0.25, 0.5 e 0.25. Hoje ele atrasou 7 minutos. Preencha a prior e a likelihood; o numerador e a soma se calculam sozinhos.</p>
<details><summary>Dica</summary><p>Para cada \(\theta\): o 7 cabe em \([0, \theta]\)? Se cabe, a likelihood é \(1/\theta\); se não, é 0.</p></details>
""" + bayes_table(
    [(r"\(\theta = 5\)", "0.25", "0", "0"), (r"\(\theta = 10\)", "0.5", "1/10", "0.8"), (r"\(\theta = 20\)", "0.25", "1/20", "0.2")],
    ok="Isso: θ = 5 sai (um atraso de 7 é impossível), e entre 10 e 20 o mais estreito leva 0.8.",
    lik_header=r"likelihood \(\phi(7 \mid \theta)\)", total=r"\(\phi(7)\)") + r"""
<p>O \(\phi(7) = 0.0625\) não é a chance de o ônibus atrasar exatamente 7 minutos (essa é 0). É a densidade do atraso em 7, antes de saber
\(\theta\), e só serve para normalizar.</p>
<p id="exponencial"><b>A regra não é "\(1/\theta\)".</b> A regra é "altura da pdf do dado"; \(1/\theta\) é só a altura da Uniforme. Com outra
distribuição, a coluna muda e o resto da tabela fica igual.</p>
<p>Para ver isso, troque a Uniforme pela <b>Exponencial</b>, a distribuição de tempos de vida. Se o tempo de vida \(X\) de uma lâmpada,
em anos, é Exponencial(\(\lambda\)), a pdf é \(\lambda e^{-\lambda x}\) para \(x \ge 0\), e a vida média é \(1/\lambda\) anos.
(É o mesmo modelo das lâmpadas da LMLE, na <a href="{LESSON0}">lição 0000</a>; lá a pergunta era o MLE de \(\lambda\), aqui é a posterior.)</p>
<p>Uma caixa de lâmpadas veio de uma de duas fábricas. Na fábrica A, as lâmpadas duram em média 1 ano (\(\lambda = 1\)); na B, meio ano
(\(\lambda = 2\)). Você não sabe de qual fábrica é a caixa e acha as duas igualmente prováveis (prior 1/2 para cada). Você testa uma
lâmpada, e ela dura 1 ano. A tabela é a mesma de antes; só a likelihood agora é a altura da pdf da Exponencial em \(x = 1\),
ou seja, \(\lambda e^{-\lambda \cdot 1}\):</p>
""".replace("{LESSON0}", LESSON0) + bayes_table(
    [(r"\(\lambda = 1\)", "0.5", "0.3679", "0.5761"), (r"\(\lambda = 2\)", "0.5", "0.2707", "0.4239")],
    ok="Isso: 1·e⁻¹ ≈ 0.368 e 2·e⁻² ≈ 0.271. A fábrica A (vida média de 1 ano) explica melhor uma lâmpada que durou 1 ano: posterior ≈ 0.576.",
    lik_header=r"likelihood \(\lambda e^{-\lambda \cdot 1}\)", total=r"\(\phi(1)\)") + r"""
<p id="calc-lik"><b>Como sai cada likelihood.</b> A likelihood de uma hipótese é a pdf do dado no valor observado, fingindo que a
hipótese é verdadeira. Para cada linha da tabela, são dois passos:</p>
<ol class="spaced">
<li><b>Escreva a pdf com a hipótese no lugar do parâmetro.</b> A pdf é \(\lambda e^{-\lambda x}\). Para \(\lambda = 1\), ela vira
\(1 \cdot e^{-1 \cdot x}\); para \(\lambda = 2\), vira \(2\,e^{-2x}\).</li>
<li><b>Ponha o dado no lugar de \(x\)</b> (a lâmpada durou \(x = 1\) ano) <b>e faça a conta</b>, com \(e \approx 2.718\):
$$\begin{aligned} \phi(1 \mid \lambda = 1) &= 1 \cdot e^{-1} = 1/e \approx 0.368 \\ \phi(1 \mid \lambda = 2) &= 2\,e^{-2} = 2/e^2 \approx 2 \cdot 0.135 = 0.271 \end{aligned}$$</li>
</ol>
<p>Daí em diante é a tabela de sempre: numeradores \(0.5 \cdot 0.368 = 0.184\) e \(0.5 \cdot 0.271 = 0.135\), soma \(\phi(1) \approx 0.319\),
posteriores \(0.184 / 0.319 \approx 0.576\) e \(0.135 / 0.319 \approx 0.424\).</p>
<p>Por que \(\lambda = 2\) perde, se a pdf dela começa mais alta (2, contra 1)? Porque ela cai mais rápido: o fator \(e^{-2x}\) encolhe
duas vezes mais depressa que \(e^{-x}\). As lâmpadas da fábrica B quase sempre queimam cedo. Em \(x = 1\), a pdf de B já está abaixo da
de A, e uma lâmpada que durou 1 ano é mais típica da fábrica A.</p>
<p>E se a lâmpada tivesse durado outro tempo? Mova o \(x\): a faixa estreita marca o dado no gráfico, e as duas likelihoods são as alturas
das curvas ali.</p>
<div class="playground">
<div class="controls">
""" + slider("xl", r"\(x\) (anos)", 0.05, 3, 0.05, 1) + r"""
</div>
<div><div class="plot-stack">
<svg class="plot marker" data-xlabel="x, tempo de vida (anos)" data-ylabel="densidade φ(x | λ)" data-fn="exp(-x)" data-x="0 3" data-y="0 2" data-shade-from="xl-0.012" data-shade-to="xl+0.012" role="img" aria-label="pdf da fábrica A, exp(-x)"></svg>
<svg class="plot second" data-fn="2*exp(-2*x)" data-x="0 3" data-y="0 2" aria-hidden="true"></svg>
</div><p class="plot-key"><b>—</b> fábrica A, \(e^{-x}\) &nbsp; - - fábrica B, \(2e^{-2x}\)</p></div>
</div>
$$P(A \mid x) = \frac{0.5 \cdot \live{exp(-xl).toFixed(3)}}{0.5 \cdot \live{exp(-xl).toFixed(3)} + 0.5 \cdot \live{(2*exp(-2*xl)).toFixed(3)}}
= \live{(1/(1 + 2*exp(-xl))).toFixed(3)}$$
<div class="stats">
<div class="stat"><div class="stat-label">posterior de A</div><div class="stat-value" data-expr="(1/(1 + 2*exp(-xl))).toFixed(3)"></div></div>
<div class="stat"><div class="stat-label">posterior de B</div><div class="stat-value" data-expr="(1 - 1/(1 + 2*exp(-xl))).toFixed(3)"></div></div>
<div class="stat"><div class="stat-label">fábrica mais provável</div><div class="stat-value" data-expr="exp(-xl) > 2*exp(-2*xl) ? 'A' : 'B'"></div></div>
</div>
<p>A virada acontece onde as curvas se cruzam, \(e^{-x} = 2e^{-2x}\), ou seja, \(x = \ln 2 \approx 0.69\) ano. Uma lâmpada que queima antes disso
aponta para B; depois, para A. Com a prior 1/2 e 1/2, quem decide é só a altura das curvas.</p>
"""

# ---------------------------------------------------------------- receita
receita = r"""
<div class="callout"><p>Prior discreta e dado contínuo: a tabela da lição 0001, com uma troca na coluna da likelihood.</p>
<ol class="spaced">
<li><b>Unidades.</b> Escreva o dado na mesma unidade de \(\theta\) (minutos ou horas, nunca misturados).</li>
<li><b>Likelihood = altura da pdf do dado no ponto observado</b>, uma conta por hipótese. Uniforme em \([0, \theta]\): \(1/\theta\) se
\(0 \le x \le \theta\), senão 0. Exponencial(\(\lambda\)): \(\lambda e^{-\lambda x}\). Pode passar de 1.</li>
<li><b>Numerador, soma e divisão</b> como na lição 0001. A soma é uma densidade e pode passar de 1; as posteriores somam 1.</li>
<li><b>Mais de um dado:</b> multiplique as likelihoods (\(\phi(x_1 \mid \theta)\,\phi(x_2 \mid \theta)\)), ou use a posterior do primeiro como
prior do segundo. Dá o mesmo.</li>
<li><b>MAP</b> (lição 0003): a hipótese com o maior numerador, que é a de maior posterior.</li>
</ol></div>
"""

# ---------------------------------------------------------------- objetivo
objetivo = quote(r"""<p>Suponha que Maria está sempre atrasada X horas para o almoço e X é uma variável aleatória uniforme em [0,θ]. Considere que a prior
para valor de θ é 1/4 ou 3/4 com a mesma probabilidade.</p>
<ul><li>Se Maria chega com 10 minutos de atraso, qual o máximo a posteriori (MAP) de θ?</li>
<li>Suponha que em um próximo encontro Maria chegue 30min atrasada. Qual o novo valor do MAP de θ?</li></ul>""",
                 f'<a href="{L03}">L03</a>, questão 3', lang="pt-BR") + check(
    r"""<p><b>Passo 1, unidades.</b> \(\theta\) está em horas. Quanto vale o dado \(x\) em horas?</p><p>\(x\) = """ + num("1/6", "0.002") + " h</p>",
    "Isso: 10/60 = 1/6 ≈ 0.167 h. Com x = 10, nenhuma hipótese cobriria o dado e a tabela zeraria.") + r"""
<p><b>Primeiro item.</b> A tabela com \(x = 1/6\):</p>
""" + bayes_table(
    [(r"\(\theta = 1/4\)", "0.5", "4", "0.75"), (r"\(\theta = 3/4\)", "0.5", "4/3", "0.25")],
    ok="Isso: posteriores 3/4 e 1/4, então o MAP é θ = 1/4 h (15 min). As duas cobrem 10 min, e a mais estreita vence.",
    lik_header=r"likelihood \(\phi(1/6 \mid \theta)\)", total=r"\(\phi(1/6)\)") + r"""
<p><b>MAP com hipóteses discretas.</b> Na <a href="{LESSON3}">lição 0003</a>, \(\theta\) era contínuo, a posterior era uma curva, e o MAP
era o \(\theta\) do pico, achado pela derivada. Aqui há só duas hipóteses, e a posterior é um número para cada uma. O MAP é a hipótese de
maior posterior (ou de maior numerador, que dá no mesmo). A resposta é o valor de \(\theta\), e não a posterior dele.</p>
""".replace("{LESSON3}", LESSON3) + check(
    r"<p>MAP de \(\theta\) depois de 10 min, em horas: " + num("0.25", "0.001") + "</p>",
    f"Isso: θ = 1/4. Confira no <a href='{L03G}'>L03G</a>, questão 3 (a solução é imagem; compare com o PDF aberto).") + r"""
<p><b>Segundo item.</b> Agora Maria chega 30 minutos atrasada. Use a posterior do primeiro item como prior (o botão "Preencher anteriores"
coloca 0.75 e 0.25) e a likelihood do novo dado:</p>
""" + bayes_table(
    [(r"\(\theta = 1/4\)", "0.75", "0", "0"), (r"\(\theta = 3/4\)", "0.25", "4/3", "1")],
    ok="Isso: 30 min = 1/2 h passa de 1/4 h, então θ = 1/4 fica com likelihood 0 e posterior 0. Toda a crença vai para θ = 3/4.",
    weight_header="prior (= posterior do 1º item)", lik_header=r"likelihood \(\phi(1/2 \mid \theta)\)", total=r"\(\phi(1/2 \mid 1/6)\)",
    carry_weight=True) + check(
    r"<p>Novo MAP de \(\theta\), em horas: " + num("0.75", "0.001") + "</p>",
    f"Isso: θ = 3/4. Pela outra via (prior 1/2 e likelihood 4 · 0 e 4/3 · 4/3) dá o mesmo. Confira no <a href='{L03G}'>L03G</a>, questão 3.") + r"""
<p>Um único atraso de 30 minutos derrubou a hipótese que tinha 75%. Com likelihood contínua isso acontece sempre que o dado cai fora do
intervalo em que a pdf é positiva: a hipótese não fica menos provável, ela fica impossível.</p>
<p>Com isso, as Q1, Q2 e Q3 da L03 estão feitas. Falta a Q4, em que a prior e o dado são Normais: é o §6 do MIT14 e o assunto da <a href="{LESSON5}">lição 0005</a>,
pelo MIT15.</p>
""".replace("{LESSON5}", LESSON5)

# ---------------------------------------------------------------- fontes
fontes = rf"""
<p>O <a href="{MIT14}">MIT14</a> é curto. Esta lição usou do §4 a troca da pmf pela pdf e o papel do \(dx\), e aplicou a troca à tabela discreta da lição 0001. O que ficou de fora:</p>
<table>
<tr><th>trecho do MIT14</th><th>por que ficou de fora</th><th>faz falta na P2?</th></tr>
<tr><td>§3: revisão dos casos discreto-discreto e contínuo-discreto</td><td>são as lições 0001 e 0003</td><td>não</td></tr>
<tr><td>§4: a tabela com \(\theta\) <em>também</em> contínuo (prior \(f(\theta)\,d\theta\), total \(\int \phi(x \mid \theta) f(\theta)\,d\theta\))</td><td>a L03 só tem esse caso na Q4, que é Normal-Normal</td><td>sim, na lição 0005</td></tr>
<tr><td>§5: digressão sobre notação (\(\phi\) × \(f\); muitos livros usam \(f\) para tudo)</td><td>só notação</td><td>não</td></tr>
<tr><td>§6, exemplos 3 e 4: prior N(2, 1), dado N(\(\theta\), 1), completar quadrado; posterior N(7/2, 1/2)</td><td>é a L03 Q4</td><td>sim, na lição 0005, junto com a regra Normal-Normal do MIT15</td></tr>
</table>
<div class="callout">Se ficou alguma dúvida, pergunte ao seu professor, que é o agente nesta conversa. Vale um passo da conta, um termo ou "por que isso funciona?".</div>
<p style="font-size:.8rem;color:var(--muted)">As citações em inglês são de J. Orloff e J. Bloom, <i>18.05 Introduction to Probability and Statistics</i>,
Spring 2022, MIT OpenCourseWare, licença CC BY-NC-SA 4.0. Trechos omitidos aparecem como […]. No texto extraído do PDF do MIT14, os símbolos
matemáticos saíram corrompidos; a prosa é literal, e as fórmulas foram reescritas a partir do contexto.</p>
"""

SPEC = {
    "title": "0004 · Likelihood contínua",
    "subtitle": "Lição 0004 · COE241 P2 · MIT14 · quando o dado é contínuo · meta: resolver a L03 Q3",
    "crumbs": (f'COE241 · P2 · Lição 0004 &nbsp;·&nbsp; anterior: <a href="{LESSON3}">0003, prior contínua e MAP</a>'
               f' &nbsp;·&nbsp; próxima: <a href="{LESSON5}">0005, priors conjugadas</a>'),
    "sections": [
        {"id": "recordacao", "heading": "Recordação: tabela de Bayes e Uniforme", "html": recordacao},
        {"id": "ideia", "heading": "Dado contínuo: a likelihood vira pdf", "html": ideia},
        {"id": "pratica", "heading": "Prática: o atraso do ônibus", "html": pratica},
        {"id": "receita", "heading": "Como resolver", "html": receita},
        {"id": "objetivo", "heading": "O objetivo: L03 Q3", "html": objetivo},
        {"id": "fontes", "heading": "O que ficou de fora do MIT14", "html": fontes},
    ],
    "quiz": [
        {"question": r"O dado é contínuo, então a chance de ele dar exatamente o valor observado é \(0\). Por que a tabela de Bayes ainda funciona com a pdf no lugar da likelihood?",
         "ref": [("ideia", "Dado contínuo: a likelihood vira pdf")],
         "options": [
             {"text": r"O \(dx\) é igual em toda linha e se cancela", "correct": True, "feedback": r"Isso: a probabilidade de verdade é \(\phi(x \mid \theta)\,dx\), e o mesmo \(dx\) multiplica os numeradores e a soma."},
             {"text": r"A pdf é a probabilidade do valor exato", "correct": False, "feedback": r"A pdf é densidade, e pode passar de \(1\). A probabilidade é \(\phi(x \mid \theta)\,dx\); o \(dx\) se cancela."},
             {"text": r"Os zeros se cancelam ao normalizar", "correct": False, "feedback": r"\(0/0\) não se define. O que se cancela é o \(dx\) de \(\phi(x \mid \theta)\,dx\), igual em toda linha."}]},
        {"question": r"Na L03 Q3, \(X\) é Uniforme em \([0, \theta]\), com \(\theta\) em horas, e Maria chega \(10\) minutos atrasada. Qual a likelihood de \(\theta = 1/4\)?",
         "ref": [("objetivo", "O objetivo: L03 Q3")],
         "options": [
             {"text": r"\(4\)", "correct": True, "feedback": r"Isso: \(1/6 \le 1/4\), então a likelihood é \(1/\theta = 4\)."},
             {"text": r"\(1/4\)", "correct": False, "feedback": r"Esse é o \(\theta\), não a altura da pdf. A altura é \(1/\theta = 4\)."},
             {"text": r"\(0\)", "correct": False, "feedback": r"Daria \(0\) com \(x = 10\), sem passar para horas. Em horas, \(x = 1/6 \le 1/4\), e a likelihood é \(4\)."}]},
        {"question": r"Duas hipóteses para o atraso máximo, \(\theta = 1/4\) e \(\theta = 3/4\) h, cobrem o atraso observado e têm a mesma prior. Qual fica com a maior posterior?",
         "ref": [("exemplo", "Um exemplo com números")],
         "options": [
             {"text": r"A mais estreita, \(\theta = 1/4\)", "correct": True, "feedback": r"Isso: a pdf dela é mais alta (\(4\) contra \(4/3\)) em todo ponto que as duas cobrem."},
             {"text": r"A mais larga, \(\theta = 3/4\)", "correct": False, "feedback": r"Cobrir mais valores espalha a área \(1\) e baixa a pdf: \(4/3\) contra \(4\)."},
             {"text": r"Nenhuma: ficam empatadas", "correct": False, "feedback": r"Ficariam empatadas se as likelihoods fossem iguais, mas \(1/\theta\) dá \(4\) e \(4/3\)."}]},
        {"question": r"Na tabela da Q3 com \(x = 1/6\), a soma dos numeradores deu \(8/3\), maior que \(1\). O que isso indica?",
         "ref": [("exemplo", "Um exemplo com números")],
         "options": [
             {"text": "Nada: a soma é uma densidade", "correct": True, "feedback": r"Isso: é a densidade de \(x\) antes de saber \(\theta\). Ela serve só para dividir, e as posteriores somam \(1\)."},
             {"text": "Erro: a soma devia dar 1", "correct": False, "feedback": r"Quem soma \(1\) é a coluna das posteriores. A dos numeradores soma \(P(D)\), aqui uma densidade."},
             {"text": "Erro: a prior está errada", "correct": False, "feedback": r"As priors \(1/2\) e \(1/2\) somam \(1\). A soma passa de \(1\) porque as likelihoods são densidades."}]},
    ],
}

if __name__ == "__main__":
    build(SPEC, ROOT / "lessons" / "0004-likelihood-continua.html")
