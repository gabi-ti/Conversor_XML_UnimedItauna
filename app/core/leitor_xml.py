from lxml import etree


def carregar_xml(caminho_arquivo):

    try:

        tree = etree.parse(caminho_arquivo)

        root = tree.getroot()

        return tree, root

    except Exception as erro:

        print(f"Erro ao ler XML: {erro}")

        return None, None
