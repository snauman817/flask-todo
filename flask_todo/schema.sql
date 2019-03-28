DROP TABLE IF EXISTS items;

CREATE TABLE items (
    id bigserial PRIMARY KEY,
    task varchar(70),
    completed boolean,
    date_created date
);