import json
import re
import logging
from email.header import decode_header
from typing import Optional, Dict

logger = logging.getLogger(__name__)

def decodificar_asunto(msg) -> str:
    raw = msg.get("Subject", "")
    dec = decode_header(raw)[0]
    subject = dec[0]
    if isinstance(subject, bytes):
        try:
            subject = subject.decode(dec[1] or "utf-8")
        except Exception:
            subject = subject.decode("utf-8", errors="replace")
    return subject

def extraer_json_de_mensaje(msg) -> Optional[Dict]:
    """
    Busca en el mensaje un adjunto .json, un cuerpo text/plain o JSON embebido en HTML.
    Devuelve el dict JSON o None.
    """
    subject = decodificar_asunto(msg)
    logger.debug(f"Decodificando mensaje con asunto: {subject}")

    if msg.is_multipart():
        for part in msg.walk():
            filename = part.get_filename()
            ctype = part.get_content_type()

            # Caso adjunto .json
            if filename and filename.lower().endswith(".json"):
                payload = part.get_payload(decode=True)
                if payload:
                    try:
                        text = payload.decode("utf-8", errors="replace")
                        return json.loads(text)
                    except Exception as e:
                        logger.warning(f"Error leyendo adjunto JSON: {e}")
                        continue

            # Caso cuerpo HTML con JSON embebido
            if ctype == "text/html":
                payload = part.get_payload(decode=True)
                if payload:
                    try:
                        html = payload.decode("utf-8", errors="replace")
                        # Buscar bloque JSON dentro del HTML
                        match = re.search(r"\{.*\}", html, re.DOTALL)
                        if match:
                            datos = json.loads(match.group(0))
                            logger.info("✅ JSON encontrado dentro de HTML.")
                            return datos
                    except Exception as e:
                        logger.warning(f"No se pudo extraer JSON de HTML: {e}")
                        continue

            # Caso cuerpo texto plano
            if ctype == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    try:
                        text = payload.decode("utf-8", errors="replace")
                        return json.loads(text)
                    except Exception:
                        continue
    else:
        # Mensaje no multipart
        payload = msg.get_payload(decode=True)
        if payload:
            text = payload.decode("utf-8", errors="replace")
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except Exception:
                    pass

    logger.info("⚠️ No se encontró JSON válido en el mensaje.")
    return None
