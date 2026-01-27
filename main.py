import os
import smtplib
from datetime import datetime
import time
import sys

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import validar_empresa
import recursos_humanos
import subcontratos
import vb_contrato
import stock_pedidos
import vb_pedidos
import pedidos_compras
import vb_orden_compras
import entrada_bodega
import salida_bodega
import contable_financiero
import vb_factura
import centralizacion_factura
import nomina
import vb_nomina
import pago_automatico

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
    
    def frenar_si_duplicado(self, driver):
        """
        Verifica si aparece una alerta o mensaje de 'dato repetido'.
        Si encuentra uno, cierra el navegador y DETIENE el script inmediatamente.
        """
        
        try:
            WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            texto_alerta = alert.text.lower()
            
            palabras_clave = ["repetido", "existe", "duplicado", "ya ingresado"]
            
            if any(palabra in texto_alerta for palabra in palabras_clave):
                mensaje_final = f"⛔ ERROR: Se detectó un número de documento duplicado. Mensaje: {alert.text}"
                self.registrar_mensaje(mensaje_final, es_error=True)
                
                alert.accept()
                
                self.registrar_mensaje("\n!!! DETENIENDO EJECUCIÓN !!!")
                self.registrar_mensaje('\n Se recomienda volver a correr manualmente')
                self.enviar_reporte_correo()
                driver.quit()
                sys.exit(1) 
            else:
                alert.accept() 

        except TimeoutException:
            pass

        try:
            lbl = driver.find_element(By.ID, "ctl00_phContenidoCentral_MensajeLbl")
            if lbl.is_displayed():
                texto_lbl = lbl.text.lower()
                if "repetido" in texto_lbl or "ya existe" in texto_lbl or "duplicado" in texto_lbl:
                    mensaje_final = f"ERROR: {lbl.text}"
                    self.registrar_mensaje(mensaje_final, es_error=True)
                    
                    self.registrar_mensaje("\n!!! DETENIENDO EJECUCIÓN !!!")
                    self.registrar_mensaje('\n Se recomienda volver a correr manualmente')
                    self.enviar_reporte_correo()
                    driver.quit()
                    sys.exit(1)
                    
        except:
            pass
    
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
        {"id": "stock", "href": "Bodega", "id_contenedor": "Bodega", "nombre": "Stock"},
        {"id": "compras", "href": "Compras", "id_contenedor": "Compras", "nombre": "Compras"},
        {"id": "entrada_y_salida", "href": "Bodega", "id_contenedor": "Bodega", "nombre": "Entrada/Salida"},
        {"id": "contable", "href": "Contabilidad", "id_contenedor": "Contabilidad", "nombre": "Contable"},
        {"id": "subcontratos", "href": "SubContratos", "id_contenedor": "SubContratos", "nombre": "Subcontratos"}
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

                elif identificador == "stock":
                    num_pedido = stock_pedidos.validar_proceso_pedido(driver, bot)
                    print(f'Pedido #{num_pedido}\n')
                    vb_pedidos.visto_bueno_pedidos(driver, bot, num_pedido)

                elif identificador == "compras":
                    num_orden = pedidos_compras.generar_orden(driver, bot, num_pedido)
                    print(f'Orden #{num_orden}\n')
                    vb_orden_compras.visto_bueno_orden_compra(driver, bot, num_orden)
                
                elif identificador == "entrada_y_salida":
                    num_entrada = entrada_bodega.entrada(driver, bot, num_orden)
                    print(f'Entrada #{num_entrada}\n')
                    salida_bodega.salida(driver, bot, num_pedido)

                elif identificador == "contable":
                    num_factura = contable_financiero.registro_factura(driver, bot, num_orden)
                    print(f'Factura #{num_factura}\n')
                    vb_factura.visto_bueno_factura(driver, bot, num_factura, num_orden)
                    comprobante = centralizacion_factura.centralizar_factura(driver, bot, num_factura)
                    print(f'Comprobante #{comprobante}\n')
                    num_nomina = nomina.nomina(driver, bot, num_factura)
                    print(f'Nomina #{num_nomina}\n')
                    comprobante_pago = vb_nomina.visto_bueno_nomina(driver, bot, num_nomina)
                    print(f'Comprobante pago #{comprobante_pago}\n')
                    pago_automatico.pago_automatico(driver, bot, num_nomina)
                
                elif identificador == "subcontratos":
                    num_contrato = subcontratos.validar_contratos(driver, bot)
                    print(f'Contrato #{num_contrato}\n')
                    vb_contrato.visto_bueno_contrato(driver, bot, num_contrato)

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

