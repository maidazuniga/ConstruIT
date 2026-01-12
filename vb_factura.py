from typing import Any
import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

def visto_bueno_factura(driver, bot, num_factura, num_orden):
    wait = WebDriverWait(driver, 10)
    bot.registrar_mensaje(f"Validando vb de factura N° {num_factura}...")

    try:
        btn_vb_factura = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='Contable/VBDocumentoContable']")))
        btn_vb_factura.click()

        try:
            wait_popup = WebDriverWait(driver, 3)
            btn_cancelar = wait_popup.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".swal2-cancel")))
            time.sleep(1)
            driver.execute_script("arguments[0].click();", btn_cancelar)
            
        except TimeoutException:
            pass 

        btn_oc = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_COrdenCompraDesdeTxt")))
        btn_oc.click()
        btn_oc.send_keys(num_orden + Keys.ENTER)

        btn_buscar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Label6")))
        btn_buscar.click()

        xpath_select = f"//tr[./td[8]//div[contains(., '{num_orden}')]]/td[6]//select"
        
        try:
            elemento_select = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_select)))
            
            select_estado = Select(elemento_select)
            select_estado.select_by_value("1")

        except TimeoutException:
            bot.registrar_mensaje(f'No se encontró la factura a aprobar')

        time.sleep(1)

        btn_grabar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Label2")))
        btn_grabar.click()
        
        try:
            wait.until(EC.url_contains("Mensaje.aspx"))
        except TimeoutException:
            pass

        bot.registrar_mensaje("Validación exitosa.\n")

        url_base = os.getenv('URL_BASE')
        if not url_base: 
            url_base = "/default.aspx"

        driver.execute_script(f"window.location.href = '{url_base}';")
        time.sleep(2)

    except Exception as e:
        bot.registrar_error(e, "Módulo Contable/VB Factura")
        pass
