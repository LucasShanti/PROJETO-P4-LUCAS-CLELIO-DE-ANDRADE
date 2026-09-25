# Decisoes

## Etapa 03: implementacao imperativa

### Estados mantidos

O programa mantem um dicionario mutavel `familia`. Dentro dele, `pessoas`
guarda o sexo e a lista de pais de cada pessoa, enquanto `filhos` guarda a
lista inversa para permitir percorrer a descendencia.

### Operacoes que modificam estado

`cadastrar_pessoa` adiciona uma entrada em `pessoas` e em `filhos`.
`cadastrar_filiacao` modifica a lista de pais do filho e a lista de filhos do
pai ou mae. Antes da mutacao, a funcao verifica pessoas existentes, limite de
um pai e uma mae, duplicidade, auto-filiacao e ciclos de ascendencia.

### Efeitos colaterais

As funcoes de cadastro recebem o dicionario da familia por parametro e o
alteram diretamente. Esse efeito colateral e intencional: o estado do cadastro
deve continuar disponivel para as consultas seguintes. As funcoes de consulta
nao alteram o cadastro.

### Estruturas de controle

`if` seleciona regras e casos de parentesco. `for` percorre pessoas, pais e
filhos. `while` implementa buscas iterativas em largura ou profundidade para
detectar ciclos, ancestrais e descendentes. Conjuntos evitam resultados
duplicados durante as travessias.

### Organizacao dos subprogramas

`criar_familia` inicializa o estado. `cadastrar_pessoa` e
`cadastrar_filiacao` realizam mutacoes validas. Funcoes auxiliares privadas
fazem buscas e normalizam tipos. `verificar_parentesco` responde uma relacao
booleana, e `listar_parentes` monta conjuntos de resultados.

### Justificativa do paradigma

A solucao e predominantemente imperativa porque descreve uma sequencia de
passos que altera uma estrutura de memoria compartilhada. O resultado depende
do estado atual da familia e das mutacoes realizadas antes de cada consulta.
Nao ha classes ou objetos de dominio escondendo esse fluxo; o cadastro e
manipulado por funcoes e atribuicoes explicitas.
