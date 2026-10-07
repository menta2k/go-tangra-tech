-- Local workstation credentials. One owned DB and non-bypass app role per service.
CREATE DATABASE inventory;
\c inventory
CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS citext;
CREATE EXTENSION IF NOT EXISTS btree_gist;
CREATE ROLE inventory_app LOGIN PASSWORD 'dev' NOBYPASSRLS;
GRANT CONNECT ON DATABASE inventory TO inventory_app;
\c postgres
