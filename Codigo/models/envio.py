ENVIOS_MOCK=[]

def guardar_envio(submission_id, problema_id, lenguaje_programacion, codigo):
    envio={
        "id": submission_id,
        "problema_id": problema_id,
        "lenguaje_programacion": lenguaje_programacion,
        "codigo": codigo,
        "estado": "en cola",
        "resultado": [] 
    }
    
    ENVIOS_MOCK.append(envio)
    return envio

def obtener_envio(submission_id):
    for envios in ENVIOS_MOCK:
        if envios["id"]==submission_id:
            return envios
    return None

def actualizar_resultados(submission_id, resultado):
    envio=obtener_envio(submission_id)
    if envio is not None:
        envio["estado"]= "Completado"
        envio["resultado"]= resultado
    return envio
