CREATE TABLE dispositivos (
    id          INTEGER PRIMARY KEY,
    dispositivo VARCHAR(100),
    valor      INTEGER DEFAULT 0
);

INSERT INTO dispositivos (id, dispositivo)
VALUES (1, 'ESP32_LED');

INSERT INTO dispositivos (id, dispositivo)
VALUES (2, 'ESP32_POTENCIOMETRO');

SELECT * FROM dispositivos;
