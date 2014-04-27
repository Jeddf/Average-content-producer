CREATE TABLE submits(
       id INTEGER PRIMARY KEY NOT NULL, 
       source TEXT, 
       date TEXT
);

CREATE TABLE wordage (
       submitid INTEGER NOT NULL,
       word TEXT NOT NULL,
       count NUMBER,
       appears NUMBER,
       FOREIGN KEY(submitid) REFERENCES submits(id) ON DELETE CASCADE
);