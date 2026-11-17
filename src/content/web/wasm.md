---
ia-translate: true
title: Compilação WebAssembly (Wasm)
shortTitle: Compilação Wasm
description: >-
  Compile aplicações web Dart para WebAssembly (WasmGC) para reduzir os tempos
  de carregamento, eliminar pausas de JIT na thread principal e melhorar a
  responsividade da renderização.
---

Você pode compilar aplicações web do Dart e do [Flutter][] para
[WebAssembly][wasm-org] (`dart2wasm`) como uma alternativa de alta performance
ao JavaScript (`dart2js`) em builds de produção. Compilar para WebAssembly
reduz os tempos de carregamento inicial da página, elimina pausas de compilação
JavaScript just-in-time (JIT) na thread principal e entrega renderização de
frames consistente em navegadores modernos.

## Compile sua aplicação web para Wasm {:#compiling-to-wasm}

Use o comando [`dart compile wasm`][dart-compile-wasm] para compilar uma
aplicação web Dart em um módulo WebAssembly. Para a lista completa de flags do
compilador, consulte [Níveis de otimização e flags do compilador](#optimization-levels-and-flags)
ou execute `dart compile wasm --help`.

:::note
Se você está criando uma aplicação web com Flutter, execute `flutter build web --wasm`
em vez de chamar `dart compile wasm` diretamente. Consulte a
[documentação do Flutter Wasm][Flutter] para as instruções de build específicas do Flutter.
:::

Para compilar e executar uma aplicação web Dart com Wasm, siga estes passos:

1. Crie uma aplicação web e entre no diretório dela:

   ```console
   $ dart create -t web mywebapp
   $ cd mywebapp
   ```

   O template cria uma pequena aplicação web que usa o [`package:web`][],
   necessário para executar Wasm. Aplicações web existentes devem ser [migradas][migrated]
   de `dart:html` para `package:web`.

1. Compile a aplicação para Wasm em um diretório de saída `site`:

   ```console
   $ dart compile wasm -O2 web/main.dart -o site/main.wasm
   ```

   Isso gera `site/main.wasm`, o runtime JavaScript complementar `site/main.mjs`
   e `site/main.wasm.map`.

   :::note
   Por padrão, o `dart compile wasm` gera um arquivo de source map `.wasm.map`
   junto com a saída `.wasm`. Para desabilitar a geração de source maps em builds
   de produção, passe `--no-source-maps`. Para conhecer as considerações de
   segurança ao publicar source maps, consulte [Deploy na web][manage-source-maps].
   :::

1. Copie os arquivos web estáticos:

   ```console
   $ cp web/index.html web/styles.css site/
   ```

1. Como o `index.html` carrega o `main.dart.js`, crie o `site/main.dart.js` para
   buscar o `site/main.wasm` e importar o runtime `site/main.mjs` gerado, em paralelo:

   ```js title="site/main.dart.js"
   (async function () {
     const wasmPromise = fetch('main.wasm');
     const { compileStreaming } = await import('./main.mjs');
     const app = await compileStreaming(wasmPromise);
     const instantiatedApp = await app.instantiate({});
     instantiatedApp.invokeMain();
   })();
   ```

1. Sirva o diretório `site` usando um servidor HTTP local, como o [`dhttpd`][]:

   ```console
   $ dart run dhttpd@ --path site
   ```

Você também pode explorar este pequeno [exemplo de sandbox][sandbox].

## Suporte e requisitos de WebAssembly {:#webassembly-support}

Ao compilar Dart para WebAssembly, tenha em mente os requisitos de navegador,
de interoperabilidade e de plataforma a seguir:

* **Padrões de WebAssembly e compatibilidade com navegadores**:
  O compilador `dart2wasm` tem como alvo três propostas padronizadas de WebAssembly:
  WebAssembly Garbage Collection (WasmGC), JS String Builtins (`wasm:js-string`)
  e Phase 4 Exception Handling (as instruções `try_table` e `exnref`).
  Para executar os módulos compilados em um navegador, é necessária pelo menos
  uma das seguintes versões mínimas:
  * Chrome ou Edge 137+
  * Safari 26.2+ (macOS e iOS)
  * Firefox 134+ (ou 147+ para Flutter web)

  Para mais detalhes de compatibilidade entre navegadores, consulte a
  [documentação do Flutter Wasm][Flutter].

* **Ambientes de destino e modo standalone**:
  Por padrão, a saída Wasm compilada tem como alvo ambientes JavaScript (como
  navegadores) e gera um arquivo de runtime complementar `<name>.mjs`. Para
  compilar um módulo WebAssembly standalone para runtimes que não são web, como
  o Wasmtime 39+ (com a flag `-W gc,exceptions,function-references=y`), passe a
  flag `--standalone` para o `dart compile wasm`. O modo standalone não permite
  a biblioteca [`dart:js_interop`][] nem a flag `--enable-deferred-loading`.

* **Interoperabilidade com JavaScript**:
  A compilação para Wasm oferece suporte apenas ao
  [mecanismo de interoperabilidade JS de próxima geração do Dart][js-interop]
  ([`dart:js_interop`][] e [`package:web`][]).

* **Ferramentas de build**:
  A ferramenta `webdev` não oferece suporte à compilação Wasm (`webdev serve`
  ou `webdev build`). Em vez disso, siga os passos em
  [Compile sua aplicação web para Wasm](#compiling-to-wasm).

### Pacotes suportados {:#supported-packages}

Para encontrar pacotes compatíveis com Wasm, use o filtro
[`wasm-ready`][] no [pub.dev][].

Um pacote é *wasm-ready* quando não importa bibliotecas legadas de web ou de
interop, como `dart:html`, `dart:js` ou `package:js`. Consulte a
[página de interoperabilidade JS antiga][past-js-interop] para a lista completa
de bibliotecas não permitidas.

### Imports condicionais e suporte a SIMD {:#conditional-imports-and-simd-support}

* **Imports condicionais (`dart.library.isolate`)**:
  Ao compilar com `dart2wasm`, `dart.library.isolate` é avaliado como `false`
  nos imports condicionais (`if (dart.library.isolate)`), igual ao comportamento
  do `dart2js` e do `ddc`.
* **SIMD de 128 bits em Wasm (`v128`)**:
  No `dart2wasm`, os tipos SIMD de `dart:typed_data` (`Int32x4`, `Float32x4`,
  `Float64x2`, `Int32x4List`, `Float32x4List` e `Float64x2List`) são
  implementados com as instruções SIMD nativas de 128 bits `v128` do WebAssembly.

## Níveis de otimização e flags do compilador {:#optimization-levels-and-flags}

Ajuste as flags de `dart compile wasm` para equilibrar a velocidade de compilação
durante o desenvolvimento com um binário menor e uma execução mais rápida nos
builds de produção:

```console
$ dart compile wasm -O2 web/main.dart -o site/main.wasm
```

### Referência dos níveis de otimização {:#optimization-levels}

Os níveis de otimização `-O0` a `-O4` habilitam passes do compilador cada vez
mais agressivos:

| Flag | Binaryen (`wasm-opt`) | Inlining de funções | Minificar nomes de runtime (`--minify`) e omitir detalhes de erro | Omitir verificações de tipo implícitas | Omitir verificações de limites de índice |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `-O0` | Desabilitado | Desabilitado | Desabilitado | Desabilitado | Desabilitado |
| `-O1` (padrão) | Habilitado | Habilitado | Desabilitado | Desabilitado | Desabilitado |
| `-O2` | Habilitado | Habilitado | Habilitado | Desabilitado | Desabilitado |
| `-O3` | Habilitado | Habilitado | Habilitado | Habilitado | Desabilitado |
| `-O4` | Habilitado | Habilitado | Habilitado | Habilitado | Habilitado |

{:.table .table-striped}

Para a maioria dos builds de produção, use a flag `-O2`. Esse nível habilita
otimizações completas de tamanho e de velocidade (incluindo `wasm-opt`, inlining
de funções e minificação), preservando a semântica padrão do runtime do Dart,
as verificações de tipo e as verificações de limites.

:::warning
O nível `-O3` omite verificações de tipo implícitas, e o nível `-O4` omite,
além disso, as verificações de limites de índice (verificações explícitas de
tipo com `as` continuam sendo aplicadas em `-O3` e `-O4`). Omitir verificações
em tempo de execução pode fazer sua aplicação travar ou se comportar de forma
inesperada se ocorrer um erro de tipo ou um acesso fora dos limites. Antes de
fazer deploy com `-O3` ou `-O4`, teste bem com a flag `-O2` para verificar que
sua aplicação nunca lança um subtipo de `Error` (como `TypeError` ou `RangeError`).
:::

### Flags adicionais de CLI para produção {:#production-cli-flags}

Use as flags a seguir com o [`dart compile wasm`][dart-compile-wasm] para
personalizar os símbolos de saída, os source maps, a divisão em módulos e a
configuração em tempo de compilação:

| Flag | Padrão | Descrição |
| :--- | :--- | :--- |
| `--minify` | `-O2` e superiores | Minifica nomes de runtime (como `runtimeType.toString()`). |
| `--[no-]strip-wasm` | Habilitado | Remove os nomes estáticos dos símbolos do binário `.wasm` para reduzir o tamanho do download. Passe `--no-strip-wasm` ao [analisar o desempenho no Chrome DevTools](#profile-wasm). |
| `--[no-]source-maps` | Habilitado | Gera `<output>.wasm.map` para mapear os offsets das instruções Wasm de volta para os arquivos Dart e para as linhas de código. |
| `--[no-]enable-deferred-loading` | Desabilitado | Divide os imports `deferred as` em módulos `<name>_module<id>.wasm` separados, carregados sob demanda. |
| `--standalone` | Desabilitado | Gera um módulo Wasm standalone, sem interoperabilidade com JavaScript, para runtimes que não são web, como o Wasmtime (não permite [`dart:js_interop`][] nem `--enable-deferred-loading`). |
| `-D<key>=<value>` ou `--define` | Nenhum | Define declarações de ambiente em tempo de compilação lidas por `String.fromEnvironment`, `int.fromEnvironment` ou `bool.fromEnvironment`. |

{:.table .table-striped}

### Detectar a compilação Wasm no código Dart {:#detecting-wasm-compilation}

Ao compilar com `dart2wasm`, o compilador define automaticamente
`dart.tool.dart2wasm` como `true` no ambiente de compilação:

<?code-excerpt "misc/lib/development/environment_declarations.dart (wasm-check)"?>
```dart
const bool isRunningAsWasm = bool.fromEnvironment('dart.tool.dart2wasm');
```

### Deferred loading {:#deferred-loading}

Por padrão, as aplicações compiladas são carregadas como um único módulo `.wasm`.
Para aplicações grandes, passe `--enable-deferred-loading` para dividir as
[bibliotecas deferidas][deferred loading] em arquivos `<name>_module<id>.wasm`
separados:

```console
$ dart compile wasm -O2 --enable-deferred-loading web/main.dart -o site/main.wasm
```

Quando você habilita o deferred loading, o carregador da sua aplicação precisa
fornecer um callback `loadDeferredModules` para `app.instantiate()`, que busca e
carrega os bytes dos módulos deferidos:

```js
import { compileStreaming } from './main.mjs';

const app = await compileStreaming(fetch('main.wasm')); // or compile(...)
const instantiatedApp = await app.instantiate({}, {
  loadDeferredModules: (modules, handleModuleByteSource) => {
    return Promise.all(
      modules.map((m) => fetch(m).then((r) => handleModuleByteSource(m, r)))
    );
  },
});
instantiatedApp.invokeMain();
```

## Como o `dart2wasm` funciona {:#architecture-and-wasmgc}

O compilador AOT (ahead-of-time) `dart2wasm` traduz o código-fonte Dart em um
bytecode WebAssembly compacto, que se integra diretamente ao coletor de lixo
nativo e ao runtime de strings do navegador.

### O pipeline de compilação AOT do `dart2wasm` {:#compilation-pipeline}

Quando você executa `dart compile wasm`, o compilador `dart2wasm` executa
quatro fases sequenciais:

1. **`cfe` (Common Front End)**:
   Analisa o código-fonte Dart, aplica a null safety sólida e transformações
   modulares do kernel, gerando uma árvore de sintaxe abstrata (AST) de kernel
   em um arquivo `.dill`.
1. **`tfa` (Type Flow Analysis)**:
   Executa uma análise de programa inteiro em mundo fechado, removendo o código
   inalcançável (tree shaking), desvirtualizando chamadas de método e inferindo
   tipos concretos e oportunidades de unboxing.
1. **`codegen` (geração de código Wasm)**:
   Traduz o kernel Dart otimizado em instruções WebAssembly e em definições de
   tipos structs e arrays do WasmGC, emitindo `<name>.wasm`, o loader de runtime
   JavaScript `<name>.mjs` e `<name>.wasm.map`.
1. **`opt` (otimização com Binaryen)**:
   Executa o `wasm-opt` (em `-O1` e superiores) para otimizar as sequências de
   instruções Wasm e reduzir o tamanho do binário.

### Padrões de WebAssembly usados pelo Dart {:#wasm-standards}

O compilador `dart2wasm` tem como alvo propostas padronizadas de WebAssembly
para minimizar o tamanho do binário e o overhead de execução:

* **WebAssembly Garbage Collection (WasmGC)**:
  Mapeia objetos, classes e coleções do Dart diretamente para estruturas de heap
  com coleta de lixo nativa, gerenciadas pelo motor do navegador (como o V8, no
  Chrome). Como o `dart2wasm` não traz um alocador de memória linear próprio nem
  um coletor de lixo duplicado junto ao coletor do navegador, os módulos ficam
  menores e evitam ciclos de memória entre heaps.
* **JS String Builtins (`wasm:js-string`)**:
  Permite que os módulos Wasm usem operações nativas de string do JavaScript e
  passem strings entre a fronteira JavaScript e Wasm sem cópias caras de
  transcodificação UTF-8 ou UTF-16.
* **Exception Handling (Phase 4)**:
  Usa tags de exceção nativas do WebAssembly (`try_table` e `exnref`) para
  tratamento de `try` e `catch` com baixo overhead e para a geração de stack traces.

### Ganhos de desempenho em relação ao JavaScript {:#why-wasm-improves-performance}

Compilar para WebAssembly melhora a latência de inicialização e a consistência
dos frames em comparação com a compilação para JavaScript (`dart2js`):

* **Elimina gargalos de parse e de avaliação JIT do JS**:
  Bundles grandes de JavaScript exigem que o navegador baixe o texto, converta os
  tokens em uma AST e execute uma compilação JIT multinível na thread principal
  antes que a renderização interativa se estabilize.
* **Compilação em segundo plano por streaming**:
  Os navegadores compilam o bytecode binário compacto `.wasm` em threads de
  segundo plano enquanto a resposta da rede chega em stream
  (`WebAssembly.compileStreaming`).
* **Execução previsível desde o primeiro frame**:
  A compilação AOT em mundo fechado e as tabelas de despacho estático entregam
  tempos de execução consistentes, sem esperar pelo aquecimento do JIT nem sofrer
  bailouts de deoptimization.

## Analise o desempenho e o tamanho do Wasm {:#profile-wasm}

Antes de fazer o deploy, analise sua aplicação compilada no [Chrome DevTools][]
para verificar os [Core Web Vitals][] e inspecionar o download do `.wasm` e o
uso de memória.

### Meça os Core Web Vitals (LCP, INP e CLS) {:#measure-core-web-vitals}

Por padrão, o `dart compile wasm` remove a seção de nomes customizada
(`name`) do WebAssembly, então as funções aparecem como índices numéricos nos
traces de CPU. Para manter os nomes legíveis de funções e classes do Dart sem
desabilitar as otimizações de produção, compile com as flags `-O2` e
`--no-strip-wasm`:

```console
$ dart compile wasm -O2 --no-strip-wasm web/main.dart -o site/main.wasm
```

:::note
Use `--no-strip-wasm` apenas em builds de profiling locais ou de staging.
Manter os nomes dos símbolos aumenta o tamanho do arquivo `.wasm`, então omita
`--no-strip-wasm` no build final de release e ao medir o tamanho transferido pela rede.
:::

Grave um trace no [painel Performance do Chrome DevTools][Chrome DevTools Performance panel]
para avaliar os [Core Web Vitals][] e verificar se `main.mjs` e `main.wasm` são
buscados em paralelo, sem tarefas longas na thread principal nem chamadas
frequentes de interop de Wasm para JS. Para a configuração geral de depuração no
navegador, consulte [Depurando aplicações web Dart][Debugging Dart web apps].

### Inspecione o tamanho e a memória do módulo Wasm {:#inspect-wasm-footprint}

Use os painéis **Network** e **Memory** do Chrome DevTools para verificar o
tamanho transferido e o uso de heap em runtime:

* **Tamanho transferido pela rede**:
  Compile um build de produção sem símbolos (`dart compile wasm -O2`, sem a flag
  `--no-strip-wasm`) e use o [painel Network do Chrome DevTools][Chrome DevTools Network panel]
  para comparar o tamanho comprimido transferido (`br` ou `gzip`) com o tamanho
  descomprimido e confirmar o cabeçalho de resposta `Content-Type: application/wasm`.
  Se o tamanho inicial do `.wasm` atrasa o carregamento, divida as rotas com a
  flag `--enable-deferred-loading` (consulte [Deferred loading](#deferred-loading)).
* **Heap do WasmGC em runtime**:
  Como o `dart2wasm` compila objetos Dart para structs e arrays nativos do WasmGC,
  gerenciados pelo coletor de lixo do V8 (e não por um `ArrayBuffer` opaco de
  memória linear), as instâncias Dart vivas aparecem diretamente nos perfis de
  heap do JavaScript. Compile com a flag `--no-strip-wasm` para que os nomes de
  tipos e campos do WasmGC continuem legíveis ao [gravar snapshots do heap][recording heap snapshots].

## Faça o deploy do Wasm em produção {:#production-deployment}

Para obter todos os benefícios de inicialização e de runtime do WebAssembly em
produção, configure seu servidor web e seu pipeline de release para transmitir,
comprimir e armazenar em cache os módulos `.wasm`, além de fornecer um fallback em
JavaScript para navegadores mais antigos. Consulte
[Serve WebAssembly em produção][serving-wasm] no guia de deploy para a web e veja
as instruções completas para as tarefas a seguir:

* Servir os arquivos `.wasm` com o cabeçalho `Content-Type: application/wasm`.
* Pré-carregar os assets `.mjs` e `.wasm` em paralelo para a compilação em streaming.
* Pré-comprimir os binários `.wasm` com Brotli (`brotli -q 11`) e Gzip.
* Configurar cache imutável com hash de conteúdo, deploys atômicos de `.mjs` e
  `.wasm` e cache de código Wasm da V8.
* Fornecer um caminho de fallback com `dart2js` para navegadores mais antigos.

[wasm-org]: https://webassembly.org/
[Flutter]: {{site.flutter}}/wasm
[js-interop]: /interop/js-interop/
[past-js-interop]: /interop/js-interop/past-js-interop#next-generation-js-interop
[`package:web`]: {{site.pub-pkg}}/web
[`dart:js_interop`]: {{site.dart-api}}/dart-js_interop/
[migrated]: /interop/js-interop/package-web/
[`wasm-ready`]: {{site.pub-pkg}}?q=is%3Awasm-ready
[pub.dev]: {{site.pub}}
[dart-compile-wasm]: /tools/dart-compile#wasm
[`dhttpd`]: {{site.pub-pkg}}/dhttpd
[deferred loading]: /language/libraries#lazily-loading-a-library
[serving-wasm]: /web/deployment#serving-wasm-in-production
[manage-source-maps]: /web/deployment#manage-source-maps-and-unneeded-build-files
[sandbox]: https://github.com/mit-mit/sandbox
[Chrome DevTools]: https://developer.chrome.com/docs/devtools/
[Chrome DevTools Performance panel]: https://developer.chrome.com/docs/devtools/performance/
[Chrome DevTools Network panel]: https://developer.chrome.com/docs/devtools/network/
[recording heap snapshots]: https://developer.chrome.com/docs/devtools/memory-problems/heap-snapshots
[Debugging Dart web apps]: /web/debugging
[Core Web Vitals]: https://web.dev/articles/vitals
