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

Os artifacts levam o número da lição no título, na ordem de leitura do MIT (não na ordem em que foram feitos).

| # | Lição | Fonte | Artifact |
|---|---|---|---|
| 0000 | Máxima verossimilhança (MLE) | MIT10, LMLE 6–10 | [abrir](https://claude.ai/artifact/MRMXzP4WVzLVFtDM72Fzks) |
| 0001 | Tabela de atualização bayesiana | MIT11, L03 Q1.1 | [abrir](https://claude.ai/artifact/XWsvKr4dXaFPnc1BAz6Wxa) |
| 0002 | Probabilidade preditiva | MIT12, L03 Q1.2–1.3 | [abrir](https://claude.ai/artifact/PDFMi8VTuLgeRxHe39qE3Z) |
| 0003 | Prior contínua e MAP | MIT13, L03 Q2 | [abrir](https://claude.ai/artifact/Mg37Am6eQ3TsQEvzxY98BT) |
| 0004 | Likelihood contínua | MIT14, L03 Q3 | [abrir](https://claude.ai/artifact/ULdAerrDUzGftPBWRQvrbC) |
| 0005 | Priors conjugadas | MIT15, MIT14 §6, L03 Q4, P2-23.2 Q4.1 | [abrir](https://claude.ai/artifact/2WoxChPHPSesBbiDpU4ZJ8) |

Os artifacts são privados. O HTML de cada lição também está em [lessons/](lessons/) e abre direto no navegador.

## Build

O visual vem do `render.py` da skill **explain-diff-html** (KaTeX, tema claro/escuro, quiz), que está no meu repositório [agent-kit](https://github.com/drbarros2004/agent-kit/tree/main/skills/explain-diff-html). [assets/build.py](assets/build.py) carrega o renderer de `~/.claude/skills/explain-diff-html/render.py` e acrescenta o que é das lições: respostas numéricas ([assets/check.js](assets/check.js)), tabela de Bayes, gráficos de pdf e textos em português. Também injeta a camada de caneta da skill [explain-diff-html-ink](https://github.com/drbarros2004/agent-kit/tree/main/skills/explain-diff-html-ink) (`~/.claude/skills/explain-diff-html-ink/ink.js`): o botão ✎ liga a caneta, e os traços ficam salvos no `db` do artifact (coleção `ink`). Também injeta a camada de notas da skill explain-diff-html-notes (`~/.claude/skills/explain-diff-html-notes/add_notes.py`): selecionar um trecho oferece **Nota** (post-it com LaTeX) ou **Destacar**, e as notas ficam no `db` do artifact (coleção `notes`). O botão das notas fica no canto inferior esquerdo, e o da caneta logo acima. Por isso os artifacts são publicados com `capabilities: {"db": {}}`.

Os módulos do MIT 18.05 aparecem como MIT10, MIT11, ... (os arquivos no Drive se chamam M10, M11, ...).

Para gerar uma lição:

```bash
python lessons/src/0001-tabela-de-atualizacao-bayesiana.py
```

O fonte fica em `lessons/src/NNNN-*.py` e a saída em `lessons/NNNN-*.html`. A ficha de referência fica em `reference/src/` e gera `reference/`. O renderer embaralha as opções do quiz a cada build.
