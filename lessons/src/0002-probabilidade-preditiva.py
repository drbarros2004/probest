"""Lesson 0002 source. Build: python lessons/src/0002-probabilidade-preditiva.py

Quotes from MIT12 (and one from MIT11) are verbatim from the PDF text (MIT OCW 18.05 Spring 2022,
CC BY-NC-SA 4.0). Only passages whose extracted text was clean are quoted.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "assets"))
from build import build, mc, quote, bayes_table, bayes_square  # noqa: E402

MIT11 = "https://drive.google.com/file/d/1-IfPV-srvMrLhYy4SMKkywMwIcA2ibZs/view"
MIT12 = "https://drive.google.com/file/d/1Kpa0gQzUJ63kKbU5iG_hxIhTMJn6rWCV/view"
L03 = "https://drive.google.com/file/d/1Nb8V3KKsByciabbw_dcDfaQ2bYXCVeQm/view"
L03G = "https://drive.google.com/file/d/1w1zevZpR8_RlVbkCjUJtHLfsXRE9wRxI/view"
LESSON1 = "https://claude.ai/artifact/XWsvKr4dXaFPnc1BAz6Wxa"
LESSON3 = "https://claude.ai/artifact/Mg37Am6eQ3TsQEvzxY98BT"


def src(where, doc="MIT12"):
    url = MIT12 if doc == "MIT12" else MIT11
    return f'<a href="{url}">{doc}</a>, {where}'


def uso(text):
    """Short pointer from an explanation to the formula the student actually uses (the summary box #receita)."""
    return f'<p class="uso"><b>Na prova:</b> {text} (<a href="#receita">as 3 fórmulas</a>)</p>'


recordacao = rf"""
<p>Duas perguntas da <a href="{LESSON1}">lição 0001</a>, de cabeça. Puxar da memória agora é o que faz o assunto ficar para a prova.</p>
""" + mc(
    "Uma hipótese tem likelihood 0.5, e o P(D) da tabela é 0.62. A posterior dela, comparada com a prior:",
    [("Fica maior que a prior", False, "Ela só ganharia se a likelihood passasse da média ponderada P(D) = 0.62. Como 0.5 < 0.62, perde."),
     ("Fica menor que a prior", True, "Isso. A posterior é prior × likelihood/P(D) = prior × 0.81. É a moeda A da lição 0001."),
     ("Fica igual à prior", False, "Só ficaria igual se a likelihood fosse exatamente P(D).")]) + r"""
<div class="check-group" data-ok="Isso: 0.2 · 0.9 / 0.62 = 0.18 / 0.62 ≈ 0.290.">
<p><b>Prior 0.2, likelihood 0.9 e P(D) = 0.62. Qual a posterior?</b> <input data-answer="0.2903" data-tol="0.003"></p>
<button class="check">Verificar</button><div class="feedback"></div>
</div>
"""

ideia = r"""
<p>A lição 0001 respondeu "qual hipótese é a verdadeira?". Muitas vezes o que interessa é outra pergunta: "qual vai ser o <em>próximo</em> resultado?".
O MIT12 abre com essa mudança:</p>
""" + quote(r"""<p>In the previous class we looked at updating the probability of hypotheses based on data. We can also use the data to update
the probability of each possible outcome of a future experiment.</p>
<p>[…] Probabilistic prediction simply means assigning a probability to each possible outcomes of an experiment.</p>""",
            src("§2 e §3")) + r"""
<p>O exemplo é uma variação das moedas da lição 0001. Atenção, porque a gaveta é outra (4 moedas, e não 5):</p>
""" + quote(r"""<p>Recall the coin example from the previous class notes: there are three types of coins which are indistinguishable apart from
their probability of landing heads when tossed.</p>
<ul><li>Type \(A\) coins are fair, with probability 0.5 of heads</li>
<li>Type \(B\) coins have probability 0.6 of heads</li>
<li>Type \(C\) coins have probability 0.9 of heads</li></ul>
<p>You have a drawer containing 4 coins: 2 of type \(A\), 1 of type \(B\), and 1 of type \(C\). You reach into the drawer and pick a coin
at random. We let \(A\) stand for the event ‘the chosen coin is of type \(A\)’. Likewise for \(B\) and \(C\).</p>""", src("§3")) + r"""
<p>As priors são, portanto, 0.5, 0.25 e 0.25.</p>

<h3 id="prior-predictive">Antes de jogar: prior predictive</h3>
<p>Qual a chance de sair cara? Você não sabe qual moeda pegou, mas sabe a chance de cara de cada uma e a chance de ter pegado cada uma.
É a probabilidade total da P1:</p>
""" + quote(r"""<p>Before taking data we can compute the probability that our chosen coin will land heads (or tails) if flipped. Let \(D_H\) be
the event it lands heads and let \(D_T\) the event it lands tails. We can use the law of total probability to determine the probabilities
of these events. […]</p>
$$\begin{aligned} P(D_H) &= P(D_H \mid A)P(A) + P(D_H \mid B)P(B) + P(D_H \mid C)P(C) \\ &= 0.5 \cdot 0.5 + 0.6 \cdot 0.25 + 0.9 \cdot 0.25 = 0.625 \end{aligned}$$
$$\begin{aligned} P(D_T) &= P(D_T \mid A)P(A) + P(D_T \mid B)P(B) + P(D_T \mid C)P(C) \\ &= 0.5 \cdot 0.5 + 0.4 \cdot 0.25 + 0.1 \cdot 0.25 = 0.375 \end{aligned}$$
<p><b>Definition:</b> These probabilities give a (probabilistic) prediction of what will happen if the coin is tossed. Because they are
computed before we collect any data they are called <b>prior predictive probabilities</b>.</p>""", src("§3.1")) + r"""
<p>Essa conta você já fez na lição 0001, com outro nome. Monte a tabela de Bayes daquela lição para esta gaveta, fingindo que o dado
observado é "saiu cara", e pare antes de dividir:</p>
<table>
<tr><th>hipótese</th><th class="num">prior \(P(H)\)</th><th class="num">likelihood \(P(\text{cara} \mid H)\)</th><th class="num">numerador</th></tr>
<tr><td>A</td><td class="num">0.5</td><td class="num">0.5</td><td class="num">0.25</td></tr>
<tr><td>B</td><td class="num">0.25</td><td class="num">0.6</td><td class="num">0.15</td></tr>
<tr><td>C</td><td class="num">0.25</td><td class="num">0.9</td><td class="num">0.225</td></tr>
<tr><th>total</th><th class="num">1</th><th></th><th class="num">\(P(D)\) = 0.625</th></tr>
</table>
<p>Cada parcela da soma da citação (0.5·0.5, 0.6·0.25 e 0.9·0.25) é um numerador, e o total é o \(P(D_H)\) = 0.625.
<b>A prior predictive de um resultado é o \(P(D)\) que a tabela de Bayes teria se esse resultado fosse o dado observado.</b>
A conta é a mesma; muda o papel do número:</p>
<ul>
<li>na lição 0001, o dado já tinha acontecido, e \(P(D)\) servia só de denominador, para normalizar a posterior;</li>
<li>aqui, a moeda ainda não foi jogada, e \(P(D_H)\) é a própria resposta para "qual a chance de sair cara?".</li>
</ul>
<p>Por isso, na lição 0001 você já calculou três prior predictive sem esse nome:</p>
<ul>
<li><b>moedas:</b> \(P(D) = 0.62\) era a chance de sair cara antes de jogar, na gaveta de 5 moedas;</li>
<li><b>dados:</b> \(P(D) = 0.085\) era a chance de tirar 5 antes de saber qual dado foi escolhido;</li>
<li><b>doença:</b> \(P(+) = 0.02485\) era a chance de uma pessoa qualquer testar positivo.</li>
</ul>
<p>No <a href="https://claude.ai/artifact/XWsvKr4dXaFPnc1BAz6Wxa">quadrado da lição 0001</a> isso fica visível: a prior predictive é a <b>área pintada total</b>.
Antes, ela era o denominador. Agora ela é a resposta.</p>
""" + bayes_square(
    [("A", .5, .5), ("B", .25, .6), ("C", .25, .9)],
    "Gaveta de 4 moedas do MIT12. Largura = prior, altura pintada = chance de cara. A área pintada é a chance de cara antes de jogar.",
    post=False, total="P(cara)") + r"""
""" + uso("esta é a fórmula 1.") + r"""

<h3 id="posterior-predictive">Depois de jogar: posterior predictive</h3>
<p>Agora a moeda é jogada uma vez e sai cara. Isso muda a crença sobre qual moeda é, e com ela a previsão do próximo lançamento:</p>
""" + quote(r"""<p>Suppose we flip the coin once and it lands heads. We now have data \(D\), which we can use to update the prior probabilities of our
hypotheses to posterior probabilities. Last class we learned to use a Bayes table to facilitate this computation:</p>
<table>
<tr><th>hypothesis</th><th>prior</th><th>likelihood</th><th>Bayes numerator</th><th>posterior</th></tr>
<tr><th>\(H\)</th><th>\(P(H)\)</th><th>\(P(D \mid H)\)</th><th>\(P(D \mid H)P(H)\)</th><th>\(P(H \mid D)\)</th></tr>
<tr><td>A</td><td>0.5</td><td>0.5</td><td>0.25</td><td>0.4</td></tr>
<tr><td>B</td><td>0.25</td><td>0.6</td><td>0.15</td><td>0.24</td></tr>
<tr><td>C</td><td>0.25</td><td>0.9</td><td>0.225</td><td>0.36</td></tr>
<tr><td>total</td><td>1</td><td>NO SUM</td><td>0.625</td><td>1</td></tr>
</table>
<p>Having flipped the coin once and gotten heads, we can compute the probability that our chosen coin will land heads (or tails) if
flipped a second time. We proceed just as before, but using the posterior probabilities \(P(A \mid D)\), \(P(B \mid D)\), \(P(C \mid D)\)
in place of the prior probabilities \(P(A)\), \(P(B)\), \(P(C)\). […]</p>
$$\begin{aligned} P(D_H \mid D) &= P(D_H \mid A)P(A \mid D) + P(D_H \mid B)P(B \mid D) \\ &\quad + P(D_H \mid C)P(C \mid D) \\ &= 0.5 \cdot 0.4 + 0.6 \cdot 0.24 + 0.9 \cdot 0.36 = 0.668 \end{aligned}$$
$$\begin{aligned} P(D_T \mid D) &= P(D_T \mid A)P(A \mid D) + P(D_T \mid B)P(B \mid D) \\ &\quad + P(D_T \mid C)P(C \mid D) \\ &= 0.5 \cdot 0.4 + 0.4 \cdot 0.24 + 0.1 \cdot 0.36 = 0.332 \end{aligned}$$
<p><b>Definition:</b> These probabilities give a (probabilistic) prediction of what will happen if the coin is tossed again. Because they
are computed after collecting data and updating the prior to the posterior, they are called <b>posterior predictive probabilities</b>.</p>
<p>Note that heads on the first toss increases the probability of heads on the second toss.</p>""", src("§3.2")) + r"""
<p>A receita geral, chamando de \(D_1\) o que já foi observado e de \(D_2\) o próximo resultado:</p>
$$P(D_2 \mid D_1) = \sum_{H} P(D_2 \mid H)\,P(H \mid D_1)$$
<p>Com as partes nomeadas:</p>
$$\underbrace{P(D_2 \mid D_1)}_{\text{posterior predictive}} \;=\; \sum_{H} \underbrace{P(D_2 \mid H)}_{\text{likelihood do próximo resultado}} \cdot \underbrace{P(H \mid D_1)}_{\text{posterior}}$$
<p>Trocando a posterior pela prior, sai a prior predictive. A conta é sempre a mesma: uma média das likelihoods das hipóteses, com
pesos dados pela crença atual em cada uma.</p>
<p>No quadrado: depois da primeira cara, só a área pintada sobrevive, e ela é esticada até virar um quadrado novo. As fatias dela
(0.4, 0.24 e 0.36) são as larguras novas. Para prever o segundo lançamento, pinte de novo com as mesmas alturas, que são a chance de cara
de cada moeda. A área pintada do quadrado novo é a posterior predictive:</p>
""" + bayes_square(
    [("A", .4, .5), ("B", .24, .6), ("C", .36, .9)],
    "O mesmo desenho depois de uma cara: C ficou mais larga e B mais estreita. As alturas não mudaram, e a área pintada subiu de 0.625 para 0.668.",
    post=False, wlabel="posterior", total="P(cara | cara)") + r"""
<p>A previsão sobe sem que nenhuma moeda mude: a faixa mais alta (C) ficou mais larga.</p>
""" + uso("esta é a fórmula 3; os pesos vêm da fórmula 2.") + r"""
<p>Falta justificar um detalhe. A rigor, o termo seria \(P(D_2 \mid H, D_1)\), a chance do próximo resultado sabendo a hipótese <em>e</em>
o primeiro resultado. Ele vira \(P(D_2 \mid H)\) porque, sabendo qual é a moeda, o primeiro lançamento não diz nada sobre o segundo.
O MIT12 dá nome a essa propriedade:</p>
""" + quote(r"""<p>Suppose we collect data in two stages, first \(D_1\), then \(D_2\). We have seen in our dice and coin examples that the final
posterior can be computed all at once or in two stages where we first update the prior using the likelihoods for \(D_1\) and then update
the resulting posterior using the likelihoods for \(D_2\). The latter approach works whenever likelihoods multiply:</p>
$$P(D_1, D_2 \mid H) = P(D_1 \mid H)\,P(D_2 \mid H).$$
<p>Since likelihoods are conditioned on hypotheses, we say that \(D_1\) and \(D_2\) are <b>conditionally independent</b> if the above
equation holds for every hypothesis \(H\).</p>""", src("nota Odds, §4.1")) + r"""
<p>Foi essa mesma propriedade que permitiu, na lição 0001, multiplicar as likelihoods de dois lançamentos.</p>
<p id="quatro">Com isso, já são quatro probabilidades com nomes parecidos. O MIT12 resume a diferença:</p>
""" + quote(r"""<p>Each hypothesis gives a different probability of heads, so the total probability of heads is a weighted average. For the prior
predictive probability of heads, the weights are given by the prior probabilities of the hypotheses. For the posterior predictive probability
of heads, the weights are given by the posterior probabilities of the hypotheses.</p>
<p>Remember: Prior and posterior probabilities are for hypotheses. Prior predictive and posterior predictive probabilities are for outcomes.
To keep this straight, remember that the predictive probabilities are used to predict future outcomes, i.e. data.</p>""", src("§3.3")) + r"""
<table>
<tr><th></th><th>é probabilidade de…</th><th>antes do dado</th><th>depois do dado</th></tr>
<tr><td><b>hipótese</b></td><td>qual moeda é</td><td>prior \(P(H)\): 0.5; 0.25; 0.25</td><td>posterior \(P(H \mid D)\): 0.4; 0.24; 0.36</td></tr>
<tr><td><b>resultado</b></td><td>o que sai no próximo lançamento</td><td>prior predictive \(P(D_H)\) = 0.625</td><td>posterior predictive \(P(D_H \mid D)\) = 0.668</td></tr>
</table>
""" + mc("No exemplo, 0.668 é a probabilidade de quê?",
         [("De sair cara no segundo lançamento, sabendo que o primeiro deu cara", True, "Isso: é uma posterior predictive, uma probabilidade de resultado."),
          ("De a moeda ser do tipo C, sabendo que o primeiro lançamento deu cara", False, "Essa é a posterior de C, 0.36. É uma probabilidade de hipótese."),
          ("De sair cara no primeiro lançamento, antes de qualquer informação", False, "Essa é a prior predictive, 0.625.")])

pratica = r"""
<p>Os cinco dados da lição 0001 (4, 6, 8, 12 e 20 lados, um escolhido ao acaso, ou seja, prior 1/5 para cada) voltam com uma
pergunta de previsão:</p>
""" + quote(r"""<p><b>Problem 4. Probabilistic prediction</b> […] With the same setup as before let:
\(D_1\) = result of first roll, \(D_2\) = result of second roll</p>
<p>(a) Find \(P(D_1 = 5)\).</p>
<p>(b) Find \(P(D_2 = 4 \mid D_1 = 5)\).</p>""", src("problemas em sala, problema 4", "MIT11")) + r"""
<p><b>(a)</b> é uma prior predictive, e a resposta já apareceu em <a href="#prior-predictive">Antes de jogar</a>: é o \(P(D)\) da tabela "tirei 5" da lição 0001, 0.085.
Para treinar a conta, calcule a prior predictive de outro resultado: a chance de o primeiro lançamento dar <b>4</b>.</p>
<details><summary>Dica</summary><p>Monte a tabela de Bayes como se o dado fosse "tirei 4" e some os numeradores: prior 1/5 para cada dado, likelihood \(P(4 \mid H)\). Agora o dado de 4 lados também entra.</p></details>
<div class="check-group" data-ok="Isso: 1/5 · (1/4 + 1/6 + 1/8 + 1/12 + 1/20) ≈ 0.135. É maior que a chance de tirar 5 (0.085), porque o dado de 4 lados também pode dar 4.">
<p>\(P(D_1 = 4)\) = <input data-answer="0.135" data-tol="0.0005"></p>
<button class="check">Verificar</button><div class="feedback"></div>
</div>
<p><b>(b)</b> é uma posterior predictive. Os pesos são as posteriores depois do 5, que você calculou na lição 0001. Tente lembrá-las
antes de usar o botão "Preencher anteriores", que coloca esses valores na tabela. A segunda coluna, \(P(D_2 = 4 \mid H)\), é a mesma likelihood \(P(4 \mid H)\) que você usou na (a): sabendo qual é o dado,
cada lançamento tem as mesmas chances, e o 5 anterior não muda isso (independência condicional). Entre a (a) e a (b), só os pesos mudam:
prior 1/5 lá, posterior depois do 5 aqui. Os produtos e a soma se calculam sozinhos.</p>
""" + bayes_table(
    [("4 lados", "0", "1/4", None), ("6 lados", "0.3922", "1/6", None), ("8 lados", "0.2941", "1/8", None),
     ("12 lados", "0.1961", "1/12", None), ("20 lados", "0.1176", "1/20", None)],
    ok="A soma é P(D₂ = 4 | D₁ = 5) ≈ 0.124. O dado de 4 lados tem a maior chance de dar 4, mas peso 0: o 5 já o eliminou.",
    weight_header="posterior \\(P(H \\mid D_1 = 5)\\)", lik_header="\\(P(D_2 = 4 \\mid H)\\)",
    prod_header="produto (automático)", carry_weight=True, total="\\(P(D_2 = 4 \\mid D_1 = 5)\\)") + r"""
<p>Antes do 5, a chance de tirar 4 era 0.135, a prior predictive que você acabou de calcular. O 5 eliminou o
dado de 4 lados, que era o mais propenso a dar 4, e por isso a previsão caiu para 0.124.</p>
"""

receita = r"""
<p><b>Passo zero: ler a pergunta.</b> Antes de qualquer fórmula, responda duas perguntas:</p>
<ol>
<li><b>A pergunta é sobre uma hipótese ou sobre um resultado?</b> "Qual moeda foi escolhida?" é sobre hipótese: a resposta é uma prior
ou uma posterior. "O que sai no próximo lançamento?" é sobre resultado: a resposta é uma predictive.</li>
<li><b>Algum dado já foi observado?</b> Se não, os pesos da média são as priors (prior predictive). Se sim, primeiro atualize para as
posteriores e use-as como pesos (posterior predictive).</li>
</ol>
<p>É a tabela das <a href="#quatro">quatro probabilidades</a>. Depois do passo zero, as fórmulas:</p>
<div class="callout"><p>Todo o resto da lição explica por que estas fórmulas funcionam; para resolver as questões, basta isto:</p>
<table>
<tr><th>#</th><th>para quê</th><th>fórmula</th></tr>
<tr><td>1</td><td>prior predictive (antes do dado)</td><td>\(P(D) = \sum_H P(D \mid H)\,P(H)\): o total da tabela de Bayes</td></tr>
<tr><td>2</td><td>os pesos depois do dado \(D_1\)</td><td>\(P(H \mid D_1) = \dfrac{P(D_1 \mid H)\,P(H)}{P(D_1)}\), a posterior da lição 0001</td></tr>
<tr><td>3</td><td>posterior predictive (depois do dado)</td><td>\(P(D_2 \mid D_1) = \sum_H P(D_2 \mid H)\,P(H \mid D_1)\)</td></tr>
</table></div>
"""

objetivo = quote(r"""<p>Suponha que você tenha uma caixa com dados de 4, 6, 8, 12 e 20 lados. Você suspeita que eles estão na proporção 1:2:10:2:1.
Seu amigo escolhe um dado aleatoriamente e joga duas vezes, obtendo 5 ambas as vezes.</p>
<p>[…] 2. Qual a probabilidade de que o próximo lançamento seja 5?</p>
<p>3. Qual a probabilidade de que o próximo lançamento seja 15?</p>""", f'<a href="{L03}">L03</a>, questão 1', lang="pt-BR") + rf"""
<p>As duas são posterior predictive: a fórmula 3, com os pesos da fórmula 2. Os pesos são as posteriores da Q1.1, que você calculou na <a href="{LESSON1}">lição 0001</a>. Se não as tiver
anotadas, o botão "Preencher anteriores" coloca esses valores na tabela.</p>
<p><b>Q1.2:</b> a segunda coluna é a chance de o próximo lançamento dar 5 com cada dado.</p>
""" + bayes_table(
    [("4 lados", "0", "0", None), ("6 lados", "0.2435", "1/6", None), ("8 lados", "0.6847", "1/8", None),
     ("12 lados", "0.0609", "1/12", None), ("20 lados", "0.0110", "1/20", None)],
    ok=f"A resposta da Q1.2 é ≈ 0.132. Confira no <a href='{L03G}'>L03G</a>, questão 1: a solução lá é imagem, então compare com o PDF aberto.",
    weight_header="posterior \\(P(H \\mid 5, 5)\\)", lik_header="\\(P(\\text{próximo} = 5 \\mid H)\\)",
    prod_header="produto (automático)", carry_weight=True, total="\\(P(\\text{próximo} = 5 \\mid 5, 5)\\)") + rf"""
<p><b>Q1.3:</b> aqui quase não há conta. Pense em quais dados conseguem dar 15.</p>
<div class="check-group" data-ok="Só o dado de 20 lados tem face 15: 0.0110 × 1/20 ≈ 0.00055. Confira no <a href='{L03G}'>L03G</a>, questão 1.">
<p>\(P(\text{{próximo}} = 15 \mid 5, 5)\) = <input data-answer="0.000548" data-tol="0.00003"></p>
<button class="check">Verificar</button><div class="feedback"></div>
</div>
<p>Com isso, a Q1 da L03 está completa. A Q2 troca as cinco hipóteses por um contínuo (a proporção \(\theta\) pode ser qualquer número
entre 0 e 1), e esse é o assunto da <a href="{LESSON3}">lição 0003</a>, pelo MIT13.</p>
"""

fontes = rf"""
<p>O arquivo do <a href="{MIT12}">MIT12</a> tem duas notas: <em>Probabilistic Prediction</em>, que esta lição cobre inteira menos o §2.1,
e <em>Odds</em>. O que ficou de fora:</p>
<table>
<tr><th>trecho do MIT12</th><th>por que ficou de fora</th><th>faz falta na P2?</th></tr>
<tr><td>Nota <em>Odds</em> inteira: odds (razão \(P(E)/P(E^c)\)), fator de Bayes (razão entre as likelihoods de duas hipóteses), atualização de odds, log odds</td><td>a L03 não usa; é outra forma de escrever a mesma atualização</td><td>sim: a L04 (PSet 7) cobra. Terá lição própria</td></tr>
<tr><td>§2.1, previsões em palavras ("é provável que chova") × previsões com probabilidade</td><td>discussão de vocabulário, sem conta</td><td>não</td></tr>
<tr><td>Problema 1 em sala: 3 moedas (0.5, 0.6 e 0.9), 1 cara em 5 lançamentos; posterior e posterior predictive</td><td>a likelihood usa a Binomial da P1, que merece revisão própria</td><td>sim, como treino; entra quando revisarmos a Binomial</td></tr>
<tr><td>Concept question 2: saber a ordem dos lançamentos (THTTT) em vez de só "1 cara em 5" muda a posterior?</td><td>depende do problema 1</td><td>não muda (o coeficiente binomial, o número de ordens possíveis de 1 cara em 5 lançamentos, aparece em todas as likelihoods e se cancela); entra junto</td></tr>
<tr><td>Problemas em sala 2 e 3 (odds do teste de doença, tipos sanguíneos)</td><td>são exercícios de odds</td><td>sim, na lição de odds</td></tr>
</table>
<div class="callout">Se ficou alguma dúvida, pergunte ao seu professor, que é o agente nesta conversa. Vale um passo da conta, um termo ou "por que isso funciona?".</div>
<p style="font-size:.8rem;color:var(--muted)">As citações em inglês são de J. Orloff e J. Bloom, <i>18.05 Introduction to Probability and Statistics</i>,
Spring 2022, MIT OpenCourseWare, licença CC BY-NC-SA 4.0. Trechos omitidos aparecem como […].</p>
"""

SPEC = {
    "title": "0002 · Probabilidade preditiva",
    "subtitle": "Lição 0002 · COE241 P2 · MIT12 · prever o próximo resultado · meta: resolver a L03 Q1.2 e Q1.3",
    "crumbs": f'COE241 · P2 · Lição 0002 &nbsp;·&nbsp; anterior: <a href="{LESSON1}">0001, tabela de atualização bayesiana</a>'
              f' &nbsp;·&nbsp; próxima: <a href="{LESSON3}">0003, prior contínua e MAP</a>',
    "sections": [
        {"id": "recordacao", "heading": "Recordação da lição 0001", "html": recordacao},
        {"id": "ideia", "heading": "De hipóteses para resultados", "html": ideia},
        {"id": "pratica", "heading": "Prática: o próximo lançamento dos cinco dados", "html": pratica},
        {"id": "receita", "heading": "Como resolver: passo zero e as 3 fórmulas", "html": receita},
        {"id": "objetivo", "heading": "O objetivo: L03 Q1.2 e Q1.3", "html": objetivo},
        {"id": "fontes", "heading": "O que ficou de fora do MIT12", "html": fontes},
    ],
    "quiz": [
        {"question": "Há quatro probabilidades com nomes parecidos: prior, posterior, prior predictive e posterior predictive. Quais duas são probabilidades de resultados (o que vai sair no próximo lançamento), e não de hipóteses?",
         "ref": [("quatro", "As quatro probabilidades")],
         "options": [
             {"text": "As duas predictive", "correct": True, "feedback": "Isso: preveem dados futuros, como a face do próximo lançamento. Prior e posterior são sobre qual hipótese é a verdadeira."},
             {"text": "Prior e prior predictive", "correct": False, "feedback": "A prior é sobre hipóteses (qual dado foi escolhido). Só as duas predictive são sobre resultados."},
             {"text": "As duas posteriores", "correct": False, "feedback": "A posterior é sobre hipóteses (qual dado foi escolhido). Só as duas predictive são sobre resultados."}]},
        {"question": r"Gaveta com \(2\) moedas A (cara com \(0.5\)), \(1\) B (\(0.6\)) e \(1\) C (\(0.9\)), uma escolhida ao acaso. Antes de jogar, a chance de cara é \(0.625\) (a prior predictive). Se você montar a tabela de Bayes para o dado 'saiu cara', onde aparece esse \(0.625\)?",
         "ref": [("prior-predictive", "Antes de jogar: prior predictive")],
         "options": [
             {"text": "No total da coluna dos numeradores", "correct": True, "feedback": r"Isso. \(\sum_H P(D \mid H)\,P(H)\) é ao mesmo tempo o \(P(D)\) da tabela e a prior predictive de \(D\)."},
             {"text": "No numerador da moeda mais comum", "correct": False, "feedback": r"O numerador de A é \(0.5 \cdot 0.5 = 0.25\). O \(0.625\) é o total dos numeradores, \(P(D)\)."},
             {"text": "Na média simples das likelihoods", "correct": False, "feedback": r"A média simples seria \(\frac{0.5 + 0.6 + 0.9}{3} \approx 0.667\). A predictive pondera pela prior."}]},
        {"question": r"A posterior predictive é \(P(D_2 \mid D_1) = \sum_H P(D_2 \mid H)\,P(H \mid D_1)\), em que \(D_1\) é o resultado já observado e \(D_2\) o próximo. Por que o termo é \(P(D_2 \mid H)\), e não \(P(D_2 \mid H, D_1)\)?",
         "ref": [("posterior-predictive", "Depois de jogar: posterior predictive")],
         "options": [
             {"text": "Dada a hipótese, os resultados são independentes", "correct": True, "feedback": "Isso: independência condicional. Sabendo qual é o dado, o primeiro lançamento não informa sobre o segundo."},
             {"text": "Os resultados são sempre independentes entre si", "correct": False, "feedback": r"Sem condicionar na hipótese eles não são: um \(5\) elimina o dado de \(4\) lados e muda a chance do próximo."},
             {"text": r"\(D_1\) já foi usado e pode ser descartado", "correct": False, "feedback": r"\(D_1\) não é descartado: ele está nos pesos, as posteriores \(P(H \mid D_1)\)."}]},
        {"question": r"Na L03 Q1.3, depois de dois \(5\), pede-se a chance de o próximo lançamento dar \(15\) (dados de \(4\), \(6\), \(8\), \(12\) e \(20\) lados). Por que só o dado de \(20\) lados entra na conta?",
         "ref": [("objetivo", "O objetivo: L03 Q1.2 e Q1.3")],
         "options": [
             {"text": r"É o único dado com face \(15\)", "correct": True, "feedback": r"Para os outros, \(P(15 \mid H) = 0\), e o produto zera."},
             {"text": "É o dado de maior posterior", "correct": False, "feedback": r"O de maior posterior é o de \(8\) lados (\(0.685\)). O que importa é a likelihood de \(15\)."},
             {"text": "É o dado de maior prior", "correct": False, "feedback": r"A maior prior é a do dado de \(8\) lados (\(\frac{10}{16}\))."}]},
        {"question": r"Gaveta com \(2\) moedas A (cara com \(0.5\)), \(1\) B (\(0.6\)) e \(1\) C (\(0.9\)), uma escolhida ao acaso. Antes de jogar, a chance de cara é \(0.625\). Depois de sair uma cara, a chance de cara no próximo lançamento sobe para \(0.668\). Por que a previsão sobe, se a chance de cara de cada moeda é fixa?",
         "ref": [("posterior-predictive", "Depois de jogar: posterior predictive")],
         "options": [
             {"text": "A crença passou para a moeda C", "correct": True, "feedback": r"Isso: a posterior de C subiu de \(0.25\) para \(0.36\), e C dá cara \(90\%\) das vezes."},
             {"text": "A moeda ficou mais propensa a cara", "correct": False, "feedback": "Cada moeda tem chance fixa. O que mudou foi a crença sobre qual moeda é."},
             {"text": "Caras seguidas são mais prováveis", "correct": False, "feedback": "Dada a moeda, os lançamentos são independentes. O efeito vem da incerteza sobre a moeda."}]},
    ],
}

if __name__ == "__main__":
    build(SPEC, ROOT / "lessons" / "0002-probabilidade-preditiva.html")
