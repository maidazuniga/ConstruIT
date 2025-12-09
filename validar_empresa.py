import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

def validar(driver, bot):
    usuario = os.getenv('USARIO')
    clave = os.getenv('CLAVE')
    url = os.getenv('URL')

    driver.get(url)
    wait = WebDriverWait(driver, 10)

    try:
        campo_usuario = wait.until(EC.presence_of_element_located((By.ID, "nombreusuario")))
        campo_clave = driver.find_element(By.ID, "claveusuario")
        boton_entrar = driver.find_element(By.ID, "EntrarBtn") 

        bot.registrar_mensaje("Iniciando login...")
        campo_usuario.clear()
        campo_usuario.send_keys(usuario)
        
        campo_clave.clear()
        campo_clave.send_keys(clave)

        boton_entrar.click()
        
        bot.registrar_mensaje("Login exitoso\n")
        bot.registrar_mensaje("Verificando que aparezca la empresa...")
        
        try:
            validar_presencia_empresa = wait.until(EC.presence_of_element_located((By.ID, "EmpresaDDL")))
            dropdown = Select(validar_presencia_empresa)
            empresas_disponibles = len(dropdown.options)

            if empresas_disponibles > 0:
                bot.registrar_mensaje(f"Verificación exitosa.\n")
            else:
                bot.registrar_mensaje(f"ERROR CRÍTICO: El selector de empresas está vacío.", es_error=True)
        
            time.sleep(1) 

        except Exception as e:
            bot.registrar_mensaje(f"Error técnico buscando el selector: {str(e)}", es_error=True)
    
    except Exception as e:
        bot.registrar_mensaje(f"Error en el proceso de login: {str(e)}", es_error=True)

