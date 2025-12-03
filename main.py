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

import validar_empresa
import recursos_humanos

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

        asunto = f"Reporte de Validaciones ERP - {fecha}"
        cuerpo_mensaje = "Resumen de la ejecución:\n\n" + "\n".join(self.log_eventos)
        
        msg = MIMEMultipart()
        msg['From'] = origen
        msg['To'] = destino
        msg['Subject'] = asunto
        msg.attach(MIMEText(cuerpo_mensaje, 'plain'))

        try:
            print("\nConectando con servidor de correo...")
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
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    modulos = [
        {"id": "rrhh", "href": "Recurso-Humano", "id_contenedor": "Recurso-Humano", "nombre": "Recursos Humanos"},
    ]

    try:
        validar_empresa.validar(driver, bot)

        for modulo in modulos:
            try:
                driver.get(os.getenv('URL_BASE'))
                time.sleep(2)

                bot.registrar_mensaje(f"--- Iniciando revisión de {modulo['nombre']} ---")
                selector_link = f"a[href*='{modulo['href']}']"
                boton_modulo = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector_link)))
                boton_modulo.click()
                
                wait.until(EC.visibility_of_element_located((By.ID, modulo['id_contenedor'])))
                time.sleep(1)

                identificador = modulo['id']

                if identificador == "rrhh":
                    recursos_humanos.validar_contratos(driver, bot)
                
                # elif identificador == "obras":
                #    obras.validar_presupuestos(driver, bot)

                else:
                    bot.registrar_mensaje(f"No hay función definida para {modulo['nombre']}")

            except Exception as e_mod:
                bot.registrar_mensaje(f"Fallo al entrar o validar {modulo['nombre']}: {str(e_mod)}", es_error=True)
                # Opcional: driver.get(os.getenv('URL')) # Volver al inicio si falla

    except Exception as e:
        bot.registrar_mensaje(f"Error general en el bot: {str(e)}", es_error=True)
    
    finally:
        print("Finalizando ejecución y cerrando navegador...")
        driver.quit()
        bot.enviar_reporte_correo()

if __name__ == "__main__":
    ejecutar_validacion()

