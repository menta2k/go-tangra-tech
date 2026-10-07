-- Local workstation credentials. One owned DB and non-bypass app role per service.
CREATE DATABASE ipam;
\c ipam
CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS citext;
CREATE EXTENSION IF NOT EXISTS btree_gist;
CREATE ROLE ipam_app LOGIN PASSWORD 'dev' NOBYPASSRLS;
GRANT CONNECT ON DATABASE ipam TO ipam_app;
\c postgres
