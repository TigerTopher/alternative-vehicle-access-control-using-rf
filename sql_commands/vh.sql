CREATE DATABASE vh;

\c vh;

CREATE TABLE vh_info(
self_vh_no integer
);

CREATE TABLE vacs_accessible(
vac_no integer,
entered boolean,
inside boolean,
token varchar(350),
nfc_uid varchar(50),
nfc_key varchar(50),
nfc_sector integer,
key_A boolean
);
