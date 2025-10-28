import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def enviarCorreo(destinatario, asunto, cuerpo, correo_origen, password):
    """Envía un correo mediante Gmail SMTP."""

    try:
        # Crear mensaje MIME
        mensaje = MIMEMultipart()
        mensaje["From"] = correo_origen
        mensaje["To"] = destinatario
        mensaje["Subject"] = asunto

        # Adjuntar cuerpo en texto plano (UTF-8 para acentos y ñ)
        mensaje.attach(MIMEText(cuerpo, "plain", "utf-8"))

        # Conectarse al servidor SMTP de Gmail
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()  # Inicia conexión segura
            servidor.login(correo_origen, password)
            servidor.send_message(mensaje)

        print(f"✅ Correo enviado correctamente a {destinatario}")

    except smtplib.SMTPAuthenticationError:
        print("❌ Error: autenticación fallida. Revisa la contraseña de aplicación.")
    except smtplib.SMTPConnectError:
        print("❌ Error: no se pudo conectar al servidor SMTP de Gmail.")
    except Exception as e:
        print(f"⚠️ Error al enviar el correo: {e}")
