"""Lesson 0001 source. Build: python lessons/src/0001-tabela-de-atualizacao-bayesiana.py

Quotes from MIT11 are verbatim from the PDF text (MIT OCW 18.05 Spring 2022, CC BY-NC-SA 4.0).
Only passages whose extracted text was clean are quoted; garbled ones are not reconstructed.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "assets"))
from build import build, prior_post, mc, quote, bayes_table, bayes_square  # noqa: E402

MIT11 = "https://drive.google.com/file/d/1-IfPV-srvMrLhYy4SMKkywMwIcA2ibZs/view"
L03 = "https://drive.google.com/file/d/1Nb8V3KKsByciabbw_dcDfaQ2bYXCVeQm/view"
L03G = "https://drive.google.com/file/d/1w1zevZpR8_RlVbkCjUJtHLfsXRE9wRxI/view"


def src(where):
    return f'<a href="{MIT11}">MIT11</a>, {where}'


def uso(text):
    """Short pointer from an explanation to the formula the student actually uses (the summary box #receita)."""
    return f'<p class="uso"><b>Na prova:</b> {text} (<a href="#receita">as 5 fórmulas</a>)</p>'


def row(h, prior, cells):
    """Practice-table row: hypothesis, given prior, then (answer, tol) input cells."""
    tds = "".join(f'<td><input data-answer="{a}" data-tol="{t}"></td>' for a, t in cells)
    return f"<tr><td>{h}</td><td>{prior}</td>{tds}</tr>"


aquecimento = r"""
<p>Esta lição se apoia na regra de Bayes da P1. Antes de construir em cima dela, vale testar o que ficou. O problema é do próprio MIT11:</p>
""" + quote(r"""<p>A screening test for a disease is both sensitive and specific. By that we mean it is usually positive when testing
a person with the disease and usually negative when testing someone without the disease. Let’s assume the true positive rate is 99%
and the false positive rate is 2%. Suppose the prevalence of the disease in the general population is 0.5%. If a random person tests
positive, what is the probability that they have the disease?</p>""", src("apêndice §5, exemplo 4")) + mc(
    "Responda de cabeça, sem conta:",
    [("Cerca de 99%", False, "Esse número é P(+ | doente), não P(doente | +). Confundir os dois é a falácia da taxa-base."),
     ("Cerca de 50%", False, "Ainda é alto demais. Pense em 1000 pessoas: só 5 estão doentes, mas uns 20 sadios testam positivo."),
     ("Cerca de 20%", True, "Isso. Dos cerca de 25 positivos em cada 1000 pessoas, só uns 5 estão doentes. A conta exata vem logo abaixo."),
     ("Cerca de 2%", False, "Esse é o falso-positivo, P(+ | sadio). A pergunta é P(doente | +).")]
) + r"""
<p>A ferramenta é a regra de Bayes, com o denominador vindo da probabilidade total:</p>
$$P(H \mid D) = \frac{P(D \mid H)\,P(H)}{P(D)}, \qquad P(D) = \sum_{H} P(D \mid H)\,P(H).$$
<p>Aqui, \(P(+) = 0.99 \cdot 0.005 + 0.02 \cdot 0.995 = 0.02485\), e portanto
\(P(\text{doente} \mid +) = 0.00495 / 0.02485 \approx 0.199\). O teste multiplicou a chance por 40,
mas a doença continua improvável, porque ela é rara: só 0.5% da população tem. Esse 0.5% é a <b>taxa-base</b>.
Quem chuta 99% caiu na <b>falácia da taxa-base</b>: ignorou a raridade e confundiu \(P(+ \mid \text{doente})\) com \(P(\text{doente} \mid +)\).</p>
<p id="quadrado">Dá para <em>ver</em> esses 20%. Desenhe a população como um quadrado de área 1:</p>
<ul>
<li>cada hipótese é uma faixa vertical, e a <b>largura</b> da faixa é a chance dela antes do teste (0.005 e 0.995);</li>
<li>dentro de cada faixa, a parte <b>pintada</b> são as pessoas que testam positivo, e a altura dela é a chance de positivo naquela faixa (0.99 e 0.02);</li>
<li>o teste deu positivo, então a pessoa está em algum lugar da área pintada. Todo o resto do quadrado foi descartado.</li>
</ul>
""" + bayes_square(
    [("doente", .005, .99), ("sadio", .995, .02)],
    "Fora de escala: com 0.5% de largura, a faixa dos doentes não apareceria. As duas áreas pintadas foram ampliadas 20 vezes, "
    "por igual, então a proporção entre elas (e a barra da direita) é a verdadeira.",
    display=[(.1, .99), (.9, .442)]) + r"""
<p>A faixa dos doentes é estreita e quase toda pintada. A dos sadios é enorme e só tem uma parte fina pintada embaixo. Mesmo assim, a área pintada dos sadios
é maior: 0.995 · 0.02 = 0.0199 contra 0.005 · 0.99 = 0.00495. Dos positivos, só 1 em cada 5 está doente. O 99% é a altura
da faixa dos doentes, mas a pergunta é sobre a <em>fatia</em> da área pintada.</p>

<h3 id="termos">Dando nome às partes</h3>
<p>Você acabou de fazer uma inferência bayesiana completa sem usar o vocabulário dela. Cada número da conta tem um nome, e o resto
da P2 usa esses nomes o tempo todo. O MIT11 define os termos usando este mesmo problema:</p>
""" + quote(r"""<p><b>Data:</b> The data are the results of the experiment. In this case, the positive test.</p>
<p><b>Hypotheses:</b> The hypotheses are the possible answers to the question being asked. In this case they are \(\mathcal{H}_+\) the
patient has the disease; \(\mathcal{H}_-\) they don’t.</p>
<p><b>Likelihoods:</b> The likelihood given a hypothesis is the probability of the data given that hypothesis. In this case there are
two likelihoods, one for each hypothesis</p>
<p style="text-align:center">\(P(\mathcal{T}_+ \mid \mathcal{H}_+) = 0.99\) and \(P(\mathcal{T}_+ \mid \mathcal{H}_-) = 0.02\).</p>
<p>We repeat: the likelihood is a probability given the hypothesis, not a probability of the hypothesis.</p>
<p><b>Prior probabilities of the hypotheses:</b> The priors are the probabilities of the hypotheses prior to collecting data. In this case,</p>
<p style="text-align:center">\(P(\mathcal{H}_+) = 0.005\) and \(P(\mathcal{H}_-) = 0.995\)</p>
<p><b>Posterior probabilities of the hypotheses:</b> The posteriors are the probabilities of the hypotheses given the data. In this case</p>
<p style="text-align:center">\(P(\mathcal{H}_+ \mid \mathcal{T}_+) = 0.199\) and \(P(\mathcal{H}_- \mid \mathcal{T}_+) = 0.801\).</p>""",
            src("problemas em sala, solução do problema 1(b)")) + r"""
<p>Na notação do MIT11, \(\mathcal{T}_+\) é "o teste deu positivo". Em português, e com o papel de cada termo na regra de Bayes:</p>
<table>
<tr><th>termo</th><th>o que é</th><th>no exemplo da doença</th><th>na fórmula</th></tr>
<tr><td><b>dado</b> (data)</td><td>o que foi observado</td><td>o teste deu positivo</td><td>\(D\)</td></tr>
<tr><td><b>hipóteses</b></td><td>as respostas possíveis para a pergunta</td><td>doente; sadio</td><td>\(H\)</td></tr>
<tr><td><b>prior</b></td><td>probabilidade de cada hipótese <em>antes</em> de ver o dado</td><td>0.005; 0.995</td><td>\(P(H)\)</td></tr>
<tr><td><b>likelihood</b></td><td>probabilidade do dado <em>supondo</em> cada hipótese verdadeira</td><td>0.99; 0.02</td><td>\(P(D \mid H)\)</td></tr>
<tr><td><b>posterior</b></td><td>probabilidade de cada hipótese <em>depois</em> de ver o dado</td><td>0.199; 0.801</td><td>\(P(H \mid D)\)</td></tr>
</table>
<p>Repare que prior e posterior são probabilidades das hipóteses: cada coluna soma 1 (0.005 + 0.995 e 0.199 + 0.801).
A likelihood é outra coisa. Ela é uma probabilidade do dado, e seus dois valores (0.99 e 0.02) não somam 1, nem precisam.
Passar da prior para a posterior tem nome próprio:</p>
""" + quote(r"""<p>The process of going from the prior probability \(P(\mathcal{H})\) to the posterior \(P(\mathcal{H} \mid D)\) is called
<b>Bayesian updating</b>. Bayesian updating uses the data to alter our understanding of the probability of each of the possible hypotheses.</p>""",
            src("§3")) + r"""
<p>Por isso o título desta lição fala em <em>atualização</em>. A tabela da próxima seção é só um jeito organizado de fazer esse cálculo.</p>
"""

tabela = r"""
<p>A tabela fica clara num exemplo pequeno, com três hipóteses. O enunciado do MIT11, completo:</p>
""" + quote(r"""<p>There are three types of coins which have different probabilities of landing heads when tossed.</p>
<ul><li>Type \(A\) coins are fair, with probability 0.5 of heads</li>
<li>Type \(B\) coins are bent and have probability 0.6 of heads</li>
<li>Type \(C\) coins are bent and have probability 0.9 of heads</li></ul>
<p>Suppose I have a drawer containing 5 coins: 2 of type \(A\), 2 of type \(B\), and 1 of type \(C\). I reach into the drawer and pick
a coin at random. Without showing you the coin I flip it once and get heads. What is the probability it is type \(A\)? Type \(B\)? Type \(C\)?</p>""",
            src("§3, exemplo 1")) + r"""
<p>Com os nomes da seção <a href="#termos">Dando nome às partes</a>:</p>
<ul>
<li><b>dado</b> \(D\): "saiu cara";</li>
<li><b>hipóteses</b>: a moeda é do tipo A, B ou C;</li>
<li><b>prior</b>: 0.4, 0.4 e 0.2, a fração de cada tipo na gaveta (2, 2 e 1 de 5 moedas);</li>
<li><b>likelihood</b>: 0.5, 0.6 e 0.9, a chance de cara para cada tipo;</li>
<li><b>posterior</b>: é o que a questão pede.</li>
</ul>
<p>Um detalhe da likelihood: nela o dado fica fixo e o que varia é a hipótese.</p>
""" + quote(r"""<p><b>Likelihood:</b> […] The likelihood function is \(P(D \mid \mathcal{H})\), i.e., the probability of the data assuming that
the hypothesis is true. Most often we will consider the data as fixed and let the hypothesis vary.</p>""", src("§3")) + r"""
<p>Para cada hipótese basta aplicar a regra de Bayes acima, e o denominador é o mesmo em todas. A tabela é essa conta organizada em
colunas, não uma fórmula nova. Cada termo da fórmula vira uma coluna:</p>
$$\underbrace{P(H \mid D)}_{\text{posterior}} \;=\; \dfrac{\overbrace{P(D \mid H)}^{\text{likelihood}}\;\cdot\;\overbrace{P(H)}^{\text{prior}}}{\underbrace{P(D)}_{\text{soma dos numeradores}}}$$
""" + uso("são as fórmulas 2, 3 e 4.") + r"""
<p>A tabela do MIT11 para o exemplo, exatamente como está lá:</p>
""" + quote(r"""<table>
<tr><th>hypothesis</th><th>prior</th><th>likelihood</th><th>Bayes numerator</th><th>posterior</th></tr>
<tr><th>\(\mathcal{H}\)</th><th>\(P(\mathcal{H})\)</th><th>\(P(D \mid \mathcal{H})\)</th><th>\(P(D \mid \mathcal{H})P(\mathcal{H})\)</th><th>\(P(\mathcal{H} \mid D)\)</th></tr>
<tr><td>A</td><td>0.4</td><td>0.5</td><td>0.2</td><td>0.3226</td></tr>
<tr><td>B</td><td>0.4</td><td>0.6</td><td>0.24</td><td>0.3871</td></tr>
<tr><td>C</td><td>0.2</td><td>0.9</td><td>0.18</td><td>0.2903</td></tr>
<tr><td>total</td><td>1</td><td>NO SUM</td><td>\(P(D) = 0.62\)</td><td>1</td></tr>
</table>
<p>The Bayes numerator is the product of the prior and the likelihood. We see in each of the Bayes’ formula computations above that
the posterior probability is obtained by dividing the Bayes numerator by \(P(D) = 0.62\). We also see that the law of total
probability says that \(P(D)\) is the sum of the entries in the Bayes numerator column.</p>""", src("§3, tabela do exemplo 1")) + prior_post(
    [("A", .4, .3226), ("B", .4, .3871), ("C", .2, .2903)],
    "Prior e posterior de cada moeda depois de uma cara. O número cinza é o fator que multiplicou a prior.") + r"""
<p>De onde vem esse fator? Dividindo os dois lados da regra de Bayes pela prior:</p>
$$\frac{P(H \mid D)}{P(H)} = \frac{P(D \mid H)}{P(D)}.$$
<p>Cada prior é multiplicada pela sua likelihood dividida por \(P(D)\). E \(P(D) = 0.62\) é a likelihood <em>média</em> das
hipóteses, ponderada pela prior: \(0.4 \cdot 0.5 + 0.4 \cdot 0.6 + 0.2 \cdot 0.9\). Daí sai uma regra que dispensa conta:
<b>a hipótese ganha probabilidade se a likelihood dela é maior que a média, e perde se é menor</b>.
Assim, A (0.5) perde bastante (× 0.81), B (0.6) perde um pouco (× 0.97) e C (0.9) ganha (× 1.45).
Mesmo multiplicada por 1.45, a prior baixa de C não alcança B, e B continua na frente.</p>
<p>A mesma tabela, no <a href="#quadrado">quadrado do aquecimento</a>, agora com três faixas e desenhado em escala:</p>
""" + bayes_square(
    [("A", .4, .5), ("B", .4, .6), ("C", .2, .9)],
    "Moedas do MIT11 depois de uma cara. A faixa de C é a mais pintada, mas tem metade da largura de B.") + r"""
<p>Cada coluna da tabela é uma peça do desenho:</p>
<table>
<tr><th>na tabela</th><th>no quadrado</th></tr>
<tr><td>prior</td><td>largura da faixa (as larguras somam 1)</td></tr>
<tr><td>likelihood</td><td>altura da parte pintada (cada faixa tem a sua, por isso não somam 1)</td></tr>
<tr><td>numerador</td><td>área pintada da faixa, largura × altura</td></tr>
<tr><td>\(P(D)\)</td><td>área pintada total</td></tr>
<tr><td>posterior</td><td>fatia da área pintada que cai na faixa</td></tr>
</table>
<p><b>Normalizar</b> (o termo vem logo abaixo) é jogar fora a parte não pintada e esticar a pintada até virar área 1.
O desenho serve para a intuição. Na prova, você faz a tabela.</p>
""" + mc("No quadrado, onde aparece a regra 'ganha quem tem likelihood acima da média'?",
         [("Faixa pintada acima da altura média", True, "Isso. A altura média ponderada pelas larguras é P(D) = 0.62; C (0.9) passa dela e ganha fatia."),
          ("Faixa mais larga que a média delas", False, "A largura é a prior. Ela pesa, mas quem decide se a faixa ganha ou perde é a altura."),
          ("Faixa com a maior área pintada", False, "A maior área pintada dá a maior posterior, não o maior ganho. Ganhar é a fatia passar da largura (a prior), e isso depende só da altura.")]) + r"""
<p>A tabela ensina mais quatro coisas, que o MIT11 lista abaixo. Antes, dois termos que elas usam. <b>Normalizar</b> é dividir cada numerador
por \(P(D)\), para que a coluna some 1 e vire probabilidade. O <b>MLE</b> (<em>maximum likelihood estimate</em>, estimativa de máxima
verossimilhança) é escolher a hipótese de maior likelihood, sem olhar a prior.</p>
""" + quote(r"""<ol start="4">
<li>If all we care about is finding the most likely hypothesis, the Bayes numerator works as well as the normalized posterior.</li>
<li>The likelihood column does not sum to 1. The likelihood function is not a probability function.</li>
<li>The posterior probability represents the outcome of a ‘tug-of-war’ between the likelihood and the prior. When calculating the
posterior, a large prior may be deflated by a small likelihood, and a small prior may be inflated by a large likelihood.</li>
<li>The maximum likelihood estimate (MLE) for Example 1 is hypothesis \(C\), with a likelihood \(P(D \mid C) = 0.9\). The MLE is useful,
but you can see in this example that it is not the entire story, since type \(B\) has the greatest posterior probability.</li></ol>
<p>[…] This leads to the most elegant form of Bayes’ theorem in the context of Bayesian updating:</p>
<p style="text-align:center"><b>posterior \(\propto\) likelihood \(\times\) prior</b></p>""", src("§3.1, itens 4 a 7")) + r"""
<p>Mais uma consequência da tabela: se o dado é impossível sob uma hipótese, \(P(D \mid H) = 0\) e o numerador dela zera, qualquer que
seja a prior. Tirar 5 num dado de 4 lados, por exemplo: essa hipótese sai do jogo de uma vez.</p>
""" + mc("Na tabela, a coluna likelihood guarda:",
         [("\\(P(\\text{dado} \\mid \\text{hipótese})\\)", True, "Isso: a probabilidade do dado supondo que a hipótese é verdadeira."),
          ("\\(P(\\text{hipótese} \\mid \\text{dado})\\)", False, "Essa é a posterior, a última coluna."),
          ("\\(P(\\text{hipótese e dado})\\)", False, "Essa é a probabilidade conjunta, de a hipótese ser verdadeira E o dado acontecer. Ela é exatamente o numerador: prior × likelihood.")])

repetidos = r"""
<p>Até aqui houve um dado só. O MIT11 continua jogando a mesma moeda. Na tabela dele, cada moeda aparece pela sua chance de cara:
0.5 é a moeda A, 0.6 é a B e 0.9 é a C.</p>
""" + quote(r"""<p>[…] In Bayesian inference, after updating the prior to the posterior, we can take more data and update again!
For the second update, the posterior from the first data becomes the prior for the second data.</p>
<p><b>Example 3.</b> Suppose you have picked a coin as in Example 1. You flip it once and get heads. Then you flip the same coin and
get heads again. What is the probability that the coin was type A? Type B? Type C?</p>
<table>
<tr><th>hypothesis</th><th>prior</th><th>likelihood 1</th><th>Bayes numerator 1</th><th>likelihood 2</th><th>Bayes numerator 2</th><th>posterior 2</th></tr>
<tr><td>0.5</td><td>0.4</td><td>0.5</td><td>0.2</td><td>0.5</td><td>0.1</td><td>0.2463</td></tr>
<tr><td>0.6</td><td>0.4</td><td>0.6</td><td>0.24</td><td>0.6</td><td>0.144</td><td>0.3547</td></tr>
<tr><td>0.9</td><td>0.2</td><td>0.9</td><td>0.18</td><td>0.9</td><td>0.162</td><td>0.3990</td></tr>
<tr><td>total</td><td>1</td><td>NO SUM</td><td></td><td>NO SUM</td><td>0.406</td><td>1</td></tr>
</table>
<p>Note that the second Bayes numerator is computed by multiplying the first Bayes numerator and the second likelihood; since we are
only interested in the final posterior, there is no need to normalize until the last step. As shown in the last column […],
after two heads the type C hypothesis has finally taken the lead!</p>""", src("§4, exemplo 3")) + prior_post(
    [("A", .4, .2463), ("B", .4, .3547), ("C", .2, .3990)],
    "Prior e posterior de cada moeda depois de duas caras. O número cinza é o fator que multiplicou a prior.") + r"""
<p>Os fatores agora são likelihood² ÷ \(P(D)\):</p>
<ul>
<li><b>A:</b> \(0.5^2/0.406 = 0.62\)</li>
<li><b>B:</b> \(0.6^2/0.406 = 0.89\)</li>
<li><b>C:</b> \(0.9^2/0.406 = 2.00\)</li>
</ul>
<p>Elevar ao quadrado afasta as likelihoods umas das outras, e por isso a segunda cara puxa
ainda mais forte para C, que passa B.</p>
<p>O trecho junta duas formas de fazer a mesma conta, e vale separá-las:</p>
<ul>
<li><b>Versão ingênua:</b> atualizar duas vezes, normalizando no meio. A posterior do primeiro lançamento vira a prior do segundo.</li>
<li><b>Atalho, que é uma otimização da ingênua e não outra fórmula:</b> multiplicar as likelihoods e normalizar só no fim. Você poupa a divisão
intermediária e não perde nada. Normalizar no meio só multiplica tudo por uma constante, e ela some na normalização final.</li>
</ul>
<p>Você vai ver as duas formas lado a lado logo depois da prática, com dados em vez de moedas.</p>
""" + uso("o atalho é a fórmula 5.")

dados = r"""
<p>Hora de usar a tabela:</p>
""" + quote(r"""<p><b>Problem 2. Dice</b> I have five dice: 4-sided, 6-sided, 8-sided, 12-sided, 20-sided.
I pick one at random, roll it and report that the roll was a 13.</p>
<p>Goal: Find the probabilities the die is 4, 6, 8, 12 or 20 sided.</p>""", src("problemas em sala, problema 2")) + r"""
<p>Com um 13, o problema quase não tem conta. Os dados de 4, 6, 8 e 12 lados não têm face 13, então a likelihood deles é 0 e eles
saem da tabela. Na solução do MIT11 (\(\mathcal{H}_n\) é "o dado tem \(n\) lados"):</p>
""" + quote(r"""<table>
<tr><th>hypothesis</th><th>prior</th><th>likelihood</th><th>Bayes numerator</th><th>posterior</th></tr>
<tr><th>\(\mathcal{H}\)</th><th>\(P(\mathcal{H})\)</th><th>\(P(D \mid \mathcal{H})\)</th><th>\(P(D \mid \mathcal{H})P(\mathcal{H})\)</th><th>\(P(\mathcal{H} \mid D)\)</th></tr>
<tr><td>\(\mathcal{H}_4\)</td><td>1/5</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>\(\mathcal{H}_6\)</td><td>1/5</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>\(\mathcal{H}_8\)</td><td>1/5</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>\(\mathcal{H}_{12}\)</td><td>1/5</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>\(\mathcal{H}_{20}\)</td><td>1/5</td><td>1/20</td><td>1/100</td><td>1</td></tr>
<tr><td>total</td><td>1</td><td></td><td>1/100</td><td>1</td></tr>
</table>
<p>The only possibility is the 20-sided die.</p>""", src("problemas em sala, solução do problema 2(c)")) + r"""
<p>O item seguinte do problema troca o 13 por um número que vários dados conseguem dar:</p>
""" + quote(r"""<p>(d) Same question if I had reported a 5.</p>""", src("problemas em sala, problema 2(d)")) + r"""
<p>Agora só o dado de 4 lados sai, e sobram quatro hipóteses disputando. Preencha a tabela. Aceita fração (<code>1/30</code>) ou decimal (<code>0.392</code>).</p>
<div class="check-group" data-ok="O dado de 4 lados sai da disputa e o de 6 lidera: quanto menos faces, mais provável fica cada face.">
<table>
<tr><th>dado</th><th>prior</th><th>likelihood</th><th>numerador</th><th>posterior</th></tr>
""" + "".join(row(h, "1/5", [(lk, .0005), (nu, .0005), (po, .003)]) for h, lk, nu, po in [
    ("4 lados", "0", "0", "0"), ("6 lados", "1/6", "1/30", "0.3922"), ("8 lados", "1/8", "1/40", "0.2941"),
    ("12 lados", "1/12", "1/60", "0.1961"), ("20 lados", "1/20", "1/100", "0.1176")]) + r"""
<tr><th>total</th><th>1</th><th></th><th>\(P(D)\) = <input data-answer="0.085" data-tol="0.0005"></th><th>1</th></tr>
</table>
<button class="check">Verificar</button><div class="feedback"></div>
</div>

<h3 id="dois-lancamentos">Dois lançamentos: passo a passo ou de uma vez</h3>
<p>Mesmos cinco dados, escolhidos ao acaso (prior 1/5 para cada um), mas agora com dois lançamentos:</p>
""" + quote(r"""<p><b>Problem 3. Iterated updates</b> Suppose I rolled a 9 and then a 5.</p>
<p>(a) Do the Bayesian update in two steps: Step 1: First update for the 9. Step 2: Then update the update for the 5.</p>
<p>(b) Do the Bayesian update in one step. That is, the data is \(D\) = ‘9 followed by 5’</p>""",
            src("problemas em sala, problema 3")) + r"""
<p><b>(a) Em dois passos.</b> O primeiro numerador usa a likelihood de tirar 9. O segundo multiplica esse numerador pela
likelihood de tirar 5, e só no fim se normaliza. Na solução do MIT11 (\(D_1\) = tirou 9, \(D_2\) = tirou 5):</p>
""" + quote(r"""<table>
<tr><th>hyp.</th><th>prior</th><th>likel. 1</th><th>Bayes num. 1</th><th>likel. 2</th><th>Bayes num. 2</th><th>posterior</th></tr>
<tr><th>\(\mathcal{H}\)</th><th>\(P(\mathcal{H})\)</th><th>\(P(D_1 \mid \mathcal{H})\)</th><th>* * *</th><th>\(P(D_2 \mid \mathcal{H})\)</th><th>* * *</th><th>\(P(\mathcal{H} \mid D_1, D_2)\)</th></tr>
<tr><td>\(\mathcal{H}_4\)</td><td>1/5</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>\(\mathcal{H}_6\)</td><td>1/5</td><td>0</td><td>0</td><td>1/6</td><td>0</td><td>0</td></tr>
<tr><td>\(\mathcal{H}_8\)</td><td>1/5</td><td>0</td><td>0</td><td>1/8</td><td>0</td><td>0</td></tr>
<tr><td>\(\mathcal{H}_{12}\)</td><td>1/5</td><td>1/12</td><td>1/60</td><td>1/12</td><td>1/720</td><td>0.735</td></tr>
<tr><td>\(\mathcal{H}_{20}\)</td><td>1/5</td><td>1/20</td><td>1/100</td><td>1/20</td><td>1/2000</td><td>0.265</td></tr>
<tr><td>total</td><td>1</td><td></td><td></td><td></td><td>0.0019</td><td>1</td></tr>
</table>""", src("problemas em sala, solução do problema 3(a)")) + r"""
<p>Os dados de 4, 6 e 8 lados já zeram no primeiro passo, porque não dão 9.</p>
<p><b>(b) De uma vez.</b> O dado observado é o par "9 depois 5", e a likelihood do par é o produto das duas: \(\tfrac{1}{12}\cdot\tfrac{1}{12} = \tfrac{1}{144}\)
e \(\tfrac{1}{20}\cdot\tfrac{1}{20} = \tfrac{1}{400}\):</p>
""" + quote(r"""<table>
<tr><th>hypothesis</th><th>prior</th><th>likelihood</th><th>Bayes numerator</th><th>posterior</th></tr>
<tr><th>\(\mathcal{H}\)</th><th>\(P(\mathcal{H})\)</th><th>\(P(D \mid \mathcal{H})\)</th><th>\(P(D \mid \mathcal{H})P(\mathcal{H})\)</th><th>\(P(\mathcal{H} \mid D)\)</th></tr>
<tr><td>\(\mathcal{H}_4\)</td><td>1/5</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>\(\mathcal{H}_6\)</td><td>1/5</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>\(\mathcal{H}_8\)</td><td>1/5</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>\(\mathcal{H}_{12}\)</td><td>1/5</td><td>1/144</td><td>1/720</td><td>0.735</td></tr>
<tr><td>\(\mathcal{H}_{20}\)</td><td>1/5</td><td>1/400</td><td>1/2000</td><td>0.265</td></tr>
<tr><td>total</td><td>1</td><td></td><td>0.0019</td><td>1</td></tr>
</table>""", src("problemas em sala, solução do problema 3(b)")) + r"""
<p>Os numeradores finais são os mesmos (1/720 e 1/2000), e portanto as posteriores também: 0.735 e 0.265. É exatamente isso que a
Q1 da lista abaixo pede, com dois 5.</p>
"""

receita = r"""
<p><b>Passo zero: ler o enunciado.</b> Antes de qualquer fórmula, responda quatro perguntas. No exemplo da gaveta de moedas:</p>
<ol>
<li><b>O que eu não sei?</b> A <b>hipótese</b> \(H\): o tipo da moeda (A, B ou C).</li>
<li><b>O que eu observei?</b> O <b>dado</b> \(D\): saiu cara.</li>
<li><b>O que eu achava antes de observar?</b> A <b>prior</b> \(P(H)\): 0.4, 0.4 e 0.2, a fração de cada tipo na gaveta.</li>
<li><b>Se eu já soubesse \(H\), qual seria a chance de ver exatamente esse dado?</b> A <b>likelihood</b> \(P(D \mid H)\): 0.5, 0.6 e 0.9.</li>
</ol>
<p>Depois do passo zero, as fórmulas:</p>
<div class="callout"><p>Todo o resto da lição explica por que estas fórmulas funcionam; para resolver as questões, basta isto:</p>
<table>
<tr><th>#</th><th>para quê</th><th>fórmula</th></tr>
<tr><td>1</td><td>prior dada como proporção</td><td>\(P(H) = \dfrac{\text{peso de } H}{\text{soma dos pesos}}\)</td></tr>
<tr><td>2</td><td>numerador (uma linha da tabela)</td><td>\(P(D \mid H)\,P(H)\)<br>(likelihood 0 zera a linha)</td></tr>
<tr><td>3</td><td>total</td><td>\(P(D) = \sum_H P(D \mid H)\,P(H)\), a soma dos numeradores</td></tr>
<tr><td>4</td><td>posterior</td><td>\(P(H \mid D) = \dfrac{P(D \mid H)\,P(H)}{P(D)}\)</td></tr>
<tr><td>5</td><td>vários dados independentes</td><td>\(P(D_1, D_2 \mid H) = P(D_1 \mid H)\,P(D_2 \mid H)\)<br>(multiplique as likelihoods e normalize só no fim)</td></tr>
</table></div>
"""

objetivo = quote(r"""<p><b>Questão 1 - Prior discreta e Likelihood discreta</b></p>
<p>Suponha que você tenha uma caixa com dados de 4, 6, 8, 12 e 20 lados. Você suspeita que eles estão na proporção 1:2:10:2:1.
Seu amigo escolhe um dado aleatoriamente e joga duas vezes, obtendo 5 ambas as vezes.</p>
<p>1. Qual a probabilidade de seu amigo ter escolhido o dado de 8 lados?</p>""",
                 f'<a href="{L03}">L03</a>, questão 1', lang="pt-BR") + rf"""
<p>A Q1.1 usa as cinco fórmulas: a 1 dá a prior, a 5 dá a likelihood dos dois 5, e a 2, a 3 e a 4 completam a tabela.</p>
<p>Faça em um passo só, como na forma (b) de <a href="#dois-lancamentos">Dois lançamentos</a>: o dado observado é o par "5 e 5", e a coluna likelihood é
\(P(5, 5 \mid H)\). Você preenche prior, likelihood e posterior. O numerador (prior × likelihood) e \(P(D)\) se calculam
sozinhos enquanto você digita, em fração exata se você digitar frações. A pergunta é só sobre o dado de 8 lados, mas a tabela
inteira é necessária, porque \(P(D)\) soma todas as linhas. As dicas são para quando travar.</p>
<details><summary>Dica 1: a prior</summary><p>Uma proporção não é uma probabilidade. Divida cada peso pelo total, 1+2+10+2+1 = 16.</p></details>
<details><summary>Dica 2: a likelihood</summary><p>Dados dois lançamentos independentes, a likelihood é \((1/n)^2\) para o dado de \(n\) faces com \(n \ge 5\). E para o dado de 4 lados?</p></details>
""" + bayes_table(
    [("4 lados", "1/16", "0", "0"), ("6 lados", "2/16", "1/36", "0.2435"), ("8 lados", "10/16", "1/64", "0.6847"),
     ("12 lados", "2/16", "1/144", "0.0609"), ("20 lados", "1/16", "1/400", "0.0110")],
    ok=f"A resposta da Q1.1 é P(8 lados | 5, 5) ≈ 0.685. Confira no <a href='{L03G}'>L03G</a>, página 1: a solução lá é imagem, então compare com o PDF aberto.",
    lik_header="likelihood \\(P(5, 5 \\mid H)\\)") + r"""
<p>As Q1.2 e Q1.3 perguntam a probabilidade do <em>próximo</em> lançamento. Isso é a <b>posterior predictive</b>, assunto da <a href="https://claude.ai/artifact/PDFMi8VTuLgeRxHe39qE3Z">lição 0002</a>
pelo MIT12, e a coluna posterior que você acabou de calcular é metade da conta. Guarde a sua tabela.</p>
"""

fontes = rf"""
<p>Esta lição foi feita para bastar sozinha naquilo que a P2 cobra do MIT11. O que ficou de fora do
<a href="{MIT11}">MIT11, Bayesian Updating with Discrete Priors</a>:</p>
<table>
<tr><th>trecho do MIT11</th><th>por que ficou de fora</th><th>faz falta na P2?</th></tr>
<tr><td>§3.2, prior e posterior escritas como pmf (função de massa de probabilidade, da P1): \(p(\theta)\), \(p(x \mid \theta)\), \(p(\theta \mid x)\)</td><td>só passa a importar com prior contínua</td><td>sim, mas entra na lição do MIT13</td></tr>
<tr><td>Tabela de likelihood completa e exemplo 2 (saiu coroa)</td><td>é a mesma conta com outro dado</td><td>não</td></tr>
<tr><td>§3.3 (como escolher a hipótese sem saber quantas moedas há de cada tipo) e a concept question (escolher entre tratamentos que curaram 3 de 3, 19 de 20 ou 90000 de 100000 pacientes)</td><td>perguntas de reflexão, sem conta</td><td>não</td></tr>
<tr><td>Problema 1 e extra 1 (doença, um dado de 4 contra 999 de 6)</td><td>repetem o aquecimento e a prática</td><td>não; servem de treino extra</td></tr>
<tr><td>Problema 4, <em>probabilistic prediction</em>: com os cinco dados, a probabilidade de tirar 5 e, depois de um 5, a de o próximo lançamento dar 4</td><td>é o começo da posterior predictive</td><td>sim, na lição 0002 (MIT12)</td></tr>
</table>
<p>O <a href="#quadrado">quadrado</a> vem do vídeo <a href="https://www.youtube.com/watch?v=HZGCoVF3YvM">Bayes theorem, the geometry of changing beliefs</a>
(3Blue1Brown, 15 min, com legendas em português). Ele é complementar: a conta continua sendo a do MIT11, e o vídeo ajuda a ver por que ela funciona.</p>
<div class="callout">Se ficou alguma dúvida, pergunte ao seu professor, que é o agente nesta conversa. Vale um passo da conta, um termo ou "por que isso funciona?".</div>
<p style="font-size:.8rem;color:var(--muted)">As citações em inglês são de J. Orloff e J. Bloom, <i>18.05 Introduction to Probability and Statistics</i>,
Spring 2022, MIT OpenCourseWare, licença CC BY-NC-SA 4.0. Trechos omitidos aparecem como […].</p>
"""

SPEC = {
    "title": "0001 · Tabela de atualização bayesiana",
    "subtitle": "Lição 0001 · COE241 P2 · MIT11 · prior discreta, likelihood discreta · meta: resolver a L03 Q1.1",
    "crumbs": 'COE241 · P2 · Lição 0001 &nbsp;·&nbsp; anterior: <a href="https://claude.ai/artifact/MRMXzP4WVzLVFtDM72Fzks">0000, MLE</a> &nbsp;·&nbsp; próxima: <a href="https://claude.ai/artifact/PDFMi8VTuLgeRxHe39qE3Z">0002, probabilidade preditiva</a>',
    "sections": [
        {"id": "aquecimento", "heading": "Aquecimento: o que sobrou da P1", "html": aquecimento},
        {"id": "tabela", "heading": "A tabela é a regra de Bayes, linha por linha", "html": tabela},
        {"id": "repetidos", "heading": "Mais de um dado observado", "html": repetidos},
        {"id": "pratica", "heading": "Prática: os cinco dados do MIT", "html": dados},
        {"id": "receita", "heading": "Como resolver: passo zero e as 5 fórmulas", "html": receita},
        {"id": "objetivo", "heading": "O objetivo: L03 Q1.1", "html": objetivo},
        {"id": "fontes", "heading": "O que ficou de fora do MIT11", "html": fontes},
    ],
    "quiz": [
        {"question": r"Moedas com priores \(0.4\), \(0.4\) e \(0.2\) e chances de cara \(0.5\), \(0.6\) e \(0.9\). Saiu cara. Quanto vale \(P(D)\)?",
         "ref": [("tabela", "A tabela é a regra de Bayes, linha por linha")],
         "options": [
             {"text": r"\(0.62\)", "correct": True, "feedback": r"Soma dos numeradores: \(0.4 \cdot 0.5 + 0.4 \cdot 0.6 + 0.2 \cdot 0.9 = 0.62\), a likelihood média ponderada pela prior."},
             {"text": r"\(2.00\)", "correct": False, "feedback": r"Essa é a soma das likelihoods, que não tem significado: o dado está fixo e a hipótese varia. Some os numeradores."},
             {"text": r"\(0.67\)", "correct": False, "feedback": r"Essa é a média das likelihoods sem pesos. \(P(D)\) pondera cada uma pela prior: \(0.4 \cdot 0.5 + 0.4 \cdot 0.6 + 0.2 \cdot 0.9 = 0.62\)."}]},
        {"question": r"Há cinco dados (\(4\), \(6\), \(8\), \(12\) e \(20\) lados), e um foi escolhido ao acaso. O lançamento deu \(7\). O que acontece com a hipótese 'é o dado de \(6\) lados'?",
         "ref": [("pratica", "Prática: os cinco dados do MIT")],
         "options": [
             {"text": r"A posterior dela vira \(0\)", "correct": True, "feedback": r"A likelihood é \(0\), então o numerador é \(0\), qualquer que seja a prior."},
             {"text": "A posterior cai, sem zerar", "correct": False, "feedback": r"Não há meio-termo: \(P(7 \mid 6 \text{ lados}) = 0\) anula o numerador, qualquer que seja a prior."},
             {"text": "A posterior dela fica igual", "correct": False, "feedback": "Só ficaria igual se a likelihood dela fosse igual a P(D). Aqui ela é 0."}]},
        {"question": r"Gaveta com \(2\) moedas A (cara com \(0.5\)), \(2\) B (\(0.6\)) e \(1\) C (\(0.9\)); uma é escolhida ao acaso e dá cara. A posterior de B (\(0.387\)) fica acima da de C (\(0.290\)), embora C tenha a maior likelihood. Por quê?",
         "ref": [("tabela", "A tabela é a regra de Bayes, linha por linha")],
         "options": [
             {"text": "A prior de B é o dobro da de C", "correct": True, "feedback": r"Os numeradores são \(0.4 \cdot 0.6 = 0.24\) contra \(0.2 \cdot 0.9 = 0.18\). É o 'tug-of-war' do MIT11, e a prior venceu essa rodada."},
             {"text": "P(D) é menor na linha de B", "correct": False, "feedback": r"\(P(D)\) é um só para a tabela inteira (\(0.62\)): todas as linhas dividem pelo mesmo número."},
             {"text": "0.6 fica mais perto de P(D)", "correct": False, "feedback": r"Ficar perto da média não faz ganhar: B até perde um pouco (\(\times 0.97\)). O que a põe na frente é a prior, \(0.4\) contra \(0.2\)."}]},
        {"question": r"Com dois lançamentos observados (por exemplo, \(9\) e depois \(5\)), há duas formas de atualizar: passo a passo, normalizando no meio, ou de uma vez, multiplicando as likelihoods. Elas dão:",
         "ref": [("repetidos", "Mais de um dado observado"), ("dois-lancamentos", "Dois lançamentos")],
         "options": [
             {"text": "Exatamente a mesma posterior", "correct": True, "feedback": "Normalizar no meio só reescala, e a escala some no fim."},
             {"text": "Posteriores um pouco diferentes", "correct": False, "feedback": "São idênticas: normalizar no meio só reescala, e a escala some no fim."},
             {"text": "Posteriores bem diferentes", "correct": False, "feedback": r"São idênticas. Na seção dos dois lançamentos, as duas formas dão \(0.735\) e \(0.265\)."}]},
        {"question": r"Na L03 Q1, a caixa tem dados de \(4\), \(6\), \(8\), \(12\) e \(20\) lados na proporção \(1:2:10:2:1\). Por que a prior do dado de \(8\) lados é \(\frac{10}{16}\)?",
         "ref": [("objetivo", "O objetivo: L03 Q1.1")],
         "options": [
             {"text": r"Peso \(10\) dividido pela soma \(16\)", "correct": True, "feedback": r"A proporção \(1:2:10:2:1\) vira probabilidade quando dividida pelo total \(1+2+10+2+1 = 16\)."},
             {"text": r"Peso \(10\) dividido por \(5\) dados", "correct": False, "feedback": r"Dividir por \(5\) só serve para prior uniforme. Aqui os pesos são diferentes."},
             {"text": r"Peso \(10\) dividido pelos outros \(6\)", "correct": False, "feedback": r"\(10:6\) é a chance (odds) contra os outros dados. A probabilidade divide pelo total, \(16\)."}]},
    ],
}

if __name__ == "__main__":
    build(SPEC, ROOT / "lessons" / "0001-tabela-de-atualizacao-bayesiana.html")
