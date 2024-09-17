from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
)
from commons import config, selectors
from loguru import logger as log


class Transparencia:
    def __init__(self, headless, url, remote_url=None):
        """
        Initializes the Transpacencia object.

        Args:
            headless (bool): Whether to run the Chrome browser in headless mode.
            url (str): The URL to navigate to.
            remote_url (str, optional): The URL of a remote WebDriver server. Defaults to None.
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": config.DOWNLOAD_FOLDER,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "plugins.always_open_pdf_externally": True,
            },
        )
        # chrome_options.binary_location = "/usr/bin/google-chrome"
        chrome_options.add_argument("--window-size=1280,1024")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        )
        if headless:
            log.info("Executando headless")
            chrome_options.add_argument("--headless")

        if remote_url:
            log.info("Executando em modo remoto")
            self.driver = webdriver.Remote(
                command_executor=remote_url, options=chrome_options
            )
        else:
            self.driver = webdriver.Chrome(options=chrome_options)
        log.info("Navegando para URL da EDP")
        self.__go_to_url(url)

    def __go_to_url(self, url: str) -> None:
        """
        Navigates to the specified URL.

        Args:
            url (str): The URL to navigate to.

        Returns:
            None
        """
        log.info(f"Acessando {url}")
        self.driver.get(url)

    def wait_element(self, selector, timeout=10):
        """
        Waits for an element to be clickable.

        Args:
            selector (str): The selector of the element to wait for.
            timeout (int, optional): The maximum time to wait in seconds. Defaults to 10.

        Raises:
            TimeoutException: If the element is not found within the specified timeout.

        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((selector))
            )
        except TimeoutException:
            print(f"Elemento não encontrado: {selector}")

    def get_element(self, selector):
        """
        Retrieves the element specified by the given selector.

        Args:
            selector: A tuple representing the selector used to locate the element.

        Returns:
            The element found using the given selector.

        Raises:
            NoSuchElementException: If the element specified by the selector is not found.
        """
        self.wait_element(selector)
        return self.driver.find_element(*selector)

    def get_elements(self, selector):
        """
        Retrieves a list of elements that match the given selector.

        Args:
            selector: A tuple representing the selector used to locate the elements.

        Returns:
            A list of elements that match the given selector.
        """
        self.wait_element(selector)
        return self.driver.find_elements(*selector)

    def close(self):
        """
        Closes the driver and quits the browser.
        """
        self.driver.quit()

    def pesquisar_processo(self, processo: str) -> None | str:
        """
        Searches for a specific process.

        Args:
            processo (str): The process to search for.

        Returns:
            link (str): The link to the process found.

        Raises:
            Exception: If the process is not found.
            TimeoutError: If a timeout occurs while searching for the process.
        """
        pass
        log.info(f"Buscando processo {processo}")
        try:
            for _ in range(5):
                try:
                    log.info("Carregando a pagina")
                    self.wait_element((By.CSS_SELECTOR, selectors.TITULO), 30)
                    log.info("Limpando a busca")
                    self.get_element((By.XPATH, selectors.LIMPAR_TUDO)).click()
                    log.info("Inserindo o processo")
                    self.wait_element((By.XPATH, selectors.PESQUISA), 30)
                    self.get_element((By.XPATH, selectors.PESQUISA)).send_keys(processo)
                    log.info("Pesquisando Processo")
                    self.get_element((By.XPATH, selectors.PESQUISAR)).click()
                    break
                except NoSuchElementException:
                    log.error("Elemento não visivel")
                    continue
                except TimeoutError:
                    log.error("Timeout ao buscar processo")
                    continue
            log.info("Validando o resultado")
            link = self.get_element((By.XPATH, selectors.PRIMEIRO_RESULTADO))
            if link:
                return link.get_attribute("href")  # type: ignore
            else:
                raise Exception("Processo não encontrado")
        except TimeoutError:
            log.error("Timeout ao buscar processo")

    def abrir_processo(self, link: str = ''):
        """
        Opens a new process in the web browser.

        Args:
            link (str, optional): The link to the process. Defaults to ''.

        Raises:
            Exception: If the link is not provided.

        Returns:
            None
        """
        if len(link)>0:
            self.driver.get(link)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.wait_element((By.XPATH, selectors.TABELA_INFO_PROCESSO))
        else:
            raise Exception("Link não informado")

    def extrair_tabelas_dados_processo(self) -> dict:
        """
        Extracts information from the process table.

        Returns:
            dict: A dictionary containing the extracted data from the process table.
        """
        log.info("Extraindo informações do processo")
        linhas_tabela = self.get_elements(
            (By.XPATH, selectors.LINHAS_TABELA_INFO_PROCESSO)
        )
        dados = {}
        for linha in linhas_tabela:
            log.info(f"Extraindo linha {linha.text}")
            colunas = linha.find_elements(By.XPATH, ".//td")
            log.debug(f"""Colunas: {" ".join([coluna.text for coluna in colunas])}""")
            dados[colunas[0].text] = (
                colunas[1].text if len(colunas[1].text) > 0 else colunas[2].text
            )
        return dados

    def extrair_movimentacoes(self) -> list:
        """
        Extracts the movements from the table and returns a list of dictionaries containing the data and description of each movement.

        Returns:
            list: A list of dictionaries, where each dictionary represents a movement with the following keys:
                - "data": The date of the movement.
                - "descricao": The description of the movement.
        """
        log.info("Extraindo movimentações")
        linhas_tabela = self.get_elements(
            (By.XPATH, selectors.LINHAS_TABELA_MOVIMENTACOES)
        )
        dados = []
        for linha in linhas_tabela:
            log.info(f"Extraindo linha {linha.text}")
            colunas = linha.find_elements(By.XPATH, ".//td")
            log.debug(f"""Colunas: {" ".join([coluna.text for coluna in colunas])}""")
            if len(colunas) > 0:
                dados.append(
                    {
                        "data": colunas[0].text,
                        "descricao": colunas[2].text,
                    }
                )
        return dados
