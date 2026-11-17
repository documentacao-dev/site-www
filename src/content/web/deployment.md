---
ia-translate: true
title: Deploy na web
description: >-
  Aprenda a compilar e servir sua aplicação web Dart para deploy em produção.
---

O deploy de uma aplicação web Dart funciona como o deploy de qualquer outra aplicação web.
Você compila seu código Dart para WebAssembly de produção (`dart compile wasm`) ou
para JavaScript (`dart compile js` ou `webdev build`), otimiza os assets gerados e
os serve a partir de um servidor web ou de uma rede de distribuição de conteúdo (CDN).

## Compile sua aplicação {:#compiling-to-javascript}

Para deploys de produção, você pode compilar sua aplicação web Dart para
[WebAssembly (Wasm)][wasm] (`dart2wasm`), para JavaScript (`dart2js`) ou para ambos
(com JavaScript como fallback para navegadores mais antigos):

* **Compile para WebAssembly (`dart compile wasm`)**:
  produz um binário de bytecode `.wasm` compacto e um loader de runtime `.mjs`
  complementar, para inicialização rápida e execução consistente dos frames em
  navegadores modernos.
* **Compile para JavaScript (`webdev build` ou `dart compile js`)**:
  produz uma saída `.dart.js` minificada e com tree shaking, compatível com todos
  os navegadores que suportam JavaScript.

Com alguns passos adicionais, você pode tornar sua aplicação implantável
[menor, mais rápida e mais confiável](#make-your-app-smaller-faster-and-more-reliable).

### Compile para WebAssembly {:#compile-to-wasm}

Use o comando [`dart compile wasm`][dart-compile-wasm] com a flag `-O2` (ou superior)
para gerar a saída otimizada em WebAssembly:

```console
$ dart compile wasm -O2 web/main.dart -o build/web/main.wasm
```

Esse comando gera `build/web/main.wasm`, o runtime JavaScript complementar
`build/web/main.mjs` e o source map `build/web/main.wasm.map`. Consulte
[Compilação para WebAssembly][wasm] para as flags de otimização do compilador e os
passos de configuração, e [Sirva WebAssembly em produção](#serving-wasm-in-production)
para a configuração do servidor.

### Compile para JavaScript com webdev {:#compile-using-webdev}

[Use o comando `webdev build`][build] (ou execute
[`dart compile js`][dart-compile-js] diretamente) para criar uma versão implantável
em JavaScript da sua aplicação. O comando `webdev build` compila seu código para
JavaScript e salva o resultado em `build/web/main.dart.js`. Você pode usar
[qualquer opção disponível para `dart compile js`][dart-compile-js] com o `webdev build`.

### Torne sua aplicação menor, mais rápida e mais confiável {:#make-your-app-smaller-faster-and-more-reliable}

As práticas a seguir ajudam a tornar sua aplicação web de produção menor, mais rápida
e mais segura:

* [Use deferred loading para reduzir o tamanho inicial do download][deferred-size]
* [Siga as melhores práticas para aplicações web][best-practices]
* [Gerencie source maps e arquivos de build desnecessários][manage-source-maps]

#### Use deferred loading para reduzir o tamanho inicial da sua aplicação {:#use-deferred-loading-to-reduce-your-apps-initial-size}

Você pode usar o suporte do Dart a deferred loading para dividir recursos pouco usados
em módulos separados, carregados sob demanda. Para detalhes de sintaxe da linguagem,
consulte o guia de bibliotecas sobre [deferred loading][]. Ao compilar para WebAssembly,
passe a flag `--enable-deferred-loading` e configure um callback de carregamento
`loadDeferredModules`, como mostrado em [deferred loading no Wasm][wasm-deferred-loading].

#### Siga as melhores práticas para aplicações web {:#follow-best-practices-for-web-apps}

Práticas gerais de performance web se aplicam às aplicações web Dart:

* [Faça o profiling da performance e do footprint do Wasm][profile-wasm]
* [Tempos de carregamento rápidos][fast-load-times]
* [Web Fundamentals][web-fundamentals]
  (especialmente [Otimização da eficiência de conteúdo][content-efficiency])
* [Progressive Web Apps][pwa]
* [Lighthouse][lighthouse]

#### Gerencie source maps e arquivos de build desnecessários {:#manage-source-maps-and-unneeded-build-files}

Por padrão, os compiladores web do Dart (`dart compile js` e `dart compile wasm`)
geram arquivos de source map (`.js.map` e `.wasm.map`) junto com a saída compilada
e incluem uma referência `sourceMappingURL` no artefato gerado.
Embora os source maps sejam úteis para depuração e para simbolizar stack traces de
produção, servi-los em servidores web públicos pode expor detalhes internos:

* **Símbolos e estrutura não minificados**:
  os source maps permitem que o DevTools do navegador reconstrua nomes originais de classes,
  nomes de funções e a lógica do código-fonte.
* **Caminhos de arquivos do desenvolvedor**:
  os source maps podem incluir URIs do sistema de arquivos (como `file:///Users/...`)
  da máquina de build.

:::warning
Para manter privados os nomes dos seus símbolos, a estrutura do código e os caminhos locais de build,
não faça deploy de arquivos de source map em hosts web públicos.
:::

Dependendo da sua estratégia de deploy, trate os source maps de uma das duas formas:

* **Desabilite os source maps no momento do build**:
  se você não precisa de source maps para depuração em produção ou para relatório de erros,
  passe a flag `--no-source-maps` para o compilador:

  ```console
  $ dart compile wasm --no-source-maps -O2 -o build/main.wasm web/main.dart
  $ dart compile js --no-source-maps -O2 -o build/main.dart.js web/main.dart
  ```

* **Envie os arquivos de map para o monitoramento de erros e exclua-os da hospedagem pública**:
  se você usa um serviço de monitoramento de erros ou de relatório de crashes (como
  Sentry ou Bugsnag), mantenha os arquivos `.js.map` ou `.wasm.map` durante a compilação
  e envie-os diretamente para o seu serviço de monitoramento, para simbolizar stack traces
  de produção. Depois, exclua-os ou remova-os do seu servidor web público ou do diretório do CDN:

  ```console
  # From the root directory of your app:
  $ find build -type f \( -name "*.js.map" -o -name "*.wasm.map" \) -exec rm {} +
  ```

## Sirva sua aplicação {:#serving-your-app}

Você pode hospedar sua aplicação web Dart compilada em qualquer host web estático ou
CDN, como GitHub Pages ou Firebase Hosting.

## Sirva WebAssembly em produção {:#serving-wasm-in-production}

Ao fazer deploy de uma aplicação Dart compilada com `dart compile wasm`, configure seu
servidor web, CDN e o loader de bootstrap do HTML para maximizar a velocidade de
compilação em streaming e a eficiência do cache.

### Configure o header `Content-Type: application/wasm` {:#wasm-mime-type}

Servidores web, CDNs e buckets de armazenamento de objetos precisam servir arquivos
`.wasm` com o MIME type `application/wasm` (e arquivos `.mjs` com `text/javascript` ou
`application/javascript`):

* Os navegadores exigem `Content-Type: application/wasm` para executar
  `WebAssembly.compileStreaming()`.
* Se o servidor retornar `application/octet-stream` ou omitir o header, a compilação
  em streaming falha ou passa a esperar o download inteiro terminar antes de começar
  a compilação.

### Compilação em streaming e preload de recursos {:#streaming-compilation}

Evite uma cascata sequencial de rede (`index.html` → `main.mjs` → `main.wasm`).
Comece a buscar `main.wasm` e `main.mjs` em paralelo a partir do `<head>` do HTML,
com alta prioridade de fetch, e passe a promise do `fetch()` diretamente para
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

### Ative a compressão HTTP com Brotli e Gzip {:#http-compression}

* Pré-comprima os artefatos `.wasm` e `.mjs` durante o build de release usando
  Brotli (`brotli -q 11`) e Gzip (`gzip -9`) como fallback
  (`Content-Encoding: br` ou `gzip`).
* Binários WasmGC contêm seções de tipos estruturadas e padrões de bytecode que são
  comprimidos em 35–50% com Brotli, reduzindo bastante a transferência do payload e
  o tempo de download no carregamento inicial da página.

### Configure cache e deploys atômicos {:#wasm-caching}

* **Nomes de arquivo com hash de conteúdo**:
  gere um hash no nome das duas saídas (por exemplo, `main.a1b2c3d4.mjs` e
  `main.a1b2c3d4.wasm`) e sirva-as com
  `Cache-Control: public, max-age=31536000, immutable`. Sirva `index.html` com
  `Cache-Control: no-cache`.
* **Deploy atômico**:
  sempre faça deploy de `main.mjs`, `main.wasm` e de quaisquer chunks deferred
  `<name>_module<id>.wasm` do mesmo build, juntos. O arquivo `.mjs` gerado contém
  índices numéricos de import e export vinculados a esse build específico do `.wasm`.
  Misturar um `.mjs` em cache com um binário `.wasm` recém-publicado causa erros de
  instanciação.
* **Cache de código Wasm no V8**:
  quando o Chrome transmite um recurso `.wasm` via HTTPS com headers de cache HTTP
  válidos, o V8 armazena automaticamente em disco o código de máquina nativo compilado.
  Visitas seguintes pulam a compilação do Wasm por completo.

### Forneça um fallback em JavaScript (`dart2js`) {:#js-fallback}

Para oferecer suporte a navegadores mais antigos que não têm WasmGC, JS String Builtins
ou Phase 4 Exception Handling, forneça um fallback em JavaScript:

1. Compile os dois alvos no seu pipeline de release:

   ```console
   $ dart compile wasm -O2 web/main.dart -o site/main.wasm
   $ dart compile js -O2 web/main.dart -o site/main.dart.js
   ```

1. No seu script de bootstrap, tente a compilação em streaming do Wasm e faça fallback
   para carregar `main.dart.js` se a instanciação falhar ou se o navegador não suportar
   os recursos necessários do Wasm:

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

### GitHub Pages {:#github-pages}

Se sua aplicação não usa roteamento do lado do servidor, você pode servi-la usando o
[GitHub Pages][gh-pages]. O pacote [peanut][] gera automaticamente uma branch
`gh-pages` para qualquer aplicação web Dart.

O [exemplo startup_namer][startup-namer]
é hospedado no GitHub Pages.
Seus arquivos estão na branch `gh-pages` do
[repositório filiph/startup_namer][startup-namer-repo]
e foram gerados com o [peanut][].

### Firebase {:#firebase}
{% comment %}
TODO: Give an example of how to deploy with Firebase, which originally was shown on https://dart.academy/build-a-real-time-chat-web-app-with-dart-angular-2-and-firebase-3/
{% endcomment %}

Para saber mais sobre deploy com Firebase, consulte os seguintes recursos:

* A [documentação do Firebase Hosting][firebase-hosting]
  descreve como fazer deploy de aplicações web com Firebase.
* Na documentação do Firebase Hosting,
  [Configure Hosting Behavior][firebase-config]
  aborda cabeçalhos personalizados (como `Content-Type` e `Cache-Control`),
  redirecionamentos, reescritas e mais.

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
[build]: /tools/webdev#build
[peanut]: {{site.pub-pkg}}/peanut
