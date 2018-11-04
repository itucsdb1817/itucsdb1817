import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS public.users
(
    id serial NOT NULL UNIQUE,
    first_name character varying(32) COLLATE pg_catalog."default" NOT NULL,
    last_name character varying(32) COLLATE pg_catalog."default" NOT NULL,
    creation_date timestamp without time zone NOT NULL DEFAULT now(),
    birth_date timestamp without time zone NOT NULL,
    post_karma integer NOT NULL DEFAULT 0,
    comment_karma integer NOT NULL DEFAULT 0,
    is_admin boolean NOT NULL DEFAULT false,
    is_banned boolean NOT NULL DEFAULT false,
    username character varying(32) COLLATE pg_catalog."default" NOT NULL,
    password character varying(32) COLLATE pg_catalog."default" NOT NULL,
    email character varying(256) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT user_id_primary PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.users
    OWNER to itucs;""",

    """
    CREATE TABLE IF NOT EXISTS public.votes
(
    id serial NOT NULL UNIQUE,
    date timestamp without time zone NOT NULL,
    parent_type character varying(32) COLLATE pg_catalog."default" NOT NULL,
    passed_time interval NOT NULL,
    vote boolean NOT NULL,
    user_id integer NOT NULL,
    CONSTRAINT vote_id_pk PRIMARY KEY (id),
    CONSTRAINT user_id_fk FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.votes
    OWNER to itucs;
    """,
    """
    CREATE TABLE IF NOT EXISTS public.reports
(
    id serial NOT NULL UNIQUE,
    violated_rule text COLLATE pg_catalog."default" NOT NULL,
    date timestamp without time zone NOT NULL,
    reason_description text COLLATE pg_catalog."default",
    action_taken text COLLATE pg_catalog."default" NOT NULL,
    is_dismissed boolean NOT NULL,
    post_id integer,
    comment_id integer,
    CONSTRAINT report_id_pk PRIMARY KEY (id),
    CONSTRAINT comment_id_fk FOREIGN KEY (comment_id)
        REFERENCES public.comments (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT post_id_fk FOREIGN KEY (post_id)
        REFERENCES public.posts (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.reports
    OWNER to itucs;

    """,
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
