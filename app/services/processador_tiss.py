from app.core.namespaces import NS


def localizar_procedimentos(root):

    procedimentos = root.xpath(
        "//ans:servicosExecutados",
        namespaces=NS
    )

    print(f"\nProcedimentos encontrados: {len(procedimentos)}\n")

    for procedimento in procedimentos:

        codigo_tabela = procedimento.xpath(
            "./ans:codigoTabela/text()",
            namespaces=NS
        )

        codigo_procedimento = procedimento.xpath(
            "./ans:codigoProcedimento/text()",
            namespaces=NS
        )

        if codigo_tabela and codigo_procedimento:

            print(
                f"Tabela: {codigo_tabela[0]} | "
                f"Procedimento: {codigo_procedimento[0]}"
            )