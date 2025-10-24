import json                             #Libreria para leer archivos .json 
import imaplib                          # Para conectarnos al servidor IMAP de Gmail
import email                            # Para procesar los emails
import smtplib                          # Para conectarnos al servidor SMTP y enviar correos
from email.mime.text import MIMEText    # Para crear el contenido del correo
from email.header import decode_header  # Para decodificar los títulos
from email.mime.multipart import MIMEMultipart  # Para correos con varias partes (texto + adjuntos)

from cuerpoEmail import * 


#TODO: DATOS DEL MAIL 
#!Cambiar a alguno de urucopy y mejorar la seguridad de las pass ; 
    #*Gmil
correo = 'testchirola@gmail.com'
    #*Pass
password = 'vyer mmxx jnae jscn'
    #*Remitnte deseado
    #!Cambiar en un principio a un exel con datos de los clientes , lo ideal seria una base de datos , creear una interfaz para que el usuario haga un CRUD
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
    datos_json = None 

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
                datos_json = convertir(body, asunto_cod)
            
            #* Solo si el JSON se procesó correctamente
            if datos_json : 
                if datos_json['upplyName'] == 'Toner' :
                    cuerpo = emailAlertaToner(datos_json)
                    print(cuerpo) 
                elif datos_json['Unidad de Imagen'] : 
                    cuerpo = emailAlertaUnidadImg(datos_json)
                    print(cuerpo) 
                else :
                    cuerpo = generarCuerpoCorreo(datos_json)
                    print(cuerpo) 
                
                mail.store(id_act, '+FLAGS', '\\Seen')  # Marcar como leído



    else:
        body = msg.get_payload(decode=True).decode()
        convertir(body , asunto_cod)



cantidad = len(email_ids)
print(f"Se encontraron {cantidad} correos de {remitente}")