**ADR-001: Selección de PostgreSQL (Supabase) como Sistema de Persistencia**

**Tipo de documento:** Architecture Decisión Record

**Proyecto:** Plataforma de Juez de Programación – USB

**Fecha:** 2 de marzo de 2026

**Estado:** Revision

**Contexto**

El proyecto requiere una base de datos relacional para almacenar usuarios, problemas de programación, casos de prueba, envíos de código y resultados de ejecución. Se necesita:

1. **Modelo relacional robusto:** Las entidades tienen relaciones claras (usuario -> envíos -> resultados; problema -> casos de prueba).
2. **Autenticación integrada:** Se requiere un sistema de auth con JWT, sesiones con expiración y manejo seguro de credenciales.
3. **Seguridad a nivel de fila:** Cada estudiante solo debe poder ver sus propios envíos.
4. **Facilidad de despliegue:** El equipo es académico con tiempo limitado; se necesita una solución gestionada.

   **Decisión**

   Se utilizará PostgreSQL como motor de base de datos, hospedado en Supabase como plataforma de infraestructura gestionada (BaaS — Backend as a Service).

   **Consecuencia**

   **Positivas**

- **Reducción drástica del time-to-market:** Auth, BD, storage y realtime listos sin configuración de infraestructura.
- **Seguridad reforzada:** RLS nativo asegura aislamiento de datos a nivel de BD, no solo de aplicación.
- **Free tier generoso:** Suficiente para todo el proyecto.
- **Dashboard visual:** Facilita la gestión de datos, usuarios y depuración durante el desarrollo.

  **Negativas**
- **Vendor lock-in parcial:** Si bien la BD es PostgreSQL estándar (portable), las features de Auth y RLS de Supabase crean dependencia.
- **Latencia de red:** La BD está en la nube; queries complejas pueden tener mayor latencia que una BD local.

  **Mitigaciones**
- **Portabilidad:** El modelo de datos son estándar — migrar a otro PostgreSQL es trivial.
- **Latencia:** Se usa connection pooling y se optimizan queries con índices adecuados.
- **Límites:** Para el scope académico, el free tier es más que suficiente.

  **Modelo de Datos**

  El sistema utiliza un modelo relacional compuesto principalmente por las siguientes entidades:**
- **profiles**

  ` `Información de los usuarios de la plataforma.
- **categories**

  ` `Clasificación de problemas por temática.
- **problems**

  ` `Problemas de programación disponibles para resolver.
- **test\_cases**

  ` `Casos de prueba asociados a cada problema.
- **submissions**

  ` `Envíos de código realizados por los usuarios.
- **submission\_results**

  ` `Resultados detallados de la evaluación de cada caso de prueba.

La autenticación y gestión de usuarios se delega a la tabla auth.users, gestionada automáticamente por Supabase.

**Seguridad y Control de Acceso**

El sistema utiliza **Row Level Security (RLS)** de PostgreSQL para controlar el acceso a los datos.

Principios aplicados:

- Los estudiantes **solo pueden visualizar sus propios envíos**.
- Los problemas activos son **visibles para todos los usuarios autenticados**.
- Los casos de prueba **privados no son visibles para los estudiantes**.

Este enfoque garantiza que la seguridad no dependa únicamente de la lógica del backend, sino también de las políticas definidas a nivel de base de datos.

**Glosario**

- **sistema de auth con JWT:** Forma común de manejar la autenticación en aplicaciones web, El usuario se identifica, El servidor genera un JWT (JSON Web Token), El cliente (navegador/app móvil) guarda ese token y lo adjunta en cada petición posterior, El servidor verifica la firma del JWT en cada solicitud para saber quién es el usuario y si el token sigue válido, sin necesidad de consultar la base de datos en cada llamada.
- **PostgreSQL será hospedado en Supabase como BaaS:** Supabase es una plataforma de “Backend as a Service” para bases de datos PostgreSQL. Proporciona una instancia administrada de PostgreSQL, accesible vía API sin tener que instalar o gestionar un servidor de base de datos.
- **Auth, BD, storage y realtime:** Son las características principales que ofrece Supabase como Backend as a Service (BaaS).

  **Auth:** Sistema de autenticación integrado, que incluye registro, login, gestión de usuarios y tokens JWT para verificar identidades.

  **BD:** Base de datos PostgreSQL administrada, donde almacenas y consultas datos de manera relacional.

  **Storage:** Servicio para subir, gestionar y servir archivos (imágenes, documentos) con URLs públicas o privadas.

  **Realtime:** Funcionalidades para actualizaciones en tiempo real, como suscripciones a cambios en la base de datos (ej. notificaciones cuando se inserta un registro).
- **RLS nativo asegura aislamiento de datos a nivel de BD:** Se refiere a Row Level Security (RLS) en PostgreSQL. Es una característica nativa de PostgreSQL que permite definir políticas de seguridad directamente en las tablas de la base de datos. Estas políticas filtran automáticamente las filas que un usuario puede ver o modificar, basado en su identidad (ej. solo ver sus propios registros).
