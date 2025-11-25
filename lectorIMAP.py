import imaplib
import email
from email.header import decode_header


# ============================
# Conexión al servidor IMAP
# ============================
def conectar_imap(correo, password):
    print("🔌 Conectando a Gmail IMAP...")
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(correo, password)
    mail.select("inbox")
    print("✅ Conectado correctamente.")
    return mail


# ============================
# Buscar correos NO leídos
# ============================
def buscar_mensajes_no_leidos(mail, remitente):
    print("📨 Buscando correos no leídos del remitente:", remitente)
    status, mensajes = mail.search(None, f'(UNSEEN FROM "{remitente}")')

    email_ids = mensajes[0].split()

    print(f"🔎 Se encontraron {len(email_ids)} correos nuevos.")
    return email_ids


# ============================
# Obtener un mensaje completo
# ============================
def fetch_message(mail, email_id):
    status, data = mail.fetch(email_id, "(RFC822)")
    
    for part in data:
        if isinstance(part, tuple):
            return email.message_from_bytes(part[1])
    
    return None


# ============================
# Marcar correo como leído
# ============================
def marcar_como_leido(mail, email_id):
    mail.store(email_id, '+FLAGS', '\\Seen')
    print(f"✔️ Mensaje {email_id.decode()} marcado como leído.")
