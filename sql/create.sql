DROP TABLE IF EXISTS users, topics, posts;

CREATE TABLE users (
    id integer PRIMARY KEY,

    -- last_posted_at timestamp,
    nick_name varchar(255) NOT NULL,
    -- num_of_npms integer DEFAULT 0 NOT NULL,
    num_of_posts integer DEFAULT 0 NOT NULL,
    num_of_topics integer DEFAULT 0 NOT NULL
);

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

    topic_id integer REFERENCES topics,
    user_id integer REFERENCES users
);

CREATE INDEX posts_created_at_idx ON posts (created_at);
CREATE INDEX posts_topic_id_idx ON posts (topic_id);
CREATE INDEX posts_user_id_idx ON posts (user_id);
