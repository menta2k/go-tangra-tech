CREATE DATABASE asterisk_registration;
CREATE USER 'asterisk_app'@'%' IDENTIFIED BY 'registration-dev-only';
GRANT ALL ON asterisk_registration.* TO 'asterisk_app'@'%';
