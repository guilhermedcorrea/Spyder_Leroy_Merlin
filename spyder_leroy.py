import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from typing import Any

import sys
try:

    sys.path.append(r'D:\app_scraping')
except:
    pass

from models.tables import insert_or_update_products

def random_delay() -> float:
    return random.uniform(0.5, 3.0)

def random_sleep() -> int:
    return random.randint(4, 15)

def retry_on_error(func: Any, max_attempts: Any, wait_time=10):
    attempts = 0
    while attempts < max_attempts:
        try:
            func()
            break
        except Exception as e:
            attempts += 1
            print(f"Erro durante a execução ({attempts}/{max_attempts}): {e}")
            if attempts < max_attempts:
                driver.delete_all_cookies()
                driver.refresh()
                time.sleep(random_sleep())
            else:
                print("Não foi possível concluir a tarefa após várias tentativas.")
                break

def click_last_page_button(driver: Any) -> (int | None):
    try:
        button = driver.find_element(By.XPATH, "/html/body/div[7]/div[4]/div[1]/div[2]/div[4]/nav/button[2]/i")
        button.click()
        WebDriverWait(driver, 10).until(EC.staleness_of(button))

        last_page_url = driver.current_url
        last_page_number = int(last_page_url.split("page=")[-1])

        return last_page_number

    except Exception as e:
        print("Erro ao clicar no botão da última página:", e)
        return None

def click_and_get_urls(driver: Any) -> (list[Any] | list):
    try:
        urls_products = driver.find_elements(By.XPATH, "/html/body/div/div/div/div/div/div/div/div/div/div/a")
        return [urls.get_attribute("href") for urls in urls_products]
    except Exception as e:
        print("Erro ao obter URLs:", e)
        return []

def extract_page_number_from_url(url: Any) ->  (int | None):
    try:
        page_number = int(url.split("page=")[-1])
        return page_number
    except Exception as e:
        print("Erro ao extrair número da página da URL:", e)
        return None

def extract_start_page_number(url: Any) ->  (int | None):
    try:
        start_page_number = int(url.split("page=")[-1])
        return start_page_number
    except Exception as e:
        print("Erro ao extrair número da página inicial da URL:", e)

def scroll() -> None:
    driver.implicitly_wait(7)
    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False
    while not match:
        lastCount = lenOfPage
        lenOfPage = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount == lenOfPage:
            match = True

def make_request(driver: Any, url: Any) -> None:
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": random.choice(user_agents)})
    time.sleep(random_delay())
    driver.get(url)
    time.sleep(random_delay())
    scroll()

def extract_product_details(driver: Any) -> dict:
    
    driver.implicitly_wait(30)
    product_dict = {}
    
    try:
        nome = driver.find_elements(By.XPATH,"/html/body/div[10]/div/div[1]/div[1]/div/div[1]/h1")[0].text
        product_dict["nome"] = nome
    except:
        pass
    
   
    try:
        precos = driver.find_elements(By.XPATH,"/html/body/div[10]/div/div[1]/div[2]/div[2]/div/div[1]/div/div[2]/div[2]/div/span[1]")[0].text
        product_dict["precos"] = float(precos.replace("R$","").replace(",","").replace(",",".").strip())
        
    except:
        pass

    try:
        preco_detalhes = driver.find_elements(
            By.XPATH,"/html/body/div[10]/div/div[1]/div[2]/div[2]/div/div[1]/div/div[3]/div/strong")[0].text
        product_dict["detalhespreco"] = preco_detalhes
        
    except:
        pass
    try:
        descricao = driver.find_elements(
            By.XPATH,"/html/body/div[10]/div/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/div/div/p")[0].text
        product_dict["descricao"] = descricao
    except:
        pass

    imagens = driver.find_elements(
        By.XPATH,"//div[@class='css-17kvx2v-wrapper__image-wrapper ejgu7z2']//img")
    cont = 0
    for imagem in imagens:
        product_dict["imagem"+str(cont)] = imagem.get_attribute(
            "src").replace("140x140.jpg","600x600.jpg").replace("140x140.jpeg","600x600.jpeg")
        cont+=1
    
    
    referencias = driver.find_elements(
        By.XPATH,"/html/body/div[10]/div/div[4]/div[2]/table/tbody/tr/th")
    atributos = driver.find_elements(
        By.XPATH,"/html/body/div[10]/div/div[4]/div[2]/table/tbody/tr/td")
    cont = 0
    for referencia in referencias:
        product_dict[referencia.text] = atributos[cont].text
        cont+=1

    return product_dict
   

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--lang=en-US")
    options.add_argument("accept-encoding=gzip, deflate, br")
    options.add_argument("referer=https://www.google.com/")

    base_url = "https://www.leroymerlin.com.br/porcelanatos?term=porcelanato&searchTerm=porcelanato&searchType=Shortcut&page="
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
    ]
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.implicitly_wait(10)

        driver.get("https://www.leroymerlin.com.br/")
        KEY = driver.find_element(By.CSS_SELECTOR, 'input[aria-autocomplete="list"]')
        KEY.send_keys("Porcelanato")
        VALLUE = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Buscar"]').click()

        time.sleep(5)

        def click_last_page_button(driver: Any) -> (int | None):
            try:
                button = driver.find_element(By.XPATH, "/html/body/div[7]/div[4]/div[1]/div[2]/div[4]/nav/button[2]/i")
                button.click()
                WebDriverWait(driver, 10).until(EC.staleness_of(button))
               
                last_page_url = driver.current_url
                last_page_number = int(last_page_url.split("page=")[-1])

                return last_page_number

            except Exception as e:
                print("Erro ao clicar no botão da última página:", e)
                return None

        last_page_number = click_last_page_button(driver)

        all_urls = []

        if last_page_number is not None:
            for page_number in range(1, last_page_number + 1):
                page_url = base_url + str(page_number)
                make_request(driver, page_url)
                page_urls = click_and_get_urls(driver)
                all_urls.extend(page_urls)

        print("URLs coletadas:")
        for url in all_urls:
            print(url)

        products = []

        for url in all_urls:
            make_request(driver, url)
            product = extract_product_details(driver)
            
            insert_or_update_products(nome=product['nome'],detalhespreco=product['detalhespreco']
                                      ,descricao=product['descricao'],precos=product['precos'])
            
            
            products.append(product)

        print("Detalhes dos produtos:")
        for product in products:
            ...
            

    finally:
        driver.quit()