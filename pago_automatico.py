from typing import Any
import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def pago_automatico(driver, bot, num_documento):
    wait = WebDriverWait(driver, 10)
    bot.registrar_mensaje(f"Validando pago automático N°{num_documento}...")

    try:
        btn_pago = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='Contable/PagoAutomatico']")))
        btn_pago.click()

        wait.until(EC.presence_of_element_located((By.ID, "ctl00_phContenidoCentral_PagoAutomaticoLbl")))

        try:
            input_trigger = wait.until(EC.element_to_be_clickable((By.ID, "ob_iDdlNNominaDdlTB")))
            input_trigger.click()
            wait.until(EC.visibility_of_element_located((By.ID, "ob_iDdlNNominaDdlItemsContainer")))

            xpath_opcion = f"//div[@id='ob_iDdlNNominaDdlItemsContainer']//div[@class='t' and normalize-space(.)='{num_documento}']"
            
            opcion = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_opcion)))
            opcion.click()

        except TimeoutException:
            bot.registrar_mensaje(f"No se encontró la nómina en la lista o el menú no se abrió.", es_error=True)

        btn_buscar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Label6")))
        btn_buscar.click()

        time.sleep(3)

        btn_grabar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Label2")))
        btn_grabar.click()

        lbl_mensaje = wait.until(EC.visibility_of_element_located((By.ID, "ctl00_phContenidoCentral_MensajeLbl")))
        enlace_numero = lbl_mensaje.find_element(By.TAG_NAME, "a")
        texto_completo = enlace_numero.text.strip()
        comprobante = texto_completo.split(':')[-1].strip()

        bot.registrar_mensaje("Validación exitosa.\n")

        driver.get(os.getenv('URL_BASE'))
        time.sleep(2)
        return comprobante

    except Exception as e:
        bot.registrar_error(e, "Módulo Contable/Pago Automático")
        pass
