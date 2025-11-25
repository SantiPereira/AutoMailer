# config.py
# Cambia estos valores por los tuyos.
# Recomiendo usar App Passwords (Gmail) y no la contraseña normal.

IMAP_HOST = "imap.gmail.com"
IMAP_PORT = 993

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

# Cuenta que recibe los JSON y desde la que se enviarán emails
EMAIL_USER = "testchirola@gmail.com"
EMAIL_PASSWORD = "vyer mmxx jnae jscn"   # -> usa App Password
# Filtro de remitente (quién envía los mails con adjuntos .json)
REMITENTE_FILTRO = "no-reply@iss.lexmark.com"

# Para pruebas: destinatario por defecto si no tenés BD todavía
DESTINO_POR_DEFECTO = EMAIL_USER

# Modo dry run: si True no enviará mails realmente (útil para pruebas)
DRY_RUN = False
