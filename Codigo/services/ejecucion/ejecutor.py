"""Ejecuta codigo de usuario en contenedores aislados y devuelve resultados."""

import subprocess
import tempfile
import os
import re
import ast
import textwrap

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


# Patrones que identifican errores de compilación por lenguaje
PATRONES_COMPILACION = {
    "python": [],
    "java": [
        "error:",
        "cannot find symbol",
        "reached end of file",
        "illegal start of expression",
    ],
    "cpp": [
        "error:",
        "expected",
        "undeclared",
        "no match for",
    ],
}

def es_error_compilacion(stderr: str, lenguaje: str) -> bool:
    
    #identifica si es un error de compilacion

    patrones = PATRONES_COMPILACION.get(lenguaje, [])
    stderr_lower = stderr.lower()
    return any(patron in stderr_lower for patron in patrones)

def limpiar_mensaje_error(stderr: str) -> str:
    lineas = stderr.strip().splitlines()
    limpias = []
    
    for linea in lineas:

        linea = linea.replace("/code/", "")

        if re.match(r"^\s+at\s+\w+", linea):
            continue

        if re.match(r"^\d+ error(s)?$", linea.strip()):
            continue

        if linea.strip():
            limpias.append(linea)

    return "\n".join(limpias)


def tiene_main_java(codigo: str) -> bool:
    return re.search(r"\bstatic\s+void\s+main\s*\(", codigo) is not None


def tiene_main_cpp(codigo: str) -> bool:
    return re.search(r"\bint\s+main\s*\(", codigo) is not None


def extraer_funcion_cpp(codigo: str):
    patron = re.compile(
        r"^[\t ]*[\w:<>&*\s]+\s+([A-Za-z_]\w*)\s*\(([^)]*)\)\s*\{",
        re.MULTILINE
    )
    for match in patron.finditer(codigo):
        nombre = match.group(1)
        if nombre == "main":
            continue
        params = (match.group(2) or "").strip()
        return nombre, params
    return None, ""


def parametros_cpp_soportados(params: str) -> str:
    if not params:
        return "sin_param"
    if "," in params:
        return "no_soportado"
    if re.search(r"\bstd::string\b|\bstring\b", params):
        return "string"
    return "no_soportado"


def ejecutar_codigo(codigo: str, lenguaje: str, timeout_ms: int = None, memory_mb: int = None) -> dict:

    # Recibe el código del usuario y el lenguaje, devuelve un dict con:
    # stdout, stderr, tipo_error, supero_tiempo_limite

    config = LENGUAJES.get(lenguaje)
    if not config:
        return {"error": f"Lenguaje '{lenguaje}' no soportado"}



    # Para Python: si el código define una función pero no tiene
    # un bloque `if __name__ == "__main__"`, añadimos un wrapper
    # que invoque la última función definida y haga `print` de su retorno.
    codigo_a_escribir = codigo
    usar_runner_java = False
    usar_runner_cpp = False
    cpp_funcion = None
    cpp_parametro = ""
    if lenguaje == "python":
        try:
            tree = ast.parse(codigo)
            func_defs = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
            has_main = any(
                isinstance(n, ast.If) and
                any(isinstance(x, ast.Name) and x.id == "__name__" for x in ast.walk(n.test))
                for n in tree.body if isinstance(n, ast.If)
            )

            if func_defs and not has_main:
                last = func_defs[-1]
                fname = last.name
                wrapper = textwrap.dedent(f"""
# Auto-generated invocation wrapper
if __name__ == '__main__':
    import sys, traceback
    _input = sys.stdin.read().strip()
    try:
        try:
            _res = {fname}()
        except TypeError:
            try:
                _res = {fname}(_input)
            except TypeError:
                _res = None
        if _res is not None:
            print(_res)
    except Exception:
        traceback.print_exc()
""")
                codigo_a_escribir = codigo + wrapper
        except Exception:
            # Si falla el parseo, no alteramos el código
            codigo_a_escribir = codigo
    elif lenguaje == "java":
        usar_runner_java = not tiene_main_java(codigo)
    elif lenguaje == "cpp":
        usar_runner_cpp = not tiene_main_cpp(codigo)
        if usar_runner_cpp:
            cpp_funcion, cpp_parametro = extraer_funcion_cpp(codigo)
            if not cpp_funcion:
                cpp_funcion = "solve"
                cpp_parametro = ""

    with tempfile.TemporaryDirectory() as carpeta_tmp: #crea un directorio temporal

        ruta_archivo = os.path.join(carpeta_tmp, config["archivo"])
        with open(ruta_archivo, "w", encoding="utf-8", newline="\n") as f:
            f.write(codigo_a_escribir)

        if lenguaje == "java" and usar_runner_java:
            runner_code = (
                "public class Runner {\n"
                "    public static void main(String[] args) throws Exception {\n"
                "        java.io.BufferedReader br = new java.io.BufferedReader(\n"
                "            new java.io.InputStreamReader(System.in)\n"
                "        );\n"
                "        StringBuilder sb = new StringBuilder();\n"
                "        String line;\n"
                "        while ((line = br.readLine()) != null) {\n"
                "            sb.append(line);\n"
                "            sb.append(\"\\n\");\n"
                "        }\n"
                "        String input = sb.toString();\n"
                "        Class<?> cls = Class.forName(\"Solution\");\n"
                "        java.lang.reflect.Method target = null;\n"
                "        for (java.lang.reflect.Method m : cls.getDeclaredMethods()) {\n"
                "            int mod = m.getModifiers();\n"
                "            if (!java.lang.reflect.Modifier.isStatic(mod)) continue;\n"
                "            if (!java.lang.reflect.Modifier.isPublic(mod)) continue;\n"
                "            if (m.getName().equals(\"main\")) continue;\n"
                "            Class<?>[] params = m.getParameterTypes();\n"
                "            if (params.length == 0 || (params.length == 1 && params[0].equals(String.class))) {\n"
                "                target = m;\n"
                "                break;\n"
                "            }\n"
                "        }\n"
                "        if (target == null) {\n"
                "            throw new RuntimeException(\"No public static method found to execute.\");\n"
                "        }\n"
                "        Object result;\n"
                "        if (target.getParameterCount() == 0) {\n"
                "            result = target.invoke(null);\n"
                "        } else {\n"
                "            result = target.invoke(null, input);\n"
                "        }\n"
                "        if (target.getReturnType() != Void.TYPE && result != null) {\n"
                "            System.out.print(result.toString());\n"
                "        }\n"
                "    }\n"
                "}\n"
            )
            runner_path = os.path.join(carpeta_tmp, "Runner.java")
            with open(runner_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(runner_code)

        if lenguaje == "cpp" and usar_runner_cpp:
            modo_parametro = parametros_cpp_soportados(cpp_parametro)
            runner_code = (
                "#include <iostream>\n"
                "#include <string>\n"
                "#include \"solution.cpp\"\n"
                "int main() {\n"
                "    std::string input;\n"
                "    std::string line;\n"
                "    while (std::getline(std::cin, line)) {\n"
                "        if (!input.empty()) {\n"
                "            input.push_back('\\n');\n"
                "        }\n"
                "        input += line;\n"
                "    }\n"
                "    std::cout << std::boolalpha;\n"
            )
            if modo_parametro == "sin_param":
                runner_code += (
                    f"    auto result = {cpp_funcion}();\n"
                    "    std::cout << result;\n"
                )
            elif modo_parametro == "string":
                runner_code += (
                    f"    auto result = {cpp_funcion}(input);\n"
                    "    std::cout << result;\n"
                )
            else:
                runner_code += (
                    "    std::cerr << \"Firma de funcion no soportada para ejecucion automatica.\";\n"
                    "    return 1;\n"
                )
            runner_code += "    return 0;\n}\n"
            runner_path = os.path.join(carpeta_tmp, "Runner.cpp")
            with open(runner_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(runner_code)

        # determinar memoria y timeout
        mem_flag = f"{memory_mb}m" if memory_mb else "128m"
        timeout_seconds = (timeout_ms / 1000) if timeout_ms else 10

        comando_base = config["comando"]
        if lenguaje == "java" and usar_runner_java:
            comando_base = ["sh", "-c", "javac Solution.java Runner.java && java Runner"]
        if lenguaje == "cpp" and usar_runner_cpp:
            comando_base = ["sh", "-c", "g++ Runner.cpp -o solution && ./solution"]

        comando_docker = [
            "docker", "run",
            "--rm",
            "--network", "none",
            "--memory", mem_flag,
            "--cpus", "0.5",
            "-v", f"{carpeta_tmp}:/code",
            "-w", "/code",
            config["imagen"],
        ] + comando_base

        try:
            resultado = subprocess.run(
                comando_docker,
                capture_output=True,
                text=True,
                timeout=timeout_seconds
            )

            # si hubo stderr, clasificamos
            stderr_raw = resultado.stderr or ""
            stdout_raw = resultado.stdout or ""
            mensaje_limpio = limpiar_mensaje_error(stderr_raw)

            if stderr_raw:
                if es_error_compilacion(stderr_raw, lenguaje):
                    return {
                        "stdout": "",
                        "stderr": mensaje_limpio,
                        "tipo_error": "compilacion",
                        "supero_tiempo_limite": False,
                        "timeout": False
                    }
                else:
                    return {
                        "stdout": stdout_raw,
                        "stderr": mensaje_limpio,
                        "tipo_error": "ejecucion",
                        "supero_tiempo_limite": False,
                        "timeout": False
                    }

            # sin errores
            return {
                "stdout": stdout_raw,
                "stderr": "",
                "tipo_error": None,
                "supero_tiempo_limite": False,
                "timeout": False
            }

        #se exedio el limite del tiempo
        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": f"Tiempo límite excedido ({timeout_seconds} segundos)",
                "tipo_error": "timeout",
                "supero_tiempo_limite": True,
                "timeout": True
            }
        
        #error al crear el contenedor
        except FileNotFoundError as e:
            #Docker no está instalado o no está en el PATH
            return {
                "stdout": "",
                "stderr": "Docker no está instalado o no está en el PATH. Asegúrate de tener Docker Desktop abierto y en ejecución.",
                "tipo_error": "sistema",
                "supero_tiempo_limite": False,
                "timeout": False
            }

        except Exception as e:
            #Cualquier otro fallo relacionado con el contenedor
            error_msg = str(e)
            if "image" in error_msg.lower() and "not found" in error_msg.lower():
                stderr_msg = "Las imágenes de Docker no están disponibles. Ejecuta: docker pull python:3.11-slim eclipse-temurin:17-jdk gcc:13"
            elif "cannot connect" in error_msg.lower() or "daemon" in error_msg.lower():
                stderr_msg = "No se puede conectar a Docker. Asegúrate de que Docker Desktop esté abierto y en ejecución."
            else:
                stderr_msg = f"Error del sistema: {error_msg}"
            
            return {
                "stdout": "",
                "stderr": stderr_msg,
                "tipo_error": "sistema",
                "supero_tiempo_limite": False,
                "timeout": False
            }
        