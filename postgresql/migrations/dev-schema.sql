CREATE SCHEMA IF NOT EXISTS dev;
CREATE SCHEMA IF NOT EXISTS public;

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'administrator') THEN
        CREATE ROLE administrator;
    END IF;

    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'app_user') THEN
        CREATE ROLE app_user;
    END IF;
END $$;

GRANT administrator TO postgres;

CREATE TABLE IF NOT EXISTS public.roles (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS dev.users (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_name TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    role_id INTEGER NOT NULL REFERENCES public.roles(id)
);

REVOKE ALL ON SCHEMA dev FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM PUBLIC;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA dev TO administrator;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO administrator;

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA dev TO administrator;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO administrator;

GRANT USAGE ON SCHEMA dev TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO administrator;

ALTER DEFAULT PRIVILEGES IN SCHEMA dev
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO administrator;

INSERT INTO public.roles (name)
VALUES ('admin'), ('user')
ON CONFLICT (name) DO NOTHING;

-- use the following to grant app_user access to specific tables
-- GRANT SELECT, INSERT, UPDATE, DELETE ON {schema}.{table} TO app_user;


commit;

DO $$ BEGIN RAISE NOTICE 'seed completed successfully'; END $$;
