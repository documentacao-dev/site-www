# CLAUDE.md — Dart Brasil

Este repositório é a tradução para português do Brasil da documentação do
Dart (dart.dev), publicada em <https://dartbrasil.dev>. É um fork do
[dart-lang/site-www](https://github.com/dart-lang/site-www) (remote
`upstream`), parte da org [`documentacao-dev`](https://github.com/documentacao-dev).
O contexto técnico do site (Jaspr, estrutura de pastas, comandos) está no
`AGENTS.md` do upstream:

@AGENTS.md

## Começando do zero (sessão nova)

Em uma máquina ou sessão de nuvem nova, a partir da raiz do repositório:

```console
bash tool/traducao/setup.sh
export PATH="$HOME/.dart-sdk/bin:$HOME/.pub-cache/bin:$PATH"
```

O script instala o Dart SDK na mesma versão do CI (lida de
`.github/workflows/build.yml`), adiciona o remote `upstream`
(dart-lang/site-www), busca histórico suficiente e roda `dart pub get`.
O instalador baixa o SDK de Linux; no macOS use um SDK local na mesma versão.

Comandos úteis depois disso:

- `dart run dash_site build`: build completo do site (gera `_site`). Rode
  antes de abrir PR.
- `dart run dash_site serve`: servidor local.
- `dart run dash_site check-link-references` e `dart run dash_site check-links`:
  os mesmos checks do job de build.
- `python3 tool/traducao/verificar.py`: valida a estrutura das traduções.

## Agentes e paralelismo

- **No máximo 5 agentes em paralelo.** Divida o trabalho em lotes
  equilibrados por tamanho (linhas ou blocos de conflito), sem dois agentes no
  mesmo arquivo. Agentes não fazem commit nem push: quem orquestra confere com
  `verificar.py`, faz o commit por lote e o push.
- **Traduzir páginas novas:** agente `agent-translator`
  (`.claude/agents/agent-translator.md`, modelo **Haiku**). O portão de
  qualidade é o `verificar.py`; se um arquivo falhar duas vezes, refaça-o no
  Haiku com o erro do `verificar.py` no prompt ou corrija o trecho à mão na
  orquestração. Não troque de modelo.
- **Atualizar páginas já traduzidas** (arquivos diff3 de
  `.traducao-pendente/`): agente `atualizar-traducao`
  (`.claude/agents/atualizar-traducao.md`, modelo **Haiku**). Confira o
  resultado com `tool/traducao/verificar.py` e procure trechos que ficaram em
  inglês.
- **Diagnósticos e lints** (`src/data/diagnostics.json` e
  `src/data/linter_rules.json`): `tool/i18n/diagnostics_i18n.py export`,
  tradução em subagentes Haiku e `import` (veja o docstring do script).
- Código Dart, workflows e dados de configuração: resolva diretamente, sem
  agente, e valide com `dart run dash_site analyze-dart` e com o build.

## Onde fica o quê

- `src/content/`: páginas em Markdown (o que se traduz), inclusive o blog.
- `src/_includes/`: parciais Markdown incluídos nas páginas
  (`effective-dart-toc.md` é gerado por `dart run dash_site effective-dart`).
- `src/data/`: menu lateral (`sidenav/`), glossário, changelog e os JSONs de
  diagnósticos e lints. Os textos visíveis também são traduzidos.
- `site/lib/`: implementação Jaspr do site (header, footer e outras
  personalizações do Dart Brasil).
- `.claude/agents/agent-translator.md`: **convenções de tradução** (termos,
  links, âncoras, código). Siga sempre.
- `tool/traducao/`: scripts de tradução e de sincronização (descritos abaixo).
- `tool/i18n/diagnostics_i18n.py`: tradução dos JSONs de diagnósticos e lints.

## Regras de tradução (resumo)

As regras completas estão em `.claude/agents/agent-translator.md`. As mais
importantes:

- Página traduzida tem `ia-translate: true` no frontmatter. Os parciais de
  `src/_includes/` usam o mesmo frontmatter (ou `<!-- ia-translate: true -->`
  na primeira linha, se não tiverem frontmatter).
- Não traduza código, comandos, URLs, chaves de frontmatter, variáveis
  `{{site.*}}`, rótulos de link de referência nem âncoras `{:#id}`.
  Use `[texto traduzido][rótulo original em inglês]`.
- Mantenha a estrutura idêntica ao inglês: títulos, listas, cercas de código,
  code-excerpts, admonitions e tags Liquid.
- Termos técnicos consagrados ficam em inglês (null safety, package, isolate,
  stream, build etc.).

## Ciclo automático: skill `traduzir`

O ciclo inteiro (sync, tradução, verificação, commit, PR, review, correção e
auto-merge) está na skill `.claude/skills/traduzir/SKILL.md`. Rode `/traduzir`
numa sessão local ou na web.

O ciclo semanal roda por rotina agendada do Claude na nuvem, que executa a
skill `traduzir`; o workflow traducao-automatica.yml fica para disparo manual.
No disparo manual (Actions → Tradução automática, com os campos `paginas` e
`sem_merge`), o workflow roda a mesma skill.

No workflow, as etapas determinísticas rodam **sem Claude**, na fase
`preparar`: detectar commits novos do upstream, páginas pendentes e
diagnósticos em inglês (sem nada, o workflow para com custo zero), sync,
`gerar_todo.py` e `verificar.py`. O Claude só entra depois, na branch já
sincronizada, para traduzir, abrir o PR, revisar e ligar o merge.

- Tradução e correção: subagentes **Haiku**. Review: agente
  `revisar-traducao` em **Sonnet**, de contexto limpo, que só aponta.
- Auto-merge só com `verificar.py` zerado e review sem problema grave; senão o
  PR fica com o label `precisa-humano`.
- O disparo manual do workflow precisa do secret `CLAUDE_CODE_OAUTH_TOKEN`
  (gerado com `claude setup-token`) neste repositório; a rotina na nuvem não.
- Os passos abaixo continuam valendo: a skill é a forma de executá-los.

## Regra principal: manter as traduções em dia com o upstream

**Traduzir páginas novas não basta: toda página já traduzida precisa ser
atualizada sempre que o inglês dela mudar no upstream.** Uma página com
`ia-translate: true` cujo conteúdo esteja defasado em relação ao inglês atual
é um bug.

Em toda sincronização com o upstream:

1. `git fetch upstream main` e crie uma branch.
2. Rode `python3 tool/traducao/sincronizar_upstream.py`. Ele:
   - faz o merge adotando a árvore do upstream (a estrutura nova do upstream
     sempre vence);
   - leva cada arquivo traduzido para o caminho novo (mesmo caminho, redirect
     1:1 do `firebase.json` ou renomeação);
   - copia a tradução quando o inglês não mudou;
   - nos JSONs de diagnósticos e lints, mescla por entrada: mantém a tradução
     do que não mudou e deixa em inglês o que mudou;
   - faz merge de 3 vias quando mudou. Sem conflito, grava o resultado. Com
     conflito, grava em `.traducao-pendente/<caminho>` com marcadores diff3
     e deixa o inglês novo no repositório;
   - grava `.traducao-pendente/RELATORIO.md` e atualiza
     `tool/traducao/ultimo-sync-upstream.txt`.
3. Faça o commit do merge **incluindo** `.traducao-pendente/`, para nada se
   perder entre sessões.
4. Resolva **todos** os arquivos de `.traducao-pendente/`, que são as páginas
   já traduzidas cujo texto mudou:
   - em cada bloco `<<<<<<< pt` / `||||||| base_en` / `=======` / `>>>>>>> new_en`,
     escreva o português do `new_en`, reaproveitando a tradução do lado `pt`
     e mudando só o que o inglês mudou;
   - grave o resultado no caminho real em `src/content/` (ou
     `src/_includes/`), com `ia-translate: true`;
   - apague o arquivo resolvido de `.traducao-pendente/` e marque-o no
     `RELATORIO.md`.
5. Revise também os "removidos ou consolidados" do relatório: se a página que
   os substituiu ainda não está traduzida, traduza-a usando a tradução antiga
   como referência.
6. Traduza os diagnósticos e lints que o sync deixou em inglês
   (`python3 tool/i18n/diagnostics_i18n.py status`).
7. Rode `python3 tool/traducao/ancorar_titulos.py` nas páginas resolvidas e
   `python3 tool/traducao/verificar.py` (sem argumentos ele confere todas as
   páginas traduzidas) e corrija o que aparecer.
8. Quando `.traducao-pendente/` estiver vazio, apague a pasta, rode
   `python3 tool/traducao/gerar_todo.py` e faça o commit.
9. Só depois disso siga para as páginas novas que ainda não foram traduzidas
   (`TODO-TRADUCAO.md`).

Nunca resolva um conflito trocando a página pela versão em inglês e mantendo
`ia-translate: true`, nem descartando o texto novo do upstream.

## Scripts de `tool/traducao/`

| Script | Para quê |
|---|---|
| `sincronizar_upstream.py` | Merge com o upstream preservando traduções (acima). |
| `verificar.py [--estrito] [arquivos]` | **Checagens determinísticas** (ver abaixo). Sem argumentos confere todas as páginas marcadas. |
| `ancorar_titulos.py <arquivos>` | Acrescenta `{:#id}` em inglês aos títulos traduzidos (mesma regra do `slugify()` de `site/lib/src/util.dart`; junta atributos como `{:.no_toc #id}`). Rode em toda página traduzida. |
| `gerar_todo.py` | Regenera `TODO-TRADUCAO.md` (status por seção a partir de `ia-translate`, mais a contagem de diagnósticos e lints em inglês). |
| `setup.sh` | Prepara o ambiente (Dart, remote `upstream`, dependências). |

`ultimo-sync-upstream.txt` guarda o commit do upstream já incorporado.

## Checagens determinísticas

Rode localmente antes do commit:

```console
python3 tool/traducao/verificar.py
python3 tool/i18n/diagnostics_i18n.py status
dart run dash_site refresh-excerpts --fail-on-update --dry-run
```

O `verificar.py` acusa como **erro**:

- `conflito`: marcadores de merge (`<<<<<<<`, `|||||||`, `>>>>>>>`) esquecidos;
- `frontmatter`: YAML inválido, `ia-translate` que não é `true` de primeiro
  nível, ou campo com valor no inglês que ficou vazio;
- `frontmatter-en`: `title`, `shortTitle` ou `description` idêntico ao inglês
  e escrito em inglês;
- `flag`: `ia-translate` fora do frontmatter (ou o comentário fora da 1ª linha
  de um parcial);
- `placeholder`: avisos de tradução pendente no texto ("Note for
  translators", "To be translated"...);
- `ingles`: página marcada como traduzida com 70% ou mais da prosa em inglês;
- `estrutura`: cercas de código, code-excerpts, tags Liquid, admonitions ou
  âncoras diferentes do inglês, e rótulo de link sem definição;
- `defasada`: o inglês da página mudou no upstream depois do último sync
  (`ultimo-sync-upstream.txt`). É a regra principal acima virando checagem;
- `pendente`: `.traducao-pendente/` com arquivos não resolvidos;
- `ancora`: título traduzido cujo id difere do id do título em inglês (links
  `#ancora` quebrariam); corrija com
  `python3 tool/traducao/ancorar_titulos.py <arquivos>`;
- `link-interno`: link para âncora da própria página que não existe;
- `dominio`: domínios que não existem, como `api.dartbrasil.dev`. A
  documentação de API não é traduzida: use `api.dart.dev`;
- `workflow`: job de `build.yml` ou `test.yml` preso por `if:` a outro
  repositório (o build e os links precisam rodar aqui).

E como **aviso** (não falha, a menos que use `--estrito`): `parcial` (30% a
70% da prosa em inglês) e `defs-link` (número de definições de link diferente
do inglês).

Quando uma checagem nova pegar um caso que escapou, acrescente-a ao
`verificar.py` em vez de corrigir só o arquivo.

## Personalizações do Dart Brasil fora do conteúdo

Ao sincronizar, confira se continuam funcionando:

- domínio e textos em `src/data/site.yaml`;
- header, footer e demais componentes em `site/lib/`;
- deploy: `.github/workflows/build.yml` (preview por PR e produção no
  Firebase, projeto `transliteradu`), `firebase.json` e `.firebaserc`;
- os exemplos em `examples/` podem ter strings traduzidas: os code-excerpts
  das páginas devem continuar batendo com eles.

## Git

- Trabalhe em branch e abra PR para a `main`.
- Commits de tradução: `translate: <caminho>`; sincronização:
  `Merge upstream dart-lang/site-www main`.

## Modelo da tradução: sempre Haiku

Toda tradução e retradução de página (tradução nova, sync com o upstream, revisão de trecho) roda no **Haiku** (`model: haiku`, hoje Claude Haiku 5.5), local ou na nuvem (Claude Code na web, GitHub App, rotinas agendadas).

- Os agentes de tradução em `.claude/agents/` (`agent-translator`, `atualizar-traducao`) declaram `model: haiku`. Não troque.
- Se um orquestrador disparar subagentes para traduzir, passe `model: "haiku"` na ferramenta Agent.
- O modelo principal da sessão fica só com a orquestração: merge do upstream, scripts de conferência, commits e PR. Ele não traduz páginas.
- Exceção: o **review** (agente `revisar-traducao`) roda em **Sonnet**. Ele só aponta problemas; quem corrige é o Haiku.
