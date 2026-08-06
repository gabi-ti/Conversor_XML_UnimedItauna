from lxml import etree

from app.core.logger import registrar_log


def validar_xml(caminho_xml):

    try:

        etree.parse(caminho_xml)

        registrar_log(
            f"XML válido: {caminho_xml}"
        )

        return True

    except Exception as erro:

        registrar_log(
            f"XML inválido: {caminho_xml}"
        )

        registrar_log(
            f"Erro: {erro}"
        )

        return False