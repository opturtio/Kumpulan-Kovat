DROP TABLE IF EXISTS citations CASCADE;

CREATE TABLE citations (
    id SERIAL PRIMARY KEY,
    citation_name TEXT,
    type TEXT,
    author TEXT,
    title TEXT,
    booktitle TEXT,
    series TEXT,
    publisher TEXT,
    school TEXT,
    address TEXT,
    journal TEXT,
    howpublished TEXT,
    year INT,
    month TEXT,
    volume TEXT,
    number INT,
    pages TEXT,
    note TEXT
);
