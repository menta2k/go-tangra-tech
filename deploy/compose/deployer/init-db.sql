-- Local workstation credentials. One owned DB and non-bypass app role per service.
CREATE DATABASE deployer;
\c deployer
CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS citext;
CREATE EXTENSION IF NOT EXISTS btree_gist;
CREATE ROLE deployer_app LOGIN PASSWORD 'dev' NOBYPASSRLS;
GRANT CONNECT ON DATABASE deployer TO deployer_app;
\c postgres
