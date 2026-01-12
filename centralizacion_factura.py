from datetime import datetime
from typing import Any
import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

fecha = datetime.now().strftime("%m/%d/%Y")

def centralizar_factura(driver, bot, num_factura):
    wait = WebDriverWait(driver, 10)
    actions = ActionChains(driver)
    bot.registrar_mensaje(f"Validando centralizacion de factura...")

    try:
        selector = (By.XPATH, "//a[text()='Centraliza Fact-NC-ND-BH' and contains(@href, 'Contable/ContabilizacionAutomatica')]")
        btn_centralizar = wait.until(EC.element_to_be_clickable(selector))
        btn_centralizar.click()

        campo_fecha = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_FechaVoucherTxt")))
        actions.double_click(campo_fecha).click(campo_fecha).send_keys(Keys.BACKSPACE).send_keys(fecha).perform()

        btn_buscar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Label6")))
        btn_buscar.click()

        time.sleep(0.5)

        box_factura = f"//tr[./td[5]//div[contains(., '{num_factura}')]]/td[2]//input[@type='checkbox']"
        factura = wait.until(EC.element_to_be_clickable((By.XPATH, box_factura)))
        factura.click()

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
        bot.registrar_error(e, "Módulo Contable/Centralización Factura")
        pass
