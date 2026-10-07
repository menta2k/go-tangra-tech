-- Local workstation credentials. One owned DB and non-bypass app role per service.
CREATE DATABASE signing;
\c signing
CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS citext;
CREATE EXTENSION IF NOT EXISTS btree_gist;
CREATE ROLE signing_app LOGIN PASSWORD 'dev' NOBYPASSRLS;
GRANT CONNECT ON DATABASE signing TO signing_app;
\c postgres
