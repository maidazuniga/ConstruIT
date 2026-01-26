from typing import Any
import time
import os
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def registro_factura(driver, bot, num_orden):
    wait = WebDriverWait(driver, 10)
    bot.registrar_mensaje(f"Validando registro de factura {num_orden}...")

    try:
        btn_factura = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='Contable/DocumentoContable']")))
        btn_factura.click()

        orden = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_OrdenesCompraTxt"))) 
        orden.send_keys(num_orden)   
        cargar_datos = wait.until(EC.presence_of_element_located((By.ID, "ctl00_phContenidoCentral_Label18")))
        cargar_datos.click()
        time.sleep(1.5)

        num_documento = wait.until(EC.presence_of_element_located((By.ID, "ctl00_phContenidoCentral_NroDocumentoTxt")))
        num_documento.send_keys(str(random.randint(0000, 99999)))
        time.sleep(0.5)

        btn_grabar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Label2")))
        btn_grabar.click()
        bot.frenar_si_duplicado(driver)

        lbl_mensaje = wait.until(EC.visibility_of_element_located((By.ID, "ctl00_phContenidoCentral_MensajeLbl")))
        enlace_numero = lbl_mensaje.find_element(By.TAG_NAME, "a")
        num_factura = enlace_numero.text.strip()

        bot.registrar_mensaje("Validación exitosa.\n")

        driver.get(os.getenv('URL_BASE'))
        time.sleep(2)
        return num_factura

    except Exception as e:
        bot.registrar_error(e, "Módulo de Contable/Registro de Factura")
        pass
