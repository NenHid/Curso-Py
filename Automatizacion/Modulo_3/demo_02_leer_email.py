"""
demo_02_leer_email.py
---------------------
Demostración real de lectura de correos desde la bandeja de entrada de Gmail (IMAP).
Usa la librería estándar 'imaplib' y 'email' para parsear asuntos y contenido.
"""

import os
import imaplib
import email
from email.header import decode_header

# Cargar variables desde .env si existe
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

def decodificar_texto(header_value):
    """Auxiliar para decodificar asuntos o nombres con acentos/emojis."""
    if not header_value:
        return ""
    partes = decode_header(header_value)
    texto_final = ""
    for fragmento, codificacion in partes:
        if isinstance(fragmento, bytes):
            texto_final += fragmento.decode(codificacion or "utf-8", errors="ignore")
        else:
            texto_final += fragmento
    return texto_final

def obtener_cuerpo_email(mensaje):
    """Extrae el texto legible de un objeto mensaje (maneja multipartes)."""
    cuerpo = ""
    if mensaje.is_multipart():
        for parte in mensaje.walk():
            tipo_contenido = parte.get_content_type()
            disposicion = str(parte.get("Content-Disposition"))
            # Buscamos la parte de texto plano y que no sea un archivo adjunto
            if tipo_contenido == "text/plain" and "attachment" not in disposicion:
                payload = parte.get_payload(decode=True)
                if payload:
                    cuerpo += payload.decode("utf-8", errors="ignore")
    else:
        payload = mensaje.get_payload(decode=True)
        if payload:
            cuerpo = payload.decode("utf-8", errors="ignore")
    return cuerpo.strip()

def leer_ultimos_correos(limite=3, solo_no_leidos=False):
    """
    Se conecta por IMAP a Gmail y lee los últimos correos recibidos.
    """
    if not EMAIL_USER or not EMAIL_PASS:
        print("❌ ERROR: Faltan configurar las variables EMAIL_USER y EMAIL_PASS.")
        return []

    correos_obtenidos = []

    try:
        print(f" Conectando con servidor IMAP {IMAP_SERVER}:{IMAP_PORT}...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL_USER, EMAIL_PASS)
        print(" Sesión iniciada con éxito.")

        # Seleccionar la bandeja de entrada ('INBOX')
        mail.select("INBOX")

        # Criterio de búsqueda: "UNSEEN" para no leídos, o "ALL" para todos
        criterio = "UNSEEN" if solo_no_leidos else "ALL"
        status, datos_busqueda = mail.search(None, criterio)
        
        if status != "OK":
            print("❌ No se pudieron buscar correos.")
            return []

        ids_mensajes = datos_busqueda[0].split()
        total_encontrados = len(ids_mensajes)
        print(f" Correos encontrados con filtro '{criterio}': {total_encontrados}")

        if total_encontrados == 0:
            print("No hay correos para mostrar.")
            return []

        # Tomamos los últimos 'limite' correos
        ultimos_ids = ids_mensajes[-limite:]

        for id_msg in reversed(ultimos_ids):
            # Obtener el mensaje completo en formato RFC822
            status, datos_msg = mail.fetch(id_msg, "(RFC822)")
            if status != "OK":
                continue

            mensaje_crudo = datos_msg[0][1]
            mensaje = email.message_from_bytes(mensaje_crudo)

            asunto = decodificar_texto(mensaje.get("Subject"))
            remitente = decodificar_texto(mensaje.get("From"))
            fecha = mensaje.get("Date")
            cuerpo = obtener_cuerpo_email(mensaje)

            info_correo = {
                "id": id_msg.decode(),
                "remitente": remitente,
                "asunto": asunto,
                "fecha": fecha,
                "cuerpo": cuerpo
            }
            correos_obtenidos.append(info_correo)

            print("\n" + "="*50)
            print(f" De: {remitente}")
            print(f" Asunto: {asunto}")
            print(f" Fecha: {fecha}")
            print(f" Cuerpo (primeros 150 caracteres):\n{cuerpo[:150]}...")
            print("="*50)

        mail.close()
        mail.logout()
        return correos_obtenidos

    except Exception as e:
        print(f"❌ Error al consultar la bandeja de entrada: {e}")
        return []

if __name__ == "__main__":
    print("=== DEMO: LECTURA DE CORREOS EN GMAIL (IMAP) ===")
    # Lee los 3 correos más recientes (puedes cambiar solo_no_leidos=True si gustas)
    leer_ultimos_correos(limite=3, solo_no_leidos=False)
