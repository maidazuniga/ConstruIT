from typing import Any
import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def visto_bueno_contrato(driver, bot, num_contrato):
    wait = WebDriverWait(driver, 10)
    bot.registrar_mensaje(f"Validando visto bueno de contrato N° {num_contrato}...")

    try:       
        btn_vb_contrato = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='SubContrato/VBContrato']")))
        btn_vb_contrato.click()

        try:
            wait_popup = WebDriverWait(driver, 3)
            btn_cancelar = wait_popup.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".swal2-cancel")))
            time.sleep(1)
            driver.execute_script("arguments[0].click();", btn_cancelar)
            
        except TimeoutException:
            pass 
        
        wait.until(EC.presence_of_element_located((By.ID, "ctl00_phContenidoCentral_VBNominaLbl")))

        btn_buscar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Label6")))
        btn_buscar.click()

        time.sleep(1)

        xpath_contrato = f"//tr[./td[2]//div[normalize-space(.)='{num_contrato}']]/td[6]//select"
        select_estado = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_contrato)))
        select_estado.click()

        time.sleep(0.5) 
    
        opcion_aprobado = select_estado.find_element(By.XPATH, ".//option[@value='1']")
        opcion_aprobado.click()

        time.sleep(1.5)

        btn_grabar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Label2")))
        btn_grabar.click()

        bot.registrar_mensaje("Validación exitosa.\n")
        
        try:
            wait.until(EC.url_contains("Mensaje.aspx"))
        except TimeoutException:
            pass
        
        url_base = os.getenv('URL_BASE')
        if not url_base: 
            url_base = "/default.aspx"

        driver.execute_script(f"window.location.href = '{url_base}';")

        time.sleep(2)

    except Exception as e:
        bot.registrar_error(e, "Módulo SubContrato/VB Contrato")
        pass
