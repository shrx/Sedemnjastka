DROP TABLE IF EXISTS users, topics, posts, quotes, quote_votes, avatars, info, avatar_guesses;

CREATE TABLE users (
    id integer PRIMARY KEY,

    nick_name varchar(255) NOT NULL,
    password varchar(60),
    token varchar(32),

    num_of_posts integer DEFAULT 0 NOT NULL,
    num_of_topics integer DEFAULT 0 NOT NULL
);

-- For the edge case where a user is deleted before we get to him
INSERT INTO users (id, nick_name) VALUES (0, 'Izbrisani');

CREATE TABLE topics (
    id integer PRIMARY KEY,

    last_post_created_at timestamp,
    num_of_posts integer DEFAULT 0 NOT NULL,
    subtitle varchar(255),
    title varchar(255) NOT NULL,

    user_id integer REFERENCES users
);

CREATE TABLE posts (
    id serial PRIMARY KEY,

    body text NOT NULL,
    created_at timestamp NOT NULL,

    tsv tsvector,

    topic_id integer REFERENCES topics,
    user_id integer REFERENCES users
);

CREATE TABLE quotes (
    id serial PRIMARY KEY,

    created_at timestamp NOT NULL,

    downvotes integer DEFAULT 0 NOT NULL,
    upvotes integer DEFAULT 0 NOT NULL,

    post_id integer NOT NULL REFERENCES posts UNIQUE,
    quoted_by integer NOT NULL REFERENCES users
);

CREATE TABLE quote_votes (
    quote_id integer REFERENCES quotes,
    user_id integer REFERENCES users,

    created_at timestamp NOT NULL,
    upvoted boolean NOT NULL,

    PRIMARY KEY (quote_id, user_id)
);

CREATE TABLE avatars (
    id serial PRIMARY KEY,

    created_at timestamp with time zone DEFAULT now() NOT NULL,
    md5sum VARCHAR(32) NOT NULL,

    -- original
    filename VARCHAR(255),
    width integer,
    height integer,

    -- thumbnail
    thumb_filename VARCHAR(255),
    thumb_width integer,
    thumb_height integer,

    user_id integer NOT NULL REFERENCES users
);

ALTER TABLE posts ADD COLUMN avatar_id integer REFERENCES avatars;
ALTER TABLE users ADD COLUMN avatar_id integer REFERENCES avatars;

CREATE TABLE avatar_guesses (
    id serial PRIMARY KEY,

    created_at timestamp DEFAULT now() NOT NULL,
    guessed boolean NOT NULL,
    guessed_avatar integer NOT NULL REFERENCES avatars,

    user_id integer NOT NULL REFERENCES users
);

CREATE INDEX posts_created_at_idx ON posts (created_at);
CREATE INDEX posts_topic_id_idx ON posts (topic_id);
CREATE INDEX posts_tsv_idx ON posts USING gin(tsv);
CREATE INDEX posts_user_id_idx ON posts (user_id);

CREATE TRIGGER posts_tsvector_update BEFORE INSERT OR UPDATE
ON posts FOR EACH ROW EXECUTE PROCEDURE
tsvector_update_trigger(tsv, 'pg_catalog.simple', body);

-- Create and populate metadata info table with defaults
CREATE TABLE info (
    id serial PRIMARY KEY,

    attribute varchar(255) UNIQUE,
    value varchar(255)
);

INSERT INTO info (attribute) VALUES ('archive_last_run');
