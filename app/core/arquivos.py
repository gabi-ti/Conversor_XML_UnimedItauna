import os


def listar_xmls(pasta):

    arquivos_xml = []

    for arquivo in os.listdir(pasta):

        if arquivo.lower().endswith(".xml"):

            caminho_completo = os.path.join(
                pasta,
                arquivo
            )

            arquivos_xml.append(caminho_completo)

    return arquivos_xml