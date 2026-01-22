from typing import Any
import time
import os
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

def validar_contratos(driver, bot):
    wait = WebDriverWait(driver, 10)
    bot.registrar_mensaje("Validando creacion de contrato...")

    try:
        btn_contrato = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='SubContrato/Contrayos']")))
        btn_contrato.click()

        elemento_titulo = wait.until(EC.presence_of_element_located((By.ID, "ctl00_phContenidoCentral_SAvancesSubContratosLbl")))
        texto_real = elemento_titulo.text.strip()
        texto_esperado = "Contratos"

        if texto_real == texto_esperado:
            creacion_contrato(driver, bot)
            bot.registrar_mensaje(f"Validación exitosa.\n")
        else:
            bot.registrar_mensaje(f"ERROR: Se esperaba '{texto_esperado}' pero se encontró '{texto_real}'", es_error=True)

        driver.get(os.getenv("URL_BASE"))
        time.sleep(2)

    except Exception as e:
        bot.registrar_error(e, "Módulo Subcontratos/Contratos")
        pass

def creacion_contrato(driver, bot):
    wait = WebDriverWait(driver, 10)
    actions = ActionChains(driver)

    nuevo_contrato = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Label1")))
    nuevo_contrato.click()
    time.sleep(2)

    subcontratista = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_HyperLink1")))
    subcontratista.click()
    iframe_generico = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "iframe")))
    driver.switch_to.frame(iframe_generico)
    btn_buscar_iframe = wait.until(EC.element_to_be_clickable((By.ID, "ob_iBBuscarBtnContainer")))
    btn_buscar_iframe.click()
    time.sleep(1.5)    

    xpath_celda = f"//td[contains(., 'Vivian ')]"
    celda = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_celda)))
    actions.double_click(celda).perform()
    driver.switch_to.default_content()
    time.sleep(1.5)
    print('subcontratista seleccionado')

    input_area = wait.until(EC.element_to_be_clickable((By.ID, "ob_iDdlSAreaGestionDDLTB")))
    input_area.click()
    wait.until(EC.visibility_of_element_located((By.ID, "ob_iDdlSAreaGestionDDLItemsContainer")))
    xpath_opcion = "//div[@id='ob_iDdlSAreaGestionDDLItemsContainer']//div[@class='v' and normalize-space(.)='10101']/parent::div"
    opcion = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_opcion)))
    opcion.click()

    nombre_contrato = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_SNombreContratoTxt")))
    nombre_contrato.send_keys('servicio de prueba')

    direccion = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_SDireccionEjecucionContratoTxt")))
    direccion.send_keys('direccion de prueba')

    input_estado = wait.until(EC.element_to_be_clickable((By.ID, "ob_iDdlSTipoContratoDDLTB")))
    input_estado.click()
    wait.until(EC.visibility_of_element_located((By.ID, "ob_iDdlSTipoContratoDDLItemsContainer")))
    xpath_estado = "//div[@id='ob_iDdlSTipoContratoDDLItemsContainer']//div[@class='v' and normalize-space(.)='CPA']/parent::div"
    opcion_estado = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_estado)))
    opcion_estado.click()

    fecha_contrato = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_SFechaContratoTxt")))
    fecha_contrato.send_keys(datetime.now().strftime("%d-%m-%Y"))

    fecha_inicio = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_SFechaInicioFaenaTxt")))
    fecha_inicio.send_keys(datetime.now().strftime("%d-%m-%Y"))

    mes_termino = datetime.now().month + 2
    if mes_termino > 12:
        mes_termino -= 12
        ano_termino = datetime.now().year + 1
    else:
        ano_termino = datetime.now().year

    fecha_termino = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_SFechaTerminoFaenaTxt")))
    fecha_termino.send_keys(f"{datetime.now().day:02d}-{mes_termino:02d}-{ano_termino}")

    decimales = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_DecimalesMonedaTxt")))
    decimales.clear()
    decimales.send_keys("2")

    input_peso = wait.until(EC.element_to_be_clickable((By.ID, "ob_iDdlSTipoMonedaDDLTB")))
    input_peso.click()
    wait.until(EC.visibility_of_element_located((By.ID, "ob_iDdlSTipoMonedaDDLItemsContainer")))
    xpath_peso = "//div[@id='ob_iDdlSTipoMonedaDDLItemsContainer']//div[@class='v' and normalize-space(.)='CLP']/parent::div"
    opcion_peso = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_peso)))
    opcion_peso.click()
    
    btn_grabar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Label2")))
    btn_grabar.click()
    
    btn_continuar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_ContinuarLnk")))
    btn_continuar.click()
    print('listo primera parte')

    # ---------
    tareas_contratadas =wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tabs-2']")))
    tareas_contratadas.click()
    time.sleep(1)
    # select una cualquiera -> iframe
    # agregar cuenta contable -> proveedores -> iframe -> aceptar
    # grabar
    # continuar
    # ---------
    # seleccionar clausulas
    # agregar clausula -> iframe
    # buscar
    # select alguna
    # seleccionar
    # grabar


    # inicio
    # vb?

    pass
