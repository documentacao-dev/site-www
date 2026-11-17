---
<<<<<<< pt
ia-translate: true
title: Deploy na web
description: Aprenda a compilar sua aplicação web Dart para deploy em produção.
||||||| base_en
title: Web deployment
description: Learn how to build your Dart web app for production deployment.
=======
title: Web deployment
description: >-
  Learn how to build and serve your Dart web app for production deployment.
>>>>>>> new_en
---

<<<<<<< pt
O deploy de uma aplicação web Dart funciona como o deploy de qualquer outra aplicação web.
Esta página descreve como compilar sua aplicação, dicas para deixá-la menor
e mais rápida, e aponta recursos para servir a aplicação.
||||||| base_en
Deploying a Dart web app works like deploying any other web app.
This page describes how to compile your app, tips for making it smaller
and faster, and points you to resources for serving the app.
=======
Deploying a Dart web app works like deploying any other web app.
You compile your Dart code to production WebAssembly (`dart compile wasm`) or
JavaScript (`dart compile js` or `webdev build`), optimize the generated
assets, and serve them from a web server or content delivery network (CDN).
>>>>>>> new_en

<<<<<<< pt
## Compilando sua aplicação {:#compiling-to-javascript}
||||||| base_en
## Building your app {:#compiling-to-javascript}
=======
## Build your app {:#compiling-to-javascript}
>>>>>>> new_en

<<<<<<< pt
Use a ferramenta `webdev` para compilar sua aplicação. Ela compila Dart para JavaScript
e gera todos os recursos de que você precisa para o deploy.
Quando você compila usando o modo de produção do compilador,
obtém um arquivo JavaScript razoavelmente pequeno,
graças ao suporte do compilador a tree shaking.
||||||| base_en
Use the `webdev` tool to build your app. It compiles Dart to JavaScript
and generates all the assets you need for deployment.
When you build using the production mode of the compiler,
you get a JavaScript file that's reasonably small,
thanks to the compiler support for tree shaking.
=======
For production deployments, you can compile your Dart web app to
[WebAssembly (Wasm)][wasm] (`dart2wasm`), JavaScript (`dart2js`), or both (with
JavaScript as a fallback for older browsers):
>>>>>>> new_en

<<<<<<< pt
Com um pouco de trabalho extra, você pode tornar sua aplicação implantável
[menor, mais rápida e mais confiável](#make-your-app-smaller-faster-and-more-reliable).
||||||| base_en
With a little extra work, you can make your deployable app
[smaller, faster, and more reliable](#make-your-app-smaller-faster-and-more-reliable).
=======
* **Compile to WebAssembly (`dart compile wasm`)**:
  Produces compact `.wasm` binary bytecode and a companion `.mjs` runtime
  loader for fast startup and consistent frame execution in modern browsers.
* **Compile to JavaScript (`webdev build` or `dart compile js`)**:
  Produces minified, tree-shaken `.dart.js` output compatible with all
  JavaScript-capable browsers.

With a few additional steps, you can make your deployable app
[smaller, faster, and more reliable](#make-your-app-smaller-faster-and-more-reliable).
>>>>>>> new_en

<<<<<<< pt
### Compile usando o webdev {:#compile-using-webdev}
||||||| base_en
### Compile using webdev
=======
### Compile to WebAssembly {:#compile-to-wasm}

Use the [`dart compile wasm`][dart-compile-wasm] command with the `-O2` flag
(or higher) to build optimized WebAssembly output:

```console
$ dart compile wasm -O2 web/main.dart -o build/web/main.wasm
```

This command generates `build/web/main.wasm`, the companion JavaScript runtime
`build/web/main.mjs`, and the source map `build/web/main.wasm.map`. Refer to
[WebAssembly compilation][wasm] for compiler optimization flags and setup
steps, and [Serve WebAssembly in production](#serving-wasm-in-production) for
server configuration.
>>>>>>> new_en

<<<<<<< pt
[Use o comando `webdev build`][build] para criar uma versão implantável
da sua aplicação. Esse comando converte seu código para JavaScript e salva
o resultado em `build/web/main.dart.js`. Você pode usar [qualquer opção
disponível para `dart compile js`](/tools/dart-compile#prod-compile-options)
com o `webdev build`.
||||||| base_en
[Use the `webdev build` command][build] to create a deployable version
of your app. This command converts your code to JavaScript and saves
the result as `build/web/main.dart.js`. You can use [any option
available to `dart compile js`](/tools/dart-compile#prod-compile-options)
with `webdev build`.
=======
### Compile to JavaScript with webdev {:#compile-using-webdev}

[Use the `webdev build` command][build] (or run
[`dart compile js`][dart-compile-js] directly) to create a deployable
JavaScript build of your app. The `webdev build` command compiles your code to
JavaScript and saves the result as `build/web/main.dart.js`. You can use
[any option available to `dart compile js`][dart-compile-js] with
`webdev build`.
>>>>>>> new_en

### Torne sua aplicação menor, mais rápida e mais confiável {:#make-your-app-smaller-faster-and-more-reliable}

<<<<<<< pt
Os passos a seguir são opcionais. Eles podem ajudar a tornar sua aplicação mais
confiável e responsiva.
||||||| base_en
The following steps are optional. They can help make your app more
reliable and responsive.
=======
The following practices help make your production web app smaller, faster, and
more secure:
>>>>>>> new_en

<<<<<<< pt
* [Use deferred loading para reduzir o tamanho inicial da sua aplicação](#use-deferred-loading-to-reduce-your-apps-initial-size)
* [Siga as melhores práticas para aplicações web](#follow-best-practices-for-web-apps)
* [Gerencie source maps e arquivos de build desnecessários](#manage-source-maps-and-unneeded-build-files)
||||||| base_en
* [Use deferred loading to reduce your app's initial size](#use-deferred-loading-to-reduce-your-apps-initial-size)
* [Follow best practices for web apps](#follow-best-practices-for-web-apps)
* [Manage source maps and unneeded build files](#manage-source-maps-and-unneeded-build-files)
=======
* [Use deferred loading to reduce initial download size][deferred-size]
* [Follow best practices for web apps][best-practices]
* [Manage source maps and unneeded build files][manage-source-maps]
>>>>>>> new_en

#### Use deferred loading para reduzir o tamanho inicial da sua aplicação {:#use-deferred-loading-to-reduce-your-apps-initial-size}

<<<<<<< pt
Você pode usar o suporte do Dart a deferred loading para
reduzir o tamanho inicial do download da sua aplicação.
Para mais detalhes, veja a parte do tour da linguagem sobre
[deferred loading](/language/libraries#lazily-loading-a-library).
||||||| base_en
You can use Dart's support for deferred loading to
reduce your app's initial download size.
For details, see the language tour's coverage of
[deferred loading](/language/libraries#lazily-loading-a-library).
=======
You can use Dart's support for deferred loading to split rarely used features
into separate modules loaded on demand.
For language syntax details, refer to the libraries guide on
[deferred loading][].
When compiling to WebAssembly, pass the `--enable-deferred-loading` flag and
configure a `loadDeferredModules` loader callback as shown in
[Wasm deferred loading][wasm-deferred-loading].
>>>>>>> new_en

#### Siga as melhores práticas para aplicações web {:#follow-best-practices-for-web-apps}

<<<<<<< pt
Os conselhos habituais para aplicações web valem para aplicações web Dart.
Aqui estão alguns recursos:
||||||| base_en
The usual advice for web apps applies to Dart web apps.
Here are a few resources:
=======
General web performance practices apply to Dart web apps:
>>>>>>> new_en

<<<<<<< pt
* [Fast load times](https://web.dev/fast/)
* [Web Fundamentals](https://developers.google.com/web/fundamentals/)
  (especialmente [Optimizing Content Efficiency](https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/))
* [Progressive Web Apps](https://web.dev/progressive-web-apps/)
* [Lighthouse](https://developers.google.com/web/tools/lighthouse/)
||||||| base_en
* [Fast load times](https://web.dev/fast/)
* [Web Fundamentals](https://developers.google.com/web/fundamentals/)
  (especially [Optimizing Content Efficiency](https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/))
* [Progressive Web Apps](https://web.dev/progressive-web-apps/)
* [Lighthouse](https://developers.google.com/web/tools/lighthouse/)
=======
* [Profile Wasm performance and footprint][profile-wasm]
* [Fast load times][fast-load-times]
* [Web Fundamentals][web-fundamentals]
  (especially [Optimizing Content Efficiency][content-efficiency])
* [Progressive Web Apps][pwa]
* [Lighthouse][lighthouse]
>>>>>>> new_en

<<<<<<< pt
#### Gerencie source maps e arquivos de build desnecessários {:#manage-source-maps-and-unneeded-build-files}
||||||| base_en
#### Manage source maps and unneeded build files
=======
#### Manage source maps and unneeded build files {:#manage-source-maps-and-unneeded-build-files}
>>>>>>> new_en

<<<<<<< pt
Por padrão, os compiladores web do Dart (`dart compile js` e `dart compile wasm`)
geram arquivos de source map (`.js.map` e `.wasm.map`)
junto com a saída compilada.
Embora os source maps sejam úteis para depuração,
servi-los em servidores web públicos pode expor informações sensíveis:
||||||| base_en
By default, Dart web compilers (`dart compile js` and `dart compile wasm`)
generate source map files (`.js.map` and `.wasm.map`)
alongside the compiled output.
While source maps are useful for debugging,
serving them on public web servers can expose sensitive information:
=======
By default, Dart web compilers (`dart compile js` and `dart compile wasm`)
generate source map files (`.js.map` and `.wasm.map`) alongside the compiled
output and embed a `sourceMappingURL` reference in the generated artifact.
While source maps are useful for debugging and symbolicating production stack
traces, serving them on public web servers can expose internal details:
>>>>>>> new_en

<<<<<<< pt
* **Símbolos e estrutura não minificados**:
  os source maps permitem que o DevTools do navegador reconstrua nomes originais de classes,
  nomes de funções e a lógica do código-fonte.
* **Caminhos de arquivos do desenvolvedor**:
  os source maps costumam incluir URIs absolutas do sistema de arquivos
  (como `file:///Users/...`) da máquina de build.
||||||| base_en
* **Unminified symbols and structure**:
  Source maps allow browser DevTools to reconstruct original class names,
  function names, and source logic.
* **Developer file paths**:
  Source maps often include absolute file system URIs
  (such as `file:///Users/...`) from the build machine.
=======
* **Unminified symbols and structure**:
  Source maps let browser DevTools reconstruct original class names,
  function names, and source logic.
* **Developer file paths**:
  Source maps can include file system URIs (such as `file:///Users/...`) from
  the build machine.
>>>>>>> new_en

:::warning
Para manter privados os nomes dos seus símbolos, a estrutura do código e os caminhos locais de build,
não faça deploy de arquivos de source map em hosts web públicos.
:::

<<<<<<< pt
Dependendo da sua estratégia de deploy,
você pode tratar os source maps de duas formas:
||||||| base_en
Depending on your deployment strategy,
you can handle source maps in one of two ways:
=======
Depending on your deployment strategy, handle source maps in one of two ways:
>>>>>>> new_en

* **Desabilite os source maps no momento do build**:
  se você não precisa de source maps para depuração em produção ou para relatório de erros,
  passe a flag `--no-source-maps` para o compilador:

  ```console
  $ dart compile wasm --no-source-maps -O2 -o build/main.wasm web/main.dart
  $ dart compile js --no-source-maps -O2 -o build/main.dart.js web/main.dart
  ```

<<<<<<< pt
* **Exclua ou remova os arquivos de map da hospedagem pública**:
  se você usa source maps em serviços privados de monitoramento de erros
  (como Sentry ou Bugsnag),
  mantenha os arquivos `.map` durante a compilação
  e envie-os diretamente para o seu serviço de monitoramento.
  Depois, exclua-os ou remova-os do seu servidor web público ou do diretório do CDN:
||||||| base_en
* **Exclude or strip map files from public hosting**:
  If you use source maps for private error monitoring services
  (such as Sentry or Bugsnag),
  keep the `.map` files during compilation
  and upload them directly to your monitoring service.
  Then, exclude or remove them from your public web server or CDN directory:
=======
* **Upload map files to error monitoring and exclude them from public hosting**:
  If you use an error-monitoring or crash-reporting service (such as Sentry or
  Bugsnag), keep the `.js.map` or `.wasm.map` files during compilation and
  upload them directly to your monitoring service to symbolicate production
  stack traces. Then exclude or remove them from your public web server or CDN
  directory:
>>>>>>> new_en

  ```console
  # From the root directory of your app:
  $ find build -type f \( -name "*.js.map" -o -name "*.wasm.map" \) -exec rm {} +
  ```

<<<<<<< pt
## Servindo sua aplicação {:#serving-your-app}

Você pode servir sua aplicação web Dart da mesma forma que serviria qualquer outra aplicação web.
Esta seção reúne dicas para servir aplicações web Dart,
além de recursos específicos do Dart para ajudar você a usar o GitHub Pages ou o Firebase
para servir sua aplicação.
||||||| base_en
## Serving your app

You can serve your Dart Web app just like you'd serve any other web app.
This section points to tips for serving Dart Web apps,
as well as Dart-specific resources to help you use GitHub Pages or Firebase
to serve your app.
=======
## Serve WebAssembly in production {:#serving-wasm-in-production}

When deploying a Dart application compiled with `dart compile wasm`, configure
your web server, CDN, and HTML bootstrap loader to maximize streaming
compilation speed and caching efficiency.

### Configure the `Content-Type: application/wasm` header {:#wasm-mime-type}

Web servers, CDNs, and object storage buckets must serve `.wasm` files with the
`application/wasm` MIME type (and `.mjs` files with `text/javascript` or
`application/javascript`):

* Browsers require `Content-Type: application/wasm` to execute
  `WebAssembly.compileStreaming()`.
* If the server returns `application/octet-stream` or omits the header,
  streaming compilation fails or falls back to waiting for the entire download
  to finish before compilation begins.

### Stream compilation and preload resources {:#streaming-compilation}

Avoid a sequential network waterfall (`index.html` → `main.mjs` → `main.wasm`).
Start fetching `main.wasm` and `main.mjs` in parallel from the HTML `<head>`
with high fetch priority, and pass the `fetch()` promise directly to
`compileStreaming()`:

```html title="index.html"
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Production Dart Wasm App</title>
  <!-- Preload the .mjs runtime and .wasm module in parallel -->
  <link rel="modulepreload" href="/main.mjs">
  <link rel="preload" href="/main.wasm" as="fetch" type="application/wasm" crossorigin="anonymous" fetchpriority="high">
</head>
<body>
  <div id="app"></div>
  <script type="module">
    import { compileStreaming } from '/main.mjs';

    const wasmResponsePromise = fetch('/main.wasm', { priority: 'high' });
    const compiledApp = await compileStreaming(wasmResponsePromise);
    const instantiatedApp = await compiledApp.instantiate({});
    instantiatedApp.invokeMain();
  </script>
</body>
</html>
```

### Enable Brotli and Gzip HTTP compression {:#http-compression}

* Pre-compress `.wasm` and `.mjs` artifacts during your release build by using
  Brotli (`brotli -q 11`) and Gzip (`gzip -9`) as a fallback
  (`Content-Encoding: br` or `gzip`).
* WasmGC binaries contain structured type sections and bytecode patterns that
  compress by 35–50% with Brotli, substantially reducing payload transfer and
  download time during initial page load.

### Configure caching and atomic deployments {:#wasm-caching}

* **Content-hashed filenames**:
  Fingerprint both outputs (for example, `main.a1b2c3d4.mjs` and
  `main.a1b2c3d4.wasm`) and serve them with
  `Cache-Control: public, max-age=31536000, immutable`. Serve `index.html` with
  `Cache-Control: no-cache`.
* **Atomic deployment**:
  Always deploy `main.mjs`, `main.wasm`, and any deferred
  `<name>_module<id>.wasm` chunks from the same build together.
  The generated `.mjs` file contains numeric import and export indices bound
  to that specific `.wasm` build. Mixing a cached `.mjs` file with a newly
  deployed `.wasm` binary causes instantiation errors.
* **V8 Wasm code caching**:
  When Chrome streams a `.wasm` resource over HTTPS with valid HTTP caching
  headers, V8 automatically caches the compiled native machine code on disk.
  Repeat visits skip Wasm compilation altogether.

### Provide a JavaScript fallback (`dart2js`) {:#js-fallback}

To support older browsers that lack WasmGC, JS String Builtins, or Phase 4
Exception Handling, provide a JavaScript fallback:

1. Build both targets in your release pipeline:

   ```console
   $ dart compile wasm -O2 web/main.dart -o site/main.wasm
   $ dart compile js -O2 web/main.dart -o site/main.dart.js
   ```

1. In your bootstrap script, attempt Wasm streaming compilation and fall back
   to loading `main.dart.js` if instantiation fails or the browser doesn't
   support the required Wasm features:

   ```js
   async function bootApp() {
     let instantiatedApp;
     try {
       const wasmPromise = fetch('/main.wasm');
       const { compileStreaming } = await import('/main.mjs');
       const compiledApp = await compileStreaming(wasmPromise);
       instantiatedApp = await compiledApp.instantiate({});
     } catch (wasmError) {
       console.warn('Wasm initialization failed; falling back to JS:', wasmError);
       const fallbackScript = document.createElement('script');
       fallbackScript.src = '/main.dart.js';
       document.head.appendChild(fallbackScript);
       return;
     }
     instantiatedApp.invokeMain();
   }

   bootApp();
   ```

## Serve your app {:#serving-your-app}

You can host your compiled Dart web app on any static web host or CDN, such as
GitHub Pages or Firebase Hosting.
>>>>>>> new_en

### GitHub Pages {:#github-pages}

<<<<<<< pt
Se sua aplicação não usa roteamento nem precisa de suporte do lado do servidor,
você pode servi-la usando o [GitHub Pages](https://pages.github.com/).
O pacote [peanut][] é
uma forma fácil de gerar automaticamente uma branch gh-pages para qualquer aplicação web Dart.
||||||| base_en
If your app doesn't use routing or require server-side support,
you can serve the app using [GitHub Pages](https://pages.github.com/).
The [peanut][] package is
an easy way to automatically produce a gh-pages branch for any Dart web app.
=======
If your app doesn't use server-side routing, you can serve the app by using
[GitHub Pages][gh-pages].
The [peanut][] package automatically produces a `gh-pages` branch for any Dart
web app.
>>>>>>> new_en

<<<<<<< pt
O [exemplo startup_namer](https://filiph.github.io/startup_namer/)
é hospedado com GitHub Pages.
Seus arquivos estão na branch **gh-pages** do
[repositório filiph/startup_namer](https://github.com/filiph/startup_namer)
e foram gerados com o [peanut.][peanut]
||||||| base_en
The [startup_namer example](https://filiph.github.io/startup_namer/)
is hosted using GitHub Pages.
Its files are in the **gh-pages** branch of the
[filiph/startup_namer repo](https://github.com/filiph/startup_namer)
and were built using [peanut.][peanut]
=======
The [startup_namer example][startup-namer]
is hosted on GitHub Pages.
Its files are in the `gh-pages` branch of the
[filiph/startup_namer repo][startup-namer-repo]
and were built with [peanut][].
>>>>>>> new_en

<<<<<<< pt
### Firebase {:#firebase}
||||||| base_en
### Firebase
=======
### Firebase

>>>>>>> new_en
{% comment %}
TODO: Give an example of how to deploy with Firebase, which originally was shown on https://dart.academy/build-a-real-time-chat-web-app-with-dart-angular-2-and-firebase-3/
{% endcomment %}

<<<<<<< pt
Para saber mais sobre deploy com Firebase, veja os seguintes recursos:
||||||| base_en
To learn more about deploying with Firebase, see the following resources:
=======
To learn more about deploying with Firebase, refer to the following resources:
>>>>>>> new_en

<<<<<<< pt
* A [documentação do Firebase Hosting](https://firebase.google.com/docs/hosting/)
  descreve como fazer deploy de aplicações web com Firebase.
* Na documentação do Firebase Hosting,
  [Configure Hosting Behavior](https://firebase.google.com/docs/hosting/full-config)
  aborda redirecionamentos, reescritas e mais.

||||||| base_en
* The [Firebase Hosting documentation](https://firebase.google.com/docs/hosting/)
  describes how to deploy web apps with Firebase.
* In the Firebase Hosting documentation,
  [Configure Hosting Behavior](https://firebase.google.com/docs/hosting/full-config)
  covers redirects, rewrites, and more.

=======
* The [Firebase Hosting documentation][firebase-hosting]
  describes how to deploy web apps with Firebase.
* In the Firebase Hosting documentation,
  [Configure Hosting Behavior][firebase-config]
  covers custom headers (such as `Content-Type` and `Cache-Control`),
  redirects, and rewrites.

[wasm]: /web/wasm
[profile-wasm]: /web/wasm#profile-wasm
[wasm-deferred-loading]: /web/wasm#deferred-loading
[dart-compile-wasm]: /tools/dart-compile#wasm
[dart-compile-js]: /tools/dart-compile#prod-compile-options
[deferred-size]: #use-deferred-loading-to-reduce-your-apps-initial-size
[best-practices]: #follow-best-practices-for-web-apps
[manage-source-maps]: #manage-source-maps-and-unneeded-build-files
[deferred loading]: /language/libraries#lazily-loading-a-library
[fast-load-times]: https://web.dev/fast/
[web-fundamentals]: https://developers.google.com/web/fundamentals/
[content-efficiency]: https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/
[pwa]: https://web.dev/progressive-web-apps/
[lighthouse]: https://developers.google.com/web/tools/lighthouse/
[gh-pages]: https://pages.github.com/
[startup-namer]: https://filiph.github.io/startup_namer/
[startup-namer-repo]: https://github.com/filiph/startup_namer
[firebase-hosting]: https://firebase.google.com/docs/hosting/
[firebase-config]: https://firebase.google.com/docs/hosting/full-config
>>>>>>> new_en
[build]: /tools/webdev#build
[peanut]: {{site.pub-pkg}}/peanut
