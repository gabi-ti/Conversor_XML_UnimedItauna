
from app.core.namespaces import NS


def regra_cod_104(root):

    total_alterados = 0
    mensagens = []

    # VALIDA SE O XML É DO HOSPITAL 104
    prestador = root.xpath(
        "//ans:cabecalho"
        "/ans:origem"
        "/ans:identificacaoPrestador"
        "/ans:codigoPrestadorNaOperadora/text()",
        namespaces=NS
    )

    prestador = prestador[0].strip() if prestador else ""

    print(f"Hospital identificado na nova regra: {prestador}")

    if prestador != "104":
        return total_alterados, mensagens

    # MAPEAMENTO DAS TAXAS
    mapa_servicos = {
        "25700372": "60000325",
        "25700373": "60000325",
        "25700374": "60000325"
    }

    # MAPEAMENTO DAS CONSULTAS
    mapa_procedimentos = {
        "10101040": "10101039",
        "10101041": "10101039",
        "10101042": "10101039",
        "10101043": "10101039",
        "10101044": "10101039",
        "10101045": "10101039"
    }

    # 1 - TAXAS
    servicos = root.xpath(
        "//ans:outrasDespesas/ans:despesa/ans:servicosExecutados",
        namespaces=NS
    )

    for servico in servicos:

        codigos = servico.xpath(
            "./ans:codigoProcedimento",
            namespaces=NS
        )

        for codigo_tag in codigos:

            codigo_atual = (codigo_tag.text or "").strip()

            if codigo_atual in mapa_servicos:

                novo_codigo = mapa_servicos[codigo_atual]
                codigo_tag.text = novo_codigo

                total_alterados += 1

                mensagens.append(
                    f"Taxas: {codigo_atual} → {novo_codigo}"
                )

    # 2 - CONSULTAS
    procedimentos = root.xpath(
        "//ans:procedimentosExecutados//ans:procedimentoExecutado",
        namespaces=NS
    )

    print(f"Procedimentos encontrados: {len(procedimentos)}")

    for procedimento in procedimentos:

        codigos = procedimento.xpath(
            "./ans:procedimento/ans:codigoProcedimento",
            namespaces=NS
        )

        for codigo_tag in codigos:

            codigo_atual = (codigo_tag.text or "").strip()

            if codigo_atual in mapa_procedimentos:

                novo_codigo = mapa_procedimentos[codigo_atual]
                codigo_tag.text = novo_codigo

                total_alterados += 1

                mensagens.append(
                    f"Consultas: {codigo_atual} → {novo_codigo}"
                )

    print(
        f"\nCódigos hospital 104 alterados: {total_alterados}"
    )

    return total_alterados, mensagens
