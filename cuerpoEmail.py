

def generarCuerpoCorreo (datos_json) :

    cuerpo = f"""
    Estimado,

    Se detectó que el equipo {datos_json.get('assetModel', 'N/A')}
    ubicado en {datos_json.get('location', 'Ubicación desconocida')}
    tiene bajo nivel de {datos_json.get('supply', 'Insumo desconocido')}
    ({datos_json.get('currentValue', '?')} unidades restantes).

    Por favor, considere reponer el insumo a la brevedad.

    Saludos cordiales,
    Sistema Automático de Alertas
    """
    return cuerpo 


def emailAlertaToner(datos_json) : 
    cuerpo2 = f"""
    Estimado,

    Se detectó que el equipo {datos_json.get('assetModel', 'N/A')}
    ubicado en {datos_json.get('location', 'Ubicación desconocida')}
    tiene bajo nivel de {datos_json.get('supply', 'Insumo desconocido')}
    ({datos_json.get('currentValue', '?')} unidades restantes).

    Por favor, considere reponer el insumo a la brevedad.

    Saludos cordiales,
    Sistema Automático de Alertas
    """
    return cuerpo2



def emailAlertaUnidadImg(datos_json) : 
    cuerpo3 = f"""
    Estimado,

    Se detectó que el equipo {datos_json.get('assetModel', 'N/A')}
    ubicado en {datos_json.get('location', 'Ubicación desconocida')}
    tiene bajo nivel de {datos_json.get('supply', 'Insumo desconocido')}
    ({datos_json.get('currentValue', '?')} unidades restantes).

    Por favor, considere reponer el insumo a la brevedad.

    Saludos cordiales,
    Sistema Automático de Alertas
    """
    return cuerp3


