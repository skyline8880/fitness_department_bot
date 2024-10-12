import asyncio
import pandas as pd
import datetime
import asyncpg
import socket
import logging
import xlsxwriter
from dotenv import load_dotenv

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def fetch_data(pool, month):
    async with pool.acquire() as connection:
        async with connection.transaction():
            result = await connection.fetch(f"""
            SELECT 
                ev.event_date, 
                ev.name AS event_name,
                sub.name AS club, 
                dep.name AS department,                  
                CONCAT(u.last_name, ' ', u.first_name, ' ', u.patronymic) AS fio, 
                u.phone AS phone, 
                ea.name AS active,
                CASE
                    WHEN u.is_admin IS not FALSE THEN 'Сотрудник'
                    ELSE ''
                END AS worker
                FROM fit.event ev
                LEFT JOIN fit.enroll e ON ev.id = e.event_id
                LEFT JOIN fit.enroll_action ea ON e.enroll_action_id = ea.id
                LEFT JOIN fit.user u ON e.telegram_id = u.telegram_id
                LEFT JOIN fit.department dep ON ev.department_id = dep.id
                LEFT JOIN fit.subdivision sub ON ev.subdivision_id = sub.id
                WHERE EXTRACT(MONTH FROM ev.event_date) = ABS($1);
            """, 
                abs(month),
            )
    
        if result:
            column_names = ['event_date', 'event_name', 'club', 'department', 'fio', 'phone', 'active','worker']
            df = pd.DataFrame(result, columns=column_names)
            
            df['event_dt'] = pd.to_datetime(df['event_date']).dt.date
            df['event_tm'] = pd.to_datetime(df['event_date']).dt.time
    
            df = df.drop('event_date', axis=1)
    
            return df
    
        else:
            logging.info(f"Данные не найдены за месяц {month}")
            return None

async def main():
    try:
        host = "192.168.100.254"
        try:
            ip = socket.gethostbyname(host)
        except socket.gaierror:
            logging.info("Ошибка получения ip-адреса. Убедитесь, что хост доступен.")
            return
    
        database = "fit_db"
        user = "postgres"
        password = "postgres"
        port = 5438

        dsn = f"postgresql://{user}:{password}@{ip}:{port}/{database}"
        pool = await asyncpg.create_pool(dsn=dsn)
    
        month = 9
    
        df = await fetch_data(pool, month)
        if df is not None:  #  Если данные получены, подготовка и сохранение в Exce
            save_df_to_excel = df[['event_dt', 'event_tm', 'event_name', 'department', 'club', 'fio', 'phone', 'active','worker']].copy()
            save_df_to_excel.columns = ['Дата', 'Время', 'Событие', 'Клуб', 'Подразделение', 'ФИО', 'Телефон', 'Активность','Сотрудник']
            
            currentdate = datetime.datetime.now().strftime("%Y-%m-%d")
            file_name = f'event_group{currentdate}.xlsx'
            
            writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
            save_df_to_excel.to_excel(writer, index=False, sheet_name='События по датам')
            workbook = writer.book
            worksheet = writer.sheets['События по датам']
            
            for i, column in enumerate(save_df_to_excel.columns):
               column_len = max(save_df_to_excel[column].astype(str).str.len().max(), len(column)) + 5
               worksheet.set_column(i, i, column_len)
               
            for department_name, data in save_df_to_excel.groupby('Клуб'):
                data.to_excel(writer, sheet_name=department_name, index=False)
            for sheet_name in writer.sheets:
                writer.sheets[sheet_name].set_column('A:I', 20)                       
           
               
            writer.close()
            logging.info(f"Данные успешно сохранены в файл {file_name}")
    
    except Exception as e:
        logging.info(f"Произошла ошибка: {e}")

if __name__ == '__main__':
    asyncio.run(main())