# TODO de tradução — Dart Brasil

> Arquivo gerado por `python3 tool/traducao/gerar_todo.py`.
> Para mudar este cabeçalho, edite `tool/traducao/todo_cabecalho.md`.
> O processo completo (tradução e sincronização com o upstream) está em `CLAUDE.md`.

Uma página conta como traduzida quando o frontmatter tem `ia-translate: true`.
Parciais em `src/_includes/` usam o mesmo frontmatter (ou
`<!-- ia-translate: true -->` na primeira linha, se não tiverem frontmatter).
Os diagnósticos e lints de `src/data/diagnostics.json` e
`src/data/linter_rules.json` são traduzidos com `tool/i18n/diagnostics_i18n.py`.

Prioridade: primeiro as páginas **traduzidas cujo inglês mudou** (aparecem em
`.traducao-pendente/` depois de uma sincronização), depois as páginas novas e
as entradas de diagnósticos e lints em inglês.
