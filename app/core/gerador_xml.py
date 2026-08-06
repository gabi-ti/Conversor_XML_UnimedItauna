#def salvar_xml(tree, caminho_saida):

 #   tree.write(
  #      caminho_saida,
   #     pretty_print=True,
    #    xml_declaration=True,
     #   encoding="utf-8"
  #  )

    #print(
#        f"\nXML salvo em: {caminho_saida}"
 #   )
 
## TESTE DE HASH

import hashlib
from lxml import etree
from app.core.namespaces import NS


def atualizar_hash(root):

    hash_tag = root.xpath(
        "//ans:epilogo/ans:hash",
        namespaces=NS
    )

    if not hash_tag:
        return

    hash_tag = hash_tag[0]

    # limpa temporariamente o valor
    hash_tag.text = ""

    conteudo = etree.tostring(
        root,
        encoding="ISO-8859-1"
    )

    novo_hash = hashlib.md5(
        conteudo
    ).hexdigest()

    hash_tag.text = novo_hash

    print(
        f"Hash atualizado: {novo_hash}"
    )
    
def salvar_xml(tree, root, caminho_saida):

    # REMOVE ASSINATURA DIGITAL
    assinaturas = root.xpath(

        "//*[local-name()='Signature']"
    )

    for assinatura in assinaturas:

        assinatura.getparent().remove(
            assinatura
        )

    # SALVA XML
    tree.write(
        caminho_saida,
        pretty_print=False,
        xml_declaration=True,
        encoding="ISO-8859-1"
    )

    print(
        f"\nXML salvo em: {caminho_saida}"
    )