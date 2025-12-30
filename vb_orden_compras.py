from typing import Any
import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

def visto_bueno_orden_compra(driver, bot, num_orden):
    wait = WebDriverWait(driver, 10)
    bot.registrar_mensaje(f"Validando aceptación de orden de compra N° {num_orden}...")

    try:       
        btn_vb_orden_compra = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='Compra/VBOrdenCompra']")))
        btn_vb_orden_compra.click()

        try:
            wait_popup = WebDriverWait(driver, 3)
            btn_cancelar = wait_popup.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".swal2-cancel")))
            time.sleep(1)
            driver.execute_script("arguments[0].click();", btn_cancelar)
            
        except TimeoutException:
            pass 
        
        wait.until(EC.presence_of_element_located((By.ID, "ctl00_phContenidoCentral_VBCotizacionesLbl")))

        buscar_pedido = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_OrdenCompraDesdeTxt")))
        buscar_pedido.clear()
        buscar_pedido.send_keys(f"{num_orden}")

        btn_buscar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Label6")))
        btn_buscar.click()

        xpath_orden = f"//tr[./td[2]//div[normalize-space(.)='{num_orden}']]/td[3]//select"
        select_estado = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_orden)))
        select_estado.click()

        time.sleep(0.5) 
    
        opcion_aprobado = select_estado.find_element(By.XPATH, ".//option[@value='1']")
        opcion_aprobado.click()

        time.sleep(1.5)

        btn_grabar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Label2")))
        btn_grabar.click()

        bot.registrar_mensaje("Validación exitosa.\n")
        
        driver.get(os.getenv('URL_BASE'))
        time.sleep(2)

    except Exception as e:
        bot.registrar_error(e, "Módulo Compras/VB Orden de Compra")
        pass
