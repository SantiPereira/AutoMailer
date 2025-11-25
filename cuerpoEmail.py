# cuerpoEmail.py

def generarCuerpoCorreo(datos_json: dict) -> str:
    cuerpo = f"""Estimado/a,

Se detectó que el equipo {datos_json.get('assetModel', 'N/A')}
ubicado en {datos_json.get('location', 'Ubicación desconocida')}
tiene bajo nivel de {datos_json.get('supply', 'Insumo desconocido')}
({datos_json.get('currentValue', '?')} unidades restantes).

Por favor, considere reponer el insumo a la brevedad.

Saludos cordiales,
Sistema Automático de Alertas
"""
    return cuerpo


def emailAlertaToner(datos_json: dict) -> str:
    cuerpo = f"""Estimado/a,

ALERTA TONER:
Equipo: {datos_json.get('assetModel', 'N/A')}
Ubicación: {datos_json.get('location', 'Ubicación desconocida')}
Insumo: {datos_json.get('supply', 'Toner')}
Nivel actual: {datos_json.get('currentValue', '?')}

Acción recomendada: reponer/ordenar toner.

Saludos,
Sistema Automático de Alertas
"""
    return cuerpo


def emailAlertaUnidadImg(datos_json: dict) -> str:
    cuerpo = f"""Estimado/a,

ALERTA UNIDAD DE IMAGEN:
Equipo: {datos_json.get('assetModel', 'N/A')}
Ubicación: {datos_json.get('location', 'Ubicación desconocida')}
Detalle: posible falla / consumo alto de unidad de imagen.

Por favor, revise el equipo.

Saludos,
Sistema Automático de Alertas
"""
    return cuerpo
