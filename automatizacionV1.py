import time
import logging

from config import *

from lectorIMAP import (
    conectar_imap,
    buscar_mensajes_no_leidos,
    fetch_message,
    marcar_como_leido
)

from procesarJSON import (
    extraer_json_de_mensaje,
    decodificar_asunto
)

from enviarEmail import enviarCorreo


# =============================================================
# CONFIGURACIÓN DE LOGS
# =============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


# =============================================================
# PROCESA UN CICLO COMPLETO DE REVISIÓN
# =============================================================

def ejecutar_una_vez():
    logging.info("🔍 Revisando correos nuevos...")

    # Conectar IMAP
    imap = conectar_imap(EMAIL_USER, EMAIL_PASSWORD)

    # Buscar mensajes
    ids = buscar_mensajes_no_leidos(imap, REMITENTE_FILTRO)

    if not ids:
        logging.info("📭 No hay mensajes nuevos.")
        imap.logout()
        return

    # Procesar cada email encontrado
    for id_msg in ids:
        logging.info(f"📨 Procesando mensaje ID {id_msg}...")

        msg = fetch_message(imap, id_msg)
        asunto = decodificar_asunto(msg)

        logging.info(f"📌 Asunto: {asunto}")

        datos_json = extraer_json_de_mensaje(msg)

        if not datos_json:
            logging.warning("⚠️ No se encontró JSON válido en este correo.")
            marcar_como_leido(imap, id_msg)
            continue

        logging.info(f"📄 JSON procesado correctamente: {datos_json}")

        # Definir destinatario
        destinatario = DESTINO_POR_DEFECTO

        # Enviar correo (a menos que sea Dry Run)
        if DRY_RUN:
            logging.info("🧪 DRY RUN ACTIVADO → No se enviará correo real.")
        else:
            logging.info("📤 Enviando correo generado...")
            try:
                enviarCorreo(
                    destinatario,
                    f"Alerta: {datos_json.get('supplyName', 'Insumo')}",
                    "Este es el cuerpo del email generado automáticamente.",
                    EMAIL_USER,
                    EMAIL_PASSWORD
                )
            except Exception as e:
                logging.error(f"❌ Error al enviar correo: {e}")

        # Marcar como leído
        marcar_como_leido(imap, id_msg)

        logging.info(f"✔ Mensaje ID {id_msg} procesado con éxito.")

    imap.logout()
    logging.info("🔁 Ciclo completado.\n")


# =============================================================
# BUCLE PRINCIPAL (SE EJECUTA PARA SIEMPRE)
# =============================================================

def main():
    logging.info("🚀 Iniciando automatizador de mails (v1).")
    logging.info("⏳ Ejecutando en modo permanente. CTRL + C para detener.\n")

    try:
        while True:
            ejecutar_una_vez()
            time.sleep(30)  # revisar cada 30 segundos
    except KeyboardInterrupt:
        logging.info("⛔ Automatizador detenido manualmente por el usuario.")
    except Exception as e:
        logging.error(f"💥 Error fatal no controlado: {e}")

    logging.info("🛑 Automatizador finalizado correctamente.")


# =============================================================
# EJECUCIÓN DIRECTA
# =============================================================

if __name__ == "__main__":
    main()
