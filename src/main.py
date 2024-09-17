"""
Main Workflow
This function is the main workflow of the program. It processes the given process number and performs the following steps:
1. Searches for the process number in the transparency system.
2. If the process number is found, opens the process.
3. Extracts initial data and movement data from the process.
4. Saves the extracted data as a JSON file.
5. Closes the transparency system.
Parameters:
- processo (str): The process number to be processed.
- headless (bool): Flag indicating whether to run the process in headless mode or not. Defaults to True.
Returns:
None
Raises:
- Exception: If no process number is provided.
"""
from libs import transpacencia
from commons import config
from loguru import logger as log
import json
import argparse
import os


def create_folders(folders: list):
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)


def main_workflow(processo: str = "", headless: bool = True):
    try:
        if len(processo) > 0:
            log.info("Processando o processo: {processo}")

            transp_flow = transpacencia.Transparencia(
                headless=headless, url=config.URL, remote_url=config.REMOTE_URL
            )
            link = transp_flow.pesquisar_processo(processo.strip())
            if link:
                transp_flow.abrir_processo(link=link)
            else:
                log.error(f"Processo {processo} não foi encontrado")
                return
            # dados_processo = transp_flow.extrair_dados_iniciais()
            dados_processo = transp_flow.extrair_tabelas_dados_processo()
            dados_movimentacoes = transp_flow.extrair_movimentacoes()
            log.debug(dados_processo)
            log.debug(dados_movimentacoes)
            dados_processo["movimentacoes"] = dados_movimentacoes
            json_resultado = json.dumps(dados_processo, ensure_ascii=False, indent=4)
            with open(
                os.path.join(config.OUTPUT_FOLDER, f"{processo.strip()}.json"), "w"
            ) as f:
                f.write(json_resultado)
            transp_flow.close()  # type: ignore
        else:
            log.error("Nenhum processo foi informado, encerrando execução")
            raise Exception("Processo não informado")
    except Exception as e:
        log.error(f"Erro ao executar o fluxo principal {str(e)}")
        transp_flow.close()  # type: ignore


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-p", "--processo", type=str, action="append", help="Número do processo"
    )
    parser.add_argument("-f", "--file", help="Arquivo com lista de processos")
    parser.add_argument("-d", "--debug", help="Ativa o modo debug", action="store_true")
    args = parser.parse_args()
    # Criando as pastas
    create_folders([config.DOWNLOAD_FOLDER, config.OUTPUT_FOLDER])
    if args.debug:
        HEADLESS = False
    else:
        HEADLESS = True
    if args.processo:
        for processo in args.processo:
            main_workflow(processo)
    elif args.file:
        with open(args.file, "r") as f:
            processos = f.readlines()
            for processo in processos:
                main_workflow(processo)
