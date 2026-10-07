-- Local workstation credentials. One owned DB and non-bypass app role per service.
CREATE DATABASE ticket;
\c ticket
CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS citext;
CREATE EXTENSION IF NOT EXISTS btree_gist;
CREATE ROLE ticket_app LOGIN PASSWORD 'dev' NOBYPASSRLS;
GRANT CONNECT ON DATABASE ticket TO ticket_app;
\c postgres
