-- Local workstation credentials. One owned DB and non-bypass app role per service.
CREATE DATABASE asset;
\c asset
CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS citext;
CREATE EXTENSION IF NOT EXISTS btree_gist;
CREATE ROLE asset_app LOGIN PASSWORD 'dev' NOBYPASSRLS;
GRANT CONNECT ON DATABASE asset TO asset_app;
\c postgres
