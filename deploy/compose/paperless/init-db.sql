-- Local workstation credentials. One owned DB and non-bypass app role per service.
CREATE DATABASE paperless;
\c paperless
CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS citext;
CREATE EXTENSION IF NOT EXISTS btree_gist;
CREATE ROLE paperless_app LOGIN PASSWORD 'dev' NOBYPASSRLS;
GRANT CONNECT ON DATABASE paperless TO paperless_app;
\c postgres
