---
ia-translate: true
title: Interoperabilidade com JavaScript
shortTitle: JS interop
description: Integre código JavaScript na sua aplicação web Dart.
nextpage:
  url: /interop/js-interop/usage
  title: Uso
---

Integre bibliotecas e APIs JavaScript em aplicações web Dart.

## Visão geral {: #overview }

A [plataforma web Dart][Dart web platform] fornece ferramentas para
chamar JavaScript a partir do Dart e Dart a partir do JavaScript, trazendo
o ecossistema JavaScript diretamente para o código Dart.

Encontre recursos para começar, guias de uso e a documentação da biblioteca
`dart:js_interop` para chamar bibliotecas JavaScript, interagir com APIs do
navegador e compilar aplicações web para [WebAssembly (Wasm)][wasm].

Comece com o JS interop:
  * [Começando com interop JavaScript][Get started with JavaScript interop]
  * [Como fazer mock de objetos de interop JavaScript][How to mock JavaScript interop objects]

Revise os guias de referência:
  * [Referência de uso][Usage reference]
  * [Referência de tipos JS][JS types reference]

Interaja com o navegador:
  * [`package:web` e migração][`package:web` and migration]

## Suporte a WebAssembly (`dart2wasm`) {: #wasm-support }

Ao compilar aplicações web Dart para [WebAssembly][wasm] (`dart compile wasm`),
tenha em mente estas práticas de interoperabilidade e desempenho:

  * **Use `dart:js_interop` e `package:web`**:
    as bibliotecas web e de interop legadas e descontinuadas (`dart:html`, `dart:js`,
    `dart:js_util` e `package:js`) não têm suporte nos alvos Wasm.
  * **Minimize chamadas de alta frequência entre a fronteira Wasm e JS**:
    em código sensível a desempenho ou em loops críticos, mantenha o cálculo no Dart
    ou agrupe os valores, em vez de fazer chamadas de interop repetidas a cada iteração.
  * **Encontre pacotes compatíveis com Wasm**:
    use o filtro [`wasm-ready`][] no [pub.dev][] para verificar se os pacotes usam
    `dart:js_interop` e `package:web`.

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

Explore as bibliotecas anteriores de interoperabilidade com JavaScript:
  * [JS interop anterior][Past JS interop]

Explore a documentação de referência da API:
  * [Referência da API `dart:js_interop`][`dart:js_interop` API reference]
  * [Referência da API `dart:js_interop_unsafe`][`dart:js_interop_unsafe` API reference]

[Past JS interop]: /interop/js-interop/past-js-interop
[`dart:js_interop` API reference]: {{site.dart-api}}/dart-js_interop/
[`dart:js_interop_unsafe` API reference]: {{site.dart-api}}/dart-js_interop_unsafe/
