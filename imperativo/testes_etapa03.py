"""Testes da implementacao imperativa baseados no contrato da Etapa 2."""

from genealogia import (
    ErroCadastro,
    ErroPessoaInexistente,
    cadastrar_filiacao,
    cadastrar_pessoa,
    criar_familia,
    listar_parentes,
    verificar_parentesco,
)


PESSOAS = [
    ("João", "M"),
    ("Maria", "F"),
    ("Ana", "F"),
    ("Pedro", "M"),
    ("Lucas", "M"),
    ("Beatriz", "F"),
    ("Clara", "F"),
    ("Rafael", "F"),
    ("Sofia", "F"),
    ("Tiago", "M"),
]

FILIACOES = [
    ("João", "Ana"),
    ("Maria", "Ana"),
    ("João", "Pedro"),
    ("Maria", "Pedro"),
    ("Ana", "Lucas"),
    ("Pedro", "Beatriz"),
    ("João", "Clara"),
    ("Rafael", "Clara"),
    ("Sofia", "Tiago"),
]


def familia_base():
    familia = criar_familia()
    for nome, sexo in PESSOAS:
        cadastrar_pessoa(familia, nome, sexo)
    for pai_ou_mae, filho in FILIACOES:
        cadastrar_filiacao(familia, pai_ou_mae, filho)
    return familia


def verificar_casos_normais():
    familia = familia_base()
    casos = [
        ("N01", verificar_parentesco(familia, "João", "Ana", "pai"), True),
        ("N02", verificar_parentesco(familia, "Maria", "Ana", "mãe"), True),
        ("N03", verificar_parentesco(familia, "Ana", "Pedro", "irmão completo"), True),
        ("N04", verificar_parentesco(familia, "Ana", "Clara", "meio-irmão"), True),
        ("N05", verificar_parentesco(familia, "João", "Lucas", "avô"), True),
        ("N06", verificar_parentesco(familia, "Maria", "Lucas", "avó"), True),
        ("N07", verificar_parentesco(familia, "Pedro", "Lucas", "tio"), True),
        ("N08", verificar_parentesco(familia, "Lucas", "Beatriz", "primo"), True),
        ("N09", verificar_parentesco(familia, "João", "Lucas", "ancestral"), True),
        ("N10", verificar_parentesco(familia, "Lucas", "João", "descendente"), True),
    ]
    for identificador, resultado, esperado in casos:
        assert resultado == esperado, identificador


def verificar_casos_limite():
    familia = criar_familia()
    cadastrar_pessoa(familia, "Sofia", "F")
    assert listar_parentes(familia, "Sofia", "ancestral") == set()

    familia = familia_base()
    assert listar_parentes(familia, "Tiago", "descendente") == set()
    assert verificar_parentesco(familia, "Ana", "Ana", "ancestral") is False


def verificar_casos_invalidos():
    familia = familia_base()
    try:
        verificar_parentesco(familia, "João", "Gustavo", "pai")
        raise AssertionError("I01 nao gerou erro")
    except ErroPessoaInexistente:
        pass

    try:
        cadastrar_filiacao(familia, "Lucas", "João")
        raise AssertionError("I02 nao gerou erro")
    except ErroCadastro:
        pass


def executar_testes():
    verificar_casos_normais()
    verificar_casos_limite()
    verificar_casos_invalidos()
    print("15 casos da Etapa 2 aprovados: 10 normais, 3 limite e 2 invalidos.")


if __name__ == "__main__":
    executar_testes()