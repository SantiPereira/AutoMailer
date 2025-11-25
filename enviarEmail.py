# enviarEmail.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import config

logger = logging.getLogger(__name__)

def enviarCorreo(destinatario: str, asunto: str, cuerpo: str, correo_origen: str, password: str, dry_run: bool = False) -> (bool, str):
    """Envía un correo mediante Gmail SMTP. Retorna (ok, mensaje)."""

    logger.info(f"Preparando envío a: {destinatario} - Asunto: {asunto}")

    if dry_run or config.DRY_RUN:
        logger.info("DRY RUN activo: no se enviará correo realmente.")
        return True, "Dry run: simulación OK."

    try:
        mensaje = MIMEMultipart()
        mensaje["From"] = correo_origen
        mensaje["To"] = destinatario
        mensaje["Subject"] = asunto

        mensaje.attach(MIMEText(cuerpo, "plain", "utf-8"))

        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=30) as servidor:
            servidor.ehlo()
            servidor.starttls()
            servidor.ehlo()
            servidor.login(correo_origen, password)
            servidor.send_message(mensaje)

        logger.info(f"Correo enviado a {destinatario}.")
        return True, "Enviado correctamente."
    except smtplib.SMTPAuthenticationError:
        logger.exception("Autenticación SMTP fallida.")
        return False, "Error: autenticación fallida."
    except Exception as e:
        logger.exception("Error general al enviar correo.")
        return False, f"Error al enviar: {e}"
