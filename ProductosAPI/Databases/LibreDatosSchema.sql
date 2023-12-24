CREATE DATABASE  Users;

USE Users;

CREATE TABLE UserData
(
    username NVARCHAR(15),
    email    NVARCHAR(31),
    password NCHAR(60)
);

CREATE TABLE UserBaskets
(
    id        INT,
    username  NVARCHAR(16),
    basket_id NVARCHAR(31)
);