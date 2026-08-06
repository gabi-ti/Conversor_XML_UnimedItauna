from app.core.namespaces import NS
from app.core.leitor_planilha import carregar_mapa_pacotes


def pacotes(root):
    
    prestador = root.xpath(
        "//ans:cabecalho"
        "/ans:origem"
        "/ans:identificacaoPrestador"
        "/ans:codigoPrestadorNaOperadora/text()",
        namespaces=NS
    )
    
    prestador = prestador[0].strip() if prestador else ""

    mapa_pacotes = carregar_mapa_pacotes()
    

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

            # REGRA PACOTES
            if (
                valor_tabela == "98"
                and valor_codigo.startswith("00000")
            ):

                novo_codigo = valor_codigo.lstrip("0")

                codigo_tag.text = novo_codigo

                total_alterados += 1

                mensagens.append(
                    
                    f"{valor_codigo} → {novo_codigo}"
                
                )
                
            # NOVA REGRA - APENAS PARA O PRESTADOR 104
        if prestador == "104":

            codigo_atual = codigo_tag.text.strip()

            if codigo_atual in mapa_pacotes:

                codigo_tag.text = mapa_pacotes[codigo_atual]

                total_alterados += 1

                mensagens.append(
                    f"{codigo_atual} → {mapa_pacotes[codigo_atual]}"
            ) 

    print(
        f"\nPacotes alterados: "
        f"{total_alterados}"
    )
    
    return total_alterados, mensagens