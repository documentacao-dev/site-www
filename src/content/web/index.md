---
ia-translate: true
title: Plataforma web
shortTitle: Web
description: Recursos para desenvolver aplicações web em Dart.
showToc: false
---

O Dart oferece suporte à web como uma de suas [plataformas][platforms] principais.
Para desenvolvimento, o compilador de JavaScript do Dart para desenvolvimento
(`ddc`) oferece um ciclo rápido de editar e atualizar.
Para o [deploy][deployment] em produção, você pode compilar Dart para
[WebAssembly (Wasm)][wasm] (`dart2wasm`), para inicialização rápida e execução
consistente de frames em navegadores modernos, ou para JavaScript minificado
(`dart2js`).

Além dos compiladores,
a plataforma web do Dart oferece [bibliotecas principais][core libraries],
acesso ao [Document Object Model (DOM)][DOM] por meio do [`package:web`][]
e [interoperabilidade para chamar JavaScript][interop] a partir do Dart.

Você também pode combinar a web do Dart com um framework de nível mais alto.
Dá para criar apps multiplataforma para web, mobile e desktop usando o
[Flutter][] e o [Flutter web][], ou usar o [Jaspr][] para criar sites baseados
em HTML. A plataforma web do Dart dá suporte ao Flutter web, ao Jaspr
e a outros frameworks web do Dart.

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
    alt="aplicativo Flutter Gallery executando em um navegador web">
  <figcaption>Flutter Gallery, executando em um navegador web</figcaption>
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
