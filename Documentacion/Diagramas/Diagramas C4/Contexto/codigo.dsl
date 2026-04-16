 # --- Se usó la herramienta: https://playground.structurizr.com/ ---

workspace "LeetCode Clone" {

    model {
        # === PERSONAS ===
      
        Programador = person "Programador" "Resuelve ejercicios, realiza envíos y consulta sus resultados."
        admin      = person "Administrador" "Gestiona problemas, categorías y casos de prueba."

        # === SISTEMA PRINCIPAL ===
        # Tu backend en Flask
        plataforma = softwareSystem "LeetCode clon" "Procesa la lógica; la ejecución de código y gestiona el catálogo de problemas."

        # === SISTEMAS EXTERNOS (Basados en ADR-001) ===
        supabase = softwareSystem "Supabase" "Provee la base de datos PostgreSQL, gestión de identidad (Auth JWT) y políticas de seguridad (RLS)." "External"
        docker   = softwareSystem "Motor de Ejecución" "Entorno aislado (Sandbox) que ejecuta el código de forma segura." "External"

        # === RELACIONES ===
        # El estudiante interactúa con la plataforma, pero el ADR dice que Auth es vía Supabase
        Programador -> plataforma "Ejecuta código y resuelve problemas usando" "HTTPS"
        Programador -> supabase   "Inicia sesión y obtiene token JWT a través de " "OAuth/JWT"
        
        admin      -> plataforma "Administra retos y casos de prueba en " "HTTPS"

        # El backend Flask se conecta a Supabase como dice el ADR (PostgreSQL Estándar)
        plataforma -> supabase   "Maneja la información de los usuarios; los ejercicios y envíos con" "SQL(psycopg2)"
        
        # El backend coordina la ejecución segura
        plataforma -> docker     "Envía código para ser evaluado por" "Internal API"
    }

    views {
        systemContext plataforma "Contexto" {
            include *
            autoLayout lr
        }

        styles {
            element "Person" {
                shape Person
                background #046e8f
                color #ffffff
            }
            element "Software System" {
                background #2d6a7d
                color #ffffff
            }
            element "External" {
                background #707a7d
                color #ffffff
            }
        }
    }
}