-- Replace the auth.users -> perfiles trigger with a safer version.
-- This should be executed in Supabase SQL Editor.

create or replace function public.crear_perfil_usuario()
returns trigger
language plpgsql
security definer
set search_path = public, auth
as $$
declare
    v_nombre_usuario text;
    v_rol text;
begin
    v_nombre_usuario := coalesce(
        nullif(new.raw_user_meta_data->>'nombre_usuario', ''),
        nullif(new.raw_user_meta_data->>'username', ''),
        nullif(new.raw_user_meta_data->>'user_name', ''),
        nullif(new.raw_user_meta_data->>'name', ''),
        nullif(new.raw_user_meta_data->>'nickname', ''),
        nullif(new.raw_user_meta_data->>'display_name', ''),
        nullif(split_part(coalesce(new.email, ''), '@', 1), '')
    );

    if v_nombre_usuario is null then
        v_nombre_usuario := 'user_' || replace(new.id::text, '-', '');
    end if;

    v_rol := coalesce(
        nullif(new.raw_user_meta_data->>'rol', ''),
        'estudiante'
    );

    begin
        insert into public.perfiles (
            id,
            nombre_usuario,
            nombre_completo,
            rol,
            creado_el,
            actualizado_el
        ) values (
            new.id,
            v_nombre_usuario,
            nullif(new.raw_user_meta_data->>'nombre_completo', ''),
            v_rol,
            now(),
            now()
        )
        on conflict (id) do update
        set nombre_usuario = excluded.nombre_usuario,
            nombre_completo = coalesce(excluded.nombre_completo, public.perfiles.nombre_completo),
            rol = excluded.rol,
            actualizado_el = now();
    exception when others then
        raise notice 'crear_perfil_usuario failed for user %: %', new.id, sqlerrm;
        return new;
    end;

    return new;
end;
$$;

-- If you are still debugging signup failures, do NOT recreate the trigger yet.
-- Your Flask backend now creates/updates `perfiles` after auth user creation.
-- Once signup is stable, you can re-enable the trigger if you really need it.
-- drop trigger if exists on_auth_user_created on auth.users;
-- create trigger on_auth_user_created
-- after insert on auth.users
-- for each row
-- execute function public.crear_perfil_usuario();

-- If you still get a 500 after this, the next thing to check is whether RLS policies
-- on public.perfiles block inserts/updates for this trigger (less likely with security definer,
-- but worth confirming in the dashboard).
