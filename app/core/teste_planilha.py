from app.core.leitor_planilha import carregar_mapa_pacotes

mapa = carregar_mapa_pacotes()

print(len(mapa))

for codigo, pacote in list(mapa.items())[:10]:
    print(codigo, "->", pacote)