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
import subcontratos
import stock_pedidos
import vb_pedidos
import pedidos_compras
import vb_orden_compras
import entrada_bodega
import salida_bodega

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
    
    def registrar_error(self, e, seccion):
        """
        Recibe una excepción técnica (e) y la traduce a español simple
        antes de guardarla en el reporte.
        """
        mensaje_sucio = str(e).split('\n')[0]
        mensaje_limpio = mensaje_sucio

        if "element click intercepted" in mensaje_sucio:
            mensaje_limpio = "Algo tapó el botón y no se pudo hacer clic (Click Intercepted)."
        elif "no such element" in mensaje_sucio:
            mensaje_limpio = "No se encontró el elemento esperado en la pantalla."
        elif "TimeoutException" in str(type(e)):
            mensaje_limpio = "El sistema tardó demasiado (10s) y el elemento no apareció."
        elif "stale element reference" in mensaje_sucio:
            mensaje_limpio = "La página cambió y el elemento viejo ya no existe (Stale Element)."

        self.registrar_mensaje(f"Error en {seccion}: {mensaje_limpio}", es_error=True)

def ejecutar_validacion():
    bot = BotValidaciones()
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    modulos = [
        {"id": "rrhh", "href": "Recurso-Humano", "id_contenedor": "Recurso-Humano", "nombre": "Recursos Humanos"},
        {"id": "subcontratos", "href": "SubContratos", "id_contenedor": "SubContratos", "nombre": "Subcontratos"},
        {"id": "stock", "href": "Bodega", "id_contenedor": "Bodega", "nombre": "Stock"},
        {"id": "compras", "href": "Compras", "id_contenedor": "Compras", "nombre": "Compras"},
        {"id": "entrada_y_salida", "href": "Bodega", "id_contenedor": "Bodega", "nombre": "Entrada/Salida"}
    ]

    try:
        validar_empresa.validar(driver, bot)

        for modulo in modulos:
            try:
                bot.registrar_mensaje(f"--- Iniciando revisión de {modulo['nombre']} ---")
                selector_link = f"a[href*='{modulo['href']}']"
                boton_modulo = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector_link)))
                boton_modulo.click()
                
                wait.until(EC.visibility_of_element_located((By.ID, modulo['id_contenedor'])))
                time.sleep(1)

                identificador = modulo['id']

                if identificador == "rrhh":
                    recursos_humanos.validar_contratos(driver, bot)
                    recursos_humanos.validar_calculo(driver, bot)
                    recursos_humanos.validar_liquidacion_sueldo(driver, bot)
                
                elif identificador == "subcontratos":
                    subcontratos.validar_contratos(driver, bot)

                elif identificador == "stock":
                    num_pedido = stock_pedidos.validar_proceso_pedido(driver, bot)
                    print(f'pedido #{num_pedido}\n')
                    vb_pedidos.visto_bueno_pedidos(driver, bot, num_pedido)

                elif identificador == "compras":
                    num_orden = pedidos_compras.generar_orden(driver, bot, num_pedido)
                    print(f'orden #{num_orden}\n')
                    vb_orden_compras.visto_bueno_orden_compra(driver, bot, num_orden)
                
                elif identificador == "entrada_y_salida":
                    num_entrada = entrada_bodega.entrada(driver, bot, num_orden)
                    print(f'entrada #{num_entrada}\n')
                    salida_bodega.salida(driver, bot, num_pedido)

                else:
                    bot.registrar_mensaje(f"No hay función definida para {modulo['nombre']}")

            except Exception:
                bot.registrar_mensaje(f"Hay 1 o más errores en el módulo {modulo['nombre']}\n", es_error=True)

    except Exception as e:
        bot.registrar_mensaje(f"Error general en el bot: {str(e)}", es_error=True)
    
    finally:
        print("Finalizando ejecución y cerrando navegador...")
        driver.quit()
        bot.enviar_reporte_correo()

if __name__ == "__main__":
    ejecutar_validacion()

