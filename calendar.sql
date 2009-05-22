begin transaction;

create table clients (
    client varchar,
    machine varchar,
    selldate date,
    deltamonth integer,
    anticiped bool);

create table payments (
    clients_client varchar references clients(client),
    clients_machine varchar references clients(machine),
    datepayd date);

commit;
