import json                             # Librería para leer archivos .json 
import imaplib                          # Para conectarnos al servidor IMAP de Gmail
import email                            # Para procesar los emails
from email.header import decode_header  # Para decodificar los títulos

from cuerpoEmail import *               # Funciones que generan el cuerpo del correo
from enviarEmail import *               # Función que envía los correos


# =============================================================
# TODO: DATOS DEL MAIL 
# =============================================================

correo = 'testchirola@gmail.com'          # Cuenta de Gmail
password = 'vyer mmxx jnae jscn'          # Contraseña (usar App Password)
remitente = 'testchirola@gmail.com'       # Desde qué remitente buscar correos

#! En un futuro: cambiar a lectura desde Excel o BD
with open('test.json', 'r') as conexion:
    datos = json.load(conexion)


# =============================================================
# CONEXIÓN CON GMAIL (IMAP)
# =============================================================

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(correo, password)
mail.select("inbox")

# Buscar mails del remitente
status, mensajes = mail.search(None, f'FROM "{remitente}"')
email_ids = mensajes[0].split()  # Lista de los correos encontrados


# =============================================================
# FUNCIONES AUXILIARES
# =============================================================

def convertir(body, subject):
    """Convierte el cuerpo de un correo en JSON (si es válido)."""
    try:
        datos = json.loads(body)
        print(f"✅ JSON encontrado en correo '{subject}':\n", datos)
        return datos
    except json.JSONDecodeError:
        print(f"⚠️ No hay JSON válido en correo '{subject}'")
        return None


# =============================================================
# PROCESAR CADA CORREO
# =============================================================

for id_act in email_ids:
    datos_json = None
    status, msg_data = mail.fetch(id_act, "(RFC822)")  # Trae todo el correo

    for posicion_correo in msg_data:
        if isinstance(posicion_correo, tuple):
            msg = email.message_from_bytes(posicion_correo[1])

    # Decodificar asunto
    asunto_cod = decode_header(msg.get("Subject"))[0][0]
    if isinstance(asunto_cod, bytes):
        asunto_cod = asunto_cod.decode()

    # Verificar si el correo tiene varias partes
    if msg.is_multipart():
        for part in msg.walk():
            nombre_arch_adj = part.get_filename()
            tipo_conteido = part.get_content_type()

            # Procesar si hay un adjunto JSON
            if nombre_arch_adj and nombre_arch_adj.endswith(".json"):
                body = part.get_payload(decode=True).decode()
                datos_json = convertir(body, asunto_cod)

            # Si se pudo procesar el JSON
            if datos_json:
                # Generar el cuerpo del correo según el tipo de alerta
                if datos_json.get('supplyName') == 'Toner':
                    cuerpo = emailAlertaToner(datos_json)
                elif datos_json.get('Unidad de Imagen'):
                    cuerpo = emailAlertaUnidadImg(datos_json)
                else:
                    cuerpo = generarCuerpoCorreo(datos_json)

                # Destinatario — más adelante se puede obtener del JSON
                destinatario = remitente 

                # Enviar el correo
                enviarCorreo(
                    destinatario,
                    f"Alerta: {datos_json.get('supplyName', 'Insumo')}",
                    cuerpo,
                    correo,
                    password
                )

                # Marcar como leído
                mail.store(id_act, '+FLAGS', '\\Seen')

    else:
        # Si el correo no es multipart
        body = msg.get_payload(decode=True).decode()
        convertir(body, asunto_cod)


# =============================================================
# FINALIZAR
# =============================================================

cantidad = len(email_ids)
print(f"\n📩 Se encontraron {cantidad} correos de {remitente}")
mail.logout()
print("✅ Conexión cerrada correctamente.")
