from typing import Any
import time
import os
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def salida(driver, bot, num_pedido):
    wait = WebDriverWait(driver, 10)
    actions = ActionChains(driver)
    bot.registrar_mensaje("Validando salida de bodega...")

    try:
        btn_entrada = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='Bodega/SalidaBodega']")))
        btn_entrada.click()

        tipo_salida = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_SalidaCIRB")))
        tipo_salida.click()

        pedido = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_NumeroPedidoLnk")))
        pedido.click()
        iframe_generico = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "iframe")))
        driver.switch_to.frame(iframe_generico)
        selector_obra = wait.until(EC.element_to_be_clickable((By.ID, "ob_iDdlObraFiltroDDLTB")))
        selector_obra.click()
        contenedor_items_obra = wait.until(EC.visibility_of_element_located((By.ID, "ob_iDdlObraFiltroDDLItemsContainer")))
        xpath_obra = ".//div[@class='t']/div[text()='OBRA_UNO']"
        opcion_obra = contenedor_items_obra.find_element(By.XPATH, xpath_obra)
        opcion_obra.click()
        campo_pedido = wait.until(EC.element_to_be_clickable((By.ID, "PedidoNroTxt")))
        campo_pedido.send_keys(num_pedido + Keys.ENTER)
        xpath_celda = f"//td[contains(., '{num_pedido}')]"
        celda = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_celda)))
        actions.double_click(celda).perform()
        driver.switch_to.default_content()

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

        btn_grabar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Label2")))
        btn_grabar.click()

        # lbl_mensaje = wait.until(EC.visibility_of_element_located((By.ID, "ctl00_phContenidoCentral_MensajeLbl")))
        # enlace_numero = lbl_mensaje.find_element(By.TAG_NAME, "a")
        # num_entrada = enlace_numero.text.strip()

        bot.registrar_mensaje("Validación exitosa.\n")

        driver.get(os.getenv('URL_BASE'))
        time.sleep(2)
        # return num_entrada

    except Exception as e:
        bot.registrar_error(e, "Módulo de Stock/Salida")
        pass
