-- Local workstation credentials. One owned DB and non-bypass app role per service.
CREATE DATABASE sms_gw;
\c sms_gw
CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS citext;
CREATE EXTENSION IF NOT EXISTS btree_gist;
CREATE ROLE smsgw_app LOGIN PASSWORD 'dev' NOBYPASSRLS;
GRANT CONNECT ON DATABASE sms_gw TO smsgw_app;
\c postgres
