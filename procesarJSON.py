# procesadorJSON.py
import json
from email.header import decode_header
from typing import Optional, Tuple, Dict
import logging

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
    Busca en el mensaje (multipart o no) un adjunto .json o un cuerpo que sea JSON.
    Devuelve el dict JSON o None.
    """
    subject = decodificar_asunto(msg)
    logger.debug(f"Decodificando mensaje con asunto: {subject}")

    # Si multipart, buscar adjuntos
    if msg.is_multipart():
        for part in msg.walk():
            filename = part.get_filename()
            ctype = part.get_content_type()
            if filename and filename.lower().endswith(".json"):
                logger.info(f"Adjunto JSON encontrado: {filename} (asunto: {subject})")
                payload = part.get_payload(decode=True)
                if not payload:
                    logger.warning("Adjunto encontrado pero sin contenido.")
                    continue
                try:
                    text = payload.decode("utf-8")
                except Exception:
                    text = payload.decode("latin1", errors="replace")
                try:
                    datos = json.loads(text)
                    return datos
                except json.JSONDecodeError:
                    logger.warning("JSON inválido en adjunto.")
                    continue

        # Si no hubo adjuntos .json, también podemos buscar en partes text/plain o text/html
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == "text/plain":
                payload = part.get_payload(decode=True)
                if not payload:
                    continue
                try:
                    text = payload.decode("utf-8")
                except Exception:
                    text = payload.decode("latin1", errors="replace")
                try:
                    datos = json.loads(text)
                    logger.info("JSON encontrado en cuerpo text/plain.")
                    return datos
                except json.JSONDecodeError:
                    continue
    else:
        # no multipart -> cuerpo simple
        payload = msg.get_payload(decode=True)
        if payload:
            try:
                text = payload.decode("utf-8")
            except Exception:
                text = payload.decode("latin1", errors="replace")
            try:
                datos = json.loads(text)
                logger.info("JSON encontrado en cuerpo del mensaje (no multipart).")
                return datos
            except json.JSONDecodeError:
                logger.debug("Cuerpo no es JSON.")

    logger.info("No se encontró JSON en el mensaje.")
    return None
