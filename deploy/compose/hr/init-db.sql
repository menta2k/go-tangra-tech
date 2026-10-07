-- Local workstation credentials. One owned DB and non-bypass app role per service.
CREATE DATABASE hr;
\c hr
CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS citext;
CREATE EXTENSION IF NOT EXISTS btree_gist;
CREATE ROLE hr_app LOGIN PASSWORD 'dev' NOBYPASSRLS;
GRANT CONNECT ON DATABASE hr TO hr_app;
\c postgres
