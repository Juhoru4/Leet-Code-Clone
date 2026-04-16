 # --- Se usó la herramienta: https://playground.structurizr.com/ ---

workspace "LeetCode Clone" "Diagrama de Componentes - Nivel 3" {

    model {
        estudiante = person "Estudiante" "Usuario que resuelve retos."
        admin      = person "Administrador" "Gestiona problemas."

        # INFRAESTRUCTURA EXTERNA
        supabase = softwareSystem "Supabase" "Servicios de Auth y Base de Datos." "External,Database"
        dockerHost = softwareSystem "Motor de Ejecución (Host)" "Docker Engine para sandboxes." "External"

        plataforma = softwareSystem "Plataforma Juez" {
            
            # --- ZOOM FRONTEND ---
            frontend = container "Aplicación Web" "Interfaz de usuario." "React / Next.js" {
                authContext = component "AuthContext / useAuth" "Maneja el estado de sesión y tokens JWT." "React Context"
                apiClient = component "API Client" "Fetch wrapper con cabeceras de autorización." "TypeScript"
                problemComponents = component "Problem Components" "Lista y detalle de retos (ProblemCard, Editor)." "React Components"
                submissionView = component "Submission View" "Muestra resultados y estadísticas." "React Components"
            }

            # --- ZOOM BACKEND ---
            backend = container "API Backend" "Lógica de negocio y orquestación." "Python / Flask" {
                flaskApp = component "Flask Application " "Configura la app y registra Blueprints." "Flask"
                authBP = component "Auth Blueprint" "Endpoints para registro y validación de usuarios." "Flask Blueprint"
                problemsBP = component "Problems Blueprint" "Gestión de retos y categorías." "Flask Blueprint"
                submissionsBP = component "Submissions Blueprint" "Recibe códigos y consulta estados." "Flask Blueprint"
                execService = component "CodeExecutionService" "Servicio de dominio que coordina con Celery y Docker." "Python Class"
                dbModels = component "Modelos ORM" "Mapeo de tablas (Profiles, Submissions, etc.)." "SQLAlchemy"
            }

            redis = container "Cola de Tareas" "Broker de mensajes." "Redis"
            worker = container "Worker" "Proceso que ejecuta el código." "Celery Worker"
        }

        # --- RELACIONES COMPONENTES ---
        estudiante -> problemComponents "Ve retos y escribe código"
        problemComponents -> apiClient "Envía submit"
        apiClient -> authContext "Obtiene JWT"
        
        # Conexión Frontend -> Backend
        apiClient -> flaskApp "Peticiones HTTPS/JWT"
        
        # Lógica Interna Backend
        flaskApp -> authBP "Enruta"
        flaskApp -> problemsBP "Enruta"
        flaskApp -> submissionsBP "Enruta"
        
        authBP -> supabase "Valida identidad"
        problemsBP -> dbModels "Consulta retos"
        submissionsBP -> execService "Solicita ejecución"
        
        execService -> redis "Encola tarea (run_code.delay)"
        execService -> dbModels "Crea registros iniciales"
        
        # Conexión Worker (Fuera del Backend pero parte del flujo)
        worker -> redis "Lee tareas"
        worker -> dockerHost "Instancia Sandbox"
        worker -> dbModels "Actualiza resultados finales"
        
        dbModels -> supabase "Persistencia en PostgreSQL"
    }

    views {
        # Vista de Componentes del Backend
        component backend "Componentes_Backend" {
            include *
            autoLayout lr
        }

        # Vista de Componentes del Frontend
        component frontend "Componentes_Frontend" {
            include *
            autoLayout lr
        }

        styles {
            element "Component" {
                background #85BBF0
                color #000000
            }
            element "External" {
                background #999999
                color #ffffff
            }
            element "Container" {
                background #438DD5
                color #ffffff
            }
            
                element "Database" {
                 shape Cylinder
                 background #FFCE1B
                 color #ffffff
            }
        }
    }
}