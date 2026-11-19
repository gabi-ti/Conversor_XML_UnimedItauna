
import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image

from app.regras.regra_cod_104 import regra_cod_104

# ==========================================================
# CONFIGURAÇÕES VISUAIS
# ==========================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

VERDE = "#008D50"
VERDE_ESCURO = "#006B3F"
VERDE_CLARO = "#E8F5ED"
FUNDO = "#F3F6F5"
BRANCO = "#FFFFFF"
TEXTO = "#172B25"
CINZA = "#64748B"
BORDA = "#DCE5E0"
LOG_FUNDO = "#172B25"


class TelaPrincipal(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Conversor Unimed Itaúna")
        self.geometry("1150x700")
        self.minsize(950, 600)

        self.configure(fg_color=FUNDO)

        self.arquivos_selecionados = []

        self.resultados = {
            "Prestadores": 0,
            "Materiais": 0,
            "Medicamentos": 0,
            "Pacotes": 0,
            "Hospital 104": 0,
            "Taxas": 0,
            "Consultas": 0
        }

        self.cards_resultados = {}

        self.criar_interface()

    # ======================================================
    # INTERFACE PRINCIPAL
    # ======================================================

    def criar_interface(self):

        # CABEÇALHO
        self.cabecalho = ctk.CTkFrame(
            self,
            height=115,
            fg_color=VERDE,
            corner_radius=0
        )

        self.cabecalho.pack(fill="x")
        self.cabecalho.pack_propagate(False)

        # LOGO
        caminho_logo = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__))
                )
            ),
            "app",
            "assets",
            "Logo_UnimedItauna.png"
        )

        try:

            imagem = Image.open(caminho_logo).convert("RGBA")

            self.logo = ctk.CTkImage(
                light_image=imagem,
                dark_image=imagem,
                size=(180, 68)
            )

            self.label_logo = ctk.CTkLabel(
                self.cabecalho,
                text="",
                image=self.logo
            )

            self.label_logo.pack(
                side="left",
                padx=(25, 20),
                pady=15
            )

        except Exception as erro:

            print("Erro ao carregar logo:", erro)

            ctk.CTkLabel(
                self.cabecalho,
                text="UNIMED ITAÚNA",
                font=("Segoe UI", 22, "bold"),
                text_color=BRANCO
            ).pack(side="left", padx=25)

        # TÍTULO
        area_titulo = ctk.CTkFrame(
            self.cabecalho,
            fg_color="transparent"
        )

        area_titulo.pack(
            side="left",
            padx=10,
            pady=20
        )

        ctk.CTkLabel(
            area_titulo,
            text="Conversor Unimed Itaúna",
            font=("Segoe UI", 25, "bold"),
            text_color=BRANCO
        ).pack(anchor="w")

        ctk.CTkLabel(
            area_titulo,
            text="Conversão de arquivos XML - Padrão TISS",
            font=("Segoe UI", 13),
            text_color="#E1F4E9"
        ).pack(anchor="w", pady=(3, 0))

        # CONTEÚDO PRINCIPAL
        self.conteudo = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.conteudo.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=12
        )

        self.conteudo.grid_columnconfigure(0, weight=5)
        self.conteudo.grid_columnconfigure(1, weight=7)
        self.conteudo.grid_rowconfigure(0, weight=1)

        # PAINEL ESQUERDO
        self.painel_arquivos = ctk.CTkFrame(
            self.conteudo,
            fg_color=BRANCO,
            corner_radius=18,
            border_width=1,
            border_color=BORDA
        )

        self.painel_arquivos.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 7)
        )

        # PAINEL DIREITO
        self.painel_resultados = ctk.CTkFrame(
            self.conteudo,
            fg_color="transparent"
        )

        self.painel_resultados.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(7, 0)
        )

        self.painel_resultados.grid_columnconfigure(0, weight=1)
        self.painel_resultados.grid_rowconfigure(1, weight=1)

        self.criar_painel_arquivos()
        self.criar_painel_resultados()
        self.criar_painel_logs()

    # ======================================================
    # PAINEL DE SELEÇÃO DE ARQUIVOS
    # ======================================================

    def criar_painel_arquivos(self):

        ctk.CTkLabel(
            self.painel_arquivos,
            text="↥  Seleção de Arquivos",
            font=("Segoe UI", 20, "bold"),
            text_color=VERDE_ESCURO
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 3)
        )

        ctk.CTkLabel(
            self.painel_arquivos,
            text="Selecione os arquivos XML que deseja converter.",
            font=("Segoe UI", 12),
            text_color=CINZA
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 10)
        )

        # ÁREA DE SELEÇÃO
        self.area_selecao = ctk.CTkFrame(
            self.painel_arquivos,
            fg_color="#F8FCF9",
            border_width=2,
            border_color="#A7D8BC",
            corner_radius=15
        )

        self.area_selecao.pack(
            fill="x",
            padx=16,
            pady=3
        )

        ctk.CTkLabel(
            self.area_selecao,
            text="▤",
            font=("Segoe UI", 38),
            text_color=VERDE
        ).pack(pady=(8, 0))

        ctk.CTkLabel(
            self.area_selecao,
            text="Selecione seus arquivos XML",
            font=("Segoe UI", 15, "bold"),
            text_color=TEXTO
        ).pack(pady=(2, 2))

        ctk.CTkLabel(
            self.area_selecao,
            text="Clique no botão abaixo para localizar os arquivos.",
            font=("Segoe UI", 11),
            text_color=CINZA
        ).pack(pady=(0, 8))

        self.botao_selecionar = ctk.CTkButton(
            self.area_selecao,
            text="▣  Selecionar XMLs",
            command=self.selecionar_arquivos,
            height=38,
            width=210,
            corner_radius=10,
            fg_color=VERDE,
            hover_color=VERDE_ESCURO,
            font=("Segoe UI", 13, "bold")
        )

        self.botao_selecionar.pack(pady=(0, 10))

        # TÍTULO DA LISTA
        area_lista = ctk.CTkFrame(
            self.painel_arquivos,
            fg_color="transparent"
        )

        area_lista.pack(
            fill="x",
            padx=18,
            pady=(12, 3)
        )

        self.label_quantidade = ctk.CTkLabel(
            area_lista,
            text="Arquivos selecionados (0)",
            font=("Segoe UI", 13, "bold"),
            text_color=TEXTO
        )

        self.label_quantidade.pack(side="left")

        self.botao_limpar = ctk.CTkButton(
            area_lista,
            text="Limpar",
            command=self.limpar_arquivos,
            width=65,
            height=26,
            corner_radius=8,
            fg_color="#EDF3EF",
            hover_color="#DCEAE1",
            text_color=VERDE_ESCURO,
            font=("Segoe UI", 11, "bold")
        )

        self.botao_limpar.pack(side="right")

        # LISTA DE ARQUIVOS
        self.lista_arquivos = ctk.CTkTextbox(
            self.painel_arquivos,
            height=90,
            fg_color="#F8FAF9",
            text_color=TEXTO,
            border_color=BORDA,
            border_width=1,
            corner_radius=12,
            font=("Segoe UI", 11),
            wrap="word"
        )

        self.lista_arquivos.pack(
            fill="both",
            expand=True,
            padx=16,
            pady=4
        )

        # BOTÃO CONVERTER
        self.botao_converter = ctk.CTkButton(
            self.painel_arquivos,
            text="▶  Converter XML",
            command=self.converter_xmls,
            height=48,
            corner_radius=12,
            fg_color=VERDE,
            hover_color=VERDE_ESCURO,
            font=("Segoe UI", 17, "bold")
        )

        self.botao_converter.pack(
            fill="x",
            padx=16,
            pady=12
        )

    # ======================================================
    # PAINEL DE RESULTADOS
    # ======================================================

    def criar_painel_resultados(self):

        self.card_resumo = ctk.CTkFrame(
            self.painel_resultados,
            fg_color=BRANCO,
            corner_radius=18,
            border_width=1,
            border_color=BORDA
        )

        self.card_resumo.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        titulo_resultado = ctk.CTkFrame(
            self.card_resumo,
            fg_color="transparent"
        )

        titulo_resultado.pack(
            fill="x",
            padx=16,
            pady=(13, 6)
        )

        ctk.CTkLabel(
            titulo_resultado,
            text="▥  Resultado da Conversão",
            font=("Segoe UI", 19, "bold"),
            text_color=TEXTO
        ).pack(side="left")

        self.label_status = ctk.CTkLabel(
            titulo_resultado,
            text="● Aguardando",
            font=("Segoe UI", 11, "bold"),
            text_color=CINZA
        )

        self.label_status.pack(side="right")

        grade = ctk.CTkFrame(
            self.card_resumo,
            fg_color="transparent"
        )

        grade.pack(
            fill="x",
            padx=10,
            pady=(3, 12)
        )

        nomes = [
            "Prestadores",
            "Materiais",
            "Medicamentos",
            "Pacotes",
            "Hospital 104",
            "Taxas",
            "Consultas"
        ]

        for indice, nome in enumerate(nomes):

            linha = indice // 3
            coluna = indice % 3

            card = ctk.CTkFrame(
                grade,
                fg_color=VERDE_CLARO,
                corner_radius=12
            )

            card.grid(
                row=linha,
                column=coluna,
                padx=4,
                pady=4,
                sticky="nsew"
            )

            valor = ctk.CTkLabel(
                card,
                text="0",
                font=("Segoe UI", 23, "bold"),
                text_color=VERDE_ESCURO
            )

            valor.pack(pady=(8, 0))

            ctk.CTkLabel(
                card,
                text=nome,
                font=("Segoe UI", 10, "bold"),
                text_color=TEXTO
            ).pack(pady=(0, 8))

            self.cards_resultados[nome] = valor

        for coluna in range(3):
            grade.grid_columnconfigure(coluna, weight=1)

    # ======================================================
    # PAINEL DE LOGS
    # ======================================================

    def criar_painel_logs(self):

        self.card_logs = ctk.CTkFrame(
            self.painel_resultados,
            fg_color=BRANCO,
            corner_radius=18,
            border_width=1,
            border_color=BORDA
        )

        self.card_logs.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        ctk.CTkLabel(
            self.card_logs,
            text="▤  Log de Processamento",
            font=("Segoe UI", 19, "bold"),
            text_color=TEXTO
        ).pack(
            anchor="w",
            padx=16,
            pady=(13, 8)
        )

        self.logs = ctk.CTkTextbox(
            self.card_logs,
            fg_color=LOG_FUNDO,
            text_color="#E5F5EB",
            corner_radius=12,
            border_width=0,
            font=("Consolas", 11),
            wrap="word"
        )

        self.logs.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 12)
        )

        self.adicionar_log(
            "[INFO] Sistema iniciado. Aguardando arquivos XML."
        )

    # ======================================================
    # ATUALIZAÇÃO DOS RESULTADOS
    # ======================================================

    def atualizar_resultados(self):

        for nome, valor in self.resultados.items():

            self.cards_resultados[nome].configure(
                text=str(valor)
            )

    # ======================================================
    # ADICIONAR MENSAGEM NA TELA
    # ======================================================

    def adicionar_log(self, mensagem):

        self.logs.insert("end", mensagem + "\n")
        self.logs.see("end")
        self.update_idletasks()

    # ======================================================
    # SELECIONAR ARQUIVOS
    # ======================================================

    def selecionar_arquivos(self):

        arquivos = filedialog.askopenfilenames(
            title="Selecionar XMLs",
            filetypes=[
                ("Arquivos XML", "*.xml")
            ]
        )

        if arquivos:

            self.arquivos_selecionados = arquivos

            self.lista_arquivos.delete("1.0", "end")

            for arquivo in arquivos:

                nome = os.path.basename(arquivo)

                self.lista_arquivos.insert(
                    "end",
                    f"📄 {nome}\n\n"
                )

            quantidade = len(arquivos)

            self.label_quantidade.configure(
                text=f"Arquivos selecionados ({quantidade})"
            )

            self.adicionar_log(
                f"[INFO] {quantidade} arquivo(s) selecionado(s)."
            )

    # ======================================================
    # LIMPAR ARQUIVOS
    # ======================================================

    def limpar_arquivos(self):

        self.arquivos_selecionados = []

        self.lista_arquivos.delete("1.0", "end")

        self.label_quantidade.configure(
            text="Arquivos selecionados (0)"
        )

        self.adicionar_log(
            "[INFO] Seleção de arquivos limpa."
        )

    # ======================================================
    # CONVERSÃO DOS XMLs
    # ======================================================

    def converter_xmls(self):

        if not self.arquivos_selecionados:

            self.adicionar_log(
                "[AVISO] Nenhum XML selecionado."
            )
            return

        from app.core.leitor_xml import carregar_xml
        from app.core.gerador_xml import salvar_xml

        from app.regras.regra_prestador import prestador as prest
        from app.regras.regra_materiais import materiais as mat
        from app.regras.regra_medicamentos import medicamentos as med
        from app.regras.regra_pacotes import pacotes as p

        from app.core.logger import registrar_log

        self.logs.delete("1.0", "end")

        for nome in self.resultados:
            self.resultados[nome] = 0

        self.atualizar_resultados()

        self.label_status.configure(
            text="● Processando...",
            text_color="#D97706"
        )

        self.botao_converter.configure(
            state="disabled",
            text="Processando..."
        )

        self.adicionar_log(
            "[INFO] Iniciando conversão dos arquivos XML."
        )

        pasta_saida = filedialog.askdirectory(
            title="Selecionar pasta de saída"
        )

        if not pasta_saida:

            self.adicionar_log(
                "[AVISO] Nenhuma pasta de saída selecionada."
            )

            self.label_status.configure(
                text="● Aguardando",
                text_color=CINZA
            )

            self.botao_converter.configure(
                state="normal",
                text="▶  Converter XML"
            )

            return

        arquivos_com_erro = 0
        arquivos_convertidos = 0

        try:

            for caminho_xml in self.arquivos_selecionados:

                try:

                    nome_arquivo = os.path.basename(caminho_xml)

                    self.adicionar_log(
                        f"\n[INFO] Processando: {nome_arquivo}"
                    )

                    # CARREGA XML
                    tree, root = carregar_xml(caminho_xml)

                    if root is None:

                        arquivos_com_erro += 1

                        self.adicionar_log(
                            "[ERRO] Não foi possível carregar o XML."
                        )

                        continue

                    # EXECUTA AS REGRAS EXISTENTES
                    total_prestadores, logs_prestadores = prest(root)

                    total_materiais, logs_materiais = mat(root)

                    total_medicamentos, logs_medicamentos = med(root)

                    total_pacotes, logs_pacotes = p(root)

                    total_cod_104, logs_cod_104 = regra_cod_104(root)

                    # SEPARA AS ALTERAÇÕES DO HOSPITAL 104
                    total_taxas = sum(
                        1 for mensagem in logs_cod_104
                        if mensagem.startswith("Taxas:")
                    )

                    total_consultas = sum(
                        1 for mensagem in logs_cod_104
                        if mensagem.startswith("Consultas:")
                    )

                    # ATUALIZA CONTADORES
                    self.resultados["Prestadores"] += total_prestadores
                    self.resultados["Materiais"] += total_materiais
                    self.resultados["Medicamentos"] += total_medicamentos
                    self.resultados["Pacotes"] += total_pacotes
                    self.resultados["Hospital 104"] += total_cod_104
                    self.resultados["Taxas"] += total_taxas
                    self.resultados["Consultas"] += total_consultas

                    self.atualizar_resultados()

                    # CAMINHO DE SAÍDA
                    caminho_saida = os.path.join(
                        pasta_saida,
                        f"convertido_{nome_arquivo}"
                    )

                    # SALVA XML
                    salvar_xml(
                        tree,
                        root,
                        caminho_saida
                    )

                    # REGISTRA LOGS
                    grupos_logs = [
                        (
                            "PRESTADORES ALTERADOS",
                            logs_prestadores,
                            total_prestadores,
                            "Prestadores"
                        ),
                        (
                            "MATERIAIS ALTERADOS",
                            logs_materiais,
                            total_materiais,
                            "Materiais"
                        ),
                        (
                            "MEDICAMENTOS ALTERADOS",
                            logs_medicamentos,
                            total_medicamentos,
                            "Medicamentos"
                        ),
                        (
                            "PACOTES ALTERADOS",
                            logs_pacotes,
                            total_pacotes,
                            "Pacotes"
                        ),
                        (
                            "CÓDIGOS HOSPITAL 104 ALTERADOS",
                            logs_cod_104,
                            total_cod_104,
                            "Códigos hospital 104"
                        )
                    ]

                    for titulo, mensagens, total, descricao in grupos_logs:

                        registrar_log(
                            caminho_xml,
                            f"\n{titulo}"
                        )

                        for mensagem in mensagens:

                            registrar_log(
                                caminho_xml,
                                mensagem
                            )

                        registrar_log(
                            caminho_xml,
                            f"{descricao} alterados: {total}"
                        )

                    registrar_log(
                        caminho_xml,
                        f"\nXML convertido: {nome_arquivo}"
                    )

                    arquivos_convertidos += 1

                    self.adicionar_log(
                        f"[OK] XML convertido: {nome_arquivo}"
                    )

                    self.adicionar_log(
                        f"[OK] Prestadores alterados: {total_prestadores}"
                    )

                    self.adicionar_log(
                        f"[OK] Materiais alterados: {total_materiais}"
                    )

                    self.adicionar_log(
                        f"[OK] Medicamentos alterados: {total_medicamentos}"
                    )

                    self.adicionar_log(
                        f"[OK] Pacotes alterados: {total_pacotes}"
                    )

                    self.adicionar_log(
                        f"[OK] Hospital 104: {total_cod_104}"
                    )

                    self.adicionar_log(
                        f"[OK] Taxas alteradas: {total_taxas}"
                    )

                    self.adicionar_log(
                        f"[OK] Consultas alteradas: {total_consultas}"
                    )

                    self.adicionar_log(
                        f"[OK] Arquivo salvo em: {caminho_saida}"
                    )

                except Exception as erro:

                    arquivos_com_erro += 1

                    print("ERRO:", erro)

                    self.adicionar_log(
                        f"[ERRO] {nome_arquivo}: {erro}"
                    )

            if arquivos_com_erro == 0:

                self.label_status.configure(
                    text="● Concluído",
                    text_color=VERDE
                )

                self.adicionar_log(
                    "\n[OK] Todas as conversões foram concluídas!"
                )

            else:

                self.label_status.configure(
                    text="● Concluído com erros",
                    text_color="#D97706"
                )

                self.adicionar_log(
                    f"\n[AVISO] Arquivos convertidos: {arquivos_convertidos}"
                    f" | Arquivos com erro: {arquivos_com_erro}"
                )

        finally:

            self.botao_converter.configure(
                state="normal",
                text="▶  Converter XML"
            )
