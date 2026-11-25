# probest

Estudo para a P2 de COE241 (Estatística e Modelos Probabilísticos), com lições interativas em HTML geradas com o Claude Code.

## Materiais

Os PDFs (MIT 18.05, listas, gabaritos e provas antigas) estão na pasta do Google Drive:
https://drive.google.com/drive/folders/1epRBrXuGYCBsixNzqd4vQqDMDyAh2PFo

O [RESOURCES.md](RESOURCES.md) liga cada arquivo da pasta ao tópico e à lista em que ele é usado.

## Como o workspace funciona

O workspace segue a skill `/mattpocock-skills:teach`, que define estes arquivos:

- [MISSION.md](MISSION.md): o objetivo (passar na P2), como é o sucesso e o que fica fora.
- [RESOURCES.md](RESOURCES.md): as fontes, com o MIT 18.05 como fonte primária.
- [NOTES.md](NOTES.md): preferências, decisões, contas já feitas e o ponto em que a última sessão parou.
- [GLOSSARY.md](GLOSSARY.md): os termos.
- [learning-records/](learning-records/): diagnósticos do que eu já sei e do que travou.

## Lições

Todas as lições ficam num site só (um artifact privado), com um menu no topo para ir de uma lição a outra: **[abrir o site](https://claude.ai/artifact/3QNqa8LUGvw27jfVpR7UzT)**. A ordem é a de leitura do MIT, e não a ordem em que as lições foram feitas.

| # | Lição | Fonte |
|---|---|---|
| 0000 | Máxima verossimilhança (MLE) | MIT10, LMLE 6–10 |
| 0001 | Tabela de atualização bayesiana | MIT11, L03 Q1.1 |
| 0002 | Probabilidade preditiva | MIT12, L03 Q1.2–1.3 |
| 0003 | Prior contínua e MAP | MIT13, L03 Q2 |
| 0004 | Likelihood contínua | MIT14, L03 Q3 |
| 0005 | Priors conjugadas | MIT15, MIT14 §6, L03 Q4, P2-23.2 Q4.1 |
| 0006 | Intervalos de probabilidade | MIT16, MEX2 13(c–d), P2-23.2 Q4.6 |

A lista das lições, com parte e fontes, fica em `PARTS` no [assets/build.py](assets/build.py): o menu e a página inicial do site saem dela. O HTML de cada lição também está em [lessons/](lessons/) e abre direto no navegador.

## Build

O visual vem do `render.py` da skill **explain-html** (KaTeX, tema claro/escuro, quiz), que está no meu repositório [agent-kit](https://github.com/drbarros2004/agent-kit/tree/main/skills/explain-html). [assets/build.py](assets/build.py) carrega o renderer de `~/.claude/skills/explain-html/render.py` e acrescenta o que é das lições: respostas numéricas ([assets/check.js](assets/check.js)), tabela de Bayes, gráficos de pdf e textos em português. Também injeta a camada de caneta da skill [explain-html-ink](https://github.com/drbarros2004/agent-kit/tree/main/skills/explain-html-ink) (`~/.claude/skills/explain-html-ink/ink.js`): o botão ✎ liga a caneta, e os traços ficam salvos no `db` do artifact (coleção `ink`). Também injeta a camada de notas da skill explain-html (`~/.claude/skills/explain-html/add_notes.py`): selecionar um trecho oferece **Nota** (post-it com LaTeX) ou **Destacar**, e as notas ficam no `db` do artifact (coleção `notes`). O botão das notas fica no canto inferior esquerdo, e o da caneta logo acima. Por isso o site é publicado com `capabilities: {"db": {}}`. Como todas as lições dividem o `db` do site, cada uma usa as coleções `notes-NNNN` e `ink-NNNN`.

Os módulos do MIT 18.05 aparecem como MIT10, MIT11, ... (os arquivos no Drive se chamam M10, M11, ...).

Para gerar uma lição:

```bash
python lessons/src/0001-tabela-de-atualizacao-bayesiana.py
```

Para gerar todas as lições e a página inicial do site (`lessons/index.html`):

```bash
python assets/build.py
```

O fonte fica em `lessons/src/NNNN-*.py` e a saída em `lessons/NNNN-*.html`. A ficha de referência fica em `reference/src/` e gera `reference/`. O renderer embaralha as opções do quiz a cada build.
