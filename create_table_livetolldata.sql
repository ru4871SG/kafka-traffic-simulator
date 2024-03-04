-- Table: public.livetolldata

-- DROP TABLE IF EXISTS public.livetolldata;
CREATE TABLE IF NOT EXISTS public.livetolldata
(
    "timestamp" date,
    vehicle_id integer,
    vehicle_type character(15) COLLATE pg_catalog."default",
    toll_plaza_id smallint
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.livetolldata
    -- change postgres to your database username
    OWNER to postgres;