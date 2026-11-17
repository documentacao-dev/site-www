---
ia-translate: true
title: "Anunciando o Dart 3.14"
description: >-
  Fechando o ciclo do fluxo de trabalho do Dart com migrações automáticas do SDK,
  WebAssembly mais rápido e um DartPad reprojetado.
publishDate: 2026-11-11
author: conooi
image: images/dart3-14-cover.webp
category: releases
layout: blog
---

<DashImage src="images/dart3-14.webp" alt="Chef Dash tirando do forno uma torta recém-assada com o logo do Dart, ao lado de números 3.14 brilhantes." caption="Anunciando o Dart 3.14" />

Estamos muito animados para anunciar o Dart 3.14!

Em sintonia com o nosso release pi,
o Dart 3.14 fecha o ciclo completo do fluxo de trabalho do desenvolvedor:
desde experimentar ideias no navegador
até criar apps multiplataforma
e atualizar seus pacotes para a próxima versão.
Você pode testar ideias e pacotes do `pub.dev` em um DartPad reprojetado,
migrar automaticamente sua base de código entre versões do SDK com `dart migrate`,
acelerar o WebAssembly com SIMD em hardware,
executar módulos Wasm fora do navegador
e chamar APIs nativas das plataformas com suporte estável ao FFIgen e ao JNIgen.

Então, [atualize o Dart](/get-dart)
ou execute [`flutter upgrade`](https://docs.flutter.dev/install/upgrade)
e acompanhe enquanto exploramos as novidades do Dart 3.14!
Quando quiser ver as novidades do framework de UI,
confira o post complementar
[Novidades do Flutter 3.50](https://flutter.dev/blog/whats-new-in-flutter-3-50).

## Atualizações de ferramentas {:#tools-updates}

### Atualizações automáticas de pacotes com a ferramenta `dart migrate` {:#automated-package-upgrades-with-the-dart-migrate-tool}

Atualizar um pacote Dart para uma versão mais nova do SDK geralmente envolve
ajustar a restrição de SDK e atualizar o código
para seguir as novas recomendações de estilo
ou evitar quebras com a versão que chega.
No entanto, descobrir quais lints habilitar
ou quais mudanças de código são necessárias em cada release pode ser complicado.

Para tirar o trabalho de adivinhação da atualização entre releases,
a nova ferramenta `dart migrate` automatiza esse fluxo
avançando um pacote uma versão por vez.
Para cada versão, ela faz o seguinte:

1. Prepara seu pacote aplicando as correções do `dart fix`
   que precisam ser feitas antes de subir a versão.
1. Aumenta o limite inferior da restrição de SDK no seu `pubspec.yaml`.

Depois que seu pacote estiver na nova versão,
você pode, opcionalmente, limpá-lo aplicando correções
que usam os novos recursos ou seguem as novas recomendações de estilo.

Por exemplo, em um pacote com restrição de SDK `^3.12.0`:

```dart
class WeakPasswordException implements Exception {}

void checkPassword(final String password, final int minLength) {
  if (password.length < minLength) {
    throw WeakPasswordException();
  }
}
```

A ferramenta prepara o código removendo `final` dos parâmetros,
o que é um erro de compilação no Dart 3.13.
Ela aumenta a restrição de SDK no pubspec
e, em seguida, faz a limpeza adotando a nova sintaxe de corpo com ponto e vírgula
para classes vazias:

```dart
class WeakPasswordException implements Exception;

void checkPassword(String password, int minLength) {
  if (password.length < minLength) {
    throw WeakPasswordException();
  }
}
```

Quando terminar de executar,
a ferramenta migrate mostra um resumo das edições de cada etapa,
junto com as correções opcionais de limpeza que seu pacote ainda pode aplicar:

```text
my_package:
  3.12.0 -> 3.13.0:
    Preparatory changes:
      2 changes made in 1 file.

      my_package/lib/password.dart
        avoid_final_parameters • 2 changes

    SDK constraint:
      Bumped ^3.12.0 -> ^3.13.0

Optional cleanup fixes can modernize your code further:

  my_package: 1 change in 1 file
    empty_container_bodies • 1 change

To preview them, run 'dart pub get' and then 'dart migrate --dry-run --step=cleanup' on the same packages.
```

Para visualizar as mudanças de um pacote, use a flag `--dry-run`:

```bash
dart migrate --dry-run
```

Para aplicar as mudanças propostas, use a flag `--apply`:

```bash
dart migrate --apply
```

Para bases de código maiores, em que você pode querer revisar as correções
antes ou depois de subir a restrição de SDK,
é possível executar etapas específicas com a flag `--step`:

```bash
# Only run preparatory fixes without bumping the constraint
dart migrate --apply --step=prepare

# After applying the preparatory fixes, bump the constraint and apply cleanup fixes
dart migrate --apply --step=bump,cleanup
```

Por padrão, ao executar a ferramenta, o pacote sobe uma versão minor.
Para migrar várias versões em uma única execução, use a flag `--target-sdk`:

```bash
dart migrate --apply --target-sdk=3.14.0
```

:::note
`dart migrate` só oferece suporte a pacotes
cuja restrição de SDK exige Dart 3.0 ou superior.
:::

**Saiba mais:** [documentação do Dart migrate](/tools/dart-migrate)

### Melhorias de desempenho do Analysis Server {:#analysis-server-performance-improvements}

Junto com atualizações de SDK mais suaves,
manter sua IDE responsiva e acelerar fluxos de trabalho com agentes de codificação de IA
conforme seu workspace cresce é uma prioridade máxima para nossa equipe de ferramentas.
Várias melhorias de desempenho foram incorporadas ao Dart Analysis Server:

- **Descoberta de arquivos mais rápida:**
  Acelera requisições como **Find References**,
  especialmente quando o workspace inclui muitos Analysis Contexts.
- **Tarefas menos bloqueantes:**
  Tarefas que antes bloqueavam outras ações, como a formatação de código,
  agora bloqueiam menos.
- **Inicialização do servidor mais rápida:**
  Reduz o tempo de inicialização,
  inclusive quando o analysis server reinicia a análise
  por causa de mudanças na configuração de pacotes e nas opções de análise.
- **Requisições `documentColor` mais rápidas:**
  Acelera a requisição `documentColor`,
  que libera muitas outras requisições do analysis server enquanto um arquivo é editado.
- **Raízes de plugins do analyzer com escopo:**
  Restringe as raízes de análise dos plugins às raízes de contexto dos plugins,
  o que faz os plugins do analyzer analisarem mais rápido.

### Atualizações do pub {:#pub-updates}

#### Suporte a cache ETag para resolução de dependências mais rápida {:#etag-cache-support-for-faster-dependency-resolution}

A resolução de dependências com cache aquecido no `dart pub` agora é mais rápida
e usa bem menos banda em projetos médios e grandes.
Ao resolver dependências com `dart pub get`, `upgrade` ou `add`,
o `pub` consulta o `pub.dev` para obter a lista de versões de cada pacote
para verificar versões recém-publicadas, retratações e avisos de segurança,
o que antes significava baixar de novo megabytes de metadados de pacotes
mesmo quando nada havia mudado.

Agora, o `dart pub` armazena o `ETag` do servidor
junto com as listas de pacotes no seu cache local do pub
e envia requisições condicionais `If-None-Match` ao resolver com cache aquecido.
Quando a lista de um pacote não mudou,
o `pub.dev` responde com `304 Not Modified` e um corpo vazio,
e o `pub` reaproveita diretamente a lista em cache, sem baixá-la de novo.
Em um projeto Flutter com 144 dependências,
isso elimina cerca de 1,5 MB de downloads repetidos de listas de versões,
acelerando a resolução com cache aquecido,
especialmente em conexões mais lentas ou com maior latência.

### Beta do DartPad reprojetado {:#re-engineered-dartpad-beta}

Estamos animados para compartilhar uma versão beta do
[DartPad](https://dartpad.dev) reprojetado,
que facilita e acelera a experimentação com Dart e Flutter
direto no seu navegador.

Ele é construído sobre o `package:dartpad`,
que compila o compilador do Dart, o analyzer e o cliente do pub
para WebAssembly e os executa localmente em um Web Worker.
Isso significa que o DartPad agora analisa e compila seu código diretamente no navegador,
então você recebe feedback mais rápido, sem esperar por um servidor remoto.
Ele também traz suporte completo ao Language Server Protocol (LSP):
você tem o mesmo code completion, documentação ao passar o mouse, go-to-definition
e quick fixes que já conhece da sua IDE.

Um recurso empolgante dessa nova stack é que
ela permite importar pacotes do `pub.dev`,
então você não fica mais limitado a uma lista de permissões escolhida à mão.
Traga as bibliotecas que usaria em um projeto real e teste-as na hora.
Além disso, o DartPad agora oferece suporte a vários arquivos,
para que você possa organizar widgets e modelos de dados
da mesma forma que faria em um app real.

O novo DartPad mostra a versatilidade do Dart como linguagem full-stack,
que pode rodar na sua máquina, no servidor ou em um navegador web.
Como essas ferramentas principais são escritas em Dart,
compilá-las para WebAssembly torna possível
executar todo o fluxo de trabalho diretamente no navegador.

**Experimente:** [dartpad.dev](https://dartpad.dev)

## Atualizações da plataforma web {:#web-platform-updates}

### Exceções do WebAssembly padronizadas para navegadores e runtimes Wasm {:#standardized-webassembly-exceptions-for-browsers-and-wasm-runtimes}

Apps Dart em WebAssembly agora rodam em mais navegadores
e em ambientes Wasm fora do navegador, sem configuração extra.
No navegador, o `dart2wasm` agora emite, por padrão, as
[instruções de tratamento de exceção `try_table`](https://github.com/dart-lang/sdk/issues/54394)
do WebAssembly, já finalizadas, e contorna
[problemas de compilação em streaming no Safari 26.5 e versões anteriores](https://github.com/dart-lang/sdk/issues/63543),
habilitando o WebAssembly no Chrome 137+, no Safari 26.2+ e no Firefox 147+.

Fora do navegador, a adoção do `try_table` elimina
a última dependência do compilador de wrappers de exceção do JavaScript
em `dart compile wasm --standalone`
(contribuição de [Simon Binder](https://github.com/simolus3), membro da comunidade).
Isso gera binários `.wasm` padrão
que executam diretamente em runtimes Wasm, como o [Wasmtime](https://wasmtime.dev/),
sem precisar de um host JavaScript,
o que facilita muito rodar Dart em edge workers, sistemas de plugins
e ambientes Wasm do lado do servidor.
Para experimentar o WASI e o WebAssembly Component Model,
explore o pacote [`wasm_tools`](https://pub.dev/packages/wasm_tools)
da comunidade de Simon Binder, no [GitHub](https://github.com/simolus3/wasm.dart).

**Saiba mais:** [documentação do WebAssembly](/web/wasm)

### SIMD de 128 bits do WebAssembly em hardware {:#hardware-128-bit-webassembly-simd}

Junto com o suporte mais amplo nos runtimes,
o desempenho do WebAssembly recebe um grande impulso nesta versão.
Graças a mais de 60 contribuições ao SDK feitas por
[Modestas Valauskas](https://github.com/modulovalue), membro da comunidade,
o `dart2wasm` agora compila `Int32x4`, `Float32x4`, `Float64x2`
e suas views de listas de typed data diretamente para
[instruções WebAssembly SIMD de 128 bits em hardware (`v128`)](https://github.com/dart-lang/sdk/issues/64170),
junto com operações de `Int32x4` expandidas e otimizadas em `dart:typed_data`
nas plataformas nativas,
chegando a até 4x de ganho em benchmarks de SIMD nativo e WebAssembly.

**Saiba mais:** [documentação da biblioteca `dart:typed_data`](https://api.dart.dev/dart-typed_data/)

### Remoção de bibliotecas web legadas com `--no-deprecated-js-interop` {:#legacy-web-library-removal-with-no-deprecated-js-interop}

Conforme a adoção do WebAssembly cresce e continuamos modernizando
a plataforma web do Dart, as bibliotecas legadas de interoperabilidade com web e JavaScript
(`dart:html`, `dart:js`, `dart:js_util`, `package:js`
e outras bibliotecas `dart:*` de navegador relacionadas)
estão descontinuadas e programadas para remoção do SDK do Dart
em uma versão futura.
Sabemos que migrações levam tempo, mas a mudança para `package:web` e `dart:js_interop`
traz um futuro muito mais robusto e padronizado para o Dart na web,
incluindo compatibilidade total com WebAssembly.

Para ajudar você a preparar o código com antecedência,
`dart compile js` (`dart2js`) e `ddc` agora oferecem suporte a
[`--no-deprecated-js-interop`](https://github.com/dart-lang/sdk/issues/63919),
que rejeita importações diretas ou transitivas dessas bibliotecas em tempo de compilação
e define as condições de ambiente `dart.library.*` como `false`
nos imports condicionais.

Execute `dart compile js --no-deprecated-js-interop`
(ou `flutter build web --no-deprecated-js-interop`
no [Flutter 3.50](https://flutter.dev/blog/whats-new-in-flutter-3-50))
nos seus pacotes e apps hoje,
e migre os usos restantes para [`dart:js_interop`](/interop/js-interop)
e [`package:web`](/interop/js-interop/package-web).

**Saiba mais:** [documentação de JS interop](/interop/js-interop) e
[Migrando para o package:web](/interop/js-interop/package-web)

## Atualizações do engine e do runtime {:#core-engine-and-runtime-updates}

### Comparações rápidas de intervalos em `dart:typed_data` {:#fast-range-comparisons-in-dart-typed_data}

Comparar fatias de buffers de bytes em código sensível a desempenho
não exige mais alocar `sublistView`s nem iterar elemento por elemento
(por exemplo, com o `ListEquality` do `package:collection`).
Agora, `dart:typed_data` inclui um método de extensão `rangeEquals`
em todas as listas de typed data inteiras
(`Uint8List`, `Int8List`, `Uint8ClampedList`, `Uint16List`, `Int16List`,
`Uint32List`, `Int32List`, `Uint64List`, `Int64List`)
e em `ByteData`:

```dart
import 'dart:typed_data';

void main() {
  final packet = Uint8List.fromList([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A]);
  final pngMagic = Uint8List.fromList([0x89, 0x50, 0x4E, 0x47]);

  // Compare packet[0..4] against pngMagic[0..4] without allocating views:
  if (packet.rangeEquals(0, 4, pngMagic)) {
    print('PNG header matched');
  }
}
```

Por baixo dos panos, o `rangeEquals` é traduzido para `memcmp` na Dart VM,
para acessos diretos a arrays Wasm no `dart2wasm` (com chunks de 32 bits para `ByteData`)
e para loops enxutos sobre typed arrays no JS,
oferecendo comparações rápidas e sem alocação em todos os targets.

**Saiba mais:** [documentação da biblioteca `dart:typed_data`](https://api.dart.dev/dart-typed_data/)

## Interoperabilidade nativa direta {:#direct-native-interoperability}

Além do runtime principal,
chamar bibliotecas nativas das plataformas a partir do Dart agora está pronto para produção.
Com o Dart 3.14, o [FFIgen](https://pub.dev/packages/ffigen) para Objective-C
e o [JNIgen](https://pub.dev/packages/jnigen) são **estáveis**!

Em vez de escrever o boilerplate manual de platform channels,
você pode usar o FFIgen e o JNIgen para gerar automaticamente
bindings em Dart idiomáticos e com tipos seguros, e chamar
APIs de Objective-C, Java e Kotlin diretamente do Dart.
A estabilidade é resultado de anos de design, iteração e feedback,
com foco em reduzir o atrito de construir pacotes Dart e plugins do Flutter.
Em breve, compartilharemos no [blog do Flutter](https://flutter.dev/blog)
um mergulho mais profundo sobre como escolher a melhor abordagem de interop
para o seu caso de uso.

**Saiba mais:** [documentação de interoperabilidade nativa](https://docs.flutter.dev/interop)

## Olhando para o futuro: roadmap da linguagem {:#looking-ahead-language-roadmap}

A equipe continua avançando em `this` promotion e extensões estáticas.
Fique de olho para saber mais sobre elas em uma versão futura!

**Saiba mais:** [funil de funcionalidades da linguagem Dart](https://github.com/dart-lang/language/projects/1)

## Comunidade {:#community}

### Um processo estruturado de RFC para o Dart {:#a-structured-rfc-process-for-dart}

Contribuidores da comunidade têm um papel importante em todo release do Dart,
incluindo as melhorias do WebAssembly standalone e do SIMD em hardware
presentes no Dart 3.14.
À medida que o ecossistema Dart continua crescendo,
queremos facilitar ainda mais o acompanhamento e a contribuição
nas principais decisões do projeto.
O projeto Dart está adotando uma nova abordagem estruturada
para propor e avaliar mudanças grandes que exigem consenso da equipe:
essas mudanças agora exigem a escrita de uma Request for Comments (RFC).

Tanto membros da equipe quanto contribuidores da comunidade
podem usar esse processo para pedir feedback e aprovação formal
da equipe do Dart e da liderança do projeto.
Ele também busca dar visibilidade clara sobre o que a equipe está trabalhando,
reunindo discussões de design e registros de decisões em um único lugar.

**Saiba mais:** [repositório de RFCs do Dart](https://dart.googlesource.com/rfc)

## Experimente o Dart 3.14 {:#take-dart-3-14-for-a-spin}

Nosso release pi fecha o ciclo do Dart:
conecta o seu fluxo, desde testar pacotes do `pub.dev` no navegador
com o DartPad,
até entregar apps nativos e WebAssembly de alto desempenho,
passando por automatizar atualizações de versão com `dart migrate`.
Por baixo dos panos, o compilador, o analyzer e o cliente `pub` do próprio Dart
agora compilam para WebAssembly, para rodar o Dart no navegador.

Esse ciclo completo também se estende à comunidade do Dart.
Os principais destaques do Dart 3.14 foram impulsionados diretamente por contribuidores de código aberto,
e nosso novo processo de RFC traz mais transparência
sobre como grandes mudanças de engenharia são projetadas, revisadas
e compartilhadas em todo o projeto Dart.
Obrigado a todos que contribuíram com código, abriram issues e compartilharam feedback
durante este release!

Pronto para mergulhar?
Execute [`flutter upgrade`](https://docs.flutter.dev/install/upgrade)
ou [baixe o SDK mais recente do Dart](/get-dart),
experimente o novo preview beta do [DartPad](https://dartpad.dev)
e compartilhe seu feedback no nosso
[gerenciador de issues do GitHub](https://github.com/dart-lang/sdk/issues).
Obrigado por construir conosco!

**Saiba mais:** [changelog do SDK do Dart](https://github.com/dart-lang/sdk/blob/main/CHANGELOG.md#3140)
