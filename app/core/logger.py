import logging
import os


def registrar_log(nome_arquivo, mensagem):

    if not os.path.exists("logs"):
        os.makedirs("logs")

    nome_base = os.path.basename(
        nome_arquivo
    )

    nome_sem_extensao = os.path.splitext(
        nome_base
    )[0]

    caminho_log = (
        f"logs/{nome_sem_extensao}.log"
    )

    logger = logging.getLogger(
        nome_sem_extensao
    )

    logger.setLevel(logging.INFO)

    if not logger.handlers:

        file_handler = logging.FileHandler(
            caminho_log,
            encoding="utf-8"
        )

        formatter = logging.Formatter(
            "%(asctime)s - %(message)s"
        )

        file_handler.setFormatter(
            formatter
        )

        logger.addHandler(
            file_handler
        )

    logger.info(mensagem)

    print(mensagem)