import json                             #Libreria para leer archivos .json 
import imaplib                          # Para conectarnos al servidor IMAP de Gmail
import email                            # Para procesar los emails
from email.header import decode_header  # Para decodificar los títulos

#TODO: DATOS DEL MAIL 
#!Cambiar a alguno de urucopy ; 
    #*Gmil
correo = 'testchirola@gmail.com'
    #*Pass
password = 'vyer mmxx jnae jscn'
    #*Remitnte deseado
remitente = 'testchirola@gmail.com'
with open('test.json' , 'r') as conexion :
    datos = json.load(conexion) ;

#TODO: CONEXION CON GMAIL 
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(correo, password)

#*Seleccionamos la bandeja de entrada
mail.select("inbox")

#* Buscar mails del remitente
status , mensajes = mail.search(None , f'FROM "{remitente}"')
email_ids = mensajes[0].split() #Lista de los correos encontrado del remitente 

#TODO: FUNCION PARA PASAR UN .JOSN A TEXT
def convertir(body , subject) :
    try:
        datos = json.loads(body)
        print(f"JSON encontrado en correo '{subject}':\n", datos)
        return datos
    except json.JSONDecodeError:
        print(f"No hay JSON válido en correo '{subject}'")
        return None


#*Recorremos los correos encontrados
for id_act in email_ids : 
    status , msg_data = mail.fetch(id_act , "(RFC822)") #Trae todo el correo 

    #*Recorremos el correo 
    for posicion_correo in msg_data :
        if isinstance(posicion_correo , tuple) :
            msg = email.message_from_bytes(posicion_correo[1]) 

    #*Decodificamos el asunto del correo
    asunto_cod = decode_header(msg.get("Subject"))[0][0]
    if isinstance(asunto_cod , bytes) : 
        asunto_cod = asunto_cod.decode()

    #*Verificamoe que el correo tenga varias partes
    if msg.is_multipart():
        for part in msg.walk() :
            nombre_arch_adj = part.get_filename() 
            tipo_conteido = part.get_content_type()

            if nombre_arch_adj and nombre_arch_adj.endswith(".json"):
                body = part.get_payload(decode=True).decode()
                convertir(body, asunto_cod)

            if convertir(body, asunto_cod):  # Solo si el JSON se procesó correctamente
                    mail.store(id_act, '+FLAGS', '\\Seen')  # Marcar como leído

    else:
        body = msg.get_payload(decode=True).decode()
        convertir(body , asunto_cod)



cantidad = len(email_ids)
print(f"Se encontraron {cantidad} correos de {remitente}")