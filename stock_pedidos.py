# validar procesos de pedido
from typing import Any
import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

def validar_proceso_pedido(driver, bot):
    wait = WebDriverWait(driver, 15)
    actions = ActionChains(driver)
    bot.registrar_mensaje("Validando creación de pedido...")

    try:
        btn_pedido = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='Bodega/BodegaPedido']")))
        btn_pedido.click()

        # comenzar flujo de validaciones de relleno de campos
        wait.until(EC.presence_of_element_located((By.ID, "ctl00_phContenidoCentral_Label1")))

        selector_obra = wait.until(EC.element_to_be_clickable((By.ID, "ob_iDdlObraFiltroDDLTB")))
        selector_obra.click()
        contenedor_items_obra = wait.until(EC.visibility_of_element_located((By.ID, "ob_iDdlObraFiltroDDLItemsContainer")))
        xpath_obra = ".//div[@class='t']/div[text()='OBRA_UNO']"
        opcion_obra = contenedor_items_obra.find_element(By.XPATH, xpath_obra)
        opcion_obra.click()
        time.sleep(1)

        selector_bodega = wait.until(EC.element_to_be_clickable((By.ID, "ob_iDdlBodegaFiltroDDLTB")))        
        selector_bodega.click()
        contenedor_items_bodega = wait.until(EC.visibility_of_element_located((By.ID, "ob_iDdlBodegaFiltroDDLItemsContainer")))
        xpath_bodega = ".//div[@class='t']/div[text()='BODEGA OBRA_UNO']"
        opcion_bodega = contenedor_items_bodega.find_element(By.XPATH, xpath_bodega)
        opcion_bodega.click()
        time.sleep(1)

        solicitud = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_SolicitadoPorLnk")))
        solicitud.click()
        iframe_generico = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "iframe")))
        driver.switch_to.frame(iframe_generico)
        campo_codigo = wait.until(EC.element_to_be_clickable((By.ID, "MRecurso_CodigoTxt")))
        campo_codigo.clear()
        campo_codigo.send_keys("211829680" + Keys.ENTER)
        xpath_celda = f"//td[contains(., 'Zúñiga Garfias')]"
        celda = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_celda)))
        actions.double_click(celda).perform()
        driver.switch_to.default_content()
        time.sleep(1.5)
        
        comentario = driver.find_element(By.ID, "ctl00_phContenidoCentral_BPedido_ComentarioTxt")
        comentario.send_keys("Comentario de prueba")
        time.sleep(1)
        
        recursos = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_Label4")))
        recursos.click()
        iframe_generico2 = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "iframe")))
        driver.switch_to.frame(iframe_generico2)
        buscar_recursos = wait.until(EC.element_to_be_clickable((By.ID, "ob_iBBuscarBtnContainer")))
        buscar_recursos.click()
        check_recurso1 = f"//tr[./td[3]//div[contains(., 'ACEITE 2T')]]/td[1]//a"
        recurso1 = wait.until(EC.element_to_be_clickable((By.XPATH, check_recurso1)))
        recurso1.click()
        time.sleep(1)
        check_recurso2 = f"//tr[./td[3]//div[contains(., 'WC MODELO ANDES')]]/td[1]//a"
        recurso2 = wait.until(EC.element_to_be_clickable((By.XPATH, check_recurso2)))
        recurso2.click()
        time.sleep(1)
        check_recurso3 = f"//tr[./td[3]//div[contains(., 'BROCA Hss-G METAL 10MM')]]/td[1]//a"
        recurso3 = wait.until(EC.element_to_be_clickable((By.XPATH, check_recurso3)))
        recurso3.click()
        time.sleep(1)
        seleccionar_recursos = wait.until(EC.element_to_be_clickable((By.ID, "ob_iBSeleccionarBtnContainer")))
        seleccionar_recursos.click()
        driver.switch_to.default_content()
        time.sleep(3)

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ob_gR")))
        
        filas_recursos = driver.find_elements(By.XPATH, "//tr[contains(@class, 'ob_gR') and normalize-space(./td[3])!='']")
        
        for fila in filas_recursos:
            try:
                cantidad_pnl = fila.find_element(By.XPATH, ".//td[5]//div[contains(@id, 'Cantidadpnl')]")
                cantidad_pnl.click()
                
                input_cantidad = fila.find_element(By.XPATH, ".//td[5]//input[contains(@id, 'CantidadTxt')]")
                wait.until(EC.visibility_of(input_cantidad))
                
                time.sleep(0.5) 
                input_cantidad.send_keys(Keys.CONTROL + "a")
                # input_cantidad.send_keys(Keys.DELETE) 
                input_cantidad.send_keys("5")
                input_cantidad.send_keys(Keys.TAB)
                time.sleep(0.5)
            except Exception:
                continue

        espacio_vacio = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_Grilla_ctl04_ctl02_ctl20_ctl00_pnlIndicePpto1")))
        espacio_vacio.click()
        contenedor_activo = wait.until(EC.visibility_of_element_located((By.ID, "ctl00_phContenidoCentral_Grilla_ctl04_ctl02_ctl20_ctl00_pnlIndicePpto2")))
        boton_lupa = contenedor_activo.find_element(By.TAG_NAME, "img")
        driver.execute_script("arguments[0].click();", boton_lupa)
        iframe_generico3 = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "iframe")))
        driver.switch_to.frame(iframe_generico3)
        buscar_indice = wait.until(EC.element_to_be_clickable((By.ID, "ob_iBBuscarBtnContainer")))
        buscar_indice.click()
        xpath_celda2 = f"//td[contains(., 'ENTRADAS Y SALIDAS')]"
        celda2 = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_celda2)))
        actions.double_click(celda2).perform()
        seleccionar_indice = wait.until(EC.element_to_be_clickable((By.ID, "ob_iBSeleccionarBtnContainer")))
        seleccionar_indice.click()
        driver.switch_to.default_content()        

        try:
            wait_popup = WebDriverWait(driver, 5)
            btn_ok = wait_popup.until(EC.element_to_be_clickable((By.ID, "popup_ok")))
            driver.execute_script("arguments[0].click();", btn_ok)
        except TimeoutException:
            pass

        btn_grabar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_GrabarBtn")))
        driver.execute_script("arguments[0].click();", btn_grabar)

        try:
            wait_alerta = WebDriverWait(driver, 5)
            wait_alerta.until(EC.alert_is_present())
            alerta = driver.switch_to.alert
            alerta.accept()

        except TimeoutException:
            pass

        # guardar número pedido
        lbl_mensaje = wait.until(EC.visibility_of_element_located((By.ID, "ctl00_phContenidoCentral_MensajeLbl")))
        enlace_numero = lbl_mensaje.find_element(By.TAG_NAME, "a")
        num_pedido = enlace_numero.text.strip()

        bot.registrar_mensaje("Validación exitosa.\n")
        
        driver.get(os.getenv('URL_BASE'))
        time.sleep(2)
        return num_pedido

    except Exception as e:
        bot.registrar_error(e, "Módulo de Stock/Pedidos")
        pass



        