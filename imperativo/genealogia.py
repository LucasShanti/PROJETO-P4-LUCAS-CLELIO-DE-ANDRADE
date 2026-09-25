"""Implementacao imperativa do cadastro genealogico da Etapa 3."""


class ErroCadastro(Exception):
    """Erro causado por uma regra violada durante o cadastro."""


class ErroPessoaInexistente(Exception):
    """Erro causado por uma consulta a pessoa nao cadastrada."""


def criar_familia():
    """Cria o estado mutavel que sera manipulado pelas operacoes."""
    return {"pessoas": {}, "filhos": {}}


def cadastrar_pessoa(familia, nome, sexo):
    """Adiciona uma pessoa ao estado, rejeitando identificadores repetidos."""
    if nome in familia["pessoas"]:
        raise ErroCadastro("identificador de pessoa ja cadastrado")
    if sexo not in ("M", "F"):
        raise ErroCadastro("sexo deve ser M ou F")

    familia["pessoas"][nome] = {"sexo": sexo, "pais": []}
    familia["filhos"][nome] = []


def _existe_pessoa(familia, nome):
    return nome in familia["pessoas"]


def _exigir_pessoa(familia, nome):
    if not _existe_pessoa(familia, nome):
        raise ErroPessoaInexistente("pessoa nao cadastrada: " + nome)


def _ha_caminho(familia, inicio, destino):
    """Percorre filhos para verificar se existe um caminho entre pessoas."""
    pendentes = [inicio]
    visitados = set()

    while pendentes:
        atual = pendentes.pop()
        if atual == destino:
            return True
        if atual in visitados:
            continue
        visitados.add(atual)
        for filho in familia["filhos"][atual]:
            if filho not in visitados:
                pendentes.append(filho)
    return False


def cadastrar_filiacao(familia, pai_ou_mae, filho):
    """Adiciona uma filiação e preserva as regras de consistencia."""
    _exigir_pessoa(familia, pai_ou_mae)
    _exigir_pessoa(familia, filho)

    if pai_ou_mae == filho:
        raise ErroCadastro("uma pessoa nao pode ser pai ou mae de si mesma")
    if _ha_caminho(familia, filho, pai_ou_mae):
        raise ErroCadastro("a filiacao criaria um ciclo de ascendencia")
    if pai_ou_mae in familia["pessoas"][filho]["pais"]:
        raise ErroCadastro("filiacao ja cadastrada")

    sexo_pai_ou_mae = familia["pessoas"][pai_ou_mae]["sexo"]
    pais_do_filho = familia["pessoas"][filho]["pais"]
    for pai_existente in pais_do_filho:
        if familia["pessoas"][pai_existente]["sexo"] == sexo_pai_ou_mae:
            raise ErroCadastro("filho ja possui pai ou mae desse sexo")

    pais_do_filho.append(pai_ou_mae)
    familia["filhos"][pai_ou_mae].append(filho)


def _pais(familia, nome):
    return familia["pessoas"][nome]["pais"]


def _sexo(familia, nome):
    return familia["pessoas"][nome]["sexo"]


def _normalizar_tipo(tipo):
    tipos = {
        "pai": "pai",
        "mae": "mae",
        "mãe": "mae",
        "avo": "avo",
        "avó": "avo",
        "avô": "avo",
        "irmao": "irmao",
        "irmão": "irmao",
        "irmao completo": "irmao_completo",
        "irmão completo": "irmao_completo",
        "meio-irmao": "meio_irmao",
        "meio-irmão": "meio_irmao",
        "meia-irma": "meio_irmao",
        "meia-irmã": "meio_irmao",
        "tio": "tio",
        "tia": "tio",
        "primo": "primo",
        "prima": "primo",
        "ancestral": "ancestral",
        "descendente": "descendente",
    }
    if tipo not in tipos:
        raise ErroCadastro("tipo de parentesco desconhecido")
    return tipos[tipo]


def _tem_ancestral(familia, ancestral, pessoa):
    pendentes = list(_pais(familia, pessoa))
    visitados = set()
    while pendentes:
        atual = pendentes.pop()
        if atual == ancestral:
            return True
        if atual in visitados:
            continue
        visitados.add(atual)
        pendentes.extend(_pais(familia, atual))
    return False


def _irmaos(familia, pessoa):
    resultado = set()
    for pai in _pais(familia, pessoa):
        resultado.update(familia["filhos"][pai])
    resultado.discard(pessoa)
    return resultado


def _irmaos_comuns(familia, primeira, segunda):
    return set(_pais(familia, primeira)).intersection(_pais(familia, segunda))


def _eh_tipo_parentesco(familia, primeira, segunda, tipo):
    if primeira == segunda:
        return False
    pais_segunda = _pais(familia, segunda)

    if tipo == "pai":
        return _sexo(familia, primeira) == "M" and primeira in pais_segunda
    if tipo == "mae":
        return _sexo(familia, primeira) == "F" and primeira in pais_segunda
    if tipo == "ancestral":
        return _tem_ancestral(familia, primeira, segunda)
    if tipo == "descendente":
        return _tem_ancestral(familia, segunda, primeira)
    if tipo in ("irmao", "irmao_completo", "meio_irmao"):
        quantidade = len(_irmaos_comuns(familia, primeira, segunda))
        mesmo_sexo = _sexo(familia, primeira) == "M"
        if quantidade == 2:
            return tipo in ("irmao", "irmao_completo")
        if quantidade == 1:
            return tipo in ("irmao", "meio_irmao")
        return False
    if tipo == "avo":
        for pai in pais_segunda:
            if primeira in _pais(familia, pai):
                return True
        return False
    if tipo == "tio":
        for pai in pais_segunda:
            if primeira in _irmaos(familia, pai):
                return True
        return False
    if tipo == "primo":
        for pai in pais_segunda:
            for tio in _irmaos(familia, pai):
                if primeira in familia["filhos"][tio]:
                    return True
        return False
    return False


def verificar_parentesco(familia, primeira, segunda, tipo):
    """Retorna True/False para uma consulta valida de parentesco."""
    _exigir_pessoa(familia, primeira)
    _exigir_pessoa(familia, segunda)
    tipo_normalizado = _normalizar_tipo(tipo)
    return _eh_tipo_parentesco(familia, primeira, segunda, tipo_normalizado)


def _ancestrais(familia, pessoa):
    resultado = set()
    pendentes = list(_pais(familia, pessoa))
    while pendentes:
        atual = pendentes.pop()
        if atual in resultado:
            continue
        resultado.add(atual)
        pendentes.extend(_pais(familia, atual))
    return resultado


def _descendentes(familia, pessoa):
    resultado = set()
    pendentes = list(familia["filhos"][pessoa])
    while pendentes:
        atual = pendentes.pop()
        if atual in resultado:
            continue
        resultado.add(atual)
        pendentes.extend(familia["filhos"][atual])
    return resultado


def listar_parentes(familia, pessoa, tipo):
    """Lista pessoas que possuem o tipo de relacao solicitado com pessoa."""
    _exigir_pessoa(familia, pessoa)
    tipo_normalizado = _normalizar_tipo(tipo)
    resultado = set()

    if tipo_normalizado == "ancestral":
        return _ancestrais(familia, pessoa)
    if tipo_normalizado == "descendente":
        return _descendentes(familia, pessoa)

    for candidato in familia["pessoas"]:
        if _eh_tipo_parentesco(familia, candidato, pessoa, tipo_normalizado):
            resultado.add(candidato)
    return resultado