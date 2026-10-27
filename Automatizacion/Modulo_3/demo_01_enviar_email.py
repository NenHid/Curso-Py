"""
demo_01_enviar_email.py
-----------------------
Demostración real de envío de correos automatizados usando Python y Gmail (SMTP).
Usa la librería estándar 'smtplib' y 'email.message.EmailMessage'.
"""

import os
import smtplib
from email.message import EmailMessage

# Intentamos cargar variables desde .env si python-dotenv está instalado
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configuración de credenciales (obtenidas de variables de entorno)
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# Servidor SMTP de Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # Puerto SSL directo

def enviar_correo(destinatario: str, asunto: str, cuerpo_texto: str, cuerpo_html: str = None):
    """
    Envía un correo electrónico mediante el servidor SMTP de Gmail.
    """
    if not EMAIL_USER or not EMAIL_PASS:
        print("❌ ERROR: Faltan configurar las variables EMAIL_USER y EMAIL_PASS.")
        print("Revisa el archivo README_GMAIL_SETUP.md para configurar tu contraseña de aplicación.")
        return False

    # 1. Construir el mensaje
    mensaje = EmailMessage()
    mensaje["Subject"] = asunto
    mensaje["From"] = f"Sistema de Automatización <{EMAIL_USER}>"
    mensaje["To"] = destinatario
    
    # Contenido en texto plano (fallback)
    mensaje.set_content(cuerpo_texto)
    
    # Contenido enriquecido en HTML (opcional)
    if cuerpo_html:
        mensaje.add_alternative(cuerpo_html, subtype="html")

    # 2. Conectar y enviar vía SSL seguro
    try:
        print(f" Conectando con {SMTP_SERVER}:{SMTP_PORT}...")
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as servidor:
            servidor.login(EMAIL_USER, EMAIL_PASS)
            print(" Autenticación exitosa.")
            servidor.send_message(mensaje)
            print(f" Correo enviado con éxito a: {destinatario}")
            return True

    except smtplib.SMTPAuthenticationError:
        print("❌ Error de autenticación: Verifica tu correo y que la contraseña sea la de 16 caracteres de 'Contraseña de aplicación'.")
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado al enviar: {e}")
        return False

if __name__ == "__main__":
    print("=== DEMO: ENVÍO DE CORREO AUTOMATIZADO CON GMAIL ===")
    
    # Para la prueba, enviamos un correo a la misma cuenta de Gmail del remitente
    destinatario_prueba = EMAIL_USER or "tu_correo@gmail.com"
    
    asunto_prueba = " Reporte Automático de Prueba - Curso Python"
    
    texto_plano = """
    Hola, probando en vivo el envío de correos automáticos desde Python.

    saludos a la clase de Automatización con Python.
    Este es un correo enviado automáticamente mediante un script de Python utilizando smtplib.
    
    Estado del sistema: Operativo al 100%
    Fecha y hora: Generado automáticamente
    """
    
    texto_html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #2b6cb0;"> Reporte Automático del Sistema</h2>
        <p>{texto_plano}</p>
        <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; border-color: #ddd;">
          <tr bgcolor="#f7fafc"><th>Módulo</th><th>Estado</th></tr>
          <tr><td>APIs Públicas</td><td><b style="color: green;">Conectado</b></td></tr>
          <tr><td>Servidor SMTP</td><td><b style="color: green;">Autenticado</b></td></tr>
        </table>
        <br>
        <p style="font-size: 12px; color: #777;">Enviado desde el curso de Automatización con Python.</p>
      </body>
    </html>
    """
    
    enviar_correo(
        destinatario=destinatario_prueba,
        asunto=asunto_prueba,
        cuerpo_texto=texto_plano,
        cuerpo_html=texto_html
    )
