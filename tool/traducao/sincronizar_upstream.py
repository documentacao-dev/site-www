#!/usr/bin/env python3
"""Sincroniza este repositório com o upstream (dart-lang/site-www) preservando
as traduções e marcando o que precisa ser retraduzido.

Uso (a partir da raiz do repositório, com a árvore limpa):

    git fetch upstream main
    python3 tool/traducao/sincronizar_upstream.py [--alvo upstream/main]

O que o script faz:

1. Lê o último commit do upstream já sincronizado em
   tool/traducao/ultimo-sync-upstream.txt (a "base").
2. Inicia um merge com o alvo cuja árvore é exatamente a do upstream
   (`git merge -s ours` + `git read-tree`), para que a estrutura nova do
   upstream seja sempre respeitada.
3. Para cada arquivo que o Dart Brasil alterou em relação à base
   (páginas traduzidas, parciais, dados, componentes, exemplos):
   - descobre o caminho novo (mesmo caminho, redirect 1:1 do firebase.json
     ou renomeação detectada pelo git);
   - se o original em inglês não mudou, copia a versão do Dart Brasil;
   - nos JSONs traduzidos de src/data/ (diagnostics.json e
     linter_rules.json), mescla entrada por entrada: mantém a tradução das
     entradas cujo inglês não mudou e adota o inglês novo nas outras (que
     aparecem em `python3 tool/i18n/diagnostics_i18n.py status`);
   - se mudou, faz merge de 3 vias (versão BR, inglês base, inglês novo).
     Sem conflito, grava o resultado. Com conflito, grava o arquivo com
     marcadores diff3 em .traducao-pendente/<caminho novo> e deixa o
     inglês novo no lugar, SEM a flag ia-translate (a página volta a
     aparecer como pendente no relatório).
4. Grava o relatório em .traducao-pendente/RELATORIO.md e atualiza
   ultimo-sync-upstream.txt para o alvo.

Depois: resolva cada arquivo de .traducao-pendente/ (veja CLAUDE.md),
rode tool/traducao/verificar.py, apague .traducao-pendente/ e faça o commit.
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SYNC = ROOT / 'tool' / 'traducao' / 'ultimo-sync-upstream.txt'
PEND = ROOT / '.traducao-pendente'
CONTENT = 'src/content/'
# Arquivos exclusivos do Dart Brasil ou que não devem ser mesclados.
IGNORAR = ('tool/traducao/', '.traducao-pendente/', 'CLAUDE.md', 'plan/',
           '.claude/')
# Arquivos do upstream que o Dart Brasil NÃO quer: voltam a cada sync com a
# árvore do upstream e são removidos de novo. Vazio por enquanto (os workflows
# presos a `github.repository == 'dart-lang/site-www'` só geram execuções
# puladas aqui). Para remover um, acrescente o caminho.
REMOVIDOS_NO_FORK = ()
# JSONs gerados pelo upstream e traduzidos aqui (tool/i18n/diagnostics_i18n.py):
# caminho -> chave que identifica cada entrada. O merge é por entrada, não por
# linha, para que uma mudança no upstream nunca vire conflito no arquivo todo.
JSON_I18N = {
    'src/data/diagnostics.json': 'id',
    'src/data/linter_rules.json': 'name',
}


def git(*args, check=True, entrada=None):
    r = subprocess.run(['git', '-C', str(ROOT), *args], capture_output=True,
                       text=True, input=entrada)
    if check and r.returncode != 0:
        sys.exit(f'git {" ".join(args)} falhou:\n{r.stderr}')
    return r.stdout


def show(ref, caminho):
    r = subprocess.run(['git', '-C', str(ROOT), 'show', f'{ref}:{caminho}'],
                       capture_output=True)
    return r.stdout if r.returncode == 0 else None


def redirects(alvo):
    """Mapa url -> url dos redirects 1:1 do firebase.json do upstream."""
    bruto = show(alvo, 'firebase.json')
    if not bruto:
        return {}, []
    exatos, globs = {}, []
    for r in json.loads(bruto).get('hosting', {}).get('redirects', []):
        if 'source' not in r or not r['destination'].startswith('/'):
            continue
        s, d = r['source'], r['destination']
        # `/caminho{,/**}` redireciona a página e tudo abaixo dela.
        if s.endswith('{,/**}'):
            s = s[:-len('{,/**}')]
        s = s.rstrip('/')
        if ':rest*' in s:
            globs.append((s.split('/:rest*')[0], d.split('/:rest*')[0]))
        elif '*' in s or '{' in s:
            continue  # curinga: não é renomeação 1:1
        else:
            exatos[s] = d
    return exatos, globs


def mesclar_json_i18n(br, en_base, en_novo, chave):
    """Merge por entrada dos JSONs traduzidos. Retorna (bytes, n_em_ingles):
    n_em_ingles conta as entradas novas ou alteradas no upstream, que ficam
    em inglês até serem traduzidas."""
    br_l, base_l, novo_l = (json.loads(x) for x in (br, en_base, en_novo))
    br_m = {e.get(chave): e for e in br_l}
    base_m = {e.get(chave): e for e in base_l}
    saida, em_ingles = [], 0
    for e in novo_l:
        k = e.get(chave)
        if k in br_m and base_m.get(k) == e:
            saida.append(br_m[k])
        else:
            saida.append(e)
            em_ingles += 1
    texto = json.dumps(saida, indent=2, ensure_ascii=False)
    if en_novo.endswith(b'\n'):
        texto += '\n'
    return texto.encode('utf-8'), em_ingles


def url_de(caminho):
    if not caminho.startswith(CONTENT) or not caminho.endswith('.md'):
        return None
    u = '/' + caminho[len(CONTENT):-3]
    return u[:-6] if u.endswith('/index') else u


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--alvo', default='upstream/main')
    a = ap.parse_args()

    if git('status', '--porcelain').strip():
        sys.exit('A árvore de trabalho precisa estar limpa.')
    base = SYNC.read_text().strip()
    alvo = git('rev-parse', a.alvo).strip()
    if base == alvo:
        sys.exit('Já sincronizado com ' + alvo)
    head = git('rev-parse', 'HEAD').strip()

    arquivos_alvo = set(git('ls-tree', '-r', '--name-only', alvo).split())
    exatos, globs = redirects(alvo)
    destinos = {}
    for d in list(exatos.values()):
        destinos[d] = destinos.get(d, 0) + 1

    def arquivo_de_url(u):
        u = u.split('#')[0].rstrip('/')
        for c in (f'{CONTENT}{u.lstrip("/")}.md', f'{CONTENT}{u.lstrip("/")}/index.md'):
            if c in arquivos_alvo:
                return c

    def por_redirect(u, prof=0):
        if prof > 5:
            return None
        d = exatos.get(u)
        if d is None:
            for s, dd in globs:
                if u == s or u.startswith(s + '/'):
                    d = dd + u[len(s):]
                    break
        if d is None or destinos.get(d, 1) > 1:  # consolidação, não mudança
            return None
        return arquivo_de_url(d) or por_redirect(d.split('#')[0].rstrip('/'), prof + 1)

    renomes = {}
    for linha in git('-c', 'diff.renameLimit=50000', 'diff', '-M70%',
                     '--name-status', base, alvo).splitlines():
        partes = linha.split('\t')
        if partes[0].startswith('R'):
            renomes[partes[1]] = partes[2]

    def caminho_novo(p):
        if p in arquivos_alvo:
            return p
        u = url_de(p)
        if u:
            f = por_redirect(u)
            if f:
                return f
        if p in renomes and renomes[p] in arquivos_alvo:
            return renomes[p]
        return None

    alterados = [l.split('\t') for l in git('diff', '--name-status', '--no-renames',
                                             base, head).splitlines()]
    alterados = [(s, p) for s, p in alterados
                 if s in ('M', 'A') and not p.startswith(IGNORAR)]

    print(f'Base {base[:9]} → alvo {alvo[:9]}; {len(alterados)} arquivos do Dart Brasil.')
    exclusivos_br = [p for p in git('ls-tree', '-r', '--name-only', head).split()
                     if p.startswith(IGNORAR)]
    git('merge', '-q', '--no-commit', '--no-ff', '-s', 'ours', alvo)
    git('read-tree', '-u', '--reset', alvo)
    # Arquivos exclusivos do Dart Brasil que não passam pelo merge
    # (CLAUDE.md, .claude/, plan/, tool/traducao/): o read-tree os apaga
    # porque não existem no upstream, então restaura do HEAD.
    if exclusivos_br:
        git('checkout', head, '--', *exclusivos_br)
    for p in REMOVIDOS_NO_FORK:
        if (ROOT / p).exists():
            git('rm', '-qf', '--', p)

    copiados, mesclados, conflitos, sem_destino, exclusivos = [], [], [], [], []
    json_em_ingles = []
    mapeados = set()
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for status, p in alterados:
            br = show(head, p)
            en_base = show(base, p)
            n = caminho_novo(p)
            if n is None:
                if en_base is None:  # arquivo exclusivo do Dart Brasil
                    (ROOT / p).parent.mkdir(parents=True, exist_ok=True)
                    (ROOT / p).write_bytes(br)
                    exclusivos.append(p)
                else:
                    sem_destino.append(p)
                continue
            mapeados.add(p)
            en_novo = show(alvo, n)
            if en_base == en_novo or en_base is None:
                (ROOT / n).write_bytes(br)
                copiados.append(n)
                continue
            if n in JSON_I18N:
                conteudo, em_ingles = mesclar_json_i18n(br, en_base, en_novo,
                                                        JSON_I18N[n])
                (ROOT / n).write_bytes(conteudo)
                mesclados.append(n)
                json_em_ingles.append((n, em_ingles))
                continue
            (tmp / 'br').write_bytes(br)
            (tmp / 'base').write_bytes(en_base)
            (tmp / 'novo').write_bytes(en_novo)
            r = subprocess.run(['git', 'merge-file', '-p', '--diff3', '-L', 'pt',
                                '-L', 'base_en', '-L', 'new_en', str(tmp / 'br'),
                                str(tmp / 'base'), str(tmp / 'novo')],
                               capture_output=True)
            if r.returncode == 0:
                (ROOT / n).write_bytes(r.stdout)
                mesclados.append(n)
            else:
                destino = PEND / n
                destino.parent.mkdir(parents=True, exist_ok=True)
                destino.write_bytes(r.stdout)
                conflitos.append((n, r.stdout.count(b'\n<<<<<<< pt')))

    # Checagem final: nenhum arquivo que só existe no Dart Brasil (não está
    # no upstream) pode desaparecer sem ter sido tratado acima.
    sumidos = [p for p in git('ls-tree', '-r', '--name-only', head).split()
               if p not in arquivos_alvo and not (ROOT / p).exists()
               and p not in sem_destino and p not in mapeados]
    if sumidos:
        print('ATENÇÃO: arquivos do Dart Brasil que sumiram no merge '
              '(restaure com git checkout HEAD -- <arquivo> se forem necessários):')
        for p in sumidos[:50]:
            print('   ', p)

    SYNC.write_text(alvo + '\n')
    PEND.mkdir(exist_ok=True)
    rel = [f'# Sincronização {base[:9]} → {alvo[:9]}', '',
           f'- Copiados sem mudança no inglês: {len(copiados)}',
           f'- Mesclados automaticamente: {len(mesclados)}',
           f'- **Com conflito (retraduzir)**: {len(conflitos)}',
           f'- Removidos ou consolidados no upstream: {len(sem_destino)}',
           f'- Exclusivos do Dart Brasil (restaurados): {len(exclusivos)}', '',
           '## Com conflito', '',
           'Cada arquivo abaixo está em `.traducao-pendente/<caminho>` com marcadores',
           'diff3 (`pt` / `base_en` / `new_en`). No repositório ficou o inglês novo.', '']
    rel += [f'- [ ] `{n}` ({c} bloco(s))' for n, c in sorted(conflitos)]
    if json_em_ingles:
        rel += ['', '## Diagnósticos e lints (JSON)', '',
                'Mesclados por entrada. As entradas novas ou alteradas no upstream',
                'ficaram em inglês: liste com `python3 tool/i18n/diagnostics_i18n.py',
                'status` e traduza com `export`/`import` (veja CLAUDE.md).', '']
        rel += [f'- `{n}`: {c} entrada(s) em inglês' for n, c in json_em_ingles]
    rel += ['', '## Removidos ou consolidados no upstream', '',
            'Não existem mais com o mesmo conteúdo. Se a página nova que os',
            'substitui ainda não está traduzida, a tradução antiga pode servir de',
            'referência (`git show <commit-anterior>:<caminho>`).', '']
    rel += [f'- `{p}`' for p in sorted(sem_destino)]
    (PEND / 'RELATORIO.md').write_text('\n'.join(rel) + '\n')
    print('\n'.join(rel[:8]))
    print('\nRelatório: .traducao-pendente/RELATORIO.md')


if __name__ == '__main__':
    main()
