// Copyright (c) 2025, the Dart project authors. Please see the AUTHORS file
// for details. All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.

import 'package:jaspr/dom.dart';
import 'package:jaspr/jaspr.dart';
import 'package:jaspr_content/jaspr_content.dart';

import '../../utils/page_source_info.dart';

/// Aviso, no topo do conteúdo, de que a página ainda está em inglês.
///
/// Decidido no build pelo frontmatter: aparece só em páginas de
/// documentação vindas de um arquivo Markdown do repositório (`inputPath`
/// terminando em `.md`, o que exclui páginas geradas em memória e páginas
/// HTML como busca e 404), fora da página inicial, e que não têm
/// `ia-translate: true`. O link leva ao arquivo da página no GitHub para
/// quem quiser traduzir.
class UntranslatedNotice extends StatelessComponent {
  const UntranslatedNotice({super.key});

  /// Se o aviso deve aparecer em [page].
  static bool appliesTo(Page page) {
    final pageData = page.data.page;
    final inputPath = pageData['inputPath'] as String?;
    if (inputPath == null || !inputPath.endsWith('.md')) return false;
    if (page.path == 'index.md') return false;
    return pageData['ia-translate'] != true;
  }

  @override
  Component build(BuildContext context) {
    final page = context.page;
    final sourceUrl = page.sourceInfo.sourceUrl;

    return aside(
      classes: 'alert alert-info untranslated-notice',
      attributes: {'role': 'note', 'lang': 'pt-BR'},
      [
        div(classes: 'alert-content', [
          p([
            const .text(
              'Esta página ainda está em inglês. '
              'A tradução para o português ainda não chegou aqui. '
              'Quer ajudar? ',
            ),
            if (sourceUrl != null)
              a(
                href: sourceUrl,
                attributes: {'target': '_blank', 'rel': 'noopener'},
                [
                  const .text('Traduza no GitHub'),
                  const span(
                    attributes: {'aria-hidden': 'true'},
                    [.text(' →')],
                  ),
                ],
              ),
          ]),
        ]),
      ],
    );
  }
}
