import customtkinter as ctk
 

from tkinter import filedialog


# TEMA
ctk.set_appearance_mode("light")

ctk.set_default_color_theme("green")


class TelaPrincipal(ctk.CTk):

    def __init__(self):

        super().__init__()
        
        self.arquivos_selecionados = []

        # CONFIG JANELA
        self.title("Leitor Unimed Itaúna")

        self.geometry("850x650")

        self.configure(
            fg_color="white"
        )

        # LISTA ARQUIVOS
        self.arquivos_selecionados = []

        # BARRA SUPERIOR
        self.barra_topo = ctk.CTkFrame(
            self,
            height=40,
            fg_color="#2FA572",
            corner_radius=0
        )

        self.barra_topo.pack(
            fill="x"
        )

        # TÍTULO BARRA
        self.titulo_barra = ctk.CTkLabel(
            self.barra_topo,
            text="Leitor Unimed Itaúna",
            text_color="white",
            font=("Segoe UI", 16, "bold")
        )

        self.titulo_barra.pack(
            side="left",
            padx=15,
            pady=5
        )

        # TÍTULO PRINCIPAL
        self.label_titulo = ctk.CTkLabel(
            self,
            text="Conversor Unimed Itaúna",
            font=("Segoe UI", 28, "bold"),
            text_color="#2B2B2B"
        )

        self.label_titulo.pack(
            pady=20
        )

        # BOTÃO SELECIONAR
        self.botao_selecionar = ctk.CTkButton(
            self,
            text="Selecionar XMLs",
            command=self.selecionar_arquivos,
            width=220,
            height=40,
            fg_color="#7ED957",
            hover_color="#5CBF2A",
            text_color="white",
            font=("Segoe UI", 14, "bold")
        )

        self.botao_selecionar.pack(
            pady=10
        )

        # ÁREA ARQUIVOS
        self.lista_arquivos = ctk.CTkTextbox(
            self,
            width=700,
            height=180,
            fg_color="#F5F5F5",
            text_color="black",
            border_color="#D9D9D9",
            border_width=1,
            font=("Consolas", 12)
        )

        self.lista_arquivos.pack(
            pady=10
        )

        # BOTÃO CONVERTER
        self.botao_converter = ctk.CTkButton(
            self,
            text="Converter XML",
            command=self.converter_xmls,
            width=220,
            height=40,
            fg_color="#7ED957",
            hover_color="#5CBF2A",
            text_color="white",
            font=("Segoe UI", 14, "bold")
        )

        self.botao_converter.pack(
            pady=10
        )

        # ÁREA LOGS
        self.logs = ctk.CTkTextbox(
            self,
            width=700,
            height=220,
            fg_color="#F5F5F5",
            text_color="black",
            border_color="#D9D9D9",
            border_width=1,
            font=("Consolas", 12)
        )

        self.logs.pack(
            pady=20
        )

    # FUNÇÃO SELECIONAR ARQUIVOS
    def selecionar_arquivos(self):

        arquivos = filedialog.askopenfilenames(

            title="Selecionar XMLs",

            filetypes=[
                ("Arquivos XML", "*.xml")
            ]
        )

        if arquivos:

            self.arquivos_selecionados = arquivos

            self.lista_arquivos.delete(
                "1.0",
                "end"
            )

            for arquivo in arquivos:

                self.lista_arquivos.insert(
                    "end",
                    f"📄 {arquivo}\n"
                )

    # FUNÇÃO CONVERTER XML
    def converter_xmls(self):

        if not self.arquivos_selecionados:

            self.logs.insert(
                "end",
                "Nenhum XML selecionado\n"
            )

            return

        import os

        from app.core.leitor_xml import carregar_xml
        from app.core.gerador_xml import salvar_xml

        from app.regras.regra_prestador import prestador as prest
        from app.regras.regra_materiais import materiais as mat
        from app.regras.regra_medicamentos import medicamentos as med
        from app.regras.regra_pacotes import pacotes as p

        from app.core.logger import registrar_log

        self.logs.delete(
            "1.0",
            "end"
        )
        
        # ESCOLHER PASTA SAÍDA
        pasta_saida = filedialog.askdirectory(

        title="Selecionar pasta de saída"
        )

        if not pasta_saida:

            self.logs.insert(
            "end",
            "Nenhuma pasta selecionada\n"
        )

            return

        for caminho_xml in self.arquivos_selecionados:

            try:

                self.logs.insert(
                    "end",
                    f"\nProcessando:\n{caminho_xml}\n"
                )

                # CARREGA XML
                tree, root = carregar_xml(
                    caminho_xml
                )

                if root is not None:

                    # REGRAS
                    
                    
                    total_prestadores, logs_prestadores = prest(root)
                    
                   
                    total_materiais, logs_materiais = mat(root)

                    total_medicamentos, logs_medicamentos = med(root)

                    total_pacotes, logs_pacotes = p(root)
                    
                    

                    # NOME ARQUIVO
                    nome_arquivo = os.path.basename(
                        caminho_xml
                    )

                    # CAMINHO SAÍDA
                    caminho_saida = os.path.join(
                        pasta_saida,
                        f"convertido_{nome_arquivo}"
                    )
                    print (caminho_saida)
                    # SALVA XML
                    salvar_xml(
                        tree,
                        root,
                        caminho_saida
                    )

                    # LOG PRESTADORES
                    
                    
                    registrar_log(
                        caminho_xml,
                        "\nPRESTADORES ALTERADOS"
                    )

                    for mensagem in logs_prestadores:

                        registrar_log(
                            caminho_xml,
                            mensagem
                        )

                    registrar_log(
                        caminho_xml,
                        f"Prestadores alterados: "
                        f"{total_prestadores}"
                    )

                    # LOG MATERIAIS
                    registrar_log(
                        caminho_xml,
                        "\nMATERIAIS ALTERADOS"
                    )

                    for mensagem in logs_materiais:

                        registrar_log(
                            caminho_xml,
                            mensagem
                        )

                    registrar_log(
                        caminho_xml,
                        f"Materiais alterados: "
                        f"{total_materiais}"
                    )

                    # LOG MEDICAMENTOS
                    registrar_log(
                        caminho_xml,
                        "\nMEDICAMENTOS ALTERADOS"
                    )

                    for mensagem in logs_medicamentos:

                        registrar_log(
                            caminho_xml,
                            mensagem
                        )

                    registrar_log(
                        caminho_xml,
                        f"Medicamentos alterados: "
                        f"{total_medicamentos}"
                    )

                    # LOG PACOTES
                    registrar_log(
                        caminho_xml,
                        "\nPACOTES ALTERADOS"
                    )

                    for mensagem in logs_pacotes:

                        registrar_log(
                            caminho_xml,
                            mensagem
                        )

                    registrar_log(
                        caminho_xml,
                        f"Pacotes alterados: "
                        f"{total_pacotes}"
                    )

                    # FINAL
                    registrar_log(
                        caminho_xml,
                        f"\nXML convertido: "
                        f"{nome_arquivo}"
                    )

                    # TELA
                    self.logs.insert(
                        "end",
                        f"\n✔ XML convertido:\n"
                        f"{nome_arquivo}\n"
                    )

                    self.logs.insert(
                        "end",
                        f"\n✔ Prestadores alterados: "
                        f"{total_prestadores}\n"
                    )

                    self.logs.insert(
                        "end",
                        f"✔ Materiais alterados: "
                        f"{total_materiais}\n"
                    )

                    self.logs.insert(
                        "end",
                        f"✔ Medicamentos alterados: "
                        f"{total_medicamentos}\n"
                    )

                    self.logs.insert(
                        "end",
                        f"✔ Pacotes alterados: "
                        f"{total_pacotes}\n"
                    )

                else:

                    self.logs.insert(
                        "end",
                        "Erro ao carregar XML\n"
                    )

            except Exception as erro:

                print("ERRO:", erro)

                self.logs.insert(
                    "end",
                    f"ERRO:\n{erro}\n"
                )

            self.logs.see("end")