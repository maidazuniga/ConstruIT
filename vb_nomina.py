from typing import Any
import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def visto_bueno_nomina(driver, bot, num_documento):
    wait = WebDriverWait(driver, 10)
    bot.registrar_mensaje(f"Validando vb de nomina N°{num_documento}...")

    try:
        btn_nomina = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='Contable/VBNomina']")))
        btn_nomina.click()

        btn_buscar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Label6")))
        btn_buscar.click()

        time.sleep(1)

        xpath_nomina = f"//tr[./td[1]//div[normalize-space(.)='{num_documento}']]/td[10]//a"
        select_recurso = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_nomina)))
        select_recurso.click()

        iframe_generico = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "iframe")))
        driver.switch_to.frame(iframe_generico)

        box_click = wait.until(EC.element_to_be_clickable((By.ID, "ticketCab")))
        box_click.click()
        time.sleep(1)

        guardar_doc = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Grabar2Btn")))
        guardar_doc.click()
        driver.switch_to.default_content()

        time.sleep(3)

        xpath_orden = f"//tr[./td[1]//div[normalize-space(.)='{num_documento}']]/td[4]//select"
        select_estado = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_orden)))
        select_estado.click()

        time.sleep(0.5) 
    
        opcion_aprobado = select_estado.find_element(By.XPATH, ".//option[@value='1']")
        opcion_aprobado.click()

        time.sleep(1.5)

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
        bot.registrar_error(e, "Módulo Contable/VB Nomina")
        pass