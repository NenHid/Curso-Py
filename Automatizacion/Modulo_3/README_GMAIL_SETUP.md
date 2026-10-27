# Guía de Configuración para Gmail en Python

Google ya **no permite** usar tu contraseña habitual de Gmail en scripts de Python por motivos de seguridad. Para que los scripts funcionen, debes generar una **Contraseña de Aplicación (App Password)** de 16 letras.

---

## Paso a Paso (Solo toma 2 minutos)

1. **Activar Verificación en 2 pasos** (si aún no la tienes):
   - Ve a tu cuenta de Google: https://myaccount.google.com/security
   - En la sección *"Cómo inicias sesión en Google"*, asegúrate de tener activada la **Verificación en dos pasos**.

2. **Crear la Contraseña de Aplicación**:
   - Entra directamente a: https://myaccount.google.com/apppasswords
   - *(O busca "Contraseñas de aplicaciones" en la barra de búsqueda de tu cuenta de Google).*
   - Ponle un nombre de referencia, por ejemplo: `Python Curso`.
   - Haz clic en **Crear**.
   - Google te mostrará un código de 16 caracteres (algo como: `abcd efgh ijkl mnop`).

3. **Configurar el archivo `.env`**:
   - Crea un archivo llamado `.env` en esta carpeta (puedes duplicar `.env.ejemplo`).
   - Pega tu correo y la contraseña de 16 caracteres (sin espacios):

```env
EMAIL_USER=tu_correo@gmail.com
EMAIL_PASS=abcdefghijklmnop
OPENAI_API_KEY=sk-... (opcional para el script con IA)
```

---

## Parámetros de los servidores de Gmail
* **Servidor SMTP (Envío):** `smtp.gmail.com`
  * Puerto SSL: `465` (Recomendado y directo)
  * Puerto STARTTLS: `587`
* **Servidor IMAP (Recepción / Lectura):** `imap.gmail.com`
  * Puerto SSL: `993`
