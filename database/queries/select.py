from core.secrets import DBSecrets
from database.tables import (Department, Enroll, EnrollAction, Event,
                             Recievers, Subdivision, User)

SELECT_DEPARTMENTS = f'''
    SELECT
        {Department.ID},
        {Department.NAME}
    FROM {DBSecrets.SCHEMA_NAME}.{Department()}
    ORDER BY {Department.ID};
'''
SELECT_DEPARTMENT_BY_SIGN = f'''
    SELECT
        {Department.ID},
        {Department.NAME}
    FROM {DBSecrets.SCHEMA_NAME}.{Department()}
    WHERE {Department.ID}::VARCHAR = %({Department()})s
    OR {Department.NAME}::VARCHAR = %({Department()})s;
'''
SELECT_SUBDIVISIONS = f'''
    SELECT
        {Subdivision.ID},
        {Subdivision.NAME}
    FROM {DBSecrets.SCHEMA_NAME}.{Subdivision()}
    ORDER BY {Subdivision.ID};
'''
SELECT_SUBDIVISION_BY_SIGN = f'''
    SELECT
        {Subdivision.ID},
        {Subdivision.NAME}
    FROM {DBSecrets.SCHEMA_NAME}.{Subdivision()}
    WHERE {Subdivision.ID}::VARCHAR = %({Subdivision()})s
    OR {Subdivision.NAME}::VARCHAR = %({Subdivision()})s;
'''
SELECT_USER_BY_SIGN = f'''
    SELECT
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
        {User.SUBDIV_REFERENCES}
    FROM {DBSecrets.SCHEMA_NAME}.{User()}
    WHERE {User.PHONE}::VARCHAR = %({User()})s
        OR {User.TELEGRAM_ID}::VARCHAR = %({User()})s;
'''
SELECT_USER_REFERENCES_BY_SIGN = f'''
    WITH user_reference AS (
        SELECT
            {User.TELEGRAM_ID} AS user_telegram_id,
            UNNEST({User.SUBDIV_REFERENCES}) AS subdiv_id
        FROM {DBSecrets.SCHEMA_NAME}.{User()}
        WHERE {User.TELEGRAM_ID} = %({User.TELEGRAM_ID})s
    )
    SELECT
        subdiv.id,
        subdiv.name,
        ur.user_telegram_id
    FROM {DBSecrets.SCHEMA_NAME}.{Subdivision()} AS subdiv
    LEFT JOIN user_reference AS ur
        ON subdiv.id = ur.subdiv_id
    ORDER BY subdiv.id;
'''
SELECT_USER_DEPARTMENTS_BY_SIGN = f'''
    WITH user_department AS (
        SELECT
            {User.TELEGRAM_ID} AS user_telegram_id,
            UNNEST({User.DEPARTMENT_ID}) AS dep_id
        FROM {DBSecrets.SCHEMA_NAME}.{User()}
        WHERE {User.TELEGRAM_ID} = %({User.TELEGRAM_ID})s
    )
    SELECT
        depart.id,
        depart.name,
        ud.user_telegram_id
    FROM {DBSecrets.SCHEMA_NAME}.{Department()} AS depart
    LEFT JOIN user_department AS ud
        ON depart.id = ud.dep_id
    ORDER BY depart.id;
'''
SELECT_EVENT_BY_ID = f'''
    SELECT
        ev.{Event.ID},
        ev.{Event.EVENT_DATE},
        usr.{User.TELEGRAM_ID},
        usr.{User.LAST_NAME},
        usr.{User.FIRST_NAME},
        usr.{User.PHONE},
        dep.{Department.ID},
        dep.{Department.NAME},
        subdiv.{Subdivision.ID},
        subdiv.{Subdivision.NAME},
        ev.{Event.NAME},
        ev.{Event.DESCRIPTION},
        ev.{Event.ISFREE},
        ev.{Event.ISACTIVE},
        ev.{Event.SENT},
        ev.{Event.PHOTOID},
        ev.{Event.EXECUTOR}
    FROM {DBSecrets.SCHEMA_NAME}.{Event()} AS ev
    LEFT JOIN {DBSecrets.SCHEMA_NAME}.{User()} AS usr
        ON ev.{Event.CREATOR} = usr.{User.TELEGRAM_ID}
    LEFT JOIN {DBSecrets.SCHEMA_NAME}.{Department()} AS dep
        ON ev.{Event.DEPARTMENT_ID} = dep.{Department.ID}
    LEFT JOIN {DBSecrets.SCHEMA_NAME}.{Subdivision()} AS subdiv
        ON ev.{Event.SUBDIVISION_ID} = subdiv.{Subdivision.ID}
    WHERE ev.{Event.ID} = %({Event.ID})s;
'''
SELECT_COMMING_EVENTS = f'''
    SELECT
        {Event.ID},
        {Event.CREATOR},
        {Event.DEPARTMENT_ID},
        {Event.SUBDIVISION_ID},
        {Event.EVENT_DATE},
        {Event.NAME},
        {Event.DESCRIPTION},
        {Event.ISFREE},
        {Event.ISACTIVE},
        {Event.SENT},
        {Event.PHOTOID},
        {Event.EXECUTOR}
    FROM {DBSecrets.SCHEMA_NAME}.{Event()}
    WHERE {Event.EVENT_DATE} > CURRENT_TIMESTAMP
    AND {Event.ISACTIVE} = TRUE
    ORDER BY {Event.EVENT_DATE};
'''
SELECT_COMMING_EVENTS_BY_SENT_STATUS = f'''
    SELECT
        {Event.ID},
        {Event.CREATOR},
        {Event.DEPARTMENT_ID},
        {Event.SUBDIVISION_ID},
        {Event.EVENT_DATE},
        {Event.NAME},
        {Event.DESCRIPTION},
        {Event.ISFREE},
        {Event.ISACTIVE},
        {Event.SENT},
        {Event.PHOTOID},
        {Event.EXECUTOR}
    FROM {DBSecrets.SCHEMA_NAME}.{Event()}
    WHERE {Event.EVENT_DATE} > CURRENT_TIMESTAMP
    AND {Event.ISACTIVE} = TRUE
    AND {Event.SENT} = %({Event.SENT})s
    ORDER BY {Event.EVENT_DATE};
'''
SELECT_ENROLL_LIST = f'''
    SELECT
        CONCAT(usr.{User.LAST_NAME}, ' ', usr.{User.FIRST_NAME}),
        usr.{User.PHONE},
        era.{EnrollAction.NAME}
    FROM {DBSecrets.SCHEMA_NAME}.{Enroll()} AS er
    LEFT JOIN {DBSecrets.SCHEMA_NAME}.{User()} AS usr
        ON er.{Enroll.CUSTOMER} = usr.{User.TELEGRAM_ID}
    LEFT JOIN {DBSecrets.SCHEMA_NAME}.{EnrollAction()} AS era
        ON era.{EnrollAction.ID} = er.{Enroll.ENROLLACTIONID}
    WHERE er.{Enroll.EVENTID} = %({Enroll.EVENTID})s;
'''
SELECT_EVENT_RECIEVERS_LIST = f'''
    SELECT
        CONCAT(usr.{User.LAST_NAME}, ' ', usr.{User.FIRST_NAME}),
        usr.{User.PHONE}
    FROM {DBSecrets.SCHEMA_NAME}.{Recievers()} AS rec
    LEFT JOIN {DBSecrets.SCHEMA_NAME}.{User()} AS usr
        ON rec.{Recievers.CUSTOMER} = usr.{User.TELEGRAM_ID}
    WHERE rec.{Recievers.EVENTID} = %({Recievers.EVENTID})s;
'''
SELECT_CURRENT_CUSTOMER_ENROLL = f'''
    SELECT
        {Enroll.ENROLLACTIONID}
    FROM {DBSecrets.SCHEMA_NAME}.{Enroll()}
    WHERE {Enroll.EVENTID} = %({Enroll.EVENTID})s
        AND {Enroll.CUSTOMER} = %({Enroll.CUSTOMER})s;
'''
SELECT_CURRENT_CUSTOMER_DEALID = f'''
    SELECT
        {Enroll.DEALID}
    FROM {DBSecrets.SCHEMA_NAME}.{Enroll()}
    WHERE {Enroll.EVENTID} = %({Enroll.EVENTID})s
        AND {Enroll.CUSTOMER} = %({Enroll.CUSTOMER})s;
'''
SELECT_CUSTOMER_ENROLL_ACTIONS = f'''
    SELECT
        {EnrollAction.ID},
        {EnrollAction.NAME}
    FROM {DBSecrets.SCHEMA_NAME}.{EnrollAction()}
    ORDER BY {EnrollAction.ID};
'''
SELECT_RECIEVERS_BY_EVENT_ID = f'''
    SELECT
        {Recievers.EVENTID}
    FROM {DBSecrets.SCHEMA_NAME}.{Recievers()}
    WHERE {Recievers.EVENTID} = %({Recievers.EVENTID})s;
'''
SELECT_DEP_SUB_RECIEVERS_ID_LIST = f'''
    SELECT
        {User.TELEGRAM_ID}
    FROM {DBSecrets.SCHEMA_NAME}.{User()}
    WHERE %({User.DEPARTMENT_ID})s = ANY({User.DEPARTMENT_ID})
        AND %({User.SUBDIV_REFERENCES})s = ANY({User.SUBDIV_REFERENCES});
'''
SELECT_SUBSCRIBERS_CLUB = f'''
    SELECT
        subdiv.{Subdivision.NAME} AS club,
        dep.{Department.NAME} AS department,
        CONCAT(
            usr.{User.LAST_NAME},
            ' ',
            usr.{User.FIRST_NAME},
            ' ',
            usr.{User.PATRONYMIC}) AS fio,
        {User.PHONE} AS phone,
        CASE
            WHEN {User.ISADMIN} IS not FALSE THEN 'Сотрудник'
            ELSE ''
        END AS worker
    FROM {DBSecrets.SCHEMA_NAME}.{User()} AS usr
    LEFT JOIN {DBSecrets.SCHEMA_NAME}.{Department()} AS dep
    ON dep.{Department.ID} = ANY (usr.departments_ids)
    LEFT JOIN {DBSecrets.SCHEMA_NAME}.{Subdivision()} AS subdiv
    ON subdiv.{Subdivision.ID} = ANY (usr.Subdivisions_ids)
    WHERE {User.TELEGRAM_ID} IS NOT NULL;
'''
SELECT_GROUP_EVENTS_DATE = f'''
    SELECT
        ev.{Event.EVENT_DATE},
        ev.{Event.NAME} AS event_name,
        subdiv.{Subdivision.NAME} AS club,
        dep.{Department.NAME} AS department,
        CONCAT(
            usr.{User.LAST_NAME},
            ' ', usr.{User.FIRST_NAME},
            ' ', usr.{User.PATRONYMIC}) AS fio,
        {User.PHONE} AS phone,
        era.{EnrollAction.NAME} AS active,
        CASE
            WHEN {User.ISADMIN} IS not FALSE THEN 'Сотрудник'
            ELSE ''
        END AS worker
    FROM {DBSecrets.SCHEMA_NAME}.{Event()} AS ev
    LEFT JOIN {DBSecrets.SCHEMA_NAME}.{Enroll()} AS er
    ON ev.{Event.ID} = er.{Enroll.EVENTID}
    LEFT JOIN {DBSecrets.SCHEMA_NAME}.{EnrollAction()} AS era
    ON er.{Enroll.ENROLLACTIONID} = era.{EnrollAction.ID}
    LEFT JOIN {DBSecrets.SCHEMA_NAME}.{User()} AS usr
    ON er.{Enroll.CUSTOMER} = usr.{User.TELEGRAM_ID}
    LEFT JOIN {DBSecrets.SCHEMA_NAME}.{Department()} AS dep
    ON ev.{Event.DEPARTMENT_ID} = dep.{Department.ID}
    LEFT JOIN {DBSecrets.SCHEMA_NAME}.{Subdivision()} AS subdiv
    ON ev.{Event.SUBDIVISION_ID} = subdiv.{Subdivision.ID}
    WHERE ev.{Event.EVENT_DATE} BETWEEN %(begin)s AND %(end)s::DATE + 1;
'''
CHECK_USERS_DEP_AND_SUBDIV = f'''
    SELECT
        {User.TELEGRAM_ID}
    FROM {DBSecrets.SCHEMA_NAME}.{User()}
    WHERE %({User.DEPARTMENT_ID})s = ANY({User.DEPARTMENT_ID})
        AND %({User.SUBDIV_REFERENCES})s = ANY({User.SUBDIV_REFERENCES})
        AND {User.TELEGRAM_ID} = %({User.TELEGRAM_ID})s;
'''
SELECT_EVENTS_TO_SENT_FOR_NEW_USER = f'''
    WITH related_to_user AS (
        WITH recieved_events AS (
            SELECT
                {Recievers.EVENTID},
                {Recievers.CUSTOMER}
            FROM {DBSecrets.SCHEMA_NAME}.{Recievers()}
            WHERE {Recievers.CUSTOMER} = %({Recievers.CUSTOMER})s
        )
        SELECT
            ev.{Event.ID},
            ev.{Event.EVENT_DATE},
            ev.{Event.CREATOR},
            ev.{Event.DEPARTMENT_ID},
            ev.{Event.SUBDIVISION_ID},
            ev.{Event.NAME},
            ev.{Event.DESCRIPTION},
            ev.{Event.ISFREE},
            ev.{Event.ISACTIVE},
            ev.{Event.SENT},
            ev.{Event.PHOTOID},
            ev.{Event.EXECUTOR},
            rev.{Recievers.CUSTOMER} AS was_sent
        FROM {DBSecrets.SCHEMA_NAME}.{Event()} AS ev
        LEFT JOIN recieved_events AS rev
            ON ev.{Event.ID} = rev.{Recievers.EVENTID}
        WHERE ev.{Event.EVENT_DATE} > CURRENT_TIMESTAMP
        AND ev.{Event.ISACTIVE} = TRUE
        AND ev.{Event.SENT} = TRUE
    )
    SELECT
        rtu.{Event.ID},
        rtu.{Event.EVENT_DATE},
        usr.{User.TELEGRAM_ID},
        usr.{User.LAST_NAME},
        usr.{User.FIRST_NAME},
        usr.{User.PHONE},
        dep.{Department.ID},
        dep.{Department.NAME},
        subdiv.{Subdivision.ID},
        subdiv.{Subdivision.NAME},
        rtu.{Event.NAME},
        rtu.{Event.DESCRIPTION},
        rtu.{Event.ISFREE},
        rtu.{Event.ISACTIVE},
        rtu.{Event.SENT},
        rtu.{Event.PHOTOID},
        rtu.{Event.EXECUTOR}
    FROM related_to_user AS rtu
    LEFT JOIN {DBSecrets.SCHEMA_NAME}.{User()} AS usr
        ON rtu.{Event.CREATOR} = usr.{User.TELEGRAM_ID}
    LEFT JOIN {DBSecrets.SCHEMA_NAME}.{Department()} AS dep
        ON rtu.{Event.DEPARTMENT_ID} = dep.{Department.ID}
    LEFT JOIN {DBSecrets.SCHEMA_NAME}.{Subdivision()} AS subdiv
        ON rtu.{Event.SUBDIVISION_ID} = subdiv.{Subdivision.ID}
    WHERE rtu.was_sent IS NULL;
'''
