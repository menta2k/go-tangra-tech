-- Local workstation credentials. One owned DB and non-bypass app role per service.
CREATE DATABASE notification;
\c notification
CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS citext;
CREATE EXTENSION IF NOT EXISTS btree_gist;
CREATE ROLE notification_app LOGIN PASSWORD 'dev' NOBYPASSRLS;
GRANT CONNECT ON DATABASE notification TO notification_app;
\c postgres
