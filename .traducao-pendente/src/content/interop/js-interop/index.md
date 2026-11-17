---
ia-translate: true
title: Interoperabilidade com JavaScript
shortTitle: JS interop
description: Integre código JavaScript na sua aplicação web Dart.
nextpage:
  url: /interop/js-interop/usage
  title: Uso
---

<<<<<<< pt
Integre bibliotecas e APIs JavaScript na sua aplicação web Dart sem atrito.
||||||| base_en
Seamlessly integrate JavaScript libraries and APIs into your Dart web app.
=======
Integrate JavaScript libraries and APIs into Dart web apps.
>>>>>>> new_en

## Visão geral {: #overview }

<<<<<<< pt
A [plataforma web Dart][Dart web platform] fornece ferramentas poderosas para
chamar JavaScript a partir do Dart e vice-versa, e permite aproveitar o vasto
ecossistema JavaScript sem sair do seu código Dart.
||||||| base_en
The [Dart web platform][] provides powerful tools to
call JavaScript from Dart and vice-versa and allows you to leverage the vast
JavaScript ecosystem without leaving your Dart code.
=======
The [Dart web platform][] provides tools to call JavaScript from Dart and Dart
from JavaScript, bringing the JavaScript ecosystem directly to Dart code.
>>>>>>> new_en

<<<<<<< pt
Esta página é o ponto central para aprender sobre interoperabilidade com JavaScript
no Dart. Você vai encontrar recursos para começar, guias de uso detalhados e
informações sobre a biblioteca `dart:js_interop` mais recente. Seja se você quer
usar uma biblioteca JavaScript específica, seja se quer interagir com APIs do navegador,
este é o lugar para começar.
||||||| base_en
This page provides a central hub for learning about JavaScript interoperability
in Dart. You'll find resources to get you started, detailed usage guides, and
information on the latest `dart:js_interop` library. Whether you're looking to
use a specific JavaScript library, or interact with browser APIs, this is the
place to start.
=======
Find getting-started resources, usage guides, and `dart:js_interop` library
documentation for calling JavaScript libraries, interacting with browser APIs,
and compiling web apps to [WebAssembly (Wasm)][wasm].
>>>>>>> new_en

Comece com o JS interop:
  * [Começando com interop JavaScript][Get started with JavaScript interop]
  * [Como fazer mock de objetos de interop JavaScript][How to mock JavaScript interop objects]

Revise os guias de referência:
  * [Referência de uso][Usage reference]
  * [Referência de tipos JS][JS types reference]

Interaja com o navegador:
  * [`package:web` e migração][`package:web` and migration]

## WebAssembly (`dart2wasm`) support {: #wasm-support }

When compiling Dart web apps to [WebAssembly][wasm] (`dart compile wasm`),
keep these interoperability and performance practices in mind:

  * **Use `dart:js_interop` and `package:web`**:
    Deprecated legacy web and interop libraries (`dart:html`, `dart:js`,
    `dart:js_util`, and `package:js`) are unsupported on Wasm targets.
  * **Minimize high-frequency calls across the Wasm and JS boundary**:
    In performance-critical code or tight loops, keep computation in Dart or
    batch values rather than making repeated interop calls per iteration.
  * **Find Wasm-compatible packages**:
    Use the [`wasm-ready`][] filter on [pub.dev][] to verify that packages use
    `dart:js_interop` and `package:web`.

[Dart web platform]: /web
[wasm]: /web/wasm
[`wasm-ready`]: {{site.pub-pkg}}?q=is%3Awasm-ready
[pub.dev]: {{site.pub}}
[Usage reference]: /interop/js-interop/usage
[JS types reference]: /interop/js-interop/js-types
[`package:web` and migration]: /interop/js-interop/package-web
[Get started with JavaScript interop]: /interop/js-interop/start
[How to mock JavaScript interop objects]: /interop/js-interop/mock

<a id="next-generation-js-interop" aria-hidden="true"></a>
<a id="deprecated-features" aria-hidden="true"></a>

## Recursos adicionais {: #additional-resources }

<<<<<<< pt
Bibliotecas anteriores de interoperabilidade com JavaScript:
  * [JS interop anterior][Past JS interop]
||||||| base_en
Previous JavaScript interop libraries:
  * [Past JS interop]
=======
Explore previous JavaScript interop libraries:
  * [Past JS interop]
>>>>>>> new_en

<<<<<<< pt
Documentação adicional sobre interoperabilidade com JavaScript:
  * [Referência da API `dart:js_interop`][`dart:js_interop` API reference]
  * [Referência da API `dart:js_interop_unsafe`][`dart:js_interop_unsafe` API reference]
||||||| base_en
Additional documentation on JavaScript interop:
  * [`dart:js_interop` API reference]
  * [`dart:js_interop_unsafe` API reference]
=======
Explore the API reference documentation:
  * [`dart:js_interop` API reference]
  * [`dart:js_interop_unsafe` API reference]
>>>>>>> new_en

[Past JS interop]: /interop/js-interop/past-js-interop
[`dart:js_interop` API reference]: {{site.dart-api}}/dart-js_interop/
[`dart:js_interop_unsafe` API reference]: {{site.dart-api}}/dart-js_interop_unsafe/
