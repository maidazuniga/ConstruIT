import time
import os
from typing import Any

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

def generar_orden(driver, bot, num_pedido):
    wait = WebDriverWait(driver, 10)
    actions = ActionChains(driver)
    bot.registrar_mensaje("Validando pedidos para compras...")
    
    try:
        btn_pedido_compras = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='Compra/PedidosParaCompra']")))
        btn_pedido_compras.click()

        try:
            wait_popup = WebDriverWait(driver, 3)
            btn_cancelar = wait_popup.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".swal2-cancel")))
            time.sleep(1)
            driver.execute_script("arguments[0].click();", btn_cancelar)
            
        except TimeoutException:
            pass 

        wait.until(EC.presence_of_element_located((By.ID, "ctl00_phContenidoCentral_Label2")))

        btn_buscar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Label6")))
        btn_buscar.click()
        time.sleep(1)

        xpath_pedido = f"//tr[./td[3]//div[normalize-space(.)='{num_pedido}']]/td[4]//a"
        select_recurso = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_pedido)))
        select_recurso.click()

        iframe_generico = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "iframe")))
        driver.switch_to.frame(iframe_generico)

        box_click = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_Grilla_ob_GrillaHeaderContainer_ctl02_ctl02_ctl00_EnviarChk")))
        box_click.click()
        time.sleep(1)
        generar_orden = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_OrdenCompraimgLbl")))
        generar_orden.click()
        driver.switch_to.default_content()
        time.sleep(3)
        
        wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_Label1")))
    

        proveedor = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_ProveedorSucursalLnk")))
        proveedor.click()
        iframe_generico2 = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "iframe")))
        driver.switch_to.frame(iframe_generico2)
        btn_buscar2 = wait.until(EC.element_to_be_clickable((By.ID, "ob_iBBuscarBtnContainer")))
        btn_buscar2.click()
        time.sleep(1.5)

        xpath_celda = f"//tr[./td[3]//div[normalize-space(.)='CONSTRUIT SPA .']]"
        celda = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_celda)))
        actions.double_click(celda).perform()
        driver.switch_to.default_content()
        
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ob_gR")))
        
        filas_recursos = driver.find_elements(By.XPATH, "//tr[contains(@class, 'ob_gR') and normalize-space(./td[3])!='']")

        for fila in filas_recursos:
            try:
                precio_pnl = fila.find_element(By.XPATH, ".//td[7]//div[contains(@id, 'PrecioPnl')]")
                precio_pnl.click()
        
                input_precio = fila.find_element(By.XPATH, ".//td[7]//input[contains(@id, 'Preciotxt')]")
                wait.until(EC.visibility_of(input_precio))
                time.sleep(0.5) 
                input_precio.send_keys(Keys.CONTROL + "a")
                # input_precio.send_keys(Keys.DELETE) 
                input_precio.send_keys("5490")
                input_precio.send_keys(Keys.TAB)
                time.sleep(0.5)

            except Exception:
                continue

        btn_grabar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Label2")))
        btn_grabar.click()

        lbl_mensaje = wait.until(EC.visibility_of_element_located((By.ID, "ctl00_phContenidoCentral_MensajeLbl")))
        enlace_numero = lbl_mensaje.find_element(By.TAG_NAME, "a")
        num_orden = enlace_numero.text.strip()

        bot.registrar_mensaje("Validación exitosa.\n")

        driver.get(os.getenv('URL_BASE'))
        time.sleep(2)
        return num_orden

    except Exception as e:
        bot.registrar_error(e, "Módulo Compras")
        pass
