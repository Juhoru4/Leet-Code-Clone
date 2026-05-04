PROBLEMAS_MOCK = [
    {
        "id": "prob-001",
        "titulo": "Suma de dos números",
        "descripcion": "Dado dos números enteros, retorna su suma.",
        "casos_prueba": [
            {
                "id": "caso-001",
                "descripcion": "Suma básica positiva",
                "entrada": "3 5",
                "salida_esperada": "8",
                "es_publico": True,
                "orden": 1
            },
            {
                "id": "caso-002",
                "descripcion": "Suma con número negativo",
                "entrada": "-2 4",
                "salida_esperada": "2",
                "es_publico": True,
                "orden": 2
            }
        ]
    },
    {
        "id": "prob-002",
        "titulo": "Número mayor",
        "descripcion": "Dado dos números enteros, retorna el mayor.",
        "casos_prueba": [
            {
                "id": "caso-003",
                "descripcion": "Primer número mayor",
                "entrada": "9 3",
                "salida_esperada": "9",
                "es_publico": True,
                "orden": 1
            },
            {
                "id": "caso-004",
                "descripcion": "Segundo número mayor",
                "entrada": "4 7",
                "salida_esperada": "7",
                "es_publico": True,
                "orden": 2
            }
        ]
    },
    {
        "id": "prob-003",
        "titulo": "Palíndromo",
        "descripcion": "Dada una cadena de texto, retorna True si es un palíndromo y False en caso contrario.",
        "casos_prueba": [
            {
                "id": "caso-005",
                "descripcion": "Palíndromo simple",
                "entrada": "radar",
                "salida_esperada": "True",
                "es_publico": True,
                "orden": 1
            },
            {
                "id": "caso-006",
                "descripcion": "No es palíndromo",
                "entrada": "python",
                "salida_esperada": "False",
                "es_publico": True,
                "orden": 2
            },
            {
                "id": "caso-007",
                "descripcion": "Palíndromo con mayúsculas",
                "entrada": "Ana",
                "salida_esperada": "True",
                "es_publico": True,
                "orden": 3
            }
        ]
    }
]


def get_problema_por_id(problema_id):
    for problema in PROBLEMAS_MOCK:
        if problema["id"] == problema_id:
            return problema
    return None


def get_casos_prueba_publicos(problema_id):
    problema = get_problema_por_id(problema_id)
    if problema is None:
        return None
    return [c for c in problema["casos_prueba"] if c["es_publico"]]