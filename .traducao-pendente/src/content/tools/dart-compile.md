---
ia-translate: true
title: dart compile
description: Ferramenta de linha de comando para compilar código-fonte Dart.
---

Este guia descreve como usar o comando `dart compile`
para compilar um programa Dart para uma plataforma de destino.

## Visão geral {:#overview}

:::note
<<<<<<< pt
Se o seu pacote ou qualquer uma de suas dependências tiver [build hooks](/tools/hooks),
você deve usar o comando [`dart build`](/tools/dart-build).
Os comandos `dart compile exe` e `dart compile aot-snapshot` não
executam build hooks e falharão se houver hooks presentes.
||||||| base_en
If your package or any of its dependencies has [build hooks](/tools/hooks),
you must use the [`dart build`](/tools/dart-build) command.
The `dart compile exe` and `dart compile aot-snapshot` commands don't
run build hooks, and will fail if hooks are present.
=======
If your package or any of its dependencies has [build hooks][],
you must use the [`dart build cli`][] command.
The `dart compile exe` and `dart compile aot-snapshot` commands don't
run build hooks and fail if hooks are present.
>>>>>>> new_en
:::

<<<<<<< pt
Use o comando `dart compile` para compilar
um programa Dart para uma [plataforma de destino](/overview#platform).
A saída, que você especifica usando um subcomando, pode
incluir um [Dart runtime][] ou ser um _módulo_
(também conhecido como _snapshot_).
||||||| base_en
Use the `dart compile` command to compile
a Dart program to a [target platform](/overview#platform).
The output—which you specify using a subcommand—can 
either include a [Dart runtime][] or be a _module_
(also known as a _snapshot_).
=======
Use the `dart compile` command to compile
a Dart program to a [target platform][].
The output—which you specify with a subcommand—can
either include a [Dart runtime][] or be a _module_
(also known as a _snapshot_).
>>>>>>> new_en

{% render 'tools/dart-tool-note.md' %}

<<<<<<< pt
Aqui está um exemplo de uso do subcomando `exe`
para produzir um arquivo executável autocontido (`myapp.exe`):
||||||| base_en
Here's an example of using the `exe` subcommand
to produce a self-contained executable file (`myapp.exe`):
=======
The following example uses the `exe` subcommand
to produce a self-contained executable file (`myapp.exe`):
>>>>>>> new_en

```console
$ dart compile exe bin/myapp.dart
```

The output is similar to the following:

```console
Generated: /Users/me/myapp/bin/myapp.exe
```

<<<<<<< pt
O próximo exemplo usa o subcomando `aot-snapshot` para
produzir um módulo compilado ahead-of-time (AOT) (`myapp.aot`).
Em seguida, ele usa o [comando `dartaotruntime`](/tools/dartaotruntime)
(que fornece um [Dart runtime][])
para executar o módulo AOT:
||||||| base_en
The next example uses the `aot-snapshot` subcommand to
produce an ahead-of-time (AOT) compiled module (`myapp.aot`).
It then uses the [`dartaotruntime` command](/tools/dartaotruntime)
(which provides a [Dart runtime][])
to run the AOT module:
=======
The next example uses the `aot-snapshot` subcommand to
produce an ahead-of-time (AOT) compiled module (`myapp.aot`):
>>>>>>> new_en

```console
$ dart compile aot-snapshot bin/myapp.dart
```

The output is similar to the following:

```console
Generated: /Users/me/myapp/bin/myapp.aot
```

Use the [`dartaotruntime` command][dartaotruntime]
(which provides a [Dart runtime][])
to run the AOT module:

```console
$ dartaotruntime bin/myapp.aot
```

Para especificar o caminho do arquivo de saída,
use a opção `-o` ou `--output`:

```console
$ dart compile exe bin/myapp.dart -o bin/runme
```

<<<<<<< pt
Para mais opções e informações de uso,
execute `dart compile [<subcommand>] --help`:
||||||| base_en
For more options and usage information,
run `dart compile [<subcommand>] --help`:
=======
For more options and usage information,
run `dart compile SUBCOMMAND --help`,
replacing `SUBCOMMAND` with a subcommand such as `exe` or `wasm`:
>>>>>>> new_en

```console
$ dart compile exe --help
```

:::note
<<<<<<< pt
Você não precisa compilar programas Dart antes de executá-los.
Em vez disso, você pode usar o [comando `dart run`][dart-run],
que usa o compilador JIT (just-in-time) da Dart VM, um
recurso especialmente útil durante o desenvolvimento.
Para mais informações sobre compilação AOT e JIT,
veja a [discussão sobre plataformas](/overview#platform).
||||||| base_en
You don't need to compile Dart programs before running them.
Instead, you can use the [`dart run` command][dart-run],
which uses the Dart VM's JIT (just-in-time) compiler—a 
feature that's especially useful during development.
For more information on AOT and JIT compilation,
see the [platforms discussion](/overview#platform).
=======
You don't need to compile Dart programs before running them.
Instead, you can use the [`dart run` command][dart-run],
which uses the Dart VM's just-in-time (JIT) compiler—a
feature that's especially useful during development.
For more information on AOT and JIT compilation,
refer to the [platforms discussion][target platform].
>>>>>>> new_en
:::

<<<<<<< pt
Consulte o exemplo [native_app][] para ver um exemplo simples de uso do `dart compile`
para compilar uma aplicação nativa,
seguido de exemplos de execução da aplicação.
||||||| base_en
Refer to the [native_app][] sample for a simple example of using `dart compile`
to compile a native app, 
followed by examples of running the app.
=======
Refer to the [native_app][] sample for a simple example of using `dart compile`
to compile a native app,
followed by examples of running the app.
>>>>>>> new_en

[build hooks]: /tools/hooks
[`dart build cli`]: /tools/dart-build
[target platform]: /overview#platform
[dartaotruntime]: /tools/dartaotruntime
[native_app]: {{site.repo.dart.samples}}/tree/main/native_app
[dart-run]: /tools/dart-run

## Subcomandos {:#subcommands}

A tabela a seguir mostra os subcomandos do `dart compile`.

<table class="table table-striped nowrap">
  <tr>
<<<<<<< pt
    <th> Subcomando </th> <th> Saída </th> <th> Mais informações </th>
||||||| base_en
    <th> Subcommand </th> <th> Output </th> <th> More information </th>
=======
    <th> Subcommand </th> <th> Output </th> <th> Description </th>
>>>>>>> new_en
  </tr>
  <tr>
<<<<<<< pt
    <td> <code>exe</code> </td>
    <td> Executável <span style="white-space: nowrap">autocontido</span> </td>
    <td> Um arquivo executável independente e específico da arquitetura, contendo o código-fonte
      compilado para código de máquina e um pequeno <a href="/overview#runtime">Dart runtime</a>.
      <br><em><a href="#exe">Saiba mais.</a></em>
||||||| base_en
    <td> <code>exe</code> </td>
    <td> <span style="white-space: nowrap">Self-contained</span> executable </td>
    <td> A standalone, architecture-specific executable file containing the source code
      compiled to machine code and a small <a href="/overview#runtime">Dart runtime</a>.
      <br><em><a href="#exe">Learn more.</a></em>
=======
    <td> <a href="#exe"><code>exe</code></a> </td>
    <td> <span style="white-space: nowrap">Self-contained</span> executable </td>
    <td> A standalone, architecture-specific executable file containing the source code
      compiled to machine code and a small <a href="/overview#runtime">Dart runtime</a>.
>>>>>>> new_en
    </td>
  </tr>
  <tr>
<<<<<<< pt
    <td style="white-space: nowrap"> <code>aot-snapshot</code> </td>
    <td style="white-space: nowrap"> Módulo AOT </td>
    <td> Um arquivo específico da arquitetura contendo o código-fonte
      compilado para código de máquina, mas <b>sem Dart runtime</b>.
      <br><em><a href="#aot-snapshot">Saiba mais.</a></em>
||||||| base_en
    <td style="white-space: nowrap"> <code>aot-snapshot</code> </td>
    <td style="white-space: nowrap"> AOT module </td>
    <td> An architecture-specific file containing the source code
      compiled to machine code, but <b>no Dart runtime</b>.
      <br><em><a href="#aot-snapshot">Learn more.</a></em>
=======
    <td style="white-space: nowrap"> <a href="#aot-snapshot"><code>aot-snapshot</code></a> </td>
    <td style="white-space: nowrap"> AOT module </td>
    <td> An architecture-specific file containing the source code
      compiled to machine code, without a Dart runtime.
>>>>>>> new_en
    </td>
  </tr>
  <tr>
<<<<<<< pt
    <td> <code>jit-snapshot</code> </td>
    <td> Módulo JIT </td>
    <td> Um arquivo específico da arquitetura com
      uma representação intermediária de todo o código-fonte,
      mais uma representação otimizada do código-fonte
      que foi executado durante uma execução de treinamento do programa.
      O código compilado com JIT pode ter desempenho de pico mais rápido que o código AOT
      se os dados de treinamento forem bons.
      <br><em><a href="#jit-snapshot">Saiba mais.</a></em>
||||||| base_en
    <td> <code>jit-snapshot</code> </td>
    <td> JIT module </td>
    <td> An architecture-specific file with
      an intermediate representation of all source code,
      plus an optimized representation of the source code
      that executed during a training run of the program.
      JIT-compiled code can have faster peak performance than AOT code
      if the training data is good.
      <br><em><a href="#jit-snapshot">Learn more.</a></em>
=======
    <td> <a href="#jit-snapshot"><code>jit-snapshot</code></a> </td>
    <td> JIT module </td>
    <td> An architecture-specific file with
      an intermediate representation of all source code,
      plus an optimized representation of the source code
      that executed during a training run of the program.
      JIT-compiled code can have faster peak performance than AOT code
      if the training data is good.
>>>>>>> new_en
    </td>
  </tr>
  <tr>
<<<<<<< pt
    <td> <code>kernel</code> </td>
    <td> Módulo Kernel </td>
    <td> Uma <a href="{{site.repo.dart.sdk}}/blob/main/pkg/kernel/binary.md">representação intermediária</a>
      portável do código-fonte.
      <br><em><a href="#kernel">Saiba mais.</a></em>
||||||| base_en
    <td> <code>kernel</code> </td>
    <td> Kernel module </td>
    <td> A portable,
      <a href="{{site.repo.dart.sdk}}/blob/main/pkg/kernel/binary.md">intermediate representation</a>
      of the source code.
      <br><em><a href="#kernel">Learn more.</a></em>
=======
    <td> <a href="#kernel"><code>kernel</code></a> </td>
    <td> Kernel module </td>
    <td> A portable,
      <a href="{{site.repo.dart.sdk}}/blob/main/pkg/kernel/binary.md">intermediate representation</a>
      of the source code.
>>>>>>> new_en
    </td>
  </tr>
  <tr>
    <td> <a href="#js"><code>js</code></a> </td>
    <td> JavaScript </td>
<<<<<<< pt
    <td> Um arquivo JavaScript implantável (<code>.js</code>)
      e um source map (<code>.js.map</code>),
      compilados a partir do código-fonte.
      <br><em><a href="#js">Saiba mais.</a></em>
||||||| base_en
    <td> A deployable JavaScript file (<code>.js</code>)
      and source map (<code>.js.map</code>), 
      compiled from the source code.
      <br><em><a href="#js">Learn more.</a></em>
=======
    <td> A deployable JavaScript file (<code>.js</code>)
      and source map (<code>.js.map</code>),
      compiled from the source code.
>>>>>>> new_en
    </td>
  </tr>
  <tr>
    <td> <a href="#wasm"><code>wasm</code></a> </td>
    <td> WebAssembly </td>
<<<<<<< pt
    <td> Um módulo WebAssembly (<code>.wasm</code>),
      um runtime JavaScript complementar (<code>.mjs</code>)
      e um source map (<code>.wasm.map</code>).
      <br><em><a href="#wasm">Saiba mais.</a></em>
||||||| base_en
    <td> A WebAssembly module (<code>.wasm</code>),
      companion JavaScript runtime (<code>.mjs</code>),
      and source map (<code>.wasm.map</code>).
      <br><em><a href="#wasm">Learn more.</a></em>
=======
    <td> A WebAssembly module (<code>.wasm</code>),
      companion JavaScript runtime (<code>.mjs</code>),
      and source map (<code>.wasm.map</code>).
>>>>>>> new_en
    </td>
  </tr>
</table>


## Tipos de saída {:#types-of-output}

As seções a seguir detalham cada tipo de saída
que o `dart compile` pode produzir.


<<<<<<< pt
### Executáveis autocontidos (exe) {:#exe}
||||||| base_en
### Self-contained executables (exe) {:#exe}
=======
### Self-contained executables (`exe`) {:#exe}
>>>>>>> new_en

<<<<<<< pt
O subcomando `exe` produz um executável independente para
Windows, macOS ou Linux.
Um **executável independente** é código de máquina nativo compilado a partir
do arquivo Dart especificado e suas dependências,
mais um pequeno [Dart runtime][] que cuida da
verificação de tipos e da coleta de lixo.
||||||| base_en
The `exe` subcommand produces a standalone executable for
Windows, macOS, or Linux.
A **standalone executable** is native machine code that's compiled from
the specified Dart file and its dependencies,
plus a small [Dart runtime][] that handles
type checking and garbage collection.
=======
The `exe` subcommand produces a standalone executable for
Windows, macOS, or Linux.
A _standalone executable_ is native machine code that's compiled from
the specified Dart file and its dependencies,
plus a small [Dart runtime][] that handles
type checking and garbage collection.
>>>>>>> new_en

Você pode distribuir e executar o arquivo de saída como faria
com qualquer outro arquivo executável.

Compile sua aplicação e defina o arquivo de saída:

```console
$ dart compile exe bin/myapp.dart -o /tmp/myapp
```

Quando bem-sucedido, este comando gera a seguinte saída:

```console
Generated: /tmp/myapp
```

<<<<<<< pt
Execute sua aplicação compilada a partir do diretório `/tmp`:
||||||| base_en
Run your compiled app from the `/tmp` directory:
=======
Run your compiled executable:
>>>>>>> new_en

```console
$ /tmp/myapp
```

<a id="cross-compilation" aria-hidden="true"></a>

#### Cross-compilation {: #cross-compilation-exe }

:::version-note
O suporte à cross-compilation para Linux ARM64 e x64 foi introduzido no Dart 3.8.

O suporte para Linux ARM e RISCV64 foi introduzido no Dart 3.9.
:::

A tabela a seguir mostra quais sistemas operacionais host de 64 bits suportam
cross-compilation para quais alvos:

{% assign y = '<span class="material-symbols system-support" title="Supported" aria-label="Supported">done</span>' %}

| SO host de 64 bits | Linux ARM | Linux ARM64 | Linux RISCV64 | Linux x64 |
|----------------|-----------|-------------|---------------|-----------|
| Linux          |   {{y}}   |    {{y}}    |    {{y}}      |    {{y}}  |
| macOS          |   {{y}}   |    {{y}}    |    {{y}}      |    {{y}}  |
| Windows        |   {{y}}   |    {{y}}    |    {{y}}      |    {{y}}  |

{:.table .table-striped .nowrap}

Para usar a cross-compilation, inclua as seguintes flags:

`--target-os=linux`
<<<<<<< pt
: O sistema operacional de destino para o executável compilado.
  Atualmente, apenas o sistema operacional Linux é suportado.
||||||| base_en
: The target operating system for the compiled executable.
  Only the Linux operating system is supported at this time.
=======
: The target operating system for the compiled executable.
  Cross-compilation supports only Linux as a target operating system.
>>>>>>> new_en

`--target-arch=value`
<<<<<<< pt
: A arquitetura de destino para o executável compilado.
  O valor dessa flag pode ser:
||||||| base_en
: The target architecture for the compiled executable.
  The value for this flag can be:
=======
: The target architecture for the compiled executable.
  The value for this flag can be one of the following architectures:
>>>>>>> new_en

  - `arm`: processador ARM de 32 bits
  - `arm64`: processador ARM de 64 bits
  - `riscv64`: processador RISC-V de 64 bits (RV64GC)
  - `x64`: processador x86-64

O comando a seguir demonstra como fazer a cross-compilation de um
executável independente para um sistema Linux de 64 bits:

```console
$ dart compile exe \
  --target-os=linux \
  --target-arch=x64 \
  hello.dart
```

Internamente, este comando baixa binários adicionais do Dart SDK e
os armazena em cache no diretório `~/.dart`.

Aqui está um exemplo de saída com a flag `--verbose` especificada no
comando:

```console
Downloading https://storage.googleapis.com/dart-archive/channels/dev/signed/hash/...4864.../sdk/gen_snapshot_macos_arm64_linux_x64...
Downloading https://storage.googleapis.com/dart-archive/channels/dev/raw/hash/...64e44.../sdk/dartaotruntime_linux_x64...
Specializing Platform getters for target OS linux.
Generating AOT kernel dill.
Compiling /tmp/hello.dart to /tmp/hello.exe using format Kind.exe:
Generating AOT snapshot. path/to/dir/.dart/3.8.0-265.0.dev/gen_snapshot_macos_arm64_linux_x64 []
Generating executable.
Marking binary executable.
Generated: /tmp/hello.exe
```

#### Assinatura {:#signing}

Executáveis criados com `dart compile exe`
oferecem suporte a assinatura no macOS e no Windows.

<<<<<<< pt
Para saber mais sobre assinatura de código específica de cada plataforma,
consulte a documentação dos sistemas operacionais:
||||||| base_en
To learn more about platform-specific code signing,
see the platform documentation for those operating systems:
=======
To learn more about platform-specific code signing,
refer to the platform documentation for those operating systems:
>>>>>>> new_en

* [Documentação do `SignTool.exe`][`SignTool.exe` documentation] (Windows)
* [Guia de Code Signing da Apple][Apple Code Signing guide]

[`SignTool.exe` documentation]: https://docs.microsoft.com/dotnet/framework/tools/signtool-exe
[Apple Code Signing guide]: {{site.apple-dev}}/support/code-signing/

#### Limitações conhecidas {: #known-limitations }

O subcomando `exe` tem as seguintes limitações conhecidas:

<<<<<<< pt
* Não há suporte para `dart:mirrors` e `dart:developer`.
  Para uma lista completa das bibliotecas principais que você pode usar,
  consulte as tabelas de bibliotecas [Multi-platform][] e [Native platform][].
||||||| base_en
* No support for `dart:mirrors` and `dart:developer`.
  For a complete list of the core libraries you can use,
  reference the [Multi-platform][] and [Native platform][] library tables.
=======
* No support for `dart:mirrors` and `dart:developer`.
  For a complete list of the core libraries you can use,
  refer to the [Multi-platform][] and [Native platform][] library tables.
>>>>>>> new_en

<<<<<<< pt
* A cross-compilation é suportada, mas o SO de destino é limitado ao Linux.
  Para saber mais, confira [Cross-compilation][].
||||||| base_en
* Cross-compilation is supported, but the target OS is limited to Linux.
  To learn more, check out [Cross-compilation][].
=======
* Cross-compilation is supported, but the target OS is limited to Linux.
  To learn more, refer to [Cross-compilation][].
>>>>>>> new_en

[Multi-platform]: /libraries#multi-platform-libraries
[Native platform]: /libraries#native-platform-libraries
[Cross-compilation]: #cross-compilation-exe

<<<<<<< pt
### Módulos AOT (aot-snapshot) {:#aot-snapshot}
||||||| base_en
### AOT modules (aot-snapshot) {:#aot-snapshot}
=======
### AOT modules (`aot-snapshot`) {:#aot-snapshot}
>>>>>>> new_en

Use módulos AOT para reduzir os requisitos de espaço em disco ao distribuir
várias aplicações de linha de comando. O subcomando `aot-snapshot` produz um
arquivo de saída específico para a arquitetura atual na qual você compila
sua aplicação.

Por exemplo, se você usar macOS para criar um arquivo `.aot`,
então esse arquivo só poderá ser executado no macOS.
O Dart oferece suporte a módulos AOT no Windows, macOS e Linux.

Compile sua aplicação e defina o arquivo de saída:

```console
$ dart compile aot-snapshot bin/myapp.dart
```

Quando bem-sucedido, este comando gera a seguinte saída:

```console
Generated: /Users/me/myapp/bin/myapp.aot
```

<<<<<<< pt
Execute sua aplicação compilada a partir do diretório `/bin`:
||||||| base_en
Run your compiled app from the `/bin` directory:
=======
Run your compiled app from your project root directory:
>>>>>>> new_en

```console
$ dartaotruntime bin/myapp.aot
```

<<<<<<< pt
Para saber mais, consulte a
[documentação do `dartaotruntime`](/tools/dartaotruntime).
||||||| base_en
To learn more, see the
[`dartaotruntime` documentation](/tools/dartaotruntime).
=======
To learn more, refer to the
[`dartaotruntime` documentation][dartaotruntime].
>>>>>>> new_en

{% comment %}
  TODO: Get info from https://github.com/dart-lang/sdk/wiki/Snapshots
{% endcomment %}

#### Cross-compilation {: #cross-compilation-aot }

<<<<<<< pt
O suporte à cross-compilation do subcomando `aot-snapshot`
é o mesmo disponível para o subcomando `exe`.
Para mais informações, consulte
[Executáveis autocontidos (exe)][cross-compile-exe].
||||||| base_en
Cross-compilation support for the `aot-snapshot` subcommand
is the same as what's available for the `exe` subcommand.
For more information, see
[Self-contained executables (exe)][cross-compile-exe].
=======
Cross-compilation support for the `aot-snapshot` subcommand
is the same as what's available for the `exe` subcommand.
For more information, refer to
[Self-contained executables (`exe`)][cross-compile-exe].
>>>>>>> new_en

[cross-compile-exe]: #cross-compilation-exe

#### Limitações conhecidas {: #known-limitations-aot }

<<<<<<< pt
O subcomando `aot-snapshot` tem as mesmas limitações
do subcomando `exe`. Para mais informações, consulte
[Executáveis autocontidos (exe)][known-limitations-exe]
||||||| base_en
The `aot-snapshot` subcommand has the same limitations
as the `exe` subcommand. For more information, see
[Self-contained executables (exe)][known-limitations-exe]
=======
The `aot-snapshot` subcommand has the same limitations
as the `exe` subcommand. For more information, refer to
[Self-contained executables (`exe`)][known-limitations-exe].
>>>>>>> new_en

[known-limitations-exe]: #known-limitations

<<<<<<< pt
### Módulos JIT (jit-snapshot) {:#jit-snapshot}
||||||| base_en
### JIT modules (jit-snapshot) {:#jit-snapshot}
=======
### JIT modules (`jit-snapshot`) {:#jit-snapshot}
>>>>>>> new_en

Módulos JIT incluem todas as classes analisadas e o código compilado gerado
durante uma execução de treinamento de um programa.

Compile a JIT module from a training run:

```console
$ dart compile jit-snapshot bin/myapp.dart
```

The output is similar to the following:

```console
Compiling bin/myapp.dart to jit-snapshot file bin/myapp.jit.
Hello world!
```

Run the compiled JIT module:

```console
$ dart run bin/myapp.jit
```

The output is similar to the following:

```console
Hello world!
```

<<<<<<< pt
Ao executar a partir de um módulo de aplicação,
a Dart VM não precisa analisar ou compilar classes e funções que
já foram usadas durante a execução de treinamento,
então a VM começa a executar o código do usuário mais cedo.
||||||| base_en
When running from an application module,
the Dart VM doesn't need to parse or compile classes and functions that
were already used during the training run,
so the VM starts running user code sooner.
=======
When running from an application module,
the Dart VM doesn't need to parse or compile classes and functions that
were already used during the training run,
so the VM starts running your code sooner.
>>>>>>> new_en

<<<<<<< pt
Esses módulos são específicos da arquitetura,
ao contrário dos módulos produzidos com o
[subcomando `kernel`](#kernel).
||||||| base_en
These modules are architecture specific,
unlike modules produced using the
[`kernel` subcommand](#kernel).
=======
These modules are architecture-specific,
unlike modules produced by using the
[`kernel` subcommand][kernel-subcommand].
>>>>>>> new_en


<<<<<<< pt
### Módulos portáveis (kernel) {:#kernel}
||||||| base_en
### Portable modules (kernel) {:#kernel}
=======
### Portable modules (`kernel`) {:#kernel}
>>>>>>> new_en

<<<<<<< pt
Use o subcomando `kernel` para empacotar uma aplicação em um
único arquivo portável que
pode ser executado em todos os sistemas operacionais e arquiteturas de CPU.
Um módulo kernel contém uma forma binária da árvore de sintaxe abstrata
([Kernel AST][]) de um programa Dart.
||||||| base_en
Use the `kernel` subcommand to package up an app into a
single, portable file that
can be run on all operating systems and CPU architectures.
A kernel module contains a binary form of the abstract syntax tree
([Kernel AST][]) for a Dart program.
=======
Use the `kernel` subcommand to package an app into a
single, portable file that
runs on all operating systems and CPU architectures.
A kernel module contains a binary form of the abstract syntax tree
([Kernel AST][]) for a Dart program.
>>>>>>> new_en

<<<<<<< pt
Aqui está um exemplo de criação e execução de um módulo kernel:
||||||| base_en
Here's an example of creating and running a kernel module:
=======
Create a kernel module:
>>>>>>> new_en

```console
$ dart compile kernel bin/myapp.dart
```

The output is similar to the following:

```console
Compiling bin/myapp.dart to kernel file bin/myapp.dill.
```

Run the compiled kernel module:

```console
$ dart run bin/myapp.dill
```

Embora os módulos kernel tenham um tempo de inicialização menor que o do código Dart,
eles podem ter uma inicialização bem mais lenta do que os formatos de saída AOT específicos da arquitetura.

[kernel-subcommand]: #kernel
[Kernel AST]: {{site.repo.dart.sdk}}/blob/main/pkg/kernel/README.md


### JavaScript (`js`) {:#js}

O subcomando `js` compila código Dart para JavaScript implantável.
Por padrão, o compilador gera tanto o arquivo JavaScript (`.js`)
quanto um arquivo de source map (`.js.map`).

:::note
<<<<<<< pt
Use a [ferramenta `webdev`][webdev] em vez de executar diretamente o
compilador de Dart para JavaScript.
||||||| base_en
Use the [`webdev` tool][webdev] rather than running the 
Dart-to-JavaScript compiler directly.
=======
Use the [`webdev` tool][webdev] rather than running the
Dart-to-JavaScript compiler directly.
>>>>>>> new_en

* O comando [`webdev build`][] produz, por padrão, JavaScript minificado e implantável.

* O comando [`webdev serve`][] produz, por padrão, módulos JavaScript
  para execução e depuração durante o desenvolvimento.
:::

{% render 'tools/dart-compile-js-options.md', site: site %}

<<<<<<< pt
#### Exemplo de compilação de aplicação web {:#compile-a-web-app}
||||||| base_en
#### Compiling web app example
=======
#### Compile a web app
>>>>>>> new_en

Por exemplo, para compilar uma aplicação Dart para JavaScript otimizado, execute
o seguinte comando:

```console
$ dart compile js -O2 -o out/main.js web/main.dart
```


<<<<<<< pt
#### Melhorando a compilação web para produção {:#helping-generate-efficient-code}
||||||| base_en
#### Improving production web compilation {:#helping-generate-efficient-code}
=======
#### Improve production web compilation {:#helping-generate-efficient-code}
>>>>>>> new_en

Siga estas práticas para melhorar a inferência de tipos, reduzir o tamanho dos arquivos e
melhorar o desempenho do JavaScript:

* Não use `Function.apply()`.
* Não sobrescreva `noSuchMethod()`.
* Evite definir variáveis como `null`.
* Seja consistente com os tipos dos argumentos
  que você passa para cada função ou método.

:::tip
<<<<<<< pt
Não se preocupe com o tamanho das bibliotecas incluídas na sua aplicação.
O compilador de produção faz tree shaking para omitir
classes, funções, métodos e assim por diante que não são usados.
Importe as bibliotecas que você acha que vai precisar,
e deixe o compilador eliminar o que não for necessário.
||||||| base_en
Don't worry about the size of your app's included libraries.
The production compiler performs tree shaking to omit
unused classes, functions, methods, and so on.
Import the libraries you think you'll need,
and let the compiler get rid of what it doesn't need.
=======
Don't worry about the size of your app's included libraries.
The production compiler performs tree shaking to omit
unused classes, functions, and methods.
Import the libraries you think you'll need,
and let the compiler get rid of what it doesn't need.
>>>>>>> new_en
:::

<<<<<<< pt
Para saber mais sobre como construir e implantar aplicações JavaScript,
confira [Web deployment](/web/deployment).
||||||| base_en
To learn more about building and deploying JavaScript applications,
check out [Web deployment](/web/deployment).
=======
To learn more about building and deploying JavaScript applications,
refer to [Web deployment][].

[Web deployment]: /web/deployment
>>>>>>> new_en


### WebAssembly (`wasm`) {:#wasm}

<<<<<<< pt
O subcomando `wasm` compila código Dart para um módulo WebAssembly/WasmGC.
Por padrão, o compilador gera o módulo `.wasm`,
um arquivo de runtime JavaScript complementar `.mjs`
e um arquivo de source map `.wasm.map`.
||||||| base_en
The `wasm` subcommand compiles Dart code to a WebAssembly/WasmGC module.
By default, the compiler generates the `.wasm` module,
a companion `.mjs` JavaScript runtime file,
and a `.wasm.map` source map file.
=======
The `wasm` subcommand compiles Dart code ahead-of-time (AOT) to a
WebAssembly (WasmGC) module (`dart2wasm`).
By default, the compiler generates the `.wasm` module,
a companion `.mjs` JavaScript runtime file,
and a `.wasm.map` source map file.
>>>>>>> new_en

<<<<<<< pt
Por exemplo, para compilar uma aplicação web Dart para WebAssembly otimizado:
||||||| base_en
For example, to compile a Dart web application to optimized WebAssembly:
=======
For example, run the following command to compile a Dart web application to
optimized WebAssembly:
>>>>>>> new_en

```console
$ dart compile wasm -O2 -o site/main.wasm web/main.dart
```

| Opção | Descrição |
| :--- | :--- |
<<<<<<< pt
| `-O<0\|1\|2\|3\|4>` | Controla as otimizações do compilador para tamanho de código e velocidade de compilação (`-O1` é o padrão; `-O2` adiciona minificação; `-O3` omite verificações de tipo implícitas; `-O4` ativa otimizações unsafe mais agressivas). |
| `--[no-]minify` | Minifica nomes de runtime (como nomes de classes). Tem precedência sobre a configuração `-O`. |
| `--[no-]strip-wasm` | Se deve remover a seção de símbolos estáticos `"name"` do binário `.wasm` de saída (ativado por padrão; passe `--no-strip-wasm` para stack traces legíveis em produção). |
| `--[no-]source-maps` | Gera um arquivo de source map `.wasm.map` junto com a saída `.wasm` (ativado por padrão). |
| `--[no-]enable-deferred-loading` | Divide os imports `deferred as` em módulos `.wasm` separados, carregados sob demanda. |
| `--standalone` | Emite um binário `.wasm` independente, sem dependências do runtime JS (não permite `dart:js_interop`). |
| `-D<key>=<value>` | Define declarações de ambiente em tempo de compilação para `String.fromEnvironment`, `bool.fromEnvironment` e `int.fromEnvironment`. |
||||||| base_en
| `-O<0\|1\|2\|3\|4>` | Controls compiler optimizations for code size and compilation speed (`-O1` default; `-O2` adds minification; `-O3` omits implicit type checks; `-O4` enables more aggressive unsafe optimizations). |
| `--[no-]minify` | Minifies runtime names (such as class names). Takes precedence over the `-O` setting. |
| `--[no-]strip-wasm` | Whether to strip the static symbol `"name"` section from the output `.wasm` binary (defaults to on; pass `--no-strip-wasm` for readable production stack traces). |
| `--[no-]source-maps` | Generates a `.wasm.map` source map file alongside the `.wasm` output (defaults to on). |
| `--[no-]enable-deferred-loading` | Splits `deferred as` imports into separate `.wasm` modules loaded on demand. |
| `--standalone` | Emits a standalone `.wasm` binary without JS runtime dependencies (disallows `dart:js_interop`). |
| `-D<key>=<value>` | Defines compile-time environment declarations for `String.fromEnvironment`, `bool.fromEnvironment`, and `int.fromEnvironment`. |
=======
| `-O0` to `-O4` | Controls compiler optimizations for code size and execution speed (`-O1` is the default, `-O2` adds minification and omits error details, `-O3` omits implicit type checks, and `-O4` omits index bounds checks). |
| `--minify` | Minifies runtime names (such as `<obj>.runtimeType.toString()`). Enabled by default at `-O2` and higher. |
| `--[no-]strip-wasm` | Strips the static symbol `name` section from the output `.wasm` binary (enabled by default). Pass `--no-strip-wasm` for readable function names when profiling. |
| `--[no-]source-maps` | Generates a `.wasm.map` source map file alongside the `.wasm` output (enabled by default). |
| `--[no-]enable-deferred-loading` | Splits `deferred as` imports into separate `.wasm` modules loaded on demand. |
| `--standalone` | Emits a standalone `.wasm` binary without JS runtime dependencies (disallows `dart:js_interop` and `--enable-deferred-loading`). |
| `-D<key>=<value>` or `--define=<key>=<value>` | Defines compile-time environment declarations for `String.fromEnvironment`, `bool.fromEnvironment`, and `int.fromEnvironment`. |
>>>>>>> new_en

{:.table .table-striped}

<<<<<<< pt
Para detalhes sobre compilar, servir e implantar aplicações Wasm,
consulte [Compilando para WebAssembly][wasm-compilation].
Para saber sobre considerações de segurança ao implantar source maps,
consulte [Web deployment][manage-source-maps].
||||||| base_en
For details on compiling, serving, and deploying Wasm applications,
see [Compiling to WebAssembly][wasm-compilation].
To learn about security considerations when deploying source maps,
see [Web deployment][manage-source-maps].
=======
For details on compiling, optimizing, and loading Wasm applications,
refer to [WebAssembly compilation][wasm-compilation].
To learn about serving `.wasm` assets and managing source maps in production,
refer to [Web deployment][web-deployment].
>>>>>>> new_en

[webdev]: /tools/webdev
[`webdev build`]: /tools/webdev#build
[`webdev serve`]: /tools/webdev#serve
[Dart runtime]: /overview#runtime
[wasm-compilation]: /web/wasm
[web-deployment]: /web/deployment#serving-wasm-in-production
