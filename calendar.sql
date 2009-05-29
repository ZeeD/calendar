begin transaction;

drop table if exists clients;
create table clients (
    client varchar not null,
    machine varchar not null,
    selldate date not null,
    deltamonth integer not null,
    anticiped bool not null,
    primary key (client, machine, selldate));

drop table if exists payments;
create table payments (
    clients_client varchar references clients(client) not null,
    clients_machine varchar references clients(machine) not null,
    clients_selldate varchar references clients(selldate) not null,
    expected_datepayd date not null,
    effective_datepayd date default null,
    primary key (clients_client, clients_machine, clients_selldate,
            expected_datepayd),
    foreign key (clients_client, clients_machine, clients_selldate)
            references clients (client, machine, selldate));

commit;
