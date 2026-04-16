 # --- Se usó la herramienta: https://playground.structurizr.com/ ---

workspace "LeetCode Clone" "Arquitectura de Contenedores" {

    model {
        estudiante = person "Estudiante" "Usuario que resuelve retos y consulta sus envíos."
        admin      = person "Administrador" "Gestiona problemas y casos de prueba."

        plataforma = softwareSystem "Plataforma Juez" "Permite resolver problemas de código." {
            webApp = container "Aplicación Web" "Interfaz de usuario." "React / Next.js"
            
            backend = container "API Backend" "Lógica de negocio y validación de envíos." "Python / Flask"
            
            # --- DESGLOSE DE SUPABASE (Persistencia y Auth) ---
          
            database = container "Base de Datos (PostgreSQL)" "Almacena perfiles, problemas, casos_prueba y envíos (esquema public)." "Supabase / Postgres" "Database"
            
            authService = container "Servicio de Auth (GoTrue)" "Gestiona el registro y validación de tokens JWT." "Supabase Auth" "Auth"
            
            # --- INFRAESTRUCTURA  ---
            motorEjecucion = container "Motor de Ejecución" "Ejecuta código en sandboxes (Python, Java, C++)." "Docker Engine" "Docker"
            redis = container "Cola de Tareas" "Gestión de concurrencia de envíos." "Redis"
        }

        # --- RELACIONES ---
        estudiante -> webApp "Usa" "HTTPS"
        admin      -> webApp "Usa" "HTTPS"
        
        # Flujo de Identidad (ADR-001)
        webApp -> authService "Solicita Token JWT" "HTTPS/JSON"
        webApp -> backend "Envía código + JWT" "HTTPS/JWT"
        
        # Flujo de Persistencia (ADR-001)
        # Flask usa psycopg2 para hablar directamente con Postgres
        backend -> database "Persistencia de datos (profiles, submissions)" "SQL (psycopg2)"
        
        # Flujo de Ejecución (Camilo)
        backend -> redis "Encola evaluación" "Redis Protocol"
        backend -> motorEjecucion "Lanza sandbox (--rm, --network=none)" "Docker SDK"
    }

    views {
        container plataforma "Contenedores" {
            include *
            autoLayout lr
        }

        styles {
            element "Element" {
                color #ffffff
            }
            element "Person" {
                background #08427B
                shape Person
            }
            element "Container" {
                background #438DD5
            }
            # Estilos específicos para persistencia y soporte
            element "Database" {
                background #336791
                shape Cylinder
            }
            element "Auth" {
                background #2496ED
                shape Component
            }
            element "Docker" {
                background #08427B
                shape Cylinder
            }
        }
    }
}