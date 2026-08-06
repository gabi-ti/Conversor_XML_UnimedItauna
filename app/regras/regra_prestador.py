import re

from app.core.namespaces import NS


def prestador(root):

    prestadores = root.xpath(
        "//ans:codigoPrestadorNaOperadora"
        "[not(ancestor::ans:equipeSadt)]"
        "[not(ancestor::ans:identEquipe)]",
        namespaces=NS
    )

    total_alterados = 0
    mensagens = []

    for prestador in prestadores:

        codigo_original = prestador.text.strip()

        # Verifica se este código está dentro de <dadosExecutante>
        dentro_dados_executante = prestador.xpath(
            "boolean(ancestor::ans:dadosExecutante)",
            namespaces=NS
        )
        
        consulta__ps = bool(
            root.xpath(
                "//ans:procedimento"
                "[ans:codigoTabela='22']"
                "[ans:codigoProcedimento='10101039']",
                namespaces=NS
                
                
            )
        )

        # Regra específica
        if (
            dentro_dados_executante
            and codigo_original == "257000000236"
            and consulta__ps
        ):

            novo_codigo = "17098"

        # Regra padrão
        else:

            novo_codigo = re.sub(
                r"^2570+",
                "",
                codigo_original
            )

        if codigo_original != novo_codigo:

            prestador.text = novo_codigo

            total_alterados += 1

            mensagens.append(
                f"{codigo_original} → {novo_codigo}"
            )

    print(
        f"\nPrestadores alterados: {total_alterados}"
    )

    return total_alterados, mensagens