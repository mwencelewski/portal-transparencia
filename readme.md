# Desafio Técnico DWLAW - Extração de dados Portal Transparência

## Descrição

O projeto de _Extração de dados Portal Transparência_ é uma solução automatizada para a extração de informações de processos públicos do portal da transparência. A aplicação permite que o usuário forneça o número do processo e um json com nome do processo será criado na pasta Output com os dados extraidos.

## Estrutura do Projeto

- `src/`: Contém todos os scripts Python que constituem a aplicação principal.
  - `src/main.py`: O script principal que inicia a aplicação.
  - `src/output/`: Diretório de saída da automação
  - `src/downloads/`: Diretório onde são armazenados os arquivos baixados pela aplicação.
- `Pipfile`: Gerenciador de dependências utilizado no projeto.
- `dockerfile`: Configuração para a construção da imagem Docker do projeto.
- `docker-compose.yml`: Configuração para orquestrar contêineres Docker para o projeto.
- `.gitignore`: Arquivo que especifica quais arquivos ou diretórios devem ser ignorados pelo Git.
- `.dockerignore`: Arquivo que especifica quais arquivos ou diretórios devem ser ignorados pelo Docker.

## Instalação

### Pré-requisitos

- [Python 3.10.7](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [Git](https://git-scm.com/)

### Passos para Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/mwencelewski/portal-transparencia.git
   cd portal-transparencia
   ```

2. Instale as dependências utilizando o Pipenv:

   ```bash
   pipenv install
   ```
3. Crie um arquivo .env dentro src/
    ``` bash
    URL = "http://apps.mpf.mp.br/aptusmpf/portal"
    REMOTE_URL =""
    ```
    **Atenção: Se quiser rodar localmente deixe a variavel REMOTE_URL vazia, caso queira apontar para um browser remoto, inserir a url.**
3. Para executar a aplicação localmente:
   - 3.1 - Utilizando arquivo de entrada
        ```bash
            pipenv run python src/main.py -f <path_arquivo>.txt 
        ```
   - 3.2 - Utilizando processos

        ```bash
            pipenv run python src/main.py -p processo1 -p processo2
        ```

### Usando Docker

1. Construa a imagem Docker:

   ```bash
   docker build -t transparencia .
   ```
2. Parametrizando Docker Compose
    ```yml
        app:
        build:
        context: .
        dockerfile: Dockerfile
        environment:
        - SELENIUM_URL=http://selenium:4444
        env_file:
        - ./src/.env
        # Coloque o número da instalação e Mês que deseja extrair
        command: python -m pipenv run python src/main.py --numero_instalacao 12345678 --mes 03/2024
    ```
3. Execute a aplicação com Docker Compose:
   ```bash
   docker-compose up
   ```


