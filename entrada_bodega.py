from typing import Any
import time
import os
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def entrada(driver, bot, num_orden):
    wait = WebDriverWait(driver, 10)
    bot.registrar_mensaje("Validando entrada a bodega...")

    try:
        selector = (By.XPATH, "//a[text()='Entrada' and contains(@href, 'Bodega/EntradaABodega')]")
        btn_entrada = wait.until(EC.element_to_be_clickable(selector))
        btn_entrada.click()

        tipo_entrada = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_EntradaOCRB")))
        tipo_entrada.click()

        ingresar_orden = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_OrdenCompraNumerotxt")))
        ingresar_orden.send_keys(num_orden)
        time.sleep(1)
        btn_lupa = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@onclick, 'OrdenCompraSetByNumero')]//img")))
        driver.execute_script("arguments[0].click();", btn_lupa)
        time.sleep(2)

        num_documento = wait.until(EC.presence_of_element_located((By.ID, "ctl00_phContenidoCentral_NumeroDocumentoTxt")))
        num_documento.send_keys(str(random.randint(1000, 9999)))

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ob_gR")))
        
        filas_recursos = driver.find_elements(By.XPATH, "//tr[contains(@class, 'ob_gR') and normalize-space(./td[5])!='']")
        
        for fila in filas_recursos:
            try:
                cantidad_pnl = fila.find_element(By.XPATH, ".//td[5]//div[contains(@id, 'Cantidadpnl')]")
                cantidad_pnl.click()
                
                input_cantidad = fila.find_element(By.XPATH, ".//td[5]//input[contains(@id, 'CantidadTxt')]")
                wait.until(EC.visibility_of(input_cantidad))
                
                time.sleep(0.5) 
                input_cantidad.send_keys(Keys.CONTROL + "a")
                input_cantidad.send_keys("5")
                input_cantidad.send_keys(Keys.TAB)
                time.sleep(0.5)
            except Exception:
                continue

        btn_grabar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Label2")))
        btn_grabar.click()
        bot.frenar_si_duplicado(driver)

        lbl_mensaje = wait.until(EC.visibility_of_element_located((By.ID, "ctl00_phContenidoCentral_MensajeLbl")))
        enlace_numero = lbl_mensaje.find_element(By.TAG_NAME, "a")
        num_entrada = enlace_numero.text.strip()

        bot.registrar_mensaje("Validación exitosa.\n")

        driver.get(os.getenv('URL_BASE'))
        time.sleep(2)
        return num_entrada

    except Exception as e:
        bot.registrar_error(e, "Módulo de Stock/Entrada")
        pass