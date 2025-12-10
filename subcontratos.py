from typing import Any
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def validar_contratos(driver, bot):
    wait = WebDriverWait(driver, 10)
    bot.registrar_mensaje("Validando contratos...")

    try:
        btn_contrato = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='SubContrato/Contrayos']")))
        btn_contrato.click()

        elemento_titulo = wait.until(EC.presence_of_element_located((By.ID, "ctl00_phContenidoCentral_SAvancesSubContratosLbl")))
        texto_real = elemento_titulo.text.strip()
        texto_esperado = "Contratos"

        if texto_real == texto_esperado:
            bot.registrar_mensaje(f"Validación exitosa.\n")
        else:
            bot.registrar_mensaje(f"ERROR: Se esperaba '{texto_esperado}' pero se encontró '{texto_real}'", es_error=True)

        time.sleep(1)
        
        driver.back()
        time.sleep(2)
    except Exception as e:
        bot.registrar_error(e, "Módulo Subcontratos")
        raise e


