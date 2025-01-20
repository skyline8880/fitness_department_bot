from core.secrets import DBSecrets
from database.tables import Enroll, Event, Recievers, User

INSERT_INTO_USER_AUTH = f'''
    INSERT INTO {DBSecrets.SCHEMA_NAME}.{User()} (
        {User.PHONE},
        {User.LAST_NAME},
        {User.FIRST_NAME},
        {User.PATRONYMIC},
        {User.TELEGRAM_ID},
        {User.FULLNAME},
        {User.USERNAME}
    )
    VALUES (
        %({User.PHONE})s,
        %({User.LAST_NAME})s,
        %({User.FIRST_NAME})s,
        %({User.PATRONYMIC})s,
        %({User.TELEGRAM_ID})s,
        %({User.FULLNAME})s,
        %({User.USERNAME})s
    )
    ON CONFLICT ({User.PHONE}) DO UPDATE
        SET {User.LAST_NAME} = %({User.LAST_NAME})s,
            {User.FIRST_NAME} = %({User.FIRST_NAME})s,
            {User.PATRONYMIC} = %({User.PATRONYMIC})s,
            {User.TELEGRAM_ID} = %({User.TELEGRAM_ID})s,
            {User.FULLNAME} = %({User.FULLNAME})s,
            {User.USERNAME} = %({User.USERNAME})s
    RETURNING
        {User.ID},
        {User.ISADMIN},
        {User.PHONE},
        {User.LAST_NAME},
        {User.FIRST_NAME},
        {User.PATRONYMIC},
        {User.TELEGRAM_ID},
        {User.FULLNAME},
        {User.USERNAME},
        {User.DEPARTMENT_ID},
        {User.SUBDIV_REFERENCES};
'''
INSERT_INTO_USER_HIRE = f'''
    INSERT INTO {DBSecrets.SCHEMA_NAME}.{User()} (
        {User.ISADMIN},
        {User.PHONE}
    )
    VALUES (
        %({User.ISADMIN})s,
        %({User.PHONE})s
    )
    RETURNING
        {User.ID},
        {User.ISADMIN},
        {User.PHONE},
        {User.LAST_NAME},
        {User.FIRST_NAME},
        {User.PATRONYMIC},
        {User.TELEGRAM_ID},
        {User.FULLNAME},
        {User.USERNAME},
        {User.DEPARTMENT_ID},
        {User.SUBDIV_REFERENCES};
'''
INSERT_INTO_EVENT = f'''
    INSERT INTO {DBSecrets.SCHEMA_NAME}.{Event()} (
        {Event.CREATOR},
        {Event.DEPARTMENT_ID},
        {Event.SUBDIVISION_ID},
        {Event.EVENT_DATE},
        {Event.NAME},
        {Event.DESCRIPTION},
        {Event.ISFREE},
        {Event.PHOTOID}
    )
    VALUES (
        %({Event.CREATOR})s,
        %({Event.DEPARTMENT_ID})s,
        %({Event.SUBDIVISION_ID})s,
        %({Event.EVENT_DATE})s,
        %({Event.NAME})s,
        %({Event.DESCRIPTION})s,
        %({Event.ISFREE})s,
        %({Event.PHOTOID})s
    )
    RETURNING
        {Event.ID};
'''
INSERT_INTO_ENROLL = f'''
    INSERT INTO {DBSecrets.SCHEMA_NAME}.{Enroll()} (
        {Enroll.EVENTID},
        {Enroll.CUSTOMER},
        {Enroll.ENROLLACTIONID}
    )
    VALUES (
        %({Enroll.EVENTID})s,
        %({Enroll.CUSTOMER})s,
        %({Enroll.ENROLLACTIONID})s
    )
    ON CONFLICT ({Enroll.EVENTID}, {Enroll.CUSTOMER}) DO
    UPDATE
        SET {Enroll.ENROLLACTIONID} = %({Enroll.ENROLLACTIONID})s;
'''
INSERT_INTO_RECIEVERS = f'''
    INSERT INTO {DBSecrets.SCHEMA_NAME}.{Recievers()} (
        {Recievers.EVENTID},
        {Recievers.CUSTOMER}
    )
    VALUES (
        %({Recievers.EVENTID})s,
        %({Recievers.CUSTOMER})s
    );
'''
