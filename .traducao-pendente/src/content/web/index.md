---
ia-translate: true
title: Plataforma web
shortTitle: Web
description: Recursos para desenvolver aplicações web em Dart.
showToc: false
---

<<<<<<< pt
O Dart oferece suporte à web como uma de suas [plataformas][platforms] principais.
Há compiladores de Dart para JavaScript disponíveis tanto para desenvolvimento
(com um ciclo rápido de editar e atualizar)
quanto para produção
(com foco no tamanho e na velocidade do código).
Para builds de produção, você também pode compilar Dart para
[WebAssembly][wasm] (`dart compile wasm`).
||||||| base_en
Dart supports the web as one of its core [platforms][].
Dart-to-JavaScript compilers are available for both development
(with a quick edit-refresh cycle)
and production
(with a focus on code size and speed).
For production builds, you can also compile Dart to
[WebAssembly][wasm] (`dart compile wasm`).
=======
Dart supports the web as one of its core [platforms][].
For development, the Dart development JavaScript compiler (`ddc`) provides a
quick edit-refresh cycle.
For production [deployment][], you can compile Dart to
[WebAssembly (Wasm)][wasm] (`dart2wasm`) for fast startup and consistent frame
execution in modern browsers, or to minified JavaScript (`dart2js`).
>>>>>>> new_en

<<<<<<< pt
Além dos compiladores,
a plataforma web do Dart oferece [bibliotecas principais][core libraries],
acesso ao [DOM (Document Object Model)][DOM]
e [interoperabilidade para chamar JavaScript][interop] a partir do Dart.
||||||| base_en
In addition to compilers,
the Dart web platform provides [core libraries][],
access to the [DOM (Document Object Model)][DOM],
and [interoperability for calling JavaScript][interop] from Dart.
=======
In addition to compilers,
the Dart web platform provides [core libraries][],
access to the [Document Object Model (DOM)][DOM] through [`package:web`][],
and [interoperability for calling JavaScript][interop] from Dart.
>>>>>>> new_en

<<<<<<< pt
Você tem a opção de usar o Dart para web com um framework de nível mais alto.
Muitas aplicações que funcionam na web e também em mobile ou desktop são construídas
com o [Flutter][] e o suporte ao [Flutter web][].
Você também pode usar o [Jaspr][] para criar sites HTML rápidos e dinâmicos.
O suporte ao Flutter web, o Jaspr
e outros frameworks web para Dart são baseados na plataforma web do Dart.
||||||| base_en
You have the option of using Dart web with a higher-level framework.
Many apps that support web plus mobile or desktop are built
using [Flutter][] and [Flutter web][] support.
You can also use [Jaspr][] to build fast and dynamic HTML-based websites.
Flutter web support, Jaspr,
and other web frameworks for Dart are powered by the Dart web platform.
=======
You can also pair Dart web with a higher-level framework.
You can build multi-platform apps for web, mobile, and desktop
by using [Flutter][] and [Flutter web][],
or use [Jaspr][] to build HTML-based websites.
The Dart web platform powers Flutter web, Jaspr,
and other Dart web frameworks.
>>>>>>> new_en

<div class="side-by-side">
<div class="centered-rows">
<p class="">
  <a href="/web/get-started" class="filled-button large-button">Crie uma aplicação web com Dart</a>
</p>
</div>
<div class="centered-rows">
<figure>
  <img 
    src="/assets/img/flutter-gallery.jpg"
<<<<<<< pt
    alt="captura de tela do Flutter Gallery">
  <figcaption>Flutter Gallery, executando em um navegador web</figcaption>
||||||| base_en
    alt="screenshot of Flutter Gallery">
  <figcaption>Flutter Gallery, running in a web browser</figcaption>
=======
    alt="Flutter Gallery app running in a web browser">
  <figcaption>Flutter Gallery, running in a web browser</figcaption>
>>>>>>> new_en
</figure>
</div>
</div>

[platforms]: /overview#platform
[deployment]: /web/deployment
[wasm]: /web/wasm
[core libraries]: /libraries#web-platform-libraries
[DOM]: /web/get-started
[`package:web`]: /interop/js-interop/package-web
[Flutter]: {{site.flutter}}
[Flutter web]: {{site.flutter}}/web
[Jaspr]: https://jaspr.site
[interop]: /interop/js-interop
