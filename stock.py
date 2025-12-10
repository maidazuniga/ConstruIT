# validar procesos de pedido
from typing import Any
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def validar_proceso_pedido(driver, bot):
    wait = WebDriverWait(driver, 10)
    actions = ActionChains(driver)
    bot.registrar_mensaje("Validando procesos de pedido...")

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
        campo_codigo.send_keys("211829680")
        buscar = wait.until(EC.element_to_be_clickable((By.ID, "ob_iBBuscarBtnContainer")))
        driver.execute_script("arguments[0].click();", buscar)
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

        cantidad1 = driver.find_element(By.ID, "ctl00_phContenidoCentral_Grilla_ctl04_ctl02_ctl12_ctl00_Cantidadpnl")
        cantidad1.clear()
        cantidad1.send_keys("5")
        time.sleep(1)
        cantidad2 = driver.find_element(By.ID, "ctl00_phContenidoCentral_Grilla_ctl04_ctl03_ctl12_ctl00_Cantidadpnl")
        cantidad2.clear()
        cantidad2.send_keys("5")
        time.sleep(1)
        cantidad3 = driver.find_element(By.ID, "ctl00_phContenidoCentral_Grilla_ctl04_ctl04_ctl12_ctl00_Cantidadpnl")
        cantidad3.clear()
        cantidad3.send_keys("5")
        time.sleep(1)



        bot.registrar_mensaje("En proceso de validación :)")

        driver.back()
        time.sleep(2)


    except Exception as e:
        bot.registrar_error(e, "Módulo de Stock")
        raise e



        