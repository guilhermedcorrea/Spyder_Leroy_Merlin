import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def random_delay():
    return random.uniform(0.5, 3.0)

def random_sleep():
    return random.randint(4, 15)

def retry_on_error(func, max_attempts, wait_time=10):
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

def click_last_page_button(driver):
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

def click_and_get_urls(driver):
    try:
        urls_products = driver.find_elements(By.XPATH, "/html/body/div/div/div/div/div/div/div/div/div/div/a")
        return [urls.get_attribute("href") for urls in urls_products]
    except Exception as e:
        print("Erro ao obter URLs:", e)
        return []

def extract_page_number_from_url(url):
    try:
        page_number = int(url.split("page=")[-1])
        return page_number
    except Exception as e:
        print("Erro ao extrair número da página da URL:", e)
        return None

def extract_start_page_number(url):
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

def make_request(driver, url):
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": random.choice(user_agents)})
    time.sleep(random_delay())
    driver.get(url)
    time.sleep(random_delay())
    scroll()

def extract_product_details(driver):
    
    driver.implicitly_wait(30)
    
    try:
        nome = driver.find_elements(By.XPATH,"/html/body/div[10]/div/div[1]/div[1]/div/div[1]/h1")[0].text
        print(nome)
    except:
        print("Error nome produto")
        
    try:
        preco = driver.find_elements(By.XPATH,"/html/body/div[10]/div/div[1]/div[2]/div[2]/div/div[1]/div/div[3]/div[1]/div/p")[0].text
        print(preco)
    except:
        print("error preco produto")
        
    try:
        imagens = driver.find_elements(By.XPATH,"/html/body/div[10]/div/div[1]/div[2]/div[1]/div[1]/div[1]/div[3]/div/div[1]/div[2]/div/div/div/div/div/img")
        cont = 0
        for imagem in imagens:
            print(imagem[cont].get_attribute("src"))
        cont+=1
    except:
        print("errror imagem")
        
    
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

        def click_last_page_button(driver):
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
            products.append(product)

        print("Detalhes dos produtos:")
        for product in products:
            print(product)

    finally:
        driver.quit()