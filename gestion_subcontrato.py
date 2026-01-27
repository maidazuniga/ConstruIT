from typing import Any
import time
import os
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

mes_termino = datetime.now().month + 3
if mes_termino > 12:
    mes_termino -= 12
    ano_termino = datetime.now().year + 1
else:
    ano_termino = datetime.now().year

def gestion_subcontratista(driver, bot, num_contrato):
    wait = WebDriverWait(driver, 10)
    bot.registrar_mensaje(f"Validando gestion de subcontratista...")

    try:       
        # ### primero cambiar la fecha del periodo ###
        # btn_workflow = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='SubContrato/WorkFlow']")))
        # btn_workflow.click()

        # mes_actual = datetime.now().month
        # mes_formateado = f"{mes_actual:02d}" 

        # try:
        #     input_mes = wait.until(EC.element_to_be_clickable((By.ID, "ob_iDdlGeneralPeriodoContableDDLTB")))
        #     input_mes.click()
        #     wait.until(EC.visibility_of_element_located((By.ID, "ob_iDdlGeneralPeriodoContableDDLItemsContainer")))

        #     xpath_opcion = f"//div[@id='ob_iDdlGeneralPeriodoContableDDLItemsContainer']//div[@class='v' and normalize-space(.)='{mes_formateado}']/parent::div"
        #     opcion = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_opcion)))
        #     opcion.click()

        #     input_anio = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_phContenidoCentral_AaaammTxt")))
        #     input_anio.clear()
        #     input_anio.send_keys(str(datetime.now().year))

        #     input_periodo = wait.until(EC.element_to_be_clickable((By.ID, "ob_iDdlPeriodoDDLTB")))
        #     input_periodo.click()
        #     wait.until(EC.visibility_of_element_located((By.ID, "ob_iDdlPeriodoDDLItemsContainer")))

        #     xpath_mensualidad = "//div[@id='ob_iDdlPeriodoDDLItemsContainer']//div[@class='v' and normalize-space(.)='0']/parent::div"
        #     opcion = wait.until(EC.presence_of_element_located((By.XPATH, xpath_mensualidad)))
        #     driver.execute_script("arguments[0].click();", opcion)

        #     btn_grabar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Label2")))
        #     btn_grabar.click()

        # except Exception as e:
        #     bot.registrar_error(e, "Selección de Periodo Contable")


        ### después el proceso de gestion ###
        btn_gestion = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='SubContrato/PantallaInicial']")))
        btn_gestion.click()

        try:
            wait_popup = WebDriverWait(driver, 3)
            btn_cancelar = wait_popup.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".swal2-cancel")))
            time.sleep(1)
            driver.execute_script("arguments[0].click();", btn_cancelar)
            
        except TimeoutException:
            pass 

        input_area = wait.until(EC.element_to_be_clickable((By.ID, "ob_iDdlSAreaGestionDDLTB")))
        input_area.click()
        wait.until(EC.visibility_of_element_located((By.ID, "ob_iDdlSAreaGestionDDLItemsContainer")))
        xpath_opcion = "//div[@id='ob_iDdlSAreaGestionDDLItemsContainer']//div[@class='v' and normalize-space(.)='10101']/parent::div"
        opcion = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_opcion)))
        opcion.click()

        time.sleep(2)

        encontrado = False
        filas = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tr[.//input[contains(@id, 'ActualizarChk')]]")))
        
        for fila in filas:
            elemento_texto = fila.find_element(By.XPATH, ".//div[@class='ob_gCc2' and contains(text(), '-')]")
            texto_completo = elemento_texto.text.strip()
            numero_en_fila = texto_completo.split('-')[0].strip()
            
            if numero_en_fila == str(num_contrato):                
                checkbox = fila.find_element(By.XPATH, ".//input[contains(@id, 'ActualizarChk')]")
                driver.execute_script("arguments[0].click();", checkbox)
                encontrado = True
                break

        time.sleep(1)

        btn_calculo = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[title='Calculo EP']")))
        btn_calculo.click()

        bot.registrar_mensaje('Validación exitosa\n')

        try:
            wait.until(EC.url_contains("Mensaje.aspx"))
        except TimeoutException:
            pass

        bot.registrar_mensaje("Validación exitosa.\n")
        
        url_base = os.getenv('URL_BASE')
        if not url_base: 
            url_base = "/default.aspx"

        driver.execute_script(f"window.location.href = '{url_base}';")

        time.sleep(2)
        registro_clausulas(driver, bot, num_contrato)

    except Exception as e:
        bot.registrar_error(e, "Módulo SubContrato/Gestion Subcontratista")
        pass


def registro_clausulas(driver, bot, num_contrato):
    wait = WebDriverWait(driver, 10)
    bot.registrar_mensaje(f"Validando registro de clausulas exigibles...")

    try:       
        btn_clausulas = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='SubContrato/CaratulaAdjunto']")))
        btn_clausulas.click()

        btn_buscar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Label6")))
        btn_buscar.click()
        time.sleep(3)

        xpath_checkbox = f"//tr[.//span[normalize-space(.)='{num_contrato}']]//input[contains(@id, 'AdjuntoChk')]"
        checkbox = wait.until(EC.presence_of_element_located((By.XPATH, xpath_checkbox)))
        driver.execute_script("arguments[0].click();", checkbox)

        time.sleep(2)

        btn_grabar = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Label2")))
        btn_grabar.click()
        bot.registrar_mensaje('Validación exitosa\n')
    
    except Exception as e:
        bot.registrar_error(e, "Módulo SubContrato/Registro de claúsulas exigibles")
        pass

