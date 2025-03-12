from core.secrets import DBSecrets
from database.tables import Enroll, Event, User

UPDATE_USER_IS_ADMIN = f'''
    UPDATE {DBSecrets.SCHEMA_NAME}.{User()}
        SET {User.ISADMIN} = %({User.ISADMIN})s
    WHERE {User.PHONE} = %({User.PHONE})s;
'''
UPDATE_ADD_DEPARTMENT_TO_USER = f'''
    UPDATE {DBSecrets.SCHEMA_NAME}.{User()}
        SET {User.DEPARTMENT_ID} = ARRAY_CAT(
                {User.DEPARTMENT_ID},
                %({User.DEPARTMENT_ID})s
            )
    WHERE {User.TELEGRAM_ID} = %({User.TELEGRAM_ID})s;
'''
UPDATE_REMOVE_DEPARTMENT_FROM_USER = f'''
    UPDATE {DBSecrets.SCHEMA_NAME}.{User()}
        SET {User.DEPARTMENT_ID} = ARRAY_REMOVE(
                {User.DEPARTMENT_ID},
                %({User.DEPARTMENT_ID})s
            )
    WHERE {User.TELEGRAM_ID} = %({User.TELEGRAM_ID})s;
'''
UPDATE_ADD_SUBDIVISION_TO_USER = f'''
    UPDATE {DBSecrets.SCHEMA_NAME}.{User()}
        SET {User.SUBDIV_REFERENCES} = ARRAY_CAT(
                {User.SUBDIV_REFERENCES},
                %({User.SUBDIV_REFERENCES})s
            )
    WHERE {User.TELEGRAM_ID} = %({User.TELEGRAM_ID})s;
'''
UPDATE_REMOVE_SUBDIVISION_FROM_USER = f'''
    UPDATE {DBSecrets.SCHEMA_NAME}.{User()}
        SET {User.SUBDIV_REFERENCES} = ARRAY_REMOVE(
                {User.SUBDIV_REFERENCES},
                %({User.SUBDIV_REFERENCES})s
            )
    WHERE {User.TELEGRAM_ID} = %({User.TELEGRAM_ID})s;
'''
UPDATE_USER_DATA = f'''
    UPDATE {DBSecrets.SCHEMA_NAME}.{User()}
        SET {User.LAST_NAME} = %({User.LAST_NAME})s,
            {User.FIRST_NAME} = %({User.FIRST_NAME})s,
            {User.PATRONYMIC} = %({User.PATRONYMIC})s,
            {User.TELEGRAM_ID} = %({User.TELEGRAM_ID})s,
            {User.FULLNAME} = %({User.FULLNAME})s,
            {User.USERNAME} = %({User.USERNAME})s
    WHERE {User.PHONE} = %({User.PHONE})s;
'''
UPDATE_EVENT_STATUS = f'''
    UPDATE {DBSecrets.SCHEMA_NAME}.{Event()}
        SET {Event.ISACTIVE} = %({Event.ISACTIVE})s
    WHERE {Event.ID} = %({Event.ID})s;
'''
UPDATE_EVENT_SENT = f'''
    UPDATE {DBSecrets.SCHEMA_NAME}.{Event()}
        SET {Event.SENT} = %({Event.SENT})s
    WHERE {Event.ID} = %({Event.ID})s;
'''
UPDATE_ENROLL_DEAL_ID = f'''
    UPDATE {DBSecrets.SCHEMA_NAME}.{Enroll()}
        SET {Enroll.DEALID} = %({Enroll.DEALID})s
    WHERE {Enroll.EVENTID} = %({Enroll.EVENTID})s
        AND {Enroll.CUSTOMER} = %({Enroll.CUSTOMER})s;
'''
