import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    'DROP TABLE IF EXISTS public.reports CASCADE',
    'DROP TABLE IF EXISTS public.votes CASCADE',
    'DROP TABLE IF EXISTS public.comments CASCADE',
    'DROP TABLE IF EXISTS public.posts CASCADE',
    'DROP TABLE IF EXISTS public.tags CASCADE',
    'DROP TABLE IF EXISTS public.users CASCADE',
    'DROP TABLE IF EXISTS public.tag_moderators CASCADE',
    'DROP TABLE IF EXISTS public.tag_subscriptions CASCADE',

    """
    CREATE TABLE comments (
        id serial  NOT NULL,
        user_id int  NOT NULL,
        post_id int  NOT NULL,
        parent_id int  NULL,
        content_type varchar(32)  NOT NULL,
        content text  NOT NULL,
        is_external boolean  NOT NULL,
        rank_score bigint  NOT NULL,
        date timestamp  NOT NULL,
        current_vote int  NOT NULL,
        CONSTRAINT comments_pk PRIMARY KEY (id)
    );
    """,

    """
    CREATE TABLE posts (
        id serial  NOT NULL,
        user_id int  NOT NULL,
        tag_id int NOT NULL,
        date timestamp  NOT NULL,
        title varchar(32)  NOT NULL,
        content_type varchar(32)  NOT NULL,
        content text  NOT NULL,
        content_html  NOT NULL,
        is_external boolean  NOT NULL,
        current_vote int  NOT NULL,
        rank_score bigint  NOT NULL,
        is_banned boolean  NOT NULL,
        comment_count int  NOT NULL,
        CONSTRAINT posts_pk PRIMARY KEY (id)
    );
    """,

    """
    CREATE TABLE reports (
        id serial  NOT NULL,
        submitting_user_id int  NOT NULL,
        violated_rule text  NOT NULL,
        date timestamp  NOT NULL,
        reason_description text  NOT NULL,
        is_comment int  NOT NULL,
        action_taken text  NULL,
        is_dismissed boolean  NOT NULL,
        post_id int  NULL,
        comment_id int  NULL,
        CONSTRAINT reports_pk PRIMARY KEY (id)
    );
    """,

    """
    CREATE TABLE tag_moderators (
        id serial  NOT NULL,
        date timestamp  NOT NULL,
        user_id int  NOT NULL,
        tag_id int  NOT NULL,
        CONSTRAINT tag_moderators_pk PRIMARY KEY (id)
    );
    """,


    """
    CREATE TABLE tag_subscriptions (
        id serial  NOT NULL,
        date timestamp  NOT NULL,
        user_id int  NOT NULL,
        tag_id int  NOT NULL,
        CONSTRAINT tag_subscriptions_pk PRIMARY KEY (id)
    );
    """,

    """
    CREATE TABLE tags (
        id serial  NOT NULL,
        title text  NOT NULL,
        date timestamp  NOT NULL,
        subscriber_amount int  NOT NULL,
        is_banned boolean  NOT NULL,
        description text  NULL,
        rules text  NULL,
        CONSTRAINT tags_pk PRIMARY KEY (id)
    );
    """,

    """
    CREATE TABLE users (
        id serial  NOT NULL,
        first_name varchar(32)  NOT NULL,
        last_name varchar(32)  NOT NULL,
        username varchar(32)  NOT NULL,
        password varchar(200)  NOT NULL,
        email varchar(254)  NOT NULL,
        birth_date date  NOT NULL,
        is_admin boolean  NOT NULL,
        is_banned boolean  NOT NULL,
        date timestamp  NOT NULL,
        CONSTRAINT id PRIMARY KEY (id)
    );
    """,

    """
    CREATE TABLE votes (
        id serial  NOT NULL,
        user_id int  NOT NULL,
        date timestamp  NOT NULL,
        is_comment bool  NOT NULL,
        passed_time interval  NOT NULL,
        vote boolean  NOT NULL,
        vote_ip varchar(32) NOT NULL,
        last_update_time timestamp NOT NULL,
        post_id int  NULL,
        comment_id int  NULL,
        CONSTRAINT votes_pk PRIMARY KEY (id)
    );
    """,

    """
        ALTER TABLE comments ADD CONSTRAINT Comments_Users
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE  CASCADE 
        ON UPDATE  CASCADE 
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    """,

    """
    ALTER TABLE tag_moderators ADD CONSTRAINT Moderators_Tags
        FOREIGN KEY (tag_id)
        REFERENCES tags (id)
        ON DELETE  CASCADE 
        ON UPDATE  CASCADE 
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    """,

    """
    ALTER TABLE tag_moderators ADD CONSTRAINT Moderators_Users
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE  CASCADE 
        ON UPDATE  CASCADE 
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    """,

    """
    ALTER TABLE comments ADD CONSTRAINT Posts_Comments
        FOREIGN KEY (post_id)
        REFERENCES posts (id)
        ON DELETE  CASCADE 
        ON UPDATE  CASCADE 
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    """,

    """
    ALTER TABLE votes ADD CONSTRAINT Posts_Votes
        FOREIGN KEY (post_id)
        REFERENCES posts (id)
        ON DELETE  CASCADE 
        ON UPDATE  CASCADE 
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    """,

    """
    ALTER TABLE reports ADD CONSTRAINT Reports_Comments
        FOREIGN KEY (comment_id)
        REFERENCES comments (id)
        ON DELETE  CASCADE 
        ON UPDATE  CASCADE 
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    """,

    """
    ALTER TABLE reports ADD CONSTRAINT Reports_Posts
        FOREIGN KEY (post_id)
        REFERENCES posts (id)
        ON DELETE  CASCADE 
        ON UPDATE  CASCADE 
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    """,

    """
    ALTER TABLE reports ADD CONSTRAINT Reports_Users
        FOREIGN KEY (submitting_user_id)
        REFERENCES users (id) 
        ON UPDATE  CASCADE 
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    """,

    """
    ALTER TABLE tag_subscriptions ADD CONSTRAINT Subscriptions_Tags
        FOREIGN KEY (tag_id)
        REFERENCES tags (id)
        ON DELETE  CASCADE 
        ON UPDATE  CASCADE 
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    """,

    """
    ALTER TABLE tag_subscriptions ADD CONSTRAINT Subscriptions_Users
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE  CASCADE 
        ON UPDATE  CASCADE 
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    """,

    """
    ALTER TABLE posts ADD CONSTRAINT Tags_Posts
        FOREIGN KEY (tag_id)
        REFERENCES tags (id)
        ON DELETE  CASCADE 
        ON UPDATE  CASCADE 
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    """,

    """
    ALTER TABLE posts ADD CONSTRAINT Users_Posts
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE  CASCADE 
        ON UPDATE  CASCADE 
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    """,

    """
    ALTER TABLE votes ADD CONSTRAINT Votes_Comments
        FOREIGN KEY (comment_id)
        REFERENCES comments (id)
        ON DELETE  CASCADE 
        ON UPDATE  CASCADE 
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
    """,

    """
    ALTER TABLE votes ADD CONSTRAINT Votes_Users
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE  CASCADE 
        ON UPDATE  CASCADE 
        NOT DEFERRABLE 
        INITIALLY IMMEDIATE
    ;
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
