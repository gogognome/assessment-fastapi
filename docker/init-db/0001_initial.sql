CREATE TABLE song (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    composer VARCHAR(100),
    artist VARCHAR(100),
    year_of_release SMALLINT NOT NULL
);
