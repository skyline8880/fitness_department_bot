from core.secrets import DBSecrets
from database.tables import (Department, Enroll, EnrollAction, Event,
                             Recievers, Subdivision, User)

CREATE = f'''
    CREATE SCHEMA IF NOT EXISTS {DBSecrets.SCHEMA_NAME};

    CREATE TABLE IF NOT EXISTS {DBSecrets.SCHEMA_NAME}.{Department()} (
        {Department.ID} SERIAL,
        {Department.NAME} VARCHAR(250) NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS {DBSecrets.SCHEMA_NAME}.{Subdivision()} (
        {Subdivision.ID} SERIAL,
        {Subdivision.NAME} VARCHAR(250) NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS {DBSecrets.SCHEMA_NAME}.{EnrollAction()} (
        {EnrollAction.ID} SERIAL,
        {EnrollAction.NAME} VARCHAR(100) NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS {DBSecrets.SCHEMA_NAME}.{Enroll()} (
        {Enroll.ID} SERIAL,
        {Enroll.EVENTID} BIGINT NOT NULL,
        {Enroll.CUSTOMER} BIGINT NOT NULL,
        {Enroll.ENROLLACTIONID} INTEGER NOT NULL,
        PRIMARY KEY ({Enroll.EVENTID}, {Enroll.CUSTOMER})
    );

    CREATE TABLE IF NOT EXISTS {DBSecrets.SCHEMA_NAME}.{Recievers()} (
        {Recievers.ID} SERIAL,
        {Recievers.EVENTID} BIGINT NOT NULL,
        {Recievers.CUSTOMER} BIGINT NOT NULL,
        PRIMARY KEY ({Recievers.EVENTID}, {Recievers.CUSTOMER})
    );

    CREATE TABLE IF NOT EXISTS {DBSecrets.SCHEMA_NAME}.{Event()} (
        {Event.ID} SERIAL,
        {Event.CREATOR} BIGINT NOT NULL,
        {Event.DEPARTMENT_ID} INTEGER NOT NULL,
        {Event.SUBDIVISION_ID} INTEGER NOT NULL,
        {Event.EVENT_DATE} TIMESTAMP NOT NULL,
        {Event.NAME} VARCHAR(250) NOT NULL,
        {Event.DESCRIPTION} VARCHAR(1500) NOT NULL,
        {Event.ISFREE} BOOLEAN NOT NULL,
        {Event.ISACTIVE} BOOLEAN NOT NULL DEFAULT TRUE,
        {Event.SENT} BOOLEAN NOT NULL DEFAULT FALSE
    );

    CREATE TABLE IF NOT EXISTS {DBSecrets.SCHEMA_NAME}.{User()} (
        {User.ID} SERIAL,
        {User.ISADMIN} BOOLEAN DEFAULT FALSE,
        {User.PHONE} VARCHAR(15) NOT NULL UNIQUE,
        {User.LAST_NAME} VARCHAR(100) DEFAULT NULL,
        {User.FIRST_NAME} VARCHAR(100) DEFAULT NULL,
        {User.PATRONYMIC} VARCHAR(100) DEFAULT NULL,
        {User.TELEGRAM_ID} BIGINT DEFAULT NULL,
        {User.FULLNAME} VARCHAR(250) DEFAULT NULL,
        {User.USERNAME} VARCHAR(250) DEFAULT NULL,
        {User.DEPARTMENT_ID} INTEGER[] DEFAULT NULL,
        {User.SUBDIV_REFERENCES} INTEGER[] DEFAULT NULL
    );
'''

DEFAULT_INSERT = f'''
    INSERT INTO {DBSecrets.SCHEMA_NAME}.{Department()} ({Department.NAME})
    VALUES
        ('{Department().msk}'),
        ('{Department().vlk}'),
        ('{Department().nkr}'),
        ('{Department().btv}');

    INSERT INTO {DBSecrets.SCHEMA_NAME}.{Subdivision()} ({Subdivision.NAME})
    VALUES
        ('{Subdivision().pool}'),
        ('{Subdivision().gp}'),
        ('{Subdivision().kids}'),
        ('{Subdivision().marts}'),
        ('{Subdivision().gym}');

    INSERT INTO {DBSecrets.SCHEMA_NAME}.{EnrollAction()} ({EnrollAction.NAME})
    VALUES
        ('{EnrollAction().enroll}'),
        ('{EnrollAction().decline}'),
        ('{EnrollAction().thinkig}');
'''
DROP_SCHEMA = f'''
    DROP SCHEMA {DBSecrets.SCHEMA_NAME} CASCADE;
'''
