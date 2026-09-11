# PROJETO-P4-LUCAS-CLELIO-DE-ANDRADE

1. Descrição do problema

Sistema de cadastro genealógico que representa relações de filiação (pai/mãe → filho) e, a partir delas, deriva relações de parentesco mais complexas (irmão, avô, tio, primo, ancestral, descendente), sem que precisem ser cadastradas manualmente. Contexto: cadastro familiar simples, como uma árvore genealógica.

2. Objetivo

O sistema deverá:

Cadastrar pessoas e suas relações de filiação.
Verificar se uma relação de parentesco existe entre duas pessoas.
Listar pessoas que possuem determinado tipo de relação com uma pessoa dada.
Listar ancestrais e descendentes de uma pessoa.

3. Entradas
Pessoa: nome (identificador único) e sexo.
Filiação: identificador do pai/mãe + identificador do filho.
Consulta de relação: dois identificadores de pessoas + tipo de relação a verificar.
Consulta de listagem: um identificador de pessoa + tipo de relação desejada.

4. Saídas
Verdadeiro/falso para verificação de relação.
Lista de pessoas para consultas de listagem (pode ser vazia).
Mensagem de erro quando a entrada viola alguma regra do sistema.

5. Regras do problema
Identificador de pessoa é único.
Cada pessoa tem no máximo um pai e uma mãe cadastrados.
Ninguém pode ser pai/mãe de si mesmo.
Não são permitidos ciclos de ascendência.
Irmãos compartilham pelo menos um dos pais; irmãos completos (ambos os pais) devem ser diferenciados de meio-irmãos (um pai em comum).
Ancestral de X é qualquer pessoa na cadeia de pais de X, em qualquer geração; descendente é a relação inversa.
Tio/tia é irmão/irmã de um dos pais; primo é filho de um tio/tia.
O sexo define apenas o termo usado na resposta (pai/mãe, avô/avó etc.), não a lógica da relação.
Ninguém é considerado parente de si mesmo.

6. Casos de exemplo

Cadastro base: João e Maria são pais de Ana e Pedro. Ana é mãe de Lucas.

parentesco(Ana, Pedro, irmão) → Verdadeiro
parentesco(João, Lucas, avô) → Verdadeiro
parentesco(Pedro, Lucas, tio) → Verdadeiro
parentesco(Lucas, João, avô) → Falso (a relação não é simétrica)
listar_descendentes(João) → [Ana, Pedro, Lucas]

7. Casos-limite
Pessoa sem pais cadastrados: consulta de ancestrais retorna lista vazia, não erro.
Consulta envolvendo pessoa não cadastrada: retorna erro específico, e não "relação falsa".
Tentativa de cadastro que criaria um ciclo de ascendência: deve ser rejeitada.

8. Restrições

Fora do escopo: relações por afinidade (sogro, cunhado, genro), grau de parentesco jurídico/sucessório, persistência em banco de dados, interface gráfica, adoção e famílias reconstituídas.

9. Principais conceitos do domínio

Pessoa, Filiação, Parentesco derivado (irmão, avô, tio, primo), Geração/grau, Linha de ascendência/descendência.

10. Adequação aos quatro paradigmas

O problema combina estrutura de dados a ser percorrida (adequado a imperativo e orientado a objetos) com relações que podem ser definidas de forma declarativa e recursiva sobre fatos básicos (adequado a funcional e lógico). Em lógica, as regras de parentesco podem ser expressas diretamente como fatos e regras, contrastando com a abordagem passo a passo típica do paradigma imperativo — o que evidencia bem a diferença entre os quatro modelos de programação.

11. Linguagens inicialmente consideradas
Imperativo: C ou Python — permitem manipular estruturas de dados e laços de forma direta, sem recursos de paradigmas mais avançados.
Orientado a objetos: Java — já usada no curso, com suporte maduro a classes e referências entre objetos.
Funcional: Haskell ou Elixir — Haskell por ser funcional puro, forçando imutabilidade; Elixir como alternativa de sintaxe mais familiar.
Lógico: Prolog — linguagem de referência do paradigma, com unificação e busca nativas, ideal para expressar regras de parentesco.