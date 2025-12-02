# 🤖 Bot Automatizado ConstruIT

Este proyecto es un bot automatizado de pruebas E2E (End-to-End) desarrollado en **Python** con la librería **Selenium**.

Su objetivo es simular el comportamiento de un usuario real para auditar el funcionamiento de los módulos críticos del ERP. El bot navega por el sistema, realiza validaciones visuales y lógicas y envía un reporte automático por correo electrónico con el resultado.

## Índice
1. [Funcionalidades Principales](#funcionalidades-principales)
2. [Requisitos Previos](#requisitos-previos)
3. [Instalación](#instalación)
4. [Configuración (.env)](#configuración-archivo-env)

---

### Funcionalidades Principales
* **Inicio de Sesión Automático:** Manejo seguro de credenciales mediante variables de entorno.
* **Navegación Inteligente:** Uso de esperas explícitas (`WebDriverWait`) para manejar tiempos de carga asíncronos.
* **Validación de Negocio:** Verifica que elementos críticos contengan datos válidos.
* **Reporte vía Email:** Envía un correo con un resumen de la ejecución.

---

### Requisitos Previos

1.  Tener Python 3.8+ instalado.
2.  Tener el navegador Google Chrome instalado.
3.  Una cuenta de Gmail con "Contraseña de Aplicación" generada (para el envío de reportes).

---

### Instalación

1.  **Clona este repositorio** o descarga los archivos en tu carpeta de trabajo.

2.  **Instala las dependencias** necesarias ejecutando el siguiente comando en tu terminal:

    ```bash
    pip install selenium python-dotenv
    ```

---

### Configuración (Archivo .env)

1.  Crea un archivo nuevo llamado `.env` en la raíz del proyecto (al mismo nivel que `main.py`).
2.  Copia y pega el siguiente contenido dentro del archivo `.env`.
3.  **Reemplaza los valores de ejemplo** con tus datos reales.

```ini
# La URL donde inicia sesión el bot
URL=[https://tu-erp-construccion.com/login](https://tu-erp-construccion.com/login)

# Credenciales de un usuario de prueba o tu usuario
USUARIO=usuario_auditor
CLAVE=tu_contraseña_del_erp

# Correo desde donde sale el reporte 
EMAIL_ORIGEN=correo_ejemplo@gmail.com

# ¡IMPORTANTE! Aquí NO va tu contraseña normal.
# Va la "Contraseña de Aplicación" de 16 letras generada en Google Security.
CLAVE_EMAIL=abcd efgh ijkl mnop

# Correo de quien recibe el reporte
EMAIL_DESTINO=correo_ejemplo@gmail.com