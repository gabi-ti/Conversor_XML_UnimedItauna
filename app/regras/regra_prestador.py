
import re

from app.core.namespaces import NS


def prestador(root):

    total_alterados = 0
    mensagens = []

    # REGRA ESPECÍFICA:
    # Altera os dados da equipe somente quando:
    # - A tabela do procedimento for 22;
    # - O código do procedimento for 10101039;
    # - O código do prestador for 257000000236.

    procedimentos_executados = root.xpath(
        "//ans:procedimentoExecutado",
        namespaces=NS
    )

    for procedimento_executado in procedimentos_executados:

        procedimentos = procedimento_executado.xpath(
            "./ans:procedimento"
            "[ans:codigoTabela='22']"
            "[ans:codigoProcedimento='10101039']",
            namespaces=NS
        )

        if not procedimentos:
            continue

        equipes = procedimento_executado.xpath(
            "./ans:equipeSadt",
            namespaces=NS
        )

        for equipe in equipes:

            codigo_prestador = equipe.xpath(
                "string(./ans:codProfissional/"
                "ans:codigoPrestadorNaOperadora)",
                namespaces=NS
            ).strip()

            if codigo_prestador != "257000000236":
                continue

            # Campos que devem ser substituídos.
            alteracoes = {
                "codigoPrestadorNaOperadora": "17098",
                "nomeProf": "MARINA MOREIRA GONTIJO",
                "conselho": "6",
                "numeroConselhoProfissional": "17098",
                "CBO": "225124",
            }
            
            # Corrige explicitamente o CBO da equipe.
            campos_cbo = equipe.xpath(
                "./ans:CBOS",
                namespaces=NS
            )

            for campo_cbo in campos_cbo:
                if (campo_cbo.text or "").strip() != "225124":
                    valor_original = campo_cbo.text or ""

                    campo_cbo.text = "225124"
                    total_alterados += 1

                    mensagens.append(
                        f"[EQUIPE SADT] CBO: "
                        f"{valor_original} → 225124"
                    )

            for nome_campo, novo_valor in alteracoes.items():

                if nome_campo == "codigoPrestadorNaOperadora":
                    caminho = (
                        "./ans:codProfissional/"
                        "ans:codigoPrestadorNaOperadora"
                    )
                else:
                    caminho = f"./ans:{nome_campo}"

                campos = equipe.xpath(
                    caminho,
                    namespaces=NS
                )

                for campo in campos:

                    valor_original = (campo.text or "").strip()

                    if valor_original != novo_valor:

                        campo.text = novo_valor
                        total_alterados += 1

                        mensagens.append(
                            f"[EQUIPE SADT] {nome_campo}: "
                            f"{valor_original} → {novo_valor}"
                        )

    # REGRA GERAL:
    # Remove o prefixo 2570 dos demais prestadores,
    # sem alterar códigos dentro de equipeSadt ou identEquipe.

    prestadores = root.xpath(
        "//ans:codigoPrestadorNaOperadora"
        "[not(ancestor::ans:equipeSadt)]"
        "[not(ancestor::ans:identEquipe)]",
        namespaces=NS
    )

    for codigo in prestadores:

        codigo_original = (codigo.text or "").strip()

        novo_codigo = re.sub(
            r"^2570+",
            "",
            codigo_original
        )

        if codigo_original != novo_codigo:

            codigo.text = novo_codigo
            total_alterados += 1

            mensagens.append(
                f"[REGRA GERAL] {codigo_original} → {novo_codigo}"
            )

    print(
        f"\nPrestadores alterados: {total_alterados}"
    )

    return total_alterados, mensagens
