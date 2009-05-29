BEGIN TRANSACTION;

DROP TABLE IF EXISTS clients;
CREATE TABLE clients (
    client VARCHAR NOT NULL,
    machine VARCHAR NOT NULL,
    selldate DATE NOT NULL,
    deltamonth INTEGER NOT NULL,
    anticiped BOOLEAN NOT NULL,
    PRIMARY KEY (client, machine, selldate));

DROP TABLE IF EXISTS payments;
CREATE TABLE payments (
    clients_client VARCHAR NOT NULL,
    clients_machine VARCHAR NOT NULL,
    clients_selldate VARCHAR NOT NULL,
    expected_datepayd DATE NOT NULL,
    effective_datepayd DATE DEFAULT NULL,
    PRIMARY KEY (clients_client, clients_machine, clients_selldate,
            expected_datepayd),
    FOREIGN KEY (clients_client, clients_machine, clients_selldate)
            REFERENCES clients (client, machine, selldate));

COMMIT;
