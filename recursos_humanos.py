from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def validar_contratos(driver, bot):
    wait = WebDriverWait(driver, 10)
    bot.registrar_mensaje("Validando contratos...")

    try:
        btn_contratos = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='Remuneracion/Contrato']")))
        btn_contratos.click()

        try:
            wait_popup = WebDriverWait(driver, 3)
            btn_cancelar = wait_popup.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".swal2-cancel")))
            driver.execute_script("arguments[0].click();", btn_cancelar)
            
        except TimeoutException:
            pass 

        elemento_titulo = wait.until(EC.presence_of_element_located((By.ID, "ctl00_phContenidoCentral_ContratoLbl")))
        texto_real = elemento_titulo.text.strip()
        texto_esperado = "Contratos"

        if texto_real == texto_esperado:
            bot.registrar_mensaje(f"Validación exitosa.\n")
        else:
            bot.registrar_mensaje(f"ERROR: Se esperaba '{texto_esperado}' pero se encontró '{texto_real}'", es_error=True)

        time.sleep(1)
        
    except Exception as e:
        bot.registrar_mensaje(f"Error crítico en validación de contratos: {e}", es_error=True)
        raise e


def validar_calculo(driver, bot):
    pass


def validar_liquidacion_sueldo(driver, bot):
    pass