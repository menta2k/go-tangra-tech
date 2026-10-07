-- Local workstation credentials. One owned DB and non-bypass app role per service.
CREATE DATABASE dns;
\c dns
CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS citext;
CREATE EXTENSION IF NOT EXISTS btree_gist;
CREATE ROLE dns_app LOGIN PASSWORD 'dev' NOBYPASSRLS;
GRANT CONNECT ON DATABASE dns TO dns_app;
\c postgres
