INSERT INTO user (username, password) 
VALUES
    ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
    ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');
    -- pbkdf2 -> hashing algorithm.
    -- sha256 -> hash fn.
    -- 50000 -> number of iterations.
    -- TCI4GcX -> random salt (A random salt is a random piece of data added to a password before hashing it.)
    -- the long string -> the resulting hash.

INSERT INTO post (title, body, author_id, created)
VALUES
    ('test title', 'test' || x'0a' || 'body', 1, '2025-03-08 00:00:00');
    -- In SQL, || means string concatenation. x'0a' is a hexadecimal notation that represents the newline char \n.