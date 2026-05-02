#Recibe: el codigo y el lenguaje
#Envia: Resultado de la ejecucion del codigo

import subprocess
import tempfile
import os

#Configuración por lenguaje:
LENGUAJES = {
    "python": {
        "imagen": "python:3.11-slim",
        "archivo": "solution.py",
        "comando": ["python", "solution.py"],
    },
    "java": {
        "imagen": "eclipse-temurin:17-jdk",
        "archivo": "Solution.java",
        "comando": ["sh", "-c", "javac Solution.java && java Solution"],
    },
    "cpp": {
        "imagen": "gcc:13",
        "archivo": "solution.cpp",
        "comando": ["sh", "-c", "g++ solution.cpp -o solution && ./solution"],
    },
}



def ejecutar_codigo(codigo: str, lenguaje: str) -> dict:
    
    """
    Recibe el código del usuario y el lenguaje.
    Devuelve un dict con: output, error, y si hubo tiempo_limite.
    """

    config = LENGUAJES.get(lenguaje)
    if not config:
        return {"error": f"Lenguaje '{lenguaje}' no soportado"}



    with tempfile.TemporaryDirectory() as carpeta_tmp: #crea un directorio temporal

        ruta_archivo = os.path.join(carpeta_tmp, config["archivo"])
        with open(ruta_archivo, "w") as f:
            f.write(codigo)

        comando_docker = [
            "docker", "run",
            "--rm",
            "--network", "none",
            "--memory", "128m",
            "--cpus", "0.5",
            "-v", f"{carpeta_tmp}:/code",
            "-w", "/code",
            config["imagen"],
        ] + config["comando"]

        try:
            resultado = subprocess.run(
                comando_docker,
                capture_output=True,
                text=True,
                timeout=5
            )
            return {
                "output": resultado.stdout,
                "error": resultado.stderr,
                "tiempo_limite": False
            }

        except subprocess.TimeoutExpired:
            return {
                "output": "",
                "error": "Tiempo límite excedido (5 segundos)",
                "tiempo_limite": True
            }
        

"""
Para llamar y ejecutar, ejemplo:

from services.ejecutor import ejecutar_codigo

codigo = "print(10)"

resultado = ejecutar_codigo(codigo, "python")

if resultado.get("tiempo_limite"):
    print("⏱ Tu código tardó demasiado")
elif resultado["error"]:
    print("❌ Error:", resultado["error"])
else:
    print("✅ Salida:", resultado["output"])
"""