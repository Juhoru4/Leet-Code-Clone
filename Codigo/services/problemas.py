PROBLEMAS_MOCK = [
    {
        "id": 1,
        "titulo": "Suma de dos números",
        "descripcion": "Dado dos números enteros, retorna su suma.",
        "casos_de_prueba": [
            {
                "id": 1,
                "descripcion": "Suma básica positiva",
                "input": "3 5",
                "expected_output": "8"
            },
            {
                "id": 2,
                "descripcion": "Suma con número negativo",
                "input": "-2 4",
                "expected_output": "2"
            }
        ]
    },
    {
        "id": 2,
        "titulo": "Número mayor",
        "descripcion": "Dado dos números enteros, retorna el mayor.",
        "casos_de_prueba": [
            {
                "id": 1,
                "descripcion": "Primer número mayor",
                "input": "9 3",
                "expected_output": "9"
            },
            {
                "id": 2,
                "descripcion": "Segundo número mayor",
                "input": "4 7",
                "expected_output": "7"
            }
        ]
    },
    
    {
        "id": 3,
        "titulo": "Palíndromo",
        "descripcion": "Dada una cadena de texto, retorna True si es un palíndromo (se lee igual de izquierda a derecha que de derecha a izquierda) y False en caso contrario.",
        "casos_de_prueba": [
            {
                "id": 1,
                "descripcion": "Palíndromo simple",
                "input": "radar",
                "expected_output": "True"
            },
            {
                "id": 2,
                "descripcion": "No es palíndromo",
                "input": "python",
                "expected_output": "False"
            },
            {
                "id": 3,
                "descripcion": "Palíndromo con mayúsculas",
                "input": "Ana",
                "expected_output": "True"
            }
        ]
    }
]


def get_problema_por_id(problem_id):
    for problema in PROBLEMAS_MOCK:
        if problema["id"] == problem_id:
            return problema
    return None


def get_casos_prueba(problem_id):
    problema = get_problema_por_id(problem_id)
    if problema is None:
        return None
    return problema["casos_de_prueba"]