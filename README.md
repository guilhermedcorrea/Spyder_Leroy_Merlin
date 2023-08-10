SPYDER Leroy Merlin

Informa a categoria a ser buscada


```Python
 driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.implicitly_wait(10)

        driver.get("https://www.leroymerlin.com.br/")
        KEY = driver.find_element(By.CSS_SELECTOR, 'input[aria-autocomplete="list"]')
        KEY.send_keys("Porcelanato")
        VALLUE = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Buscar"]').click()

        time.sleep(5)


```

a partir disso, ele starta e pesquisa, com a pesquisa feita entra na pagina e coleta a quantidade de paginas que tem porcelanatos

Faz um laço com um range e a quantidade extraida e começa a percorrer as paginas extraindo os produtos



```Python
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
                
                # Extract the last page number from the URL
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

    finally:
        driver.quit()
```