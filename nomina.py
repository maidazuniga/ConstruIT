from datetime import datetime
from typing import Any
import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

mes_pago = datetime.now().month + 1
if mes_pago > 12:
    mes_pago -= 12
    ano_pago = datetime.now().year + 1
else:
    ano_pago = datetime.now().year
fecha_pago = datetime.now().strftime(f"{datetime.now().day:02d}-{mes_pago:02d}-{ano_pago}")
fecha_actual = datetime.now().strftime(f"%d-%m-%Y")

def nomina(driver, bot, num_documento):
    wait = WebDriverWait(driver, 10)
    bot.registrar_mensaje(f"Validando nomina...")

    try:
        btn_nomina = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='Contable/Nomina']")))
        btn_nomina.click()

        txt_fecha = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_CFechaPagoHastaTxt")))
        txt_fecha.clear()
        txt_fecha.send_keys(fecha_pago)

        btn_aplicar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_HyperLink2")))
        btn_aplicar.click()

        time.sleep(1.5)

        try:
            wait_alerta = WebDriverWait(driver, 5)
            wait_alerta.until(EC.alert_is_present())
            alerta = driver.switch_to.alert
            alerta.accept()

        except TimeoutException:
            pass

        box_factura = f"//tr[./td[2]//div[contains(., '{num_documento}')]]/td[1]//input[@type='checkbox']"
        factura = wait.until(EC.element_to_be_clickable((By.XPATH, box_factura)))
        factura.click()

        fecha = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_FechaPagoTxt")))
        fecha.clear()
        fecha.send_keys(fecha_actual)

        btn_grabar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Label2")))
        btn_grabar.click()

        lbl_mensaje = wait.until(EC.visibility_of_element_located((By.ID, "ctl00_phContenidoCentral_MensajeLbl")))
        enlace_numero = lbl_mensaje.find_element(By.TAG_NAME, "a")
        num_nomina = enlace_numero.text.strip()

        bot.registrar_mensaje("Validación exitosa.\n")

        driver.get(os.getenv('URL_BASE'))
        time.sleep(2)
        return num_nomina
    
    except Exception as e:
        bot.registrar_error(e, "Módulo Contable/Nomina")
        pass
