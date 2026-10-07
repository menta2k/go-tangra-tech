-- Local workstation credentials. One owned DB and non-bypass app role per service.
CREATE DATABASE warden;
\c warden
CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS citext;
CREATE EXTENSION IF NOT EXISTS btree_gist;
CREATE ROLE warden_app LOGIN PASSWORD 'dev' NOBYPASSRLS;
GRANT CONNECT ON DATABASE warden TO warden_app;
\c postgres
