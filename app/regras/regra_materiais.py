import logging
from app.core.namespaces import NS


def materiais (root):

    servicos = root.xpath(
        "//ans:servicosExecutados",
        namespaces=NS
    )

    total_alterados = 0
    mensagens = []

    for servico in servicos:

        tabela = servico.xpath(
            "./ans:codigoTabela",
            namespaces=NS
        )

        codigo = servico.xpath(
            "./ans:codigoProcedimento",
            namespaces=NS
        )

        if tabela and codigo:

            tabela_tag = tabela[0]
            codigo_tag = codigo[0]

            valor_tabela = tabela_tag.text.strip()
            valor_codigo = codigo_tag.text.strip()

            # REGRA MATERIAL
            if (
                valor_tabela == "19"
                and valor_codigo.startswith("0")
            ):

                novo_codigo = f"19{valor_codigo}"

                tabela_tag.text = "00"
                codigo_tag.text = novo_codigo

                total_alterados += 1
                
                mensagens.append(
                    f"[MATERIAL ALTERADO] "
                    f"{valor_codigo} → {novo_codigo}"
                )
                
   

    
    print(
        f"\nMateriais alterados: "
        f"{total_alterados}"
    )
    
    return total_alterados, mensagens