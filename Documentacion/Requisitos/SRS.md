





**SRS**

Especificación de Requisitos de Software

**LeetcodeClone**

Versión 1.5

Andrés Camilo Medina

Danna Isabella Ramos

Juliana Hoyos Rueda

Valeria Robles Torres

Fecha de modificación: 12 de abril de 2026


# **Historial de Revisiones**

|**Autor**|**Fecha**|**Razón del Cambio**|**Versión**|
| :-: | :-: | :-: | :-: |
|Danna|9/04/2026|Creación inicial del documento SRS|1\.0|
|Danna|9/04/2026|Desarrollo de seccion 3: Requisitos Funcionales|1\.1|
|Juliana|11/04/2026|Desarrollo de seccion 3: Historias de Usuario|1\.2|
|Juliana|12/04/2026|Desarrollo de sección 1:  propósito del documento, alcance del producto, Definiciones, Acrónimos y Abreviaciones, Referencias.|1\.3|
|Juliana|12/04/2026|Desarrollo de sección 2:  Perspectiva del Producto, Funciones del Producto, Restricciones del Producto, Supuestos y Dependencias.|1\.4|
|Valeria|13/04/2026|Desarrollo de sección 3: Requisitos funcionales del sistema|1\.5|


# **Índice de Contenidos**

**1. Introducción**

1\.1 Propósito del Documento

1\.2 Alcance del Producto

1\.3 Definiciones, Acrónimos y Abreviaciones

1\.4 Referencias

1\.5 Visión General del Documento

**2. Visión General del Producto**

2\.1 Perspectiva del Producto

2\.2 Funciones del Producto

2\.3 Restricciones del Producto

2\.4 Características del Usuario

2\.5 Supuestos y Dependencias

2\.6 Distribución de Requisitos

**3. Requisitos**

3\.1 Historias de Usuario

3\.2 Requisitos Funcionales

3\.3 Calidad de Servicio

3\.4 Diseño e Implementación

**4. Verificación**

**5. Apéndices**


# **1. Introducción**
Esta sección presenta el propósito, el alcance y el contexto general del documento SRS para LeetcodeClone.
## **1.1 Propósito del Documento**
Este documento tiene como propósito definir los requisitos funcionales y no funcionales del sistema de práctica de programación desarrollado para la Universidad de San Buenaventura (LeetCodeClone). Sirve como guía para el desarrollo, validación y mantenimiento del sistema, alineando a todos los involucrados en el proyecto.
## **1.2 Alcance del Producto**
El sistema consiste en una plataforma web inspirada en herramientas como LeetCode, orientada a estudiantes, que permite:

- Resolver problemas de programación
- Ejecutar código
- Validar soluciones mediante datos de prueba
- Gestionar problemas por parte de administradores

El producto está enfocado en mejorar las habilidades de programación de los estudiantes en un entorno educativo.
## **1.3 Definiciones, Acrónimos y Abreviaciones**

|**Término**|**Definición**|
| :-: | :-: |
|SRS|Documento de especificación de Requisitos de Software|
|||

## **1.4 Referencias**
- Documentos del curso Laboratorio de Software III (Corte Dos y Corte Tres)
## **1.5 Visión General del Documento**


# **2. Visión General del Producto**
## **2.1 Perspectiva del Producto**
El sistema es una plataforma web educativa diseñada para la práctica de problemas de programación, inspirada en plataformas como LeetCode, pero adaptada al contexto académico de la Universidad de San Buenaventura.

El producto funciona como un sistema independiente, accesible **a través de navegador,** y forma parte del proceso de formación de estudiantes en áreas relacionadas con programación.

El sistema se compone de los siguientes módulos principales:

- **Módulo de autenticación:** gestiona el acceso seguro de usuarios
- **Módulo de problemas:** administra el catálogo de problemas
- **Módulo de ejecución de código:** permite escribir, compilar y ejecutar soluciones
- **Módulo de evaluación:** válida soluciones mediante datos de prueba
- **Módulo de seguimiento**: registra progreso y resultados
- **Módulo de administración:** permite gestionar problemas y monitorear el sistema

Además, el sistema puede integrarse en el futuro con otros servicios académicos o ampliarse con nuevas funcionalidades mediante un enfoque incremental.
## **2.2 Funciones del Producto**
El sistema incluye las siguientes funcionalidades principales:

- Autenticación de usuarios (inicio de sesión seguro)
- Visualización de problemas organizados por categoría y dificultad
- Ejecución de código en distintos lenguajes (Python, Java, C++)
- Validación de soluciones con datos de prueba
- Visualización de resultados y errores
- Gestión de problemas (crear, editar) por administradores
- Registro del progreso del usuario
- Registro de actividades del sistema (logs)
## **2.3 Restricciones del Producto**
- El sistema solo soporta inicialmente los lenguajes: Python, Java y C++
- Se requiere conexión a internet para el funcionamiento
- Solo usuarios registrados pueden acceder a funcionalidades completas
- El sistema no debe exponer información sensible del backend (seguridad)
- La ejecución de código debe estar controlada para evitar riesgos
## **2.4 Características del Usuario**
\*\*Usaer persona del estudiante y el administrador\*\*
## **2.5 Supuestos y Dependencias**
**Supuestos:**

- Los usuarios cuentan con acceso a internet
- Los estudiantes tienen conocimientos básicos en programación
- El sistema será utilizado en un entorno académico controlado
- Los usuarios interactúan mediante navegador web

**Dependencias;**

- Sistema de base de datos para almacenamiento de información
- Herramientas de ejecución de código (intérpretes/compiladores)
## **2.6 Distribución de Requisitos**


# **3. Requisitos**
## **3.1 Historias de Usuario**

|**HU-001 Autorización de Usuario**||
| :-: | :- |
|**Título:** |Acceso seguro a la plataforma|
|**Descripción:**|<p>**Cómo** estudiante de primer año de la USB,</p><p>**Quiero** iniciar sesión de forma segura,</p><p>**Para** acceder a mis problemas y soluciones.</p>|
|**Prioridad (MoSCoW):** |Must|
|**Criterios de aceptación:**|<p>**Acceso exitoso:**</p><p></p><p>**Dado que** tengo una cuenta válida</p><p>**Y** estoy en la pantalla de inicio de sesión</p><p>**Cuando** ingreso credenciales correctas</p><p>**Entonces** accedo a mi tablero personal</p><p>**Y** la sesión permanece activa con un tiempo de expiración definido.</p><p></p><p>**Acceso denegado:**</p><p></p><p>**Dado que** estoy en la pantalla de inicio de sesión</p><p>**Cuando** ingresó usuario o contraseña incorrectos</p><p>**Entonces** veo un mensaje claro de error sin revelar detalles de seguridad</p><p>**Y** permanezco en la pantalla de inicio de sesión.</p>|
###

|<a name="_weztbhue1i6"></a>**HU-002 Gestión de Problemas**||
| :-: | :- |
|**Título:** |Visualización de problemas disponibles|
|**Descripción:**|<p>**Cómo** estudiante de primer año de la USB,</p><p>**Quiero** acceder a una lista de problemas organizados por categoría y dificultad,</p><p>**Para** poder seleccionar aquellos que se ajusten a mi nivel y practicar progresivamente.</p>|
|**Prioridad (MoSCoW):** |Should|
|**Criterios de aceptación:**|<p>**Listado básico:**</p><p></p><p>**Dado que** accedo al menú “Problemas”</p><p>**Cuando** abro la lista</p><p>**Entonces** veo al menos tres problemas predefinidos con id, título, dificultad (fácil/medio/difícil) y categoría.</p><p></p><p>**Filtro por dificultad:**</p><p></p><p>**Dado que** estoy en la lista</p><p>**Cuando** filtró por “fácil”</p><p>**Entonces** solo veo problemas con dificultad “fácil”.</p>|
###

|<a name="_setjy8yugzc5"></a>**HU-003 Ejecución de Soluciones**||
| :-: | :- |
|**Título:** |Validación de código en tiempo real|
|**Descripción:**|<p>**Cómo** estudiante de primer año de la USB,</p><p>**Quiero** un entorno donde pueda escribir y ejecutar código en un lenguaje de programación seleccionado,</p><p>**Para** validar mis soluciones a los problemas de programación y corregir errores en tiempo real.</p>|
|**Prioridad (MoSCoW):** |Must|
|**Criterios de aceptación:**|<p>**Ejecución correcta:**</p><p></p><p>**Dado que** seleccioné un lenguaje soportado</p><p>**Y** programé una solución válida</p><p>**Cuando** ejecuto</p><p>**Entonces** recibo el resultado “correcto” con retroalimentación clara.</p><p></p><p>**Error de compilación:**</p><p></p><p>**Dado que** que la solución contiene un error de sintaxis o de compilación</p><p>**Cuando** intento ejecutar el código</p><p>**Entonces** el sistema detiene la ejecución antes de correr los datos de prueba</p><p>**Y** muestra un mensaje de error legible que indica la línea o el tipo de error</p><p>**Y** no revela información técnica del compilador ni rutas internas del sistema.</p><p></p><p>**Error de ejecución:**</p><p></p><p>**Dado que** la solución compila correctamente</p><p>**Y** presenta un error lógico o de ejecución (por ejemplo, división por cero, acceso a índice fuera de rango, bucle infinito)</p><p>**Cuando** ejecuto los casos de prueba</p><p>**Entonces** el sistema interrumpe la ejecución del caso que falló **Y** muestra un mensaje de error legible que describe la causa general</p><p>**Y** marca ese caso con el estado “Error de ejecución”.</p>|
###

|<a name="_i69dt16z85ah"></a>**HU-004 Datos de Prueba**||
| :-: | :- |
|**Título:** |Verificación de soluciones con datos de prueba|
|**Descripción:**|<p>**Cómo** estudiante de primer año de la USB,</p><p>**Quiero** que cada problema incluya datos de prueba predefinidos,</p><p>**Para** poder validar las soluciones antes de enviarlas definitivamente.</p>|
|**Prioridad (MoSCoW):** |Must|
|**Criterios de aceptación:**|<p>**Visualización de datos de prueba:**</p><p></p><p>**Dado que** estoy en el detalle de un problema</p><p>**Cuando** consulto la sección “Datos de prueba”</p><p>**Entonces** veo un listado de casos públicos con identificador, descripción breve, entrada y salida esperada.</p><p></p><p>**Ejecución contra datos de prueba:**</p><p></p><p>**Dado que** he programado mi solución en el editor</p><p>**Y** elijo un lenguaje soportado</p><p>**Cuando** hago clic en “Probar previo a envío”</p><p>**Entonces** el sistema ejecuta la solución contra todos los casos públicos</p><p>**Y** muestra por cada caso: estado (Aprobado/Fallo)</p>|
###

|<a name="_6svneliu24ov"></a>**HU-005 Registro de Actividades del Sistema**||
| :-: | :- |
|**Título:** |Auditoría y trazabilidad de acciones en la plataforma|
|**Descripción:**|<p>**Cómo** administrador de la plataforma,</p><p>**Quiero** que el sistema registre de forma automática las acciones relevantes realizadas por los usuarios,</p><p>**Para** disponer de un historial que facilite el monitoreo, la auditoría y la resolución de</p><p>incidencias.</p>|
|**Prioridad (MoSCoW):** |Could|
|**Criterios de aceptación:**|<p>**Registro de eventos de usuario:**</p><p></p><p>**Dado que** los usuarios realizan acciones dentro de la plataforma (por ejemplo,inicio de sesión, envío de solución, creación de problema),</p><p>**Cuando** se completa una de estas acciones,</p><p>**Entonces** el sistema genera un registro con la fecha, la hora, el usuario y el tipo de evento.</p><p></p><p>**Consulta de registros:**</p><p></p><p>**Dado que** estoy autenticado como administrador,</p><p>**Cuando** accedo a la sección “Historial del sistema”,</p><p>**Entonces** puedo visualizar los eventos ordenados cronológicamente, con filtros por usuario, tipo de evento y fecha.</p><p></p><p>Las sesiones deben gestionarse de manera independiente para garantizar la privacidad.</p>|
###

|<a name="_887ag2x7plqd"></a>**HU-006 Resolución en Múltiples Lenguajes**||
| :-: | :- |
|**Título:** |Soporte para múltiples lenguajes de programación|
|**Descripción:**|<p>**Cómo** estudiante de primer año de la USB,</p><p>**Quiero** poder resolver problemas en distintos lenguajes de programación,</p><p>**Para** practicar y desarrollar habilidades en los lenguajes más relevantes para mi formación.</p>|
|**Prioridad (MoSCoW):** |Should|
|**Criterios de aceptación:**|<p>**Selección del lenguaje:**</p><p></p><p>**Dado que** estoy en la interfaz de resolución de un problema</p><p>**Cuando** selecciono un lenguaje disponible (Python, Java o C++),</p><p>**Entonces** el editor cambia automáticamente para reflejar la plantilla que debo emplear en el lenguaje seleccionado para el problema que esté abordando.</p>|
###

|<a name="_mc0n1zsr38da"></a>**HU-007 Creación de problemas**||
| :-: | :- |
|**Título:** |Gestión de inventario de problemas|
|**Descripción:**|<p>**Cómo** administrador de la plataforma,</p><p>**Quiero** poder agregar problemas al inventario ya existente,</p><p>**Para** permitir el mantenimiento y actualización de la plataforma.</p>|
|**Prioridad (MoSCoW):** |Must|
|**Criterios de aceptación:**|<p>**Registro de un nuevo problema:**</p><p></p><p>**Dado que** estoy autenticado como administrador,</p><p>**Cuando** accedo a la opción “Agregar nuevo problema” y completo los campos requeridos,</p><p>**Entonces** el sistema guarda el problema con su título, descripción, categoría y nivel de complejidad.</p><p></p><p>**Inclusión de datos de prueba:**</p><p></p><p>**Dado que** estoy creando o editando un problema,</p><p>**Cuando** defino los conjuntos de datos de prueba (públicos y privados),</p><p>**Entonces** el sistema los almacena y asocia correctamente al problema para su futura ejecución.</p>|
###
###















## <a name="_93keb9ykfuyh"></a>**3.2 Requisitos Funcionales**
Los siguientes requisitos funcionales se derivan directamente de las historias de usuario del proyecto. Cada requisito sigue el formato: “El sistema debe…” y es verificable de forma independiente.

### **HU-01: Autorización de Usuario**
**RF-01: Inicio de sesión de usuario**

El sistema debe permitir a los usuarios autenticarse mediante correo electrónico y contraseña.

**RF-01.1: Validación de credenciales**

El sistema debe validar que las credenciales ingresadas coincidan con un usuario registrado.

**RF-01.2: Acceso al sistema**

El sistema debe redirigir al usuario a su inicio personal según su rol tras la autenticación exitosa.

**RF-01.3: Manejo de error de autenticación**

El sistema debe mostrar un mensaje de error genérico cuando las credenciales sean incorrectas.

**RF-01.4: Protección de información sensible**

El sistema no debe revelar detalles técnicos sobre errores de autenticación.

**RF-01.5: Persistencia de sesión**

El sistema debe mantener la sesión activa durante un tiempo de expiración definido por el usuario.

**RF-01.6: Expiración de sesión**

El sistema debe cerrar la sesión automáticamente al superar el tiempo de inactividad.

**RF-01.7: Acceso restringido**

El sistema debe impedir el acceso a usuarios no autenticados a funcionalidades protegidas.

**RF-01.8: Visualización de pantalla de login**

El sistema debe mostrar una interfaz de inicio de sesión accesible al usuario.

**RF-01.9: Manejo de múltiples intentos**

El sistema debe permitir múltiples intentos de inicio de sesión según la política definida.

**RF-01.10: Redirección tras fallo**

El sistema debe mantener al usuario en la pantalla de inicio de sesión tras un intento fallido.
### **HU-02: Gestión de Problemas**
**RF-02: Visualización de problemas**

El sistema debe permitir al usuario acceder a una lista de problemas disponibles.

**RF-02.1: Listado básico de problemas**

El sistema debe mostrar al menos tres problemas con identificador, título, categoría, dificultad y estado.

**RF-02.2: Organización por atributos**

El sistema debe organizar los problemas por categoría y nivel de dificultad.

**RF-02.3: Navegación al módulo de problemas**

El sistema debe permitir acceder a la sección “Problemas” desde el menú principal.

**RF-02.4: Filtro por dificultad**

El sistema debe permitir filtrar problemas por nivel de dificultad (fácil, medio, difícil).

**RF-02.5: Resultado de filtrado**

El sistema debe mostrar únicamente los problemas que coincidan con el filtro aplicado.

**RF-02.6: Persistencia del filtro**

El sistema debe mantener el filtro seleccionado mientras el usuario permanezca en la búsqueda.

**RF-02.7: Actualización dinámica**

El sistema debe actualizar la lista de problemas al aplicar filtros sin recargar la página.

**RF-02.8: Visualización clara**

El sistema debe presentar los problemas en un formato legible y estructurado.

**RF-02.9: Acceso a detalle de problema**

El sistema debe permitir seleccionar un problema para ver sus características.

**RF-02.10: Disponibilidad de problemas**

El sistema debe garantizar que los problemas listados estén disponibles para ser resueltos.

**RF-02.11: Historial de problemas resueltos**

` `El sistema debe guardar los ejercicios ya realizados por el usuario junto con su calificación.

### **HU-03: Ejecución de Soluciones**
**RF-03: Ejecución de código**

El sistema debe permitir al usuario ejecutar código en un lenguaje soportado mediante la creación de un contenedor efímero por cada ejecución.

**RF-03.1: Selección de lenguaje**

El sistema debe permitir seleccionar un lenguaje de programación disponible antes de ejecutar.

**RF-03.2: Validación de lenguaje**

El sistema debe verificar que el lenguaje seleccionado sea soportado antes de crear el contenedor.

**RF-03.3: Ejecución de solución válida**

El sistema debe ejecutar el código dentro del contenedor cuando no existan errores de compilación.

**RF-03.4: Resultado exitoso**

El sistema debe mostrar un resultado “correcto” con retroalimentación clara cuando la solución sea válida.

**RF-03.5: Detección de errores de compilación**

El sistema debe detectar errores de sintaxis o compilación antes de ejecutar los casos de prueba.

**RF-03.6: Mensaje de error de compilación**

El sistema debe mostrar un mensaje de error legible que indique la línea y el tipo de error.

**RF-03.7: Protección de información técnica**

El sistema no debe exponer rutas internas, trazas del compilador ni información del contenedor al usuario.

**RF-03.8: Detección de errores de ejecución**

El sistema debe detectar errores en tiempo de ejecución (ej. división por cero, índice fuera de rango).

**RF-03.9: Interrupción por error**

El sistema debe detener la ejecución del contenedor y destruirlo cuando ocurra un error de ejecución.

**RF-03.10: Reporte de error de ejecución**

El sistema debe indicar el caso de prueba fallido, el tipo de error y marcarlo con el estado “Error de ejecución”.

**RF-03.11: Creación de contenedor por ejecución**

El sistema debe crear un contenedor efímero e independiente para cada ejecución de código del usuario.

**RF-03.12: Destrucción del contenedor**

El sistema debe eliminar el contenedor automáticamente una vez finalizada la ejecución, ya sea exitosa, fallida o interrumpida.

**RF-03.13: Límite de tiempo de ejecución**

El sistema debe configurar el contenedor con un tiempo máximo de ejecución de 3 segundos y terminarlo forzosamente si se excede.

**RF-03.14: Notificación de tiempo excedido**

El sistema debe informar al usuario con el estado “Tiempo límite excedido” cuando el contenedor sea interrumpido por timeout.

**RF-03.15: Límite de memoria del contenedor**

El sistema debe configurar el contenedor con un límite máximo de uso de memoria RAM para prevenir el consumo excesivo de recursos del host.

**RF-03.16: Restricción de acceso a red**

El sistema debe crear el contenedor sin acceso a red externa, impidiendo llamadas a servicios o recursos de internet desde el código del usuario.

**RF-03.17: Fallo en creación del contenedor**

El sistema debe informar al usuario con un mensaje genérico si el contenedor no puede crearse, sin exponer detalles técnicos internos.

**RF-03.18: Indicador de estado de ejecución**

El sistema debe mostrar un indicador visual de “ejecutando...” mientras el contenedor está activo.

**RF-03.19: Bloqueo de ejecución paralela**

El sistema debe deshabilitar el botón de ejecución mientras haya un contenedor activo para ese usuario, evitando ejecuciones simultáneas.

**RF-03.20: Conservación del código**

El sistema debe conservar el código escrito por el usuario en el editor después de cada ejecución.

**RF-03.21: Registro de solución**

El sistema debe almacenar cada solución enviada por el usuario junto con su resultado.

**RF-03.22: Registro de puntuación**

El sistema debe asignar y almacenar una puntuación a cada solución evaluada.

**RF-03.23: Historial de intentos**

El sistema debe guardar múltiples intentos de resolución por problema y por usuario.

**RF-03.24: Visualización de resultados previos**

El sistema debe permitir al usuario consultar los resultados de sus intentos anteriores.

**RF-03.25: Asociación usuario-problema**

El sistema debe asociar cada solución almacenada con el usuario y el problema correspondiente.

### **HU-04: Datos de Prueba**
**RF-04: Visualización de datos de prueba**

El sistema debe mostrar los casos de prueba asociados a un problema.

**RF-04.1: Información de casos**

El sistema debe mostrar identificador, descripción, entrada y salida esperada.

**RF-04.2: Acceso a datos de prueba**

El sistema debe permitir acceder a los datos desde el detalle del problema.

**RF-04.3: Ejecución previa**

El sistema debe permitir validar la solución antes de enviarla definitivamente.

**RF-04.4: Evaluación de solución**

El sistema debe ejecutar la solución contra todos los casos de prueba públicos.

**RF-04.5: Resultado por caso**

El sistema debe mostrar el estado de cada caso (Aprobado / Fallo).

**RF-04.6: Identificación de fallos**

El sistema debe indicar qué casos fallaron.

**RF-04.7: Integración con editor**

El sistema debe permitir ejecutar pruebas desde el editor de código.

**RF-04.8: Consistencia de resultados**

El sistema debe garantizar que los resultados sean reproducibles.

**RF-04.9: Persistencia de resultados**

El sistema debe conservar temporalmente los resultados de ejecución.

### **HU-05: Registro de Actividades del Sistema**
**RF-05: Registro de eventos**

El sistema debe registrar automáticamente las acciones relevantes de los usuarios.

**RF-05.1: Tipos de eventos**

El sistema debe registrar eventos como inicio de sesión, envío de solución y creación de problemas.

**RF-05.2: Información del evento**

El sistema debe almacenar fecha, hora, usuario y tipo de evento.

**RF-05.3: Persistencia de logs**

El sistema debe guardar los registros en un almacenamiento persistente.

**RF-05.4: Acceso administrativo**

El sistema debe permitir que solo administradores accedan al historial del sistema.

**RF-05.5: Visualización cronológica**

El sistema debe mostrar los eventos ordenados cronológicamente.

**RF-05.6: Filtros de búsqueda**

El sistema debe permitir filtrar por usuario, tipo de evento y fecha.

**RF-05.7: Seguridad de registros**

El sistema debe proteger los registros contra accesos no autorizados.

**RF-05.8: Independencia de sesiones**

El sistema debe gestionar sesiones de forma independiente por usuario.

**RF-05.9: Auditoría del sistema**

El sistema debe permitir monitoreo para auditoría y diagnóstico.

**RF-05.10: Integridad de registros**

El sistema debe garantizar que los logs no sean alterados.

### **HU-06: Resolución en Múltiples Lenguajes**
**RF-06: Soporte multilenguaje**

El sistema debe permitir resolver problemas en múltiples lenguajes.

**RF-06.1: Lenguajes disponibles**

El sistema debe ofrecer al menos Python, Java y C++.

**RF-06.2: Selección de lenguaje**

El sistema debe permitir seleccionar el lenguaje antes de programar.

**RF-06.3: Adaptación del editor**

El sistema debe ajustar el editor al lenguaje seleccionado.

**RF-06.4: Plantillas de código**

El sistema debe cargar una plantilla base según el lenguaje.

**RF-06.5: Persistencia de selección**

El sistema debe mantener el lenguaje seleccionado durante la sesión.

**RF-06.6: Compatibilidad de ejecución**

El sistema debe ejecutar código en el lenguaje seleccionado.

**RF-06.7: Validación de ejecución**

El sistema debe validar que el código corresponda al lenguaje elegido.

**RF-06.8: Cambio de lenguaje**

El sistema debe permitir cambiar de lenguaje antes de ejecutar.

**RF-06.9: Consistencia de interfaz**

El sistema debe mantener una experiencia uniforme entre lenguajes.

**RF-06.10: Restricción de lenguajes**

El sistema debe limitar la selección a lenguajes soportados.

### **HU-07: Creación de Problemas**
**RF-07: Creación de problemas**

El sistema debe permitir a administradores crear nuevos problemas.

**RF-07.1: Autenticación de administrador**

El sistema debe restringir esta funcionalidad a usuarios administradores.

**RF-07.2: Registro de problema**

El sistema debe guardar título, descripción, categoría y dificultad.

**RF-07.3: Validación de datos**

El sistema debe validar que los campos obligatorios estén completos.

**RF-07.4: Edición de problemas**

El sistema debe permitir modificar problemas existentes.

**RF-07.5: Inclusión de datos de prueba**

El sistema debe permitir definir casos de prueba públicos y privados.

**RF-07.6: Asociación de datos**

El sistema debe asociar los datos de prueba al problema correspondiente.

**RF-07.7: Persistencia de problemas**

El sistema debe almacenar los problemas en la base de datos.

**RF-07.8: Confirmación de creación**

El sistema debe mostrar confirmación al crear un problema.

**RF-07.9: Gestión de inventario**

El sistema debe mantener un catálogo actualizado de problemas.

**RF-07.10: Accesibilidad de problemas**

El sistema debe hacer disponibles los problemas creados para los usuarios.

**Requisitos Funcionales del Sistema**

Los siguientes requisitos describen comportamientos internos del sistema que no se derivan directamente de una historia de usuario específica, pero son necesarios para garantizar el correcto funcionamiento, seguridad, integridad y trazabilidad de la plataforma.

**RF-SIS-01: Gestión de roles de usuario**

El sistema debe distinguir entre al menos dos roles (estudiante y administrador), restringiendo el acceso a funcionalidades según el rol asignado a cada cuenta registrada.

**RF-SIS-02: Creación de cuentas de usuario**

El sistema debe permitir el registro de nuevos usuarios, almacenando como mínimo nombre completo, correo electrónico, contraseña cifrada y rol asignado.

**RF-SIS-03: Cifrado de contraseñas**

El sistema debe almacenar todas las contraseñas de usuario en formato cifrado mediante un algoritmo de hash seguro, sin guardar el valor en texto plano en ningún momento.

**RF-SIS-04: Unicidad de identificadores de problemas**

El sistema debe garantizar que cada problema posea un identificador único e inmutable desde su creación, independientemente de las modificaciones posteriores a su contenido.

**RF-SIS-05: Integridad de casos de prueba privados**

El sistema debe impedir que los estudiantes accedan, visualicen o modifiquen los casos de prueba ocultos asociados a un problema; únicamente los casos públicos deben ser visibles para el estudiante.

**RF-SIS-06: Aislamiento de entornos de ejecución concurrentes**

El sistema debe garantizar que la ejecución de código de un usuario no tenga acceso al espacio de memoria, archivos ni variables de entorno de otro usuario que opere simultáneamente.

**RF-SIS-07: Registro de auditoría de autenticación**

El sistema debe registrar internamente cada intento de inicio de sesión, almacenando el identificador de usuario, timestamp y resultado del intento (exitoso o fallido), sin exponer esta información en la interfaz del usuario.

**RF-SIS-08: Registro de auditoría de envío de soluciones**

El sistema debe registrar cada envío de solución realizado, almacenando el identificador del usuario, el problema asociado, el lenguaje utilizado, el código enviado, el timestamp y el resultado obtenido.

**RF-SIS-09: Trazabilidad de acciones administrativas**

El sistema debe registrar las acciones realizadas por usuarios con rol administrador, incluyendo creación, edición y desactivación de problemas, con el identificador del administrador y el timestamp correspondiente.

**RF-SIS-10: Disponibilidad dinámica de lenguajes**

El sistema debe exponer al cliente la lista de lenguajes de programación habilitados de forma dinámica, de modo que la interfaz refleje en tiempo real cuáles están disponibles para ejecución sin necesidad de redespliegue.

**RF-SIS-11: Validación de integridad de entrada de código**

El sistema debe validar que el código enviado por el usuario no supere un tamaño máximo permitido antes de procesarlo, con el fin de proteger los recursos del servidor y el almacenamiento disponible.

**RF-SIS-12: Restricción de escritura en sistema de archivos del contenedor**

El sistema debe configurar el contenedor de ejecución de forma que el código del usuario no pueda escribir archivos fuera del directorio de trabajo temporal asignado.

**RF-SIS-13: Recuperación ante fallos de infraestructura**

El sistema debe detectar cuando un contenedor de ejecución no puede crearse por fallo de infraestructura y registrar el evento internamente, informando al usuario con un mensaje genérico sin exponer detalles técnicos.

**RF-SIS-14: Consistencia de resultados de evaluación**

El sistema debe garantizar que la ejecución del mismo código contra los mismos casos de prueba produzca siempre el mismo resultado, asegurando reproducibilidad.

**RF-SIS-15: Asociación usuario–solución–problema**

El sistema debe vincular cada solución almacenada con el usuario que la envió, el problema correspondiente, el lenguaje utilizado, el timestamp del envío y el resultado final.

**RF-SIS-16: Control de versiones de soluciones**

El sistema debe permitir almacenar múltiples versiones de solución por usuario y por problema, manteniendo el historial completo de intentos sin sobrescribir los registros anteriores.

**RF-SIS-17: Desactivación de problemas**

El sistema debe permitir a los administradores desactivar problemas del catálogo, ocultándolos de la vista de los estudiantes sin eliminar los registros históricos de soluciones asociados.

**RF-SIS-18: Validación de campos obligatorios en creación de problemas**

El sistema debe validar que todo problema creado incluya como mínimo: título, descripción, categoría, dificultad y al menos un caso de prueba público y uno privado antes de publicarlo.

**RF-SIS-19: Unicidad del correo electrónico de usuario**

El sistema debe impedir el registro de múltiples cuentas con el mismo correo electrónico, retornando un mensaje de error adecuado sin revelar si el correo ya existe en el sistema.

**RF-SIS-20: Invalidación de sesión por cierre explícito**

El sistema debe invalidar el token de sesión del usuario de forma inmediata cuando este realice un cierre de sesión explícito, impidiendo su reutilización posterior.

**RF-SIS-21: Separación de casos de prueba públicos y privados en almacenamiento**

El sistema debe almacenar los casos de prueba públicos y privados de forma separada, garantizando que las consultas dirigidas a estudiantes nunca retornen datos de los casos privados.

**RF-SIS-22: Formato de respuesta uniforme de la API**

El sistema debe retornar todas las respuestas del backend en un formato uniforme, incluyendo siempre un campo de estado y un mensaje descriptivo, tanto para operaciones exitosas como para errores.

**RF-SIS-23: Manejo centralizado de errores del backend**

El sistema debe contar con un mecanismo centralizado de manejo de errores que intercepte excepciones no controladas y retorne al cliente un mensaje genérico sin exponer trazas internas, rutas del sistema ni detalles de la base de datos.

**RF-SIS-24: Restricción de acceso a rutas protegidas por rol**

El sistema debe verificar el rol del usuario en cada solicitud a rutas protegidas, rechazando con un código de error apropiado cualquier intento de acceso por parte de un rol no autorizado.

**RF-SIS-25: Validación de formato de correo electrónico en registro**

El sistema debe validar que el correo electrónico ingresado durante el registro cumpla con un formato válido antes de procesar la solicitud, retornando un error descriptivo si el formato es incorrecto.

**RF-SIS-26: Validación de longitud mínima de contraseña**

El sistema debe rechazar el registro o cambio de contraseña si esta no cumple con una longitud mínima definida, informando al usuario del requisito sin revelar detalles de la política de seguridad interna.

**RF-SIS-27: Asociación de casos de prueba al problema correspondiente**

El sistema debe garantizar que cada caso de prueba esté asociado exclusivamente al problema para el que fue creado, impidiendo que un caso de prueba sea reutilizado o compartido entre problemas distintos.

**RF-SIS-28: Identificador único de caso de prueba**

El sistema debe asignar un identificador único global a cada caso de prueba en el momento de su creación, garantizando que dicho identificador no se repita en ninguna otra tabla ni entidad del sistema.

**RF-SIS-30: Control de acceso a registros de auditoría**

El sistema debe restringir la consulta de registros de auditoría exclusivamente a usuarios con rol administrador, rechazando cualquier solicitud proveniente de usuarios con rol estudiante.

**RF-SIS-31: Persistencia del rol asignado durante la sesión**

El sistema debe mantener el rol del usuario constante durante toda la sesión activa, impidiendo que este sea modificado sin un proceso explícito de actualización de cuenta por parte de un administrador.

**RF-SIS-32: Validación de tipos de datos en entradas del sistema**

El sistema debe validar que los datos recibidos en cada endpoint correspondan al tipo esperado (texto, número, booleano, etc.) antes de procesarlos, rechazando solicitudes con tipos de datos incorrectos.

**RF-SIS-33: Restricción de caracteres especiales peligrosos en entradas**

El sistema debe sanitizar las entradas de texto del usuario antes de procesarlas o almacenarlas, previniendo la inyección de código malicioso en la base de datos o en el entorno de ejecución.

**RF-SIS-34: Generación de respuesta de error sin información de depuración**

El sistema no debe incluir en ninguna respuesta al cliente información de depuración como stack traces, nombres de variables internas, versiones de librerías o rutas del sistema de archivos del servidor.

**RF-SIS-35: Unicidad de identificador visible de caso de prueba dentro de un problema**

El sistema debe garantizar que dentro de un mismo problema no existan dos casos de prueba con el mismo identificador visible para el usuario, tanto en el conjunto de casos públicos como en el de casos privados.

**RF-SIS-36: Registro del lenguaje utilizado por ejecución**

El sistema debe almacenar el lenguaje de programación utilizado en cada ejecución de código, de forma independiente al historial general del usuario, permitiendo trazabilidad por lenguaje.

**RF-SIS-37: Validación de existencia del problema antes de ejecutar solución**

El sistema debe verificar que el problema al que está asociada una solución exista y esté activo en el catálogo antes de permitir su ejecución, rechazando solicitudes sobre problemas inexistentes o desactivados.

**RF-SIS-38: Consistencia entre casos de prueba y resultado reportado**

El sistema debe calcular el resultado final de una solución (aprobado/fallido) únicamente a partir de la ejecución real contra los casos de prueba, sin permitir que el cliente envíe o modifique el resultado desde la interfaz.

**RF-SIS-39: Restricción de eliminación física de usuarios**

El sistema debe impedir la eliminación física de cuentas de usuario que tengan soluciones almacenadas, preservando la integridad referencial de los registros históricos asociados.

**RF-SIS-40: Verificación de integridad referencial entre solución y usuario**

El sistema debe rechazar el almacenamiento de una solución si el identificador de usuario asociado no corresponde a una cuenta existente y activa en el sistema.

**RF-SIS-41: Verificación de autorización en el backend para operaciones sobre problemas** 

*El sistema debe validar el rol del usuario directamente en el servidor en cada solicitud de creación o edición de problemas, sin depender de los controles implementados en la interfaz del cliente para tomar esa decisión de seguridad.*

**RF-SIS-42: Validación de que el campo de código no esté vacío antes de ejecutar**

El sistema debe verificar que el campo de código enviado por el usuario no esté vacío o contenga únicamente espacios en blanco antes de crear el contenedor de ejecución, retornando un error descriptivo en caso contrario.

**RF-SIS-43: Control de acceso a envíos mediante políticas de base de datos**

El sistema debe implementar políticas de seguridad a nivel de base de datos (Row Level Security) que garanticen que cada estudiante únicamente pueda consultar sus propios envíos, independientemente de la lógica del backend.

**RF-SIS-44: Visibilidad de problemas activos para usuarios autenticados**

El sistema debe garantizar mediante políticas de base de datos que únicamente los problemas con estado activo sean visibles para los usuarios autenticados, sin importar el rol del solicitante.

**RF-SIS-45: Almacenamiento de resultados por caso de prueba individual**

El sistema debe registrar el resultado de la evaluación de forma detallada, almacenando un registro individual por cada caso de prueba ejecutado dentro de un envío, indicando su estado (aprobado/fallido) y el detalle del resultado obtenido.

**RF-SIS-46: Delegación de gestión de identidad a servicio de autenticación externo**

El sistema debe delegar el registro, almacenamiento y verificación de credenciales de usuario al servicio de autenticación integrado de la plataforma (Supabase Auth), evitando la implementación manual de gestión de tokens JWT.

**RF-SIS-47: Doble capa de seguridad en control de acceso**

El sistema debe aplicar control de acceso en dos niveles: en la lógica del backend mediante verificación del rol del usuario, y en la base de datos mediante políticas RLS, garantizando que ninguna de las dos capas sea el único punto de control.

**RF-SIS-48: Optimización de consultas frecuentes mediante índices**

El sistema debe definir índices en las columnas de la base de datos que sean utilizadas frecuentemente en filtros y búsquedas, como el identificador de usuario en envíos y el identificador de problema en casos de prueba, con el fin de mantener tiempos de respuesta aceptables.

**RF-SIS-49: Uso de agrupamiento de conexiones a la base de datos**

El sistema debe utilizar un mecanismo de agrupamiento de conexiones (connection pooling) al comunicarse con la base de datos, evitando la apertura de una conexión nueva por cada solicitud y reduciendo la latencia en operaciones frecuentes.

**RF-SIS-50: Portabilidad del modelo de datos**

El sistema debe implementar el modelo de datos utilizando SQL estándar compatible con PostgreSQL, de forma que sea posible migrar la base de datos a otra instancia o proveedor sin modificaciones al esquema definido.

**RF-SIS-51: Restricción de acceso a casos de prueba privados mediante políticas de base de datos**

El sistema debe implementar políticas de seguridad a nivel de base de datos que impidan que consultas realizadas con credenciales de estudiante retornen filas correspondientes a casos de prueba marcados como privados, como segunda capa de protección adicional al control en el backend.


## **3.3 Calidad de Servicio**
### **3.3.1 Rendimiento**
El sistema debe responder a las peticiones del usuario en menos de 2 segundos bajo condiciones normales de carga.
### **3.3.2 Seguridad**
El sistema debe implementar autenticación mediante correo electrónico y contraseña. Las contraseñas deben almacenarse cifradas.
### **3.3.3 Disponibilidad**
El sistema debe garantizar una disponibilidad mínima del 99% durante los periodos de operación definidos.
## **3.4 Diseño e Implementación**
Esta sección describe las restricciones de diseño e implementación de alto nivel. Los detalles se especificarán en el documento de diseño de software (SDD).
### **3.4.1 Instalación**

### **3.4.2 Construcción y Entrega**

### **3.4.3 Portabilidad**


# **4. Verificación**
La siguiente tabla resume el método de verificación asignado a cada requisito funcional principal.

|**ID Requisito**|**Método de Verificación**|**Enlace Prueba/Artefacto**|**Estado**|**Evidencia**|
| :-: | :-: | :-: | :-: | :-: |
|RF-01|Prueba funcional||Pendiente||
|RF-02|Prueba funcional||Pendiente||
|RF-03|Prueba funcional||Pendiente||
|RF-04|Prueba funcional||Pendiente||
|RF-05|Prueba funcional||Pendiente||
|RF-06|Prueba funcional||Pendiente||
|RF-07|Prueba funcional||Pendiente||

# **5. Apéndices**

SRS – LeetcodeClone  |  Versión 0.1     Página 1
