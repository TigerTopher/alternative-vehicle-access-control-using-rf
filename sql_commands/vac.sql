CREATE DATABASE vac;

\c vac;

CREATE TABLE vac_info(
self_vac_no integer,
ca_public_key varchar(250)
);

CREATE TABLE vehicles_registered(
vin integer,
public_key varchar(20)
);
