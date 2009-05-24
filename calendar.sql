begin transaction;

drop table if exists clients;
create table clients (
    client varchar not null,
    machine varchar not null,
    selldate date not null,
    deltamonth integer not null,
    anticiped bool not null);

drop table if exists payments;
create table payments (
    clients_client varchar references clients(client) not null,
    clients_machine varchar references clients(machine) not null,
    clients_selldate varchar references clients(selldate) not null,
    datepayd date,
    payed boolean not null);

commit;
