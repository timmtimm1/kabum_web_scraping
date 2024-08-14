import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_product_links(produto_escolhido, headers):
    base_url = 'https://www.kabum.com.br'
    urls = []
    for i in range(1,101):
        a = f'https://www.kabum.com.br/busca/{produto_escolhido}?page_number={i}&page_size=20&facet_filters=&sort=most_searched&variant=catalog'
        urls.append(a)

    product_links = []
    with requests.Session() as s:
        for url in urls:
            r = s.get(url, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            products = soup.find_all('article', class_='sc-9d1f1537-7 hxuzLm productCard')
            for product in products:
                href_tag = product.find('a', class_='sc-9d1f1537-10 kueyFw productLink')
                href = href_tag['href']
                full_url = f"{base_url}{href}"
                product_links.append(full_url)
    return product_links

def clean_price(text):
    return text.replace('\xa0', ' ')

def scrape_single_product(link, headers):
    with requests.Session() as s:
        r = s.get(link, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')

        name = soup.find('h1', class_='sc-58b2114e-6 brTtKt').get_text(strip=True)
        preco_atual_tag = soup.find('h4', class_='sc-5492faee-2 ipHrwP finalPrice')
        preco_atual = clean_price(preco_atual_tag.get_text(strip=True)) if preco_atual_tag else 'N/A'
        preco_antigo_tag = soup.find('span', class_='sc-5492faee-1 ibyzkU oldPrice')
        preco_antigo_text = clean_price(preco_antigo_tag.get_text(strip=True)) if preco_antigo_tag else 'N/A'
        estoque_tag = soup.find('b', class_='sc-477542eb-2 dCSsYX')
        estoque_text = estoque_tag.get_text(strip=True) if estoque_tag else 'N/A'

        return {
            'Nome': name,
            'Preço Atual': preco_atual,
            'Preço Antigo': preco_antigo_text,
            'Em estoque': estoque_text,
            'Link': link
        }

def scrape_product_details_threaded(product_links, headers, max_workers=15):# This is a conservative number for threadworkers it could be raised as you like 
    all_products = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_link = {executor.submit(scrape_single_product, link, headers): link for link in product_links}
        for future in tqdm(as_completed(future_to_link), total=len(product_links), desc="Scraping products"):
            try:
                data = future.result()
                all_products.append(data)
            except Exception as exc:
                print(f'Generated an exception: {exc}')

    return all_products

def save_data(produto_escolhido, all_products):
    # Save as CSV
    df = pd.DataFrame(all_products)
    df.to_csv(f'{produto_escolhido}.csv', index=False)
    
    # Save as JSON
    with open(f'{produto_escolhido}.json', 'w', encoding='utf-8') as f:
        json.dump(all_products, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    produto_escolhido = 'smartphone'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://www.kabum.com.br/busca/teclados',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Opera GX";v="112"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0 (Edition std-1)',
    }

    product_links = get_product_links(produto_escolhido, headers)
    print(f"Total products to scrape: {len(product_links)}")
    all_products = scrape_product_details_threaded(product_links, headers)
    save_data(produto_escolhido, all_products)
    print(f"Scraping completed. Data saved in {produto_escolhido}.csv and {produto_escolhido}.json")