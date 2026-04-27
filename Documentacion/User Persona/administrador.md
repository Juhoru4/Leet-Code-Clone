# Definición de User Personas - LeetCode Clone

Este documento describe los perfiles de usuario principales identificados para la plataforma, basándose en la arquitectura del sistema y en los objetivos educativos del proyecto.

---

## 1. El Programador (Estudiante)
**Perfil:** Mateo, el Estudiante de Ingeniería.

| Atributo | Detalle |
| :--- | :--- |
| **Edad** | 20 años |
| **Ocupación** | Estudiante de 2º año de Ingeniería Informática |
| **Nivel Técnico** | Principiante / Intermedio |
| **Cita** | *"Quiero practicar lo que veo en clase sin miedo a romper nada y saber al instante si mi lógica es correcta."* |

### Motivaciones y Metas
* **Feedback inmediato:** Saber si su código pasa los casos de prueba sin esperar a la corrección del profesor.
* **Preparación técnica:** Mejorar su lógica de programación para futuros exámenes o entrevistas de prácticas.
* **Autonomía:** Disponer de un entorno listo para programar sin tener que configurar compiladores locales complejos.

### Frustraciones
* Mensajes de error poco claros que no ayudan a identificar el fallo en la lógica.
* Perder el progreso de sus soluciones anteriores.
* Sentirse bloqueado si un problema es demasiado difícil sin una progresión clara.

### Uso del sistema
* Accede al catálogo para buscar retos por dificultad o categoría.
* Utiliza el editor para realizar múltiples ejecuciones antes de enviar la solución definitiva.
* Consulta su historial de envíos y resultados en Supabase.

---

## 2. El Administrador (Docente)
**Perfil:** Dra. Elena, la Profesora de Algoritmos.

| Atributo | Detalle |
| :--- | :--- |
| **Edad** | 42 años |
| **Ocupación** | Catedrática de Programación y Estructuras de Datos |
| **Nivel Técnico** | Avanzado |
| **Cita** | *"Necesito una forma centralizada de proponer retos y evaluar el desempeño del grupo de forma automatizada."* |

### Motivaciones y Metas
* **Estandarización:** Que todos los alumnos trabajen sobre los mismos retos y casos de prueba.
* **Eficiencia en el tiempo:** Reducir la carga de corrección manual mediante la validación automática del motor de ejecución.
* **Gestión de contenido:** Mantener un banco de problemas actualizado y categorizado por temas académicos (listas, árboles, grafos).

### Frustraciones
* La complejidad de gestionar múltiples archivos de código enviados por correo u otras plataformas.
* La posibilidad de que los estudiantes utilicen bibliotecas no permitidas (seguridad en el sandbox).
* Procesos tediosos para cargar nuevos casos de prueba.

### Uso del sistema
* Utiliza el módulo de administración para crear, editar y eliminar retos.
* Define los parámetros de entrada y los resultados esperados (test cases).
* Monitoriza la participación general a través de la persistencia de datos en Supabase.

---

## Resumen de Interacciones según la Arquitectura

| Acción | Programador (Mateo) | Administrador (Elena) |
| :--- | :--- | :--- |
| **Entrada al sistema** | Login mediante JWT (Supabase). | Login con permisos de gestión. |
| **Gestión de retos** | Lectura y consulta. | Escritura, edición y eliminación. |
| **Ejecución de código** | Envía código para validar su aprendizaje. | Envía código para probar la validez del reto creado. |
| **Seguridad** | Aislado en el sandbox del motor de ejecución. | Define los límites y políticas del sistema. |