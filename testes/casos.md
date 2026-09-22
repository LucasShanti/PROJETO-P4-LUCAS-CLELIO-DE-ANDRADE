# Casos de teste

## Contrato de comportamento

Este documento define o comportamento observável esperado das quatro
implementações. Os casos não dependem da linguagem, da estrutura de dados ou
do paradigma utilizado.

### Convenções

- Cada caso começa com um estado novo, salvo quando o caso indicar a
	`familia-base` abaixo.
- Uma pessoa possui um identificador único e um sexo (`M` ou `F`). O sexo
	determina apenas o termo exibido: pai/mãe, avô/avó, tio/tia etc.
- Uma filiação `A -> B` significa que `A` é pai ou mãe de `B`.
- `parentesco(A, B, tipo)` verifica uma relação direcionada: A é o tipo de
	parente de B. A consulta não considera uma pessoa parente de si mesma.
- Em saídas de listagem, a notação `{...}` representa um conjunto; a ordem
	dos elementos não é significativa.
- `erro(pessoa-inexistente)` e `erro(regra-violada)` são categorias de erro do
	contrato. A mensagem textual pode variar entre implementações.

### Estado compartilhado: `familia-base`

Cadastrar as pessoas:

| Identificador | Sexo |
|---|---|
| João | M |
| Maria | F |
| Ana | F |
| Pedro | M |
| Lucas | M |
| Beatriz | F |
| Clara | F |
| Rafael | M |
| Sofia | F |
| Tiago | M |

Cadastrar as filiações:

- `João -> Ana` e `Maria -> Ana`;
- `João -> Pedro` e `Maria -> Pedro`;
- `Ana -> Lucas`;
- `Pedro -> Beatriz`;
- `João -> Clara` e `Rafael -> Clara`;
- `Sofia -> Tiago`.

Assim, Ana e Pedro são irmãos completos; Ana e Clara são meio-irmãs; Lucas e
Beatriz são primos; e Sofia/Tiago formam um ramo independente.

## Casos normais

| ID | Entrada | Saída esperada | Descrição |
|---|---|---|---|
| N01 | `familia-base`; `parentesco(João, Ana, pai)` | `verdadeiro` | Reconhece a filiação paterna direta. |
| N02 | `familia-base`; `parentesco(Maria, Ana, mãe)` | `verdadeiro` | Reconhece a filiação materna direta. |
| N03 | `familia-base`; `parentesco(Ana, Pedro, irmão completo)` | `verdadeiro` | Identifica irmãos que compartilham os dois pais. |
| N04 | `familia-base`; `parentesco(Ana, Clara, meio-irmão)` | `verdadeiro` | Identifica meio-irmãos que compartilham apenas um pai. O termo deve respeitar o sexo de Clara: meio-irmã. |
| N05 | `familia-base`; `parentesco(João, Lucas, avô)` | `verdadeiro` | Reconhece avô por duas gerações. |
| N06 | `familia-base`; `parentesco(Maria, Lucas, avó)` | `verdadeiro` | Reconhece avó por duas gerações. |
| N07 | `familia-base`; `parentesco(Pedro, Lucas, tio)` | `verdadeiro` | Reconhece o irmão de um dos pais. |
| N08 | `familia-base`; `parentesco(Lucas, Beatriz, primo)` | `verdadeiro` | Reconhece filhos de irmãos como primos. |
| N09 | `familia-base`; `parentesco(João, Lucas, ancestral)` | `verdadeiro` | Reconhece ancestral em qualquer geração. |
| N10 | `familia-base`; `parentesco(Lucas, João, descendente)` | `verdadeiro` | Reconhece a relação inversa de ancestralidade. |

## Casos-limite

| ID | Entrada | Saída esperada | Descrição |
|---|---|---|---|
| L01 | Cadastrar apenas `Sofia (F)`; `listar(Sofia, ancestral)` | `{}` | Pessoa sem pais cadastrados possui lista de ancestrais vazia, sem erro. |
| L02 | `familia-base`; `listar(Tiago, descendente)` | `{}` | Pessoa cadastrada sem filhos possui lista de descendentes vazia. |
| L03 | `familia-base`; `parentesco(Ana, Ana, ancestral)` | `falso` | Ninguém é parente de si mesmo, inclusive em consultas de ancestralidade. |

## Casos de entrada inválida

| ID | Entrada | Saída esperada | Descrição |
|---|---|---|---|
| I01 | `familia-base`; `parentesco(João, Gustavo, pai)` | `erro(pessoa-inexistente)` | Consultar uma pessoa não cadastrada gera erro específico, e não `falso`. |
| I02 | `familia-base`; cadastrar filiação `Lucas -> João` | `erro(regra-violada)` | A filiação criaria um ciclo de ascendência e deve ser rejeitada. |
