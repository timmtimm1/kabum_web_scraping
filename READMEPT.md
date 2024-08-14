# Kabum Product Scraper

Este projeto é uma ferramenta de web scraping desenvolvida para extrair informações de produtos do site da Kabum. Ele recupera detalhes como o nome do produto, preço atual, preço antigo (se disponível), status de estoque e o link do produto. Os dados raspados são então salvos em um arquivo CSV e um arquivo JSON para análise posterior.

## Recursos

- **Raspagem de Múltiplas Páginas**: A ferramenta navega por várias páginas de resultados de busca para reunir dados abrangentes sobre os produtos.
- **Web Scraping Dinâmico**: Utiliza as bibliotecas `BeautifulSoup` e `requests` para analisar o conteúdo HTML e extrair as informações relevantes.
- **Raspagem Multithreaded**: O scraper utiliza threads para melhorar a eficiência e reduzir o tempo necessário para coletar os dados.
- **Exportação de Dados**: Os dados raspados são automaticamente salvos em arquivos CSV e JSON para fácil acesso e análise.

## Como Funciona

### Extração de Links de Produtos
- O script gera uma lista de URLs com base na consulta de busca para o produto escolhido.
- Em seguida, ele busca os links dos produtos em cada página de resultados.

### Raspagem de Detalhes do Produto
- Para cada link de produto, o script visita a página do produto e coleta os detalhes necessários, como nome, preço, status de estoque, etc.

### Processamento Multithreaded
- A função `scrape_product_details_threaded` usa o `ThreadPoolExecutor` do Python para raspar detalhes dos produtos de forma concorrente, tornando o processo mais rápido e eficiente.

### Armazenamento de Dados
- Os dados extraídos são armazenados em formatos CSV e JSON, nomeados de acordo com o produto pesquisado, na pasta especificada.

### Função `scrape_product_details_threaded`
Esta função gerencia o processo de scraping usando múltiplas threads, permitindo uma coleta de dados mais rápida. Ela utiliza o `ThreadPoolExecutor` para executar várias threads simultaneamente, cada thread responsável por raspar uma página de produto. Os resultados são processados à medida que ficam disponíveis, e quaisquer erros são capturados e impressos sem interromper o processo de scraping como um todo.

## Instalação

Para usar este projeto, você precisa ter o Python instalado em seu sistema. Em seguida, instale as bibliotecas Python necessárias:

```bash
pip install requests pandas beautifulsoup4 tqdm
