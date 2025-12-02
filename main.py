import os
import smtplib
from datetime import datetime
import time

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.webdriver import WebDriver

load_dotenv()

class BotValidaciones:
    def __init__(self):
        self.log_eventos = []
        self.hay_errores = False
        
    def registrar_mensaje(self, mensaje, es_error=False):
        marca = "❌" if es_error else "✅"
        linea = f"{marca} {mensaje}"
        print(linea) 
        self.log_eventos.append(linea)
        
        if es_error:
            self.hay_errores = True

    def enviar_reporte_correo(self):
        origen = os.getenv('EMAIL_ORIGEN')
        clave = os.getenv('CLAVE_EMAIL')
        destino = os.getenv('EMAIL_DESTINO')

        if not origen or not clave:
            print("Error con credenciales de correo")
            return

        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

        if self.hay_errores:
            asunto = f"Reporte Diario ERP - {fecha}"
        else:
            asunto = f"Reporte Diario ERP - {fecha}"

        cuerpo_mensaje = "Resumen de la ejecución:\n\n" + "\n".join(self.log_eventos)
        
        msg = MIMEMultipart()
        msg['From'] = origen
        msg['To'] = destino
        msg['Subject'] = asunto
        msg.attach(MIMEText(cuerpo_mensaje, 'plain'))

        try:
            print("\n Conectando con servidor de correo...")
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(origen, clave)
            server.send_message(msg)
            server.quit()
            print("Correo enviado exitosamente.")
        except Exception as e:
            print(f"Error al enviar correo: {e}")

def ejecutar_validacion():
    bot = BotValidaciones()
    usuario = os.getenv('USARIO')
    clave = os.getenv('CLAVE')
    url = os.getenv('URL')

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    wait = WebDriverWait[WebDriver](driver, 10)

    try:
        campo_usuario = wait.until(EC.presence_of_element_located((By.ID, "nombreusuario")))
        campo_clave = driver.find_element(By.ID, "claveusuario")
        boton_entrar = driver.find_element(By.ID, "EntrarBtn") 

        print("Escribiendo credenciales...")
        campo_usuario.clear()
        campo_usuario.send_keys(usuario)
        
        campo_clave.clear()
        campo_clave.send_keys(clave)

        boton_entrar.click()
        
        bot.registrar_mensaje("Verificando que aparezca la empresa")
        
        try:
            validar_presencia_empresa = wait.until(EC.presence_of_element_located((By.ID, "EmpresaDDL")))
            dropdown = Select(validar_presencia_empresa)
            empresas_disponibles = len(dropdown.options)

            if empresas_disponibles > 0:
                bot.registrar_mensaje(f"Validación exitosa")
            else:
                bot.registrar_mensaje(f"ERROR CRÍTICO: El selector de empresas está vacío", es_error=True)
        
            time.sleep(5) 

        except Exception as e:
            bot.registrar_mensaje(f"Error técnico buscando el selector: {str(e)}", es_error=True)

    except Exception as e:
        bot.registrar_mensaje(f"Error general en el bot: {str(e)}", es_error=True)
    
    finally:
        driver.quit()
        bot.enviar_reporte_correo()

if __name__ == "__main__":
    ejecutar_validacion()