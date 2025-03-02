CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);
CREATE TABLE todoitems (
    id INTEGER PRIMARY KEY,
    item TEXT,
    user_id INTEGER REFERENCES users,
    todostate_id INTEGER REFERENCES todostates
);
CREATE TABLE todostates (id INTEGER PRIMARY KEY, state TEXT);
CREATE TABLE tags (id INTEGER PRIMARY KEY, tag TEXT);
CREATE TABLE todoitems_tags (
    todoitem_id INTEGER REFERENCES todoitems,
    tag_id INTEGER REFERENCES tags,
    PRIMARY KEY (todoitem_id, tag_id)
);