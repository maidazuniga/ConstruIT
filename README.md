# 🤖 Bot Automatizado ConstruIT

Este proyecto es un bot automatizado de pruebas E2E (End-to-End) desarrollado en **Python** con la librería **Selenium**.

Su objetivo es simular el comportamiento de un usuario real para auditar el funcionamiento de los módulos críticos del ERP. El bot navega por el sistema, realiza validaciones visuales y lógicas y envía un reporte automático por correo electrónico con el resultado.

## Índice

1. [Funcionalidades Principales](#funcionalidades-principales)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Requisitos Previos](#requisitos-previos)
4. [Instalación](#instalación)
5. [Configuración (.env)](#configuración-archivo-env)
6. [Ejecución](#ejecución)
7. [Solución de Problemas](#solución-de-problemas-comunes)

---

### Funcionalidades Principales

* **Inicio de Sesión Automático:** Manejo seguro de credenciales mediante variables de entorno.
* **Navegación Inteligente:** Uso de esperas explícitas (`WebDriverWait`) para manejar tiempos de carga asíncronos.
* **Validación de Negocio:** Verifica que elementos críticos contengan datos válidos.
* **Reporte vía Email:** Envía un correo con un resumen de la ejecución.

---

### Estructura del Proyecto

El código está modularizado para facilitar el mantenimiento:

* `main.py`: Orquestador principal. Inicia el navegador y llama a los módulos.
* `validar_empresa.py`: Maneja el Login y selección de empresa.
* `stock_pedidos.py`: Lógica para crear pedidos en bodega.
* `vb_pedidos.py`: Lógica para buscar un pedido específico y aprobarlo.
* `recursos_humanos.py`: Validaciones del módulo de personal.
* `subcontratos.py`: Validaciones del módulo de contratos.

---

### Requisitos Previos

1. Tener Python 3.8+ instalado.
2. Tener el navegador Google Chrome instalado.
3. Una cuenta de Gmail con "Contraseña de Aplicación" generada (para el envío de reportes).

---

### Instalación

1. **Clonar este repositorio** o descargar los archivos en su carpeta de trabajo.
2. **Instalar las dependencias** necesarias ejecutando el siguiente comando en terminal:

   ```bash
   pip install selenium python-dotenv
   ```

---

### Configuración (Archivo .env)

1. Crear un archivo nuevo llamado `.env` en la raíz del proyecto (al mismo nivel que `main.py`).
2. Copiar y pegar el siguiente contenido dentro del archivo `.env`.
3. **Reemplazar los valores de ejemplo** con sus datos reales.

```ini
# La URL donde inicia sesión el bot
URL=[https://url_loggin.com/login](https://url_loggin.com/login)

# La URL de inicio para poder regresar ahí después de cada validación
URL_BASE=[https://url_inicio.com/index](https://url_inicio.com/index)

# Credenciales de un usuario de prueba o tu usuario
USUARIO=usuario_auditor
CLAVE=tu_contraseña_del_erp

# Correo desde donde sale el reporte 
EMAIL_ORIGEN=correo_ejemplo@gmail.com

# "Contraseña de Aplicación" de 16 letras generada en Google Security.
CLAVE_EMAIL=abcd efgh ijkl mnop

# Correo de quien recibe el reporte
EMAIL_DESTINO=correo_ejemplo@gmail.com
```

### Ejecución

Existen dos maneras de correr el bot.

La primera, es de forma manual, ejecutando el script principal desde la terminal:

```ini
python main.py
```

La segunda, es mediante la ejecución del archivo `main.exe`. Para esto, se deben seguir los siguientes pasos:
1. Ir a la sección de **Releases** del repositorio y descargar el archivo `main.exe`.
2. Crear una carpeta en el escritorio y mover los archivos `main.exe` y `.env`, con las credenciales correctamente configuradas, dentro de ella.
3. Ejecutar `main.exe`.

En ambos casos, el navegador se abrirá automáticamente, realizará las tareas y se cerrará al finalizar, enviando el correo correspondiente con el asunto " Reporte de Validaciones ERP - *datetime*".

---

### Solución de Problemas Comunes

**Error: Username and Password not accepted al enviar correo**

- Asegurarse de que en el archivo .env se esté usando una Contraseña de Aplicación de Google y no su contraseña normal.
- Verificar que la "Verificación en 2 pasos" esté activada en su cuenta de Google.

**El bot falla al encontrar un elemento (TimeoutException)**

- Si el diseño del ERP cambió, es posible que los IDs o Selectores hayan cambiado. Revisar el código y actualizar los *By.ID*
