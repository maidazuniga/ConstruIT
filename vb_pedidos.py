from typing import Any
import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

def visto_bueno_pedidos(driver, bot, num_pedido):
    wait = WebDriverWait(driver, 10)
    bot.registrar_mensaje(f"Validando aceptación de pedido N° {num_pedido}...")

    try:       
        btn_vb_pedido = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='Bodega/VBPedidoDetalle']")))
        btn_vb_pedido.click()

        try:
            wait_popup = WebDriverWait(driver, 3)
            btn_cancelar = wait_popup.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".swal2-cancel")))
            time.sleep(1)
            driver.execute_script("arguments[0].click();", btn_cancelar)
            
        except TimeoutException:
            pass 
        
        wait.until(EC.presence_of_element_located((By.ID, "ctl00_phContenidoCentral_VBPedidosLbl")))

        xpath_numero = f"//tr[contains(., '{num_pedido}')]/"
        fila = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_numero)))
        fila.click()
        xpath_select_directo = f"{xpath_numero}//select[contains(@id, 'EstadoDDL')]"

        try:
            select_element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_select_directo)))

        except TimeoutException as e:
            bot.registrar_error(e, "Módulo Stock/VB Pedidos")
            raise e

        select_element.click()
        time.sleep(0.5) 
    
        opcion_aprobado = select_element.find_element(By.XPATH, ".//option[@value='1']")
        opcion_aprobado.click()

        time.sleep(4)

        btn_grabar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Label2")))
        btn_grabar.click()

        bot.registrar_mensaje("Validación exitosa.\n")
        
        driver.get(os.getenv('URL_BASE'))
        time.sleep(2)

    except Exception as e:
        bot.registrar_error(e, "Módulo Stock/VB Pedidos")
        raise e