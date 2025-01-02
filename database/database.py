import pandas as pd
from psycopg.errors import UniqueViolation

from database.connection.create_connect import DatabaseConnection
from database.queries.insert import (INSERT_INTO_ENROLL, INSERT_INTO_EVENT,
                                     INSERT_INTO_RECIEVERS,
                                     INSERT_INTO_USER_AUTH,
                                     INSERT_INTO_USER_HIRE)
from database.queries.select import (CHECK_USERS_DEP_AND_SUBDIV,
                                     SELECT_COMMING_EVENTS,
                                     SELECT_COMMING_EVENTS_BY_SENT_STATUS,
                                     SELECT_CURRENT_CUSTOMER_ENROLL,
                                     SELECT_CUSTOMER_ENROLL_ACTIONS,
                                     SELECT_DEP_SUB_RECIEVERS_ID_LIST,
                                     SELECT_DEPARTMENT_BY_SIGN,
                                     SELECT_DEPARTMENTS, SELECT_ENROLL_LIST,
                                     SELECT_EVENT_BY_ID,
                                     SELECT_EVENT_RECIEVERS_LIST,
                                     SELECT_EVENTS_TO_SENT_FOR_NEW_USER,
                                     SELECT_GROUP_EVENTS_DATE,
                                     SELECT_SUBDIVISION_BY_SIGN,
                                     SELECT_SUBDIVISIONS,
                                     SELECT_SUBSCRIBERS_CLUB,
                                     SELECT_USER_BY_SIGN,
                                     SELECT_USER_DEPARTMENTS_BY_SIGN,
                                     SELECT_USER_REFERENCES_BY_SIGN)
from database.queries.update import (UPDATE_ADD_DEPARTMENT_TO_USER,
                                     UPDATE_ADD_SUBDIVISION_TO_USER,
                                     UPDATE_EVENT_SENT, UPDATE_EVENT_STATUS,
                                     UPDATE_REMOVE_DEPARTMENT_FROM_USER,
                                     UPDATE_REMOVE_SUBDIVISION_FROM_USER,
                                     UPDATE_USER_DATA, UPDATE_USER_IS_ADMIN)
from database.tables import (Department, Enroll, Event, Recievers, Subdivision,
                             User)
from utils.paths import set_path


class Database():
    def __init__(self) -> None:
        self.connection = DatabaseConnection()

    async def insert_into_user_auth(
            self,
            phone,
            last_name,
            first_name,
            patronymic,
            telegram_id,
            full_name,
            username):
        if username is not None:
            username = f'@{username}'
        con = await self.connection()
        cur = con.cursor()
        try:
            await cur.execute(
                query=INSERT_INTO_USER_AUTH,
                params={
                    f'{User.PHONE}': phone,
                    f'{User.LAST_NAME}': last_name,
                    f'{User.FIRST_NAME}': first_name,
                    f'{User.PATRONYMIC}': patronymic,
                    f'{User.TELEGRAM_ID}': telegram_id,
                    f'{User.FULLNAME}': full_name,
                    f'{User.USERNAME}': username})
            user = await cur.fetchone()
        except UniqueViolation:
            await con.rollback()
            await cur.execute(
                query=UPDATE_USER_DATA,
                params={
                    f'{User.PHONE}': phone,
                    f'{User.LAST_NAME}': last_name,
                    f'{User.FIRST_NAME}': first_name,
                    f'{User.PATRONYMIC}': patronymic,
                    f'{User.TELEGRAM_ID}': telegram_id,
                    f'{User.FULLNAME}': full_name,
                    f'{User.USERNAME}': username})
            user = await self.select_user_by_sign(sign=phone)
        except Exception:
            await con.rollback()
            user = False
        finally:
            await con.commit()
            await con.close()
            return user

    async def insert_into_user_admin(
            self,
            phone,
            status):
        con = await self.connection()
        cur = con.cursor()
        user = None
        try:
            await cur.execute(
                query=INSERT_INTO_USER_HIRE,
                params={
                    f'{User.PHONE}': phone,
                    f'{User.ISADMIN}': status})
            user = await cur.fetchone()
        except UniqueViolation:
            await con.rollback()
            await self.update_user_is_admin_status(
                is_admin=status,
                phone=phone)
            user = await self.select_user_by_sign(sign=phone)
        except Exception:
            raise Exception
        finally:
            await con.commit()
            await con.close()
            return user

    async def insert_event(self, data):
        print(data)
        (
            _,
            creator,
            department_id,
            subdivision_id,
            event_date,
            name,
            description,
            isfree
        ) = list(data.values())
        _isfree = True
        if isfree == 0:
            _isfree = False
        con = await self.connection()
        cur = con.cursor()
        try:
            await cur.execute(
                query=INSERT_INTO_EVENT,
                params={
                    f'{Event.CREATOR}': creator,
                    f'{Event.DEPARTMENT_ID}': department_id,
                    f'{Event.SUBDIVISION_ID}': subdivision_id,
                    f'{Event.EVENT_DATE}': event_date,
                    f'{Event.NAME}': name,
                    f'{Event.DESCRIPTION}': description,
                    f'{Event.ISFREE}': _isfree})
            event = await cur.fetchone()
        except Exception as e:
            await con.rollback()
            event = False
            print(f'event insert error: {e}')
        finally:
            await con.commit()
            await con.close()
            return event

    async def insert_enroll(self, event_id, customer_id, enrollaction_id):
        con = await self.connection()
        cur = con.cursor()
        try:
            await cur.execute(
                query=INSERT_INTO_ENROLL,
                params={
                    f'{Enroll.EVENTID}': event_id,
                    f'{Enroll.CUSTOMER}': customer_id,
                    f'{Enroll.ENROLLACTIONID}': enrollaction_id})
        except Exception as e:
            await con.rollback()
            print(f'msg: {e}')
        finally:
            await con.commit()
            await con.close()

    async def insert_reciever(self, event_id, customer_id):
        con = await self.connection()
        cur = con.cursor()
        try:
            await cur.execute(
                query=INSERT_INTO_RECIEVERS,
                params={
                    f'{Recievers.EVENTID}': event_id,
                    f'{Recievers.CUSTOMER}': customer_id})
        except Exception:
            await con.rollback()
        finally:
            await con.commit()
            await con.close()

    async def select_department_by_sign(self, sign):
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=SELECT_DEPARTMENT_BY_SIGN,
            params={f'{Department()}': str(sign)})
        result = await cur.fetchone()
        await con.close()
        return result

    async def select_departments(self):
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(query=SELECT_DEPARTMENTS)
        result = await cur.fetchall()
        await con.close()
        return result

    async def select_subdivisions(self):
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(query=SELECT_SUBDIVISIONS)
        result = await cur.fetchall()
        await con.close()
        return result

    async def select_subdivision_by_sign(self, sign):
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=SELECT_SUBDIVISION_BY_SIGN,
            params={f'{Subdivision()}': str(sign)})
        result = await cur.fetchone()
        await con.close()
        return result

    async def select_user_by_sign(self, sign):
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=SELECT_USER_BY_SIGN,
            params={f'{User()}': str(sign)})
        result = await cur.fetchone()
        await con.close()
        return result

    async def select_user_departments_by_sign(self, telegram_id):
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=SELECT_USER_DEPARTMENTS_BY_SIGN,
            params={f'{User.TELEGRAM_ID}': telegram_id})
        result = await cur.fetchall()
        await con.close()
        return result

    async def select_user_references_by_sign(self, telegram_id):
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=SELECT_USER_REFERENCES_BY_SIGN,
            params={f'{User.TELEGRAM_ID}': telegram_id})
        result = await cur.fetchall()
        await con.close()
        return result

    async def select_event_by_id(self, event_id):
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=SELECT_EVENT_BY_ID,
            params={f'{Event.ID}': event_id})
        result = await cur.fetchone()
        await con.close()
        return result

    async def select_comming_events(self):
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=SELECT_COMMING_EVENTS)
        result = await cur.fetchall()
        await con.close()
        return result

    async def select_comming_events_by_sent_status(
            self, was_sent: bool = False):
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=SELECT_COMMING_EVENTS_BY_SENT_STATUS,
            params={f'{Event.SENT}': was_sent})
        result = await cur.fetchall()
        await con.close()
        return result

    async def select_new_user_events_to_send(
            self, telegram_id: int) -> list:
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=SELECT_EVENTS_TO_SENT_FOR_NEW_USER,
            params={f'{Recievers.CUSTOMER}': telegram_id})
        result = await cur.fetchall()
        await con.close()
        return result

    async def select_enroll_list(self, event_id):
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=SELECT_ENROLL_LIST,
            params={f'{Enroll.EVENTID}': event_id}
            )
        result = await cur.fetchall()
        await con.close()
        return result

    async def select_event_recievers_list(self, event_id):
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=SELECT_EVENT_RECIEVERS_LIST,
            params={f'{Enroll.EVENTID}': event_id})
        result = await cur.fetchall()
        await con.close()
        return result

    async def check_users_dep_and_subdiv(
            self, department_id, subdivision_id, telegram_id):
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=CHECK_USERS_DEP_AND_SUBDIV,
            params={
                f'{User.DEPARTMENT_ID}': department_id,
                f'{User.SUBDIV_REFERENCES}': subdivision_id,
                f'{User.TELEGRAM_ID}': telegram_id,

            }
        )
        result = await cur.fetchone()
        await con.close()
        return result

    async def select_current_customer_enroll(self, event_id, customer_id):
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=SELECT_CURRENT_CUSTOMER_ENROLL,
            params={
                f'{Enroll.EVENTID}': event_id,
                f'{Enroll.CUSTOMER}': customer_id})
        result = await cur.fetchone()
        await con.close()
        return result

    async def select_customer_enroll_actions(self):
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=SELECT_CUSTOMER_ENROLL_ACTIONS)
        result = await cur.fetchall()
        await con.close()
        return result

    async def select_recievers_list(self, department_id, subdivision_id):
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=SELECT_DEP_SUB_RECIEVERS_ID_LIST,
            params={
                f'{User.DEPARTMENT_ID}': department_id,
                f'{User.SUBDIV_REFERENCES}': subdivision_id})
        result = await cur.fetchall()
        await con.close()
        return result

    async def update_event_status(self, status, event_id):
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=UPDATE_EVENT_STATUS,
            params={
                f'{Event.ISACTIVE}': status,
                f'{Event.ID}': event_id})
        await con.commit()
        await con.close()

    async def update_event_sent(self, status, event_id):
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=UPDATE_EVENT_SENT,
            params={
                f'{Event.SENT}': status,
                f'{Event.ID}': event_id})
        await con.commit()
        await con.close()

    async def update_user_is_admin_status(self, is_admin, phone):
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=UPDATE_USER_IS_ADMIN,
            params={
                f'{User.ISADMIN}': is_admin,
                f'{User.PHONE}': phone})
        await con.commit()
        await con.close()

    async def update_add_remove_users_department(
            self, depatment_id, telegram_id, is_add):
        query = UPDATE_ADD_DEPARTMENT_TO_USER
        array_type = '{' + f'{depatment_id}' + '}'
        if not is_add:
            query = UPDATE_REMOVE_DEPARTMENT_FROM_USER
            array_type = depatment_id
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=query,
            params={
                f'{User.TELEGRAM_ID}': telegram_id,
                f'{User.DEPARTMENT_ID}': array_type})
        await con.commit()
        await con.close()

    async def update_add_remove_users_subdivision(
            self, subdivision_id, telegram_id, is_add):
        query = UPDATE_ADD_SUBDIVISION_TO_USER
        array_type = '{' + f'{subdivision_id}' + '}'
        if not is_add:
            query = UPDATE_REMOVE_SUBDIVISION_FROM_USER
            array_type = subdivision_id
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=query,
            params={
                f'{User.TELEGRAM_ID}': telegram_id,
                f'{User.SUBDIV_REFERENCES}': array_type})
        await con.commit()
        await con.close()

    async def select_subscribers_query(self):
        con = await self.connection()
        cur = con.cursor()
        query = SELECT_SUBSCRIBERS_CLUB
        await cur.execute(query)
        rows = await cur.fetchall()

        await con.commit()
        await con.close()
        return rows

    async def select_group_events_query(self, begin, end):
        con = await self.connection()
        cur = con.cursor()
        query = SELECT_GROUP_EVENTS_DATE
        await cur.execute(
            query=query,
            params={
                'begin': str(begin),
                'end': str(end)
                })
        rows = await cur.fetchall()
        await con.commit()
        await con.close()
        return rows

    async def subscribers(self, result):
        if result is None:
            print("Ошибка: Нет данных для создания отчета.")
            return None, None

        columnnames = ['club', 'department', 'fio', 'phone', 'worker']
        df = pd.DataFrame(result, columns=columnnames)

        if df.empty:
            print("Пустой DataFrame. Нет данных для отчета.")
            return

        savedftoexcel = df[
            ['department', 'club', 'fio', 'phone', 'worker']].copy()
        savedftoexcel.columns = [
            'Клуб', 'Подразделение', 'ФИО', 'Телефон', 'Сотрудник']

        filename = 'Пользователи.xlsx'
        outputpath = set_path(filename)

        writer = pd.ExcelWriter(outputpath, engine='xlsxwriter')

        savedftoexcel.to_excel(writer, index=False, sheet_name='Подписчики')
        writer.sheets['Подписчики'].set_column('A:E', 20)

        for departmentname, data in savedftoexcel.groupby('Клуб'):
            data.to_excel(writer, sheet_name=departmentname, index=False)

        for sheet_name in writer.sheets:
            writer.sheets[sheet_name].set_column('A:E', 20)

        writer.close()
        print(f"Отчет скачать здесь {outputpath}")

        return outputpath, filename

    async def fetchdata(self, result, begin, end):
        if not result:
            print("Ошибка: Нет данных для отчета.")
            return

        columnnames = ['eventdate', 'eventname', 'club', 'department',
                       'fio', 'phone', 'active', 'worker']
        df = pd.DataFrame(result, columns=columnnames)

        df['event_dt'] = pd.to_datetime(df['eventdate']).dt.date
        df['event_tm'] = pd.to_datetime(df['eventdate']).dt.time

        df = df.drop('eventdate', axis=1)

        savedftoexcel = df[
            ['event_dt', 'event_tm', 'eventname', 'department',
             'club', 'fio', 'phone', 'active', 'worker']].copy()
        savedftoexcel.columns = [
            'Дата', 'Время', 'Событие', 'Клуб', 'Подразделение',
            'ФИО', 'Телефон', 'Активность', 'Сотрудник']

        # Выводим результат
        filename = f'Мероприятия c {begin} по {end}.xlsx'
        outputpath = set_path(filename)

        writer = pd.ExcelWriter(outputpath, engine='xlsxwriter')
        savedftoexcel.to_excel(
            writer, index=False, sheet_name='События по датам')

        # workbook = writer.book
        worksheet = writer.sheets['События по датам']

        for i, column in enumerate(savedftoexcel.columns):
            columnlen = max(
                savedftoexcel[column].astype(str).str.len().max(),
                len(column)) + 5
            worksheet.set_column(i, i, columnlen)

        for departmentname, data in savedftoexcel.groupby('Клуб'):
            data.to_excel(writer, sheet_name=departmentname, index=False)

        for sheet_name in writer.sheets:
            writer.sheets[sheet_name].set_column('A:I', 20)

        writer.close()
        print(f"Отчет успешно создан: {outputpath}")

        return outputpath, filename
