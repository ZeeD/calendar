begin transaction;

create table clients (
    client varchar not null,
    machine varchar not null,
    selldate date not null,
    deltamonth integer not null,
    anticiped bool not null);

create table payments (
    clients_client varchar references clients(client) not null,
    clients_machine varchar references clients(machine) not null,
    datepayd date not null);

commit;
