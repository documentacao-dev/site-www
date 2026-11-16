#!/usr/bin/env python3
"""Checagens determinísticas das traduções do Dart Brasil.

    python3 tool/traducao/verificar.py [--ref upstream/main] [--estrito] [arquivos...]

Sem arquivos, confere todas as páginas e parciais marcados com ia-translate
(e as checagens globais). Erros fazem o script sair com código 1 (o CI falha);
avisos só são listados, a menos que se passe --estrito.

Checagens:

ERROS
- conflito:     marcadores de merge (<<<<<<<, |||||||, >>>>>>>) no arquivo.
- frontmatter:  YAML inválido, `ia-translate` que não é o booleano `true` de
                primeiro nível (ex.: colado dentro de um `description: >`) ou
                campo que tem valor no inglês e ficou vazio na tradução.
- frontmatter-en: `title`, `shortTitle` ou `description` idêntico ao inglês e
                em inglês (3+ palavras com palavra-função inglesa); nomes de
                produto como "Dart DevTools" não disparam.
- flag:         `ia-translate` fora do frontmatter, ou o comentário
                `<!-- ia-translate: true -->` fora da primeira linha de um parcial.
- placeholder:  avisos de "tradução pendente" deixados no texto
                (ex.: "Note for translators", "To be translated").
- ingles:       página marcada como traduzida cuja prosa está em inglês
                (proporção de palavras-função em inglês >= 0.7).
- estrutura:    número de cercas de código, code-excerpts, tags Liquid,
                admonitions ou âncoras {:#} diferente do original em inglês;
                rótulo de link `[texto][rótulo]` sem definição.
- defasada:     o inglês da página mudou no upstream desde o último sync
                (tool/traducao/ultimo-sync-upstream.txt): rode
                sincronizar_upstream.py.
- pendente:     .traducao-pendente/ ainda tem arquivos para resolver.
- ancora:       título traduzido cujo id automático difere do slug em inglês e
                que não tem `{:#id}` explícito (links #ancora quebrariam).
                Corrija com tool/traducao/ancorar_titulos.py <arquivo>.
- link-interno: link para âncora da própria página (`](#id)` ou `[x]: #id`)
                que não existe (títulos, `id="..."` e parciais incluídos).
- dominio:      uso de domínios que não existem (ex.: api.dartbrasil.dev; a
                documentação de API não é traduzida e fica em api.dart.dev).
                Conferido em todo o site, não só nas páginas marcadas.
- analytics:    rastreamento herdado do upstream no código do site (site/,
                sites/, packages/, web/): Google Tag Manager, Google
                Analytics, gtag, banner de cookies do Google ou verificação
                do Search Console de dart.dev/flutter.dev. Foi removido do
                fork e não pode voltar num sync.
- workflow:     os jobs de build/links (.github/workflows/build.yml) e de
                checagem (.github/workflows/test.yml) precisam rodar neste
                repo. Se um sync trouxer um `if: github.repository ==
                'dart-lang/site-www'` nesses jobs, link quebrado só aparece
                no deploy da main, depois do merge.

AVISOS
- parcial:      proporção de inglês entre 0.3 e 0.7 (tradução incompleta).
- defs-link:    número de definições de link diferente do original
                (ex.: rótulos antigos sem crase convivendo com os novos).

O que não fica aqui: a sincronia dos code-excerpts com examples/, conferida
por `dart run dash_site refresh-excerpts --fail-on-update --dry-run` (job
`excerpts` de .github/workflows/test.yml), e os diagnósticos/lints em JSON
(src/data/), conferidos por `python3 tool/i18n/diagnostics_i18n.py status`.
"""
import argparse
import importlib.util
import re

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT = 'src/content/'
SYNC = ROOT / 'tool' / 'traducao' / 'ultimo-sync-upstream.txt'
PEND = ROOT / '.traducao-pendente'

FLAG_FM = re.compile(r'^ia-translate:\s*true\s*$', re.M)
FLAG_COMENTARIO = '<!-- ia-translate: true -->'
CONFLITO = re.compile(r'^(<{7} |\|{7} |>{7} )', re.M)
PLACEHOLDER = re.compile(
    r'note for translators|to be translated|requires a dedicated session'
    r'|marked for translation|tradu[çc][ãa]o pendente|todo:? traduzir',
    re.I)
ESTRUTURA = {
    'cercas ```': re.compile(r'^\s*```', re.M),
    'code-excerpt': re.compile(r'<\?code-excerpt'),
    'tags {% %}': re.compile(r'\{%'),
    'admonitions :::': re.compile(r'^\s*:::', re.M),
    'âncoras {:#}': re.compile(r'\{:\s*#'),
}
DEFS_LINK = re.compile(r'^\s*\[[^\]]+\]:\s', re.M)
# Domínios que NÃO existem. Os links de API devem apontar para os oficiais
# (api.dart.dev, api.flutter.dev, main-api.flutter.dev).
DOMINIOS_INEXISTENTES = re.compile(
    r'(?<![\w.-])(?:main-)?api\.flutterbrasil\.dev|(?<![\w.-])api\.dartbrasil\.dev')
PASTAS_DOMINIO = ['src', 'site/lib', 'tool/config', '.github', 'README.md']

# Analytics e consentimento herdados do upstream (dart.dev/flutter.dev): os
# visitantes do fork virariam dados nas contas do Google do projeto original.
ANALYTICS_UPSTREAM = ('googletagmanager', 'GTM-', 'google-analytics.com',
                      'gtag(', 'UA-26406144', 'cookienotificationbar',
                      'google-site-verification')
PASTAS_ANALYTICS = ('site', 'sites', 'packages', 'web')


def analytics_no_codigo():
    """Linhas `arquivo:linha:texto` do código do site com analytics do upstream."""
    pastas = [d for d in PASTAS_ANALYTICS if (ROOT / d).is_dir()]
    if not pastas:
        return []
    args = ['grep', '-nIF']
    for termo in ANALYTICS_UPSTREAM:
        args += ['-e', termo]
    return (git(*args, '--', *pastas) or '').splitlines()


# Palavras-função para estimar o idioma da prosa.
EN = set('the and of to is are you your this that with for in it be can when '
         'which by an or as from have will not these use using'.split())
PT = set('os de do da dos das que é são um uma para com no na nos nas em por '
         'você seu sua ao como mais pode isso este esta'.split())
LIMITE_ERRO, LIMITE_AVISO, MINIMO_PALAVRAS = 0.7, 0.3, 20


def git(*args):
    r = subprocess.run(['git', '-C', str(ROOT), *args], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def frontmatter(texto):
    m = re.match(r'^---\n(.*?)\n---\n', texto, re.S)
    return (m.group(1), texto[m.end():]) if m else (None, texto)


def sem_codigo(texto):
    return re.sub(r'```.*?```', '', texto, flags=re.S)


def proporcao_ingles(texto):
    _, corpo = frontmatter(texto)
    # Tags HTML/componentes (inclusive multilinha), comentários e Liquid não
    # são prosa: o texto entre tags continua sendo contado.
    corpo = re.sub(r'<!--.*?-->|\{%.*?%\}|<[^<>]*>', ' ', sem_codigo(corpo), flags=re.S)
    linhas = []
    for linha in corpo.split('\n'):
        s = linha.strip()
        if (not s or s.startswith(('<', '{%', '[', '|'))
                or re.match(r'^[*-] .*(by @|\]\(https://github\.com)', s)
                or re.match(r'^\[\d+\]\(', s)):
            continue
        linhas.append(re.sub(r'`[^`]*`|\[[^\]]*\]\[[^\]]*\]|\([^)]*\)|\{[^}]*\}', '', s))
    palavras = re.findall(r"[a-záéíóúãõçê']+", ' '.join(linhas).lower())
    e = sum(p in EN for p in palavras)
    p = sum(p in PT for p in palavras)
    return (e / (e + p), e + p) if e + p else (0.0, 0)


def rotulos_sem_definicao(texto):
    t = sem_codigo(texto)
    defs = {m.lower() for m in re.findall(r'^\s*\[([^\]]+)\]:\s', t, re.M)}
    usados = {(lab or txt).lower()
              for txt, lab in re.findall(r'\[([^\]]+)\]\[([^\]]*)\]', t)}
    # Ignora o que está dentro de código inline (ex.: `map['key'][0]`).
    inline = ' '.join(re.findall(r'`[^`]*`', t)).lower()
    return {r for r in usados - defs if f'[{r}]' not in inline}


def checar_frontmatter(fm, en_fm):
    try:
        dados = yaml.safe_load(fm) or {}
    except yaml.YAMLError as e:
        return [('frontmatter', f'YAML inválido: {str(e).splitlines()[0]}')]
    erros = []
    if dados.get('ia-translate') is not True:
        erros.append(('frontmatter', f'ia-translate não é `true` de primeiro nível '
                                     f'(valor: {str(dados.get("ia-translate"))[:40]!r})'))
    try:
        en = yaml.safe_load(en_fm or '') or {}
    except yaml.YAMLError:
        en = {}
    for chave, valor in en.items():
        if isinstance(valor, str) and valor.strip() and \
                not str(dados.get(chave) or '').strip():
            erros.append(('frontmatter', f'campo `{chave}` vazio (o inglês tem valor)'))
    for chave in ('title', 'shortTitle', 'description'):
        valor = en.get(chave)
        if isinstance(valor, str) and dados.get(chave) == valor:
            palavras = re.findall(r"[a-z']+", valor.lower())
            if len(palavras) >= 3 and any(p in EN for p in palavras):
                erros.append(('frontmatter-en', f'`{chave}` igual ao inglês: {valor[:60]!r}'))
    return erros


def marcados():
    saida = git('grep', '-lE', r'^(ia-translate: true|<!-- ia-translate: true -->)',
                '--', 'src/content', 'src/_includes') or ''
    return saida.split()


def carregar_ancorador():
    global ANC_MOD
    caminho = ROOT / 'tool' / 'traducao' / 'ancorar_titulos.py'
    spec = importlib.util.spec_from_file_location('anc', caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ANC_MOD = mod
    return mod.ancorar


ANCORAR = None
ANC_MOD = None
INCLUDES = ROOT / 'src' / '_includes'
RENDER = re.compile(r'\{%-?\s*(?:render|include)\s+["\']([^"\']+)["\']')


def ids_da_pagina(texto, profundidade=0):
    ids = set(re.findall(r'\bid=["\']([^"\']+)["\']', texto))
    for _, _, txt in ANC_MOD.titulos(texto):
        sem, tokens = ANC_MOD.separar_atributos(txt)
        explicitos = [t[1:] for t in tokens if t.startswith('#')]
        # O id explícito substitui o automático (slug do texto).
        ids.update(explicitos or [ANC_MOD.slug(sem)])
        # O site deduplica ids repetidos com sufixos -1, -2...
    base = set(ids)
    for i in base:
        ids.update(f'{i}-{n}' for n in range(1, 6))
    if profundidade < 3:
        for inc in RENDER.findall(texto):
            arq = INCLUDES / inc
            if arq.exists():
                ids |= ids_da_pagina(arq.read_text(encoding='utf-8'), profundidade + 1)
    return ids


def id_do_titulo(txt):
    sem, tokens = ANC_MOD.separar_atributos(txt)
    explicitos = [t[1:] for t in tokens if t.startswith('#')]
    return explicitos[-1] if explicitos else ANC_MOD.slug(sem)


def ids_divergentes(en, pt):
    """Quantos títulos da tradução geram id diferente do título correspondente
    em inglês (links #ancora quebrariam). Um `{:#id}` redundante não conta.
    Se os títulos não correspondem em quantidade e nível, não compara (a
    diferença de estrutura aparece nas outras checagens)."""
    te, tp = ANC_MOD.titulos(en), ANC_MOD.titulos(pt)
    if [n for _, n, _ in te] != [n for _, n, _ in tp]:
        return 0
    return sum(id_do_titulo(a) != id_do_titulo(b)
               for (_, _, a), (_, _, b) in zip(te, tp))


def links_internos_quebrados(texto):
    t = sem_codigo(texto)
    alvos = re.findall(r'\]\(#([^)\s]+)\)', t)
    alvos += re.findall(r'^\s*\[[^\]]+\]:\s*#(\S+)', t, re.M)
    alvos += re.findall(r'href=["\']#([^"\']+)["\']', t)
    ids = ids_da_pagina(texto)
    return sorted({a for a in alvos if a not in ids and '{{' not in a})


def checar_arquivo(caminho, ref, sync):
    erros, avisos = [], []
    texto = (ROOT / caminho).read_text(encoding='utf-8')
    fm, corpo = frontmatter(texto)
    eh_parcial = '/_includes/' in caminho or Path(caminho).name.startswith('_')

    if CONFLITO.search(texto):
        erros.append(('conflito', 'marcadores de merge no arquivo'))

    if fm is not None and yaml is not None:
        erros += checar_frontmatter(fm, en_fm=frontmatter(git('show', f'{ref}:{caminho}') or '')[0])

    if fm is not None and FLAG_FM.search(fm) is None and 'ia-translate' in corpo:
        erros.append(('flag', '`ia-translate` fora do frontmatter'))
    if fm is None and FLAG_COMENTARIO in texto and \
            not texto.lstrip().startswith(FLAG_COMENTARIO):
        erros.append(('flag', 'comentário ia-translate fora da primeira linha'))

    for linha in texto.split('\n'):
        if PLACEHOLDER.search(linha):
            erros.append(('placeholder', linha.strip()[:90]))
            break

    en = git('show', f'{ref}:{caminho}')
    if en is None:
        erros.append(('estrutura', f'sem original em {ref}'))
        return erros, avisos

    if not eh_parcial:
        prop, n = proporcao_ingles(texto)
        if n >= MINIMO_PALAVRAS and prop >= LIMITE_ERRO:
            erros.append(('ingles', f'marcada como traduzida, mas {prop:.0%} da prosa está em inglês'))
        elif n >= MINIMO_PALAVRAS and prop >= LIMITE_AVISO:
            avisos.append(('parcial', f'{prop:.0%} da prosa ainda em inglês'))

    if ANC_MOD is not None:
        quebrados = set(links_internos_quebrados(texto)) - set(links_internos_quebrados(en))
        if quebrados:
            erros.append(('link-interno', 'âncoras inexistentes: ' + ', '.join(sorted(quebrados))))

    if ANC_MOD is not None:
        n_ancoras = ids_divergentes(en, texto)
        if n_ancoras:
            erros.append(('ancora', f'{n_ancoras} título(s) sem `{{:#id}}` em inglês; '
                                    'rode tool/traducao/ancorar_titulos.py'))

    for nome, rx in ESTRUTURA.items():
        ne, np_ = len(rx.findall(en)), len(rx.findall(texto))
        # Âncoras a mais são permitidas (mantêm o id em inglês de títulos traduzidos).
        if ne != np_ and not (nome == 'âncoras {:#}' and np_ > ne):
            erros.append(('estrutura', f'{nome}: en={ne} pt={np_}'))
    faltando = rotulos_sem_definicao(texto) - rotulos_sem_definicao(en)
    if faltando:
        erros.append(('estrutura', 'rótulos sem definição: ' + ', '.join(sorted(faltando))))
    ne, np_ = len(DEFS_LINK.findall(en)), len(DEFS_LINK.findall(texto))
    if ne != np_:
        avisos.append(('defs-link', f'en={ne} pt={np_}'))

    if sync and sync != ref:
        en_sync = git('show', f'{sync}:{caminho}')
        if en_sync is not None and en_sync != en:
            erros.append(('defasada', f'o inglês mudou entre {sync[:9]} e {ref[:9]}; '
                                      'rode sincronizar_upstream.py'))
    return erros, avisos


REPO_FORK = 'documentacao-dev/site-www'
# Workflows cujos jobs precisam rodar neste repo (build, links, excerpts,
# firebase.json). Hoje nenhum tem `if:` de repositório; a checagem pega o caso
# de um sync trazer essa condição.
WORKFLOWS_OBRIGATORIOS = ('build.yml', 'test.yml')


def jobs_desligados_no_fork():
    """[(workflow, job)] cujo `if:` prende o job a outro repositório."""
    faltando = []
    for nome in WORKFLOWS_OBRIGATORIOS:
        wf = ROOT / '.github' / 'workflows' / nome
        if not wf.exists():
            faltando.append((nome, '(arquivo ausente)'))
            continue
        texto = wf.read_text()
        corpo = texto.split('\njobs:\n', 1)[-1]
        for m in re.finditer(r'^  ([\w-]+):\n(.*?)(?=^  \S|\Z)', corpo, re.M | re.S):
            cond = re.search(r'^    if:(.*)$', m.group(2), re.M)
            if cond and 'github.repository' in cond.group(1) and \
                    REPO_FORK not in cond.group(1):
                faltando.append((nome, m.group(1)))
    return faltando


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ref', default='upstream/main')
    ap.add_argument('--estrito', action='store_true', help='avisos também falham')
    ap.add_argument('arquivos', nargs='*')
    a = ap.parse_args()

    ref = git('rev-parse', a.ref)
    if ref is None:
        sys.exit(f'Ref {a.ref} não encontrada. Rode: git fetch upstream main')
    ref = ref.strip()
    sync = SYNC.read_text().strip() if SYNC.exists() else None
    if sync and git('cat-file', '-e', sync) is None:
        sync = None  # histórico raso: pula a checagem de defasagem
    global ANCORAR
    ANCORAR = carregar_ancorador()

    arquivos = a.arquivos or marcados()
    total_erros = total_avisos = 0
    for arq in arquivos:
        p = Path(arq)
        caminho = p.resolve().relative_to(ROOT).as_posix() if p.exists() else arq
        erros, avisos = checar_arquivo(caminho, ref, sync)
        if erros or avisos:
            print(f'{"✗" if erros else "!"} {caminho}')
            for tipo, msg in erros:
                print(f'    erro  [{tipo}] {msg}')
            for tipo, msg in avisos:
                print(f'    aviso [{tipo}] {msg}')
        total_erros += bool(erros)
        total_avisos += bool(avisos) and not erros

    if not a.arquivos and PEND.exists() and any(
            f.name != 'RELATORIO.md' for f in PEND.rglob('*') if f.is_file()):
        print('✗ .traducao-pendente/\n    erro  [pendente] ainda há conflitos para resolver')
        total_erros += 1

    if not a.arquivos:
        saida = git('grep', '-nE', r'api\.flutterbrasil\.dev|api\.dartbrasil\.dev',
                    '--', *PASTAS_DOMINIO) or ''
        achados = [l for l in saida.splitlines()
                   if DOMINIOS_INEXISTENTES.search(l.split(':', 2)[-1])]
        if achados:
            print('✗ domínios inexistentes')
            for l in achados[:20]:
                print(f'    erro  [dominio] {l[:140]}')
            total_erros += 1

    if not a.arquivos:
        achados = analytics_no_codigo()
        if achados:
            print('✗ analytics do upstream no código do site')
            for l in achados[:20]:
                print(f'    erro  [analytics] {l[:140]}')
            print('    É rastreamento do site original (dart.dev/flutter.dev) que '
                  'voltou com o sync: remova no PR de sync (veja CLAUDE.md).')
            total_erros += 1

    if not a.arquivos:
        faltando = jobs_desligados_no_fork()
        if faltando:
            print('✗ .github/workflows/')
            for wf, job in faltando:
                print(f'    erro  [workflow] {wf}: job `{job}` não roda em {REPO_FORK} '
                      f'(o `if:` precisa incluir o repo)')
            total_erros += 1

    print(f'{len(arquivos)} arquivo(s) conferido(s): {total_erros} com erro, '
          f'{total_avisos} só com aviso.')
    sys.exit(1 if total_erros or (a.estrito and total_avisos) else 0)


if __name__ == '__main__':
    main()
