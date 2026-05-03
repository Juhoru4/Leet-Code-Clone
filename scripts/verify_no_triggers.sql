-- Verify that no triggers remain on auth.users
SELECT tg.tgname, pg_get_triggerdef(tg.oid) AS trigger_def
FROM pg_trigger tg
JOIN pg_class c ON tg.tgrelid = c.oid
JOIN pg_namespace n ON c.relnamespace = n.oid
WHERE n.nspname = 'auth' AND c.relname = 'users'
ORDER BY tg.tgname;

-- If this returns rows, there are still triggers. If empty, all triggers are gone from auth.users.
