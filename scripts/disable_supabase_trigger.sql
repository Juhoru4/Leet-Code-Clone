-- Temporary/definitive fix: disable the auth.users trigger that creates perfiles.
-- Your Flask backend already creates/updates the profile after user creation.

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;

-- Keep the function in case you want to re-enable it later, but it will no longer run.
-- If you want a clean database later, you can also drop the function:
-- DROP FUNCTION IF EXISTS public.crear_perfil_usuario();
