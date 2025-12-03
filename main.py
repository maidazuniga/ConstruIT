import os
import smtplib
from datetime import datetime

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
from selenium import webdriver

import validar_empresa

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
    
    try:
        validar_empresa.validar(driver, bot)

    except Exception as e:
        bot.registrar_mensaje(f"Error general en el bot: {str(e)}", es_error=True)
    
    finally:
        print("Finalizando ejecución y cerrando navegador...")
        driver.quit()
        bot.enviar_reporte_correo()

if __name__ == "__main__":
    ejecutar_validacion()

