---
<<<<<<< pt
ia-translate: true
title: Compilação WebAssembly (Wasm)
description: Aprenda a compilar sua aplicação web Dart para WebAssembly.
||||||| base_en
title: WebAssembly (Wasm) compilation
description: Learn how to compile your Dart web app to WebAssembly.
=======
title: WebAssembly (Wasm) compilation
shortTitle: Wasm compilation
description: >-
  Compile Dart web applications to WebAssembly (WasmGC) to reduce load times,
  eliminate main-thread JIT pauses, and improve rendering responsiveness.
>>>>>>> new_en
---

<<<<<<< pt
Você pode compilar aplicações web do Dart e do [Flutter][] para
[WebAssembly][wasm-org] (`dart2wasm`) como alternativa ao JavaScript
em builds de produção.
||||||| base_en
You can compile Dart and [Flutter][] web applications to
[WebAssembly][wasm-org] (`dart2wasm`) as an alternative to JavaScript
for production builds.
=======
You can compile Dart and [Flutter][] web applications to
[WebAssembly][wasm-org] (`dart2wasm`) as a high-performance production
alternative to JavaScript (`dart2js`). Compiling to WebAssembly reduces initial
page load times, eliminates main-thread JavaScript just-in-time (JIT)
compilation pauses, and delivers consistent frame rendering in modern browsers.
>>>>>>> new_en

<<<<<<< pt
## Suporte a WebAssembly {:#webassembly-support}
||||||| base_en
## WebAssembly support
=======
## Compile your web app to Wasm {:#compiling-to-wasm}
>>>>>>> new_en

<<<<<<< pt
Ao compilar Dart para WebAssembly, tenha em mente os seguintes requisitos
e comportamentos da plataforma:
||||||| base_en
When compiling Dart to WebAssembly, keep the following requirements
and platform behaviors in mind:
=======
Use the [`dart compile wasm`][dart-compile-wasm] command to compile a Dart web
app to a WebAssembly module. For a full list of compiler flags, refer to
[Compiler optimization levels and flags](#optimization-levels-and-flags) or run
`dart compile wasm --help`.
>>>>>>> new_en

<<<<<<< pt
1. O `dart2wasm` tem como alvo três propostas padronizadas de WebAssembly:
   **WasmGC** (coleta de lixo),
   **JS String Builtins** (`wasm:js-string`) e
   **Exception Handling da Fase 4** (`try_table` e `exnref`).
   Para executar os módulos compilados em um navegador, é necessário pelo menos:
||||||| base_en
1. `dart2wasm` targets three standardized WebAssembly proposals:
   **WasmGC** (Garbage Collection),
   **JS String Builtins** (`wasm:js-string`), and
   **Phase 4 Exception Handling** (`try_table` and `exnref`).
   Running compiled modules in a browser requires at least:
=======
:::note
If you are building a Flutter web app, run `flutter build web --wasm`
instead of invoking `dart compile wasm` directly. Refer to the
[Flutter Wasm documentation][Flutter] for Flutter-specific build instructions.
:::
>>>>>>> new_en

<<<<<<< pt
   * **Chrome ou Edge 137+**
   * **Safari 26.2+** (macOS e iOS)
   * **Firefox 134+** (ou **147+** para Flutter web)
||||||| base_en
   * **Chrome or Edge 137+**
   * **Safari 26.2+** (macOS and iOS)
   * **Firefox 134+** (or **147+** for Flutter web)
=======
To compile and run a Dart web app with Wasm, follow these steps:
>>>>>>> new_en

<<<<<<< pt
   Para mais detalhes de compatibilidade entre navegadores, veja a
   [documentação do Flutter Wasm][Flutter].
||||||| base_en
   For more browser compatibility details, see the
   [Flutter Wasm documentation][Flutter].
=======
1. Create a web app and switch to its directory:
>>>>>>> new_en

<<<<<<< pt
1. Por padrão, a saída Wasm compilada tem como alvo ambientes JavaScript
   (como navegadores) e gera um arquivo de runtime complementar `<name>.mjs`.
   Para compilar um módulo WebAssembly independente para runtimes que não são web,
   como o Wasmtime 39+ (usando `-W gc,exceptions,function-references=y`),
   passe `--standalone` para o `dart compile wasm`.
   Quando `--standalone` está definido, o [`dart:js_interop`][] não é permitido.
||||||| base_en
1. By default, compiled Wasm output targets JavaScript environments
   (such as browsers) and generates a companion `<name>.mjs` runtime file.
   To compile a standalone WebAssembly module for non-web
   runtimes such as Wasmtime 39+
   (using `-W gc,exceptions,function-references=y`),
   pass `--standalone` to `dart compile wasm`.
   When `--standalone` is set, [`dart:js_interop`][] is disallowed.
=======
   ```console
   $ dart create -t web mywebapp
   $ cd mywebapp
   ```
>>>>>>> new_en

<<<<<<< pt
1. Apenas o
   [mecanismo de interoperabilidade JS de próxima geração do Dart][js-interop]
   é suportado ao compilar para Wasm.
||||||| base_en
1. Only Dart's
   [next-gen JS interop mechanism][js-interop]
   is supported when compiling to Wasm.
=======
   The template creates a small web app that uses [`package:web`][], which is
   required to run Wasm. Existing web apps must [migrate][migrated] from
   `dart:html` to `package:web`.
>>>>>>> new_en

<<<<<<< pt
1. A ferramenta `webdev` não oferece suporte atualmente à compilação Wasm
   (`webdev serve` ou `webdev build`).
   Em vez disso, siga os passos em
   [Compilando sua aplicação web para Wasm](#compiling-to-wasm).
||||||| base_en
1. The `webdev` tool doesn't currently support Wasm compilation
   (`webdev serve` or `webdev build`).
   Instead, follow the steps in
   [Compiling your web app to Wasm](#compiling-to-wasm).
=======
1. Compile the app to Wasm into a `site` output directory:
>>>>>>> new_en

<<<<<<< pt
### Deferred loading {:#deferred-loading}
||||||| base_en
### Deferred loading
=======
   ```console
   $ dart compile wasm -O2 web/main.dart -o site/main.wasm
   ```
>>>>>>> new_en

<<<<<<< pt
Por padrão, as aplicações compiladas não usam [deferred loading][].
O deferred loading em Wasm é experimental.
Para habilitá-lo, passe a flag `--enable-deferred-loading`:
||||||| base_en
By default, compiled applications do not use [deferred loading][].
Deferred loading in Wasm is experimental.
To enable it, pass the `--enable-deferred-loading` flag:
=======
   This command produces `site/main.wasm`, the companion JavaScript runtime
   `site/main.mjs`, and `site/main.wasm.map`.
>>>>>>> new_en

   :::note
   By default, `dart compile wasm` generates a `.wasm.map` source map file
   alongside the `.wasm` output. To disable source map generation for
   production builds, pass `--no-source-maps`. To learn about security
   considerations when deploying source maps, refer to
   [Web deployment][manage-source-maps].
   :::

<<<<<<< pt
Para habilitar o deferred loading, o carregador da sua aplicação precisa fornecer um callback
que carregue os bytes dos módulos deferidos:
||||||| base_en
Enabling deferred loading requires your app loader to supply a callback
that loads the deferred module bytes:
=======
1. Copy over the static web files:
>>>>>>> new_en

   ```console
   $ cp web/index.html web/styles.css site/
   ```

1. Because `index.html` loads `main.dart.js`, create `site/main.dart.js` to
   fetch `site/main.wasm` and import the generated `site/main.mjs` runtime in
   parallel:

<<<<<<< pt
### Imports condicionais e suporte a SIMD {:#conditional-imports-and-simd-support}
||||||| base_en
### Conditional imports and SIMD support
=======
   ```js title="site/main.dart.js"
   (async function () {
     const wasmPromise = fetch('main.wasm');
     const { compileStreaming } = await import('./main.mjs');
     const app = await compileStreaming(wasmPromise);
     const instantiatedApp = await app.instantiate({});
     instantiatedApp.invokeMain();
   })();
   ```
>>>>>>> new_en

<<<<<<< pt
* **Imports condicionais (`dart.library.isolate`)**:
  Ao compilar com `dart2wasm`, `dart.library.isolate` é avaliado como `false`
  nos imports condicionais (`if (dart.library.isolate)`),
  igual ao comportamento do `dart2js` e do `ddc`.
* **SIMD de 128 bits em Wasm (`v128`)**:
  No `dart2wasm`, os tipos SIMD de `dart:typed_data`
  (`Int32x4`, `Float32x4`, `Float64x2`, `Int32x4List`,
  `Float32x4List` e `Float64x2List`)
  são implementados com as instruções SIMD nativas de 128 bits `v128` do WebAssembly.
||||||| base_en
* **Conditional imports (`dart.library.isolate`)**:
  When compiling with `dart2wasm`, `dart.library.isolate` evaluates to `false`
  in conditional imports (`if (dart.library.isolate)`),
  matching the behavior of `dart2js` and `ddc`.
* **128-bit Wasm SIMD (`v128`)**:
  In `dart2wasm`, `dart:typed_data` SIMD types
  (`Int32x4`, `Float32x4`, `Float64x2`, `Int32x4List`,
  `Float32x4List`, and `Float64x2List`)
  are backed by native WebAssembly 128-bit `v128` SIMD instructions.
=======
1. Serve the `site` directory by using a local HTTP server such as [`dhttpd`][]:
>>>>>>> new_en

<<<<<<< pt
### Pacotes suportados {:#supported-packages}
||||||| base_en
### Supported packages
=======
   ```console
   $ dart run dhttpd@ --path site
   ```
>>>>>>> new_en

<<<<<<< pt
Para encontrar pacotes compatíveis com Wasm,
use o filtro [`wasm-ready`][] no [pub.dev][].
||||||| base_en
To find Wasm-compatible packages,
use the [`wasm-ready`][] filter on [pub.dev][].
=======
You can also explore this small [sandbox example][sandbox].
>>>>>>> new_en

<<<<<<< pt
Um pacote é "wasm-ready" se não importa bibliotecas não compatíveis com Wasm,
como `dart:html` ou `dart:js`. Você encontra a lista completa de bibliotecas
não permitidas na [página de interoperabilidade JS][past-js-interop].
||||||| base_en
A package is "wasm-ready" if it doesn't import non-Wasm compliant libraries
such as `dart:html` or `dart:js`. You can find the full list of disallowed
libraries on the [JS interop page][past-js-interop].
=======
## WebAssembly support and requirements {:#webassembly-support}
>>>>>>> new_en

When compiling Dart to WebAssembly, keep the following browser, interop, and
platform requirements in mind:

<<<<<<< pt
## Compilando sua aplicação web para Wasm {:#compiling-to-wasm}
||||||| base_en
## Compiling your web app to Wasm {:#compiling-to-wasm}
=======
* **WebAssembly standards and browser compatibility**:
  The `dart2wasm` compiler targets three standardized WebAssembly proposals:
  WebAssembly Garbage Collection (WasmGC), JS String Builtins
  (`wasm:js-string`), and Phase 4 Exception Handling (the `try_table` and
  `exnref` instructions). Running compiled modules in a browser requires one
  of the following minimum browser versions:
>>>>>>> new_en

<<<<<<< pt
Use o comando `dart compile wasm` na CLI `dart` para invocar o
compilador Wasm do Dart e do [Flutter][]:
||||||| base_en
Use the `dart compile wasm` command in the `dart` CLI
to invoke the Wasm compiler in Dart and [Flutter][]:
=======
  * Chrome or Edge 137+
  * Safari 26.2+ (macOS and iOS)
  * Firefox 134+ (or 147+ for Flutter web)
>>>>>>> new_en

  For additional browser compatibility details, refer to the
  [Flutter Wasm documentation][Flutter].

<<<<<<< pt
Para compilar e executar uma aplicação web Dart com Wasm, siga estes passos:
||||||| base_en
To compile and run a Dart web app with Wasm, follow these steps:
=======
* **Target environments and standalone mode**:
  By default, compiled Wasm output targets JavaScript environments (such as
  browsers) and generates a companion `<name>.mjs` runtime file. To compile a
  standalone WebAssembly module for non-web runtimes such as Wasmtime 39+
  (with the `-W gc,exceptions,function-references=y` flag), pass the
  `--standalone` flag to `dart compile wasm`. Standalone mode disallows the
  [`dart:js_interop`][] library and the `--enable-deferred-loading` flag.

* **JavaScript interop**:
  Compiling to Wasm supports only Dart's
  [next-generation JS interop mechanism][js-interop]
  ([`dart:js_interop`][] and [`package:web`][]).

* **Build tooling**:
  The `webdev` tool doesn't support Wasm compilation (`webdev serve` or
  `webdev build`). Instead, follow the steps in
  [Compile your web app to Wasm](#compiling-to-wasm).

### Supported packages {:#supported-packages}

To find Wasm-compatible packages, use the [`wasm-ready`][] filter on
[pub.dev][].
>>>>>>> new_en

<<<<<<< pt
1.  Crie uma aplicação web e entre no diretório dela:
||||||| base_en
1.  Create a web app and switch to its directory:
=======
A package is *wasm-ready* when it doesn't import legacy web or interop
libraries such as `dart:html`, `dart:js`, or `package:js`. Refer to the
[past JS interop page][past-js-interop] for the full list of disallowed
libraries.
>>>>>>> new_en

### Conditional imports and SIMD support {:#conditional-imports-and-simd-support}

<<<<<<< pt
    O template cria uma pequena aplicação web usando o [`package:web`][],
    que é necessário para executar Wasm.
    Certifique-se de que suas aplicações web foram [migradas][migrated] de `dart:html` para `package:web`.
||||||| base_en
    The template creates a small web app using [`package:web`][],
    which is necessary to run Wasm.
    Make sure your web apps are [migrated][] from `dart:html` to `package:web`.
=======
* **Conditional imports (`dart.library.isolate`)**:
  When compiling with `dart2wasm`, `dart.library.isolate` evaluates to `false`
  in conditional imports (`if (dart.library.isolate)`), matching the behavior
  of `dart2js` and `ddc`.
* **128-bit Wasm SIMD (`v128`)**:
  In `dart2wasm`, `dart:typed_data` SIMD types (`Int32x4`, `Float32x4`,
  `Float64x2`, `Int32x4List`, `Float32x4List`, and `Float64x2List`) are backed
  by native WebAssembly 128-bit `v128` SIMD instructions.
>>>>>>> new_en

<<<<<<< pt
1.  Compile a aplicação para Wasm em um diretório de saída `site`:
||||||| base_en
1.  Compile the app to Wasm into a `site` output directory:
=======
## Compiler optimization levels and flags {:#optimization-levels-and-flags}
>>>>>>> new_en

Tune `dart compile wasm` flags to balance compilation speed during development
against smaller binary size and faster execution in production builds:

<<<<<<< pt
    Isso gera `site/main.wasm`, o runtime JavaScript complementar
    `site/main.mjs` e `site/main.wasm.map`.
||||||| base_en
    This produces `site/main.wasm`, the companion JavaScript runtime
    `site/main.mjs`, and `site/main.wasm.map`.
=======
```console
$ dart compile wasm -O2 web/main.dart -o site/main.wasm
```
>>>>>>> new_en

<<<<<<< pt
    :::note
    Por padrão, o `dart compile wasm` gera um arquivo de source map `.wasm.map`
    junto com a saída `.wasm`.
    Para desabilitar a geração de source maps em builds de produção,
    passe `--no-source-maps`.
    Para conhecer as considerações de segurança ao fazer deploy de source maps,
    veja [Deploy na web][manage-source-maps].
    :::
||||||| base_en
    :::note
    By default, `dart compile wasm` generates a `.wasm.map` source map file
    alongside the `.wasm` output.
    To disable source map generation for production builds,
    pass `--no-source-maps`.
    To learn about security considerations when deploying source maps,
    see [Web deployment][manage-source-maps].
    :::
=======
### Optimization levels reference {:#optimization-levels}

The `-O0` through `-O4` optimization levels enable progressively more
aggressive compiler passes:

| Flag | Binaryen (`wasm-opt`) | Function inlining | Minify runtime names (`--minify`) and omit error details | Omit implicit type checks | Omit index bounds checks |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `-O0` | Disabled | Disabled | Disabled | Disabled | Disabled |
| `-O1` (default) | Enabled | Enabled | Disabled | Disabled | Disabled |
| `-O2` | Enabled | Enabled | Enabled | Disabled | Disabled |
| `-O3` | Enabled | Enabled | Enabled | Enabled | Disabled |
| `-O4` | Enabled | Enabled | Enabled | Enabled | Enabled |

{:.table .table-striped}

For most production builds, use the `-O2` flag. This level enables full size
and speed optimizations (including `wasm-opt`, function inlining, and
minification) while preserving standard Dart runtime semantics, type checks,
and bounds checks.

:::warning
The `-O3` level omits implicit type checks, and the `-O4` level additionally
omits index bounds checks (explicit `as` type checks are still enforced at
`-O3` and `-O4`). Omitting runtime checks can cause your app to trap or behave
unexpectedly if a runtime type error or out-of-bounds access occurs. Before
deploying with `-O3` or `-O4`, test thoroughly with the `-O2` flag to verify
that your app never throws a subtype of `Error` (such as `TypeError` or
`RangeError`).
:::

### Additional production CLI flags {:#production-cli-flags}

Use the following flags with [`dart compile wasm`][dart-compile-wasm] to
customize output symbols, source maps, module splitting, and compile-time
configuration:

| Flag | Default | Description |
| :--- | :--- | :--- |
| `--minify` | `-O2` and higher | Minifies runtime names (such as `runtimeType.toString()`). |
| `--[no-]strip-wasm` | Enabled | Strips static symbol names from the `.wasm` binary to reduce download size. Pass `--no-strip-wasm` when [profiling in Chrome DevTools](#profile-wasm). |
| `--[no-]source-maps` | Enabled | Generates `<output>.wasm.map` to map Wasm instruction offsets back to Dart source files and line numbers. |
| `--[no-]enable-deferred-loading` | Disabled | Splits `deferred as` imports into separate `<name>_module<id>.wasm` modules loaded on demand. |
| `--standalone` | Disabled | Emits a standalone Wasm module without JavaScript interop for non-web runtimes such as Wasmtime (disallows [`dart:js_interop`][] and `--enable-deferred-loading`). |
| `-D<key>=<value>` or `--define` | None | Defines compile-time environment declarations read by `String.fromEnvironment`, `int.fromEnvironment`, or `bool.fromEnvironment`. |

{:.table .table-striped}

### Detect Wasm compilation in Dart code {:#detecting-wasm-compilation}

When compiling with `dart2wasm`, the compiler automatically defines
`dart.tool.dart2wasm` as `true` in the compile-time environment:

<?code-excerpt "misc/lib/development/environment_declarations.dart (wasm-check)"?>
```dart
const bool isRunningAsWasm = bool.fromEnvironment('dart.tool.dart2wasm');
```
>>>>>>> new_en

<<<<<<< pt
1.  Copie os arquivos web estáticos:
||||||| base_en
1.  Copy over the static web files:
=======
### Deferred loading {:#deferred-loading}
>>>>>>> new_en

By default, compiled applications load as a single `.wasm` module. For large
applications, pass `--enable-deferred-loading` to split
[deferred libraries][deferred loading] into separate `<name>_module<id>.wasm`
files:

<<<<<<< pt
1.  Como o `index.html` carrega o `main.dart.js`, crie o `site/main.dart.js`
    para importar o runtime `site/main.mjs` gerado e instanciar
    o `site/main.wasm`:
||||||| base_en
1.  Because `index.html` loads `main.dart.js`, create `site/main.dart.js`
    to import the generated `site/main.mjs` runtime and instantiate
    `site/main.wasm`:
=======
```console
$ dart compile wasm -O2 --enable-deferred-loading web/main.dart -o site/main.wasm
```
>>>>>>> new_en

When you enable deferred loading, your application loader must provide a
`loadDeferredModules` callback to `app.instantiate()` that fetches and loads
the deferred module bytes:

<<<<<<< pt
1.  Sirva o diretório `site` usando o [`dhttpd`][]:
||||||| base_en
1.  Serve the `site` directory using [`dhttpd`][]:
=======
```js
import { compileStreaming } from './main.mjs';
>>>>>>> new_en

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

<<<<<<< pt
Você também pode testar este pequeno [exemplo de sandbox][sandbox].
||||||| base_en
You can also try out this small [sandbox example][sandbox].
=======
## How `dart2wasm` works {:#architecture-and-wasmgc}

The `dart2wasm` ahead-of-time (AOT) compiler translates Dart source code into
compact WebAssembly bytecode that integrates directly with the browser's native
garbage collector and string runtime.

### The `dart2wasm` AOT compilation pipeline {:#compilation-pipeline}

When you run `dart compile wasm`, the `dart2wasm` compiler executes four
sequential phases:

1. **`cfe` (Common Front End)**:
   Parses Dart source code, enforces sound null safety, and applies modular
   kernel transformations into a `.dill` kernel abstract syntax tree (AST).
1. **`tfa` (Type Flow Analysis)**:
   Performs closed-world whole-program analysis, tree-shaking unreachable code,
   devirtualizing method calls, and inferring concrete types and unboxing
   opportunities.
1. **`codegen` (Wasm code generation)**:
   Translates the optimized Dart kernel into WebAssembly instructions and
   WasmGC struct and array type definitions, emitting `<name>.wasm`, the
   `<name>.mjs` JavaScript runtime loader, and `<name>.wasm.map`.
1. **`opt` (Binaryen optimization)**:
   Runs `wasm-opt` (at `-O1` and higher) to optimize Wasm instruction sequences
   and shrink binary size.

### WebAssembly standards used by Dart {:#wasm-standards}

The `dart2wasm` compiler targets standardized WebAssembly proposals to
minimize binary size and runtime overhead:

* **WebAssembly Garbage Collection (WasmGC)**:
  Maps Dart objects, classes, and collections directly to native
  garbage-collected heap structures managed by the browser engine (such as V8
  in Chrome). Because `dart2wasm` doesn't ship a custom linear-memory allocator
  or duplicate garbage collector alongside the browser's garbage collector,
  modules are smaller and avoid cross-heap memory cycles.
* **JS String Builtins (`wasm:js-string`)**:
  Lets Wasm modules use native JavaScript string operations and pass
  strings across the JavaScript and Wasm boundary without expensive UTF-8 or
  UTF-16 transcoding copies.
* **Exception Handling (Phase 4)**:
  Uses native WebAssembly exception tags (`try_table` and `exnref`) for
  low-overhead `try` and `catch` handling and stack trace generation.

### Performance benefits over JavaScript {:#why-wasm-improves-performance}

Compiling to WebAssembly improves startup latency and frame consistency
compared to compiling to JavaScript (`dart2js`):

* **Eliminates JS parse and JIT evaluation bottlenecks**:
  Large JavaScript bundles require the browser to download text, parse source
  tokens into an AST, and run multi-tier JIT compilation on the main thread
  before interactive rendering stabilizes.
* **Streaming background compilation**:
  Browsers compile compact binary `.wasm` bytecode across background threads
  while the network response streams (`WebAssembly.compileStreaming`).
* **Predictable execution from the first frame**:
  Closed-world AOT compilation and static dispatch tables deliver consistent
  execution times without waiting for JIT warm-up or suffering deoptimization
  bailouts.

## Profile Wasm performance and footprint {:#profile-wasm}

Before deploying,
profile your compiled app in [Chrome DevTools][]
to verify [Core Web Vitals][]
and inspect your `.wasm` download and memory footprint.

### Measure Core Web Vitals (LCP, INP, and CLS) {:#measure-core-web-vitals}

By default, `dart compile wasm` strips the WebAssembly `name` custom section,
so functions appear as numeric indices in CPU traces.
To keep readable Dart function and class names
without disabling production optimizations,
compile with the `-O2` and `--no-strip-wasm` flags:

```console
$ dart compile wasm -O2 --no-strip-wasm web/main.dart -o site/main.wasm
```

:::note
Use `--no-strip-wasm` only for local or staging profiling builds.
Retaining symbol names increases `.wasm` file size,
so omit `--no-strip-wasm` for your final release build
and when measuring network transfer size.
:::

Record a trace in the [Chrome DevTools Performance panel][]
to evaluate [Core Web Vitals][] and verify that `main.mjs` and `main.wasm`
fetch in parallel without main-thread long tasks or frequent Wasm-to-JS
interop calls. For general browser debugging setup, refer to
[Debugging Dart web apps][].

### Inspect Wasm module size and memory {:#inspect-wasm-footprint}

Use the Chrome DevTools **Network** and **Memory** panels to check wire size
and runtime heap usage:

* **Network transfer size**:
  Compile a stripped production build (`dart compile wasm -O2`, without the
  `--no-strip-wasm` flag) and use the [Chrome DevTools Network panel][]
  to compare compressed transfer size (`br` or `gzip`) against uncompressed
  size and confirm the `Content-Type: application/wasm` response header. If
  initial `.wasm` size delays load, split routes with the
  `--enable-deferred-loading` flag (refer to
  [Deferred loading](#deferred-loading)).
* **Runtime WasmGC heap**:
  Because `dart2wasm` compiles Dart objects to native WasmGC structs and
  arrays managed by V8's garbage collector (rather than an opaque
  linear-memory `ArrayBuffer`), live Dart instances appear directly in
  JavaScript heap profiles. Compile with the `--no-strip-wasm` flag so WasmGC
  type and field names remain readable when [recording heap snapshots][].

## Deploy Wasm in production {:#production-deployment}

To get the full startup and runtime benefits of WebAssembly in production,
configure your web server and release pipeline to stream, compress, and cache
`.wasm` modules and provide a JavaScript fallback for older browsers. Refer to
[Serve WebAssembly in production][serving-wasm] in the web deployment guide
for complete instructions on the following tasks:

* Serving `.wasm` files with the `Content-Type: application/wasm` header.
* Preloading `.mjs` and `.wasm` assets in parallel for streaming compilation.
* Pre-compressing `.wasm` binaries with Brotli (`brotli -q 11`) and Gzip.
* Configuring content-hashed immutable caching, atomic `.mjs` and `.wasm`
  deployments, and V8 Wasm code caching.
* Providing a `dart2js` fallback pathway for older browsers.
>>>>>>> new_en

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
<<<<<<< pt
||||||| base_en

=======
[Chrome DevTools]: https://developer.chrome.com/docs/devtools/
[Chrome DevTools Performance panel]: https://developer.chrome.com/docs/devtools/performance/
[Chrome DevTools Network panel]: https://developer.chrome.com/docs/devtools/network/
[recording heap snapshots]: https://developer.chrome.com/docs/devtools/memory-problems/heap-snapshots
[Debugging Dart web apps]: /web/debugging
[Core Web Vitals]: https://web.dev/articles/vitals
>>>>>>> new_en
