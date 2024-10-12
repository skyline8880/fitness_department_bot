import asyncio
import pandas as pd
import asyncpg
import socket
import logging
from datetime import datetime

# Настройка журналирования, запись логов в файл app.log
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Асинхронная функция для извлечения данных из базы данных
async def fetch_data(pool):
    async with pool.acquire() as connection:
        async with connection.transaction():
            result = await connection.fetch(f"""
            SELECT sub.name AS club, 
                dep.name AS department, 
                CONCAT(u.last_name, ' ', u.first_name, ' ', u.patronymic) AS fio, 
                u.phone AS phone,
                CASE
                    WHEN u.is_admin IS not FALSE THEN 'Сотрудник'
                    ELSE ''
                END AS worker
            FROM fit.user u
            LEFT JOIN fit.department dep ON dep.id = ANY(u.departments_ids)
            LEFT JOIN fit.subdivision sub ON sub.id = ANY(u.subdivisions_ids)
            WHERE u.telegram_id IS NOT NULL;
            """)
                      
        if result:
            # Создание DataFrame из полученных данных
            column_names = ['club', 'department', 'fio', 'phone', 'worker']
            df = pd.DataFrame(result, columns=column_names)
    
            return df
    
        else:
            # Логирование, если данных не было получено из базы
            logging.info("Нет данных извлечены из базы данных.")
            return None

# Основная функция программы
async def main():
    try:
        host = "192.168.100.254"
        try:
            # Получение IP-адреса по имени хоста
            ip = socket.gethostbyname(host)
        except socket.gaierror:
            # Логирование ошибки при получении IP-адреса
            logging.info("Ошибка при получении IP-адреса. Убедитесь, что хост доступен.")
            return
    
        database = "fit_db"
        user = "postgres"
        password = "postgres"
        port = 5438

        # Формирование строки подключения к базе данных
        dsn = f"postgresql://{user}:{password}@{ip}:{port}/{database}"
        pool = await asyncpg.create_pool(dsn=dsn)
    
       
        # Извлечение данных из базы
        df = await fetch_data(pool)
        if df is not None:
            # Создание файла Excel с данными
            save_df_to_excel = df[['department', 'club', 'fio', 'phone', 'worker']].copy()
            save_df_to_excel.columns = ['Клуб', 'Подразделение', 'ФИО', 'Телефон','Сотрудник']
            file_name = f'subscribers_{datetime.now().strftime("%Y-%m-%d")}.xlsx'
            writer = pd.ExcelWriter(file_name, engine='xlsxwriter')

            save_df_to_excel.to_excel(writer, index=False, sheet_name='Подписчики')
            writer.sheets['Подписчики'].set_column('A:E', 20)

            for department_name, data in save_df_to_excel.groupby('Клуб'):
                data.to_excel(writer, sheet_name=department_name, index=False)

            for sheet_name in writer.sheets:
                writer.sheets[sheet_name].set_column('A:E', 20)

            writer.close()
            logging.info(f"Данные успешно сохранены в файл {file_name}.")

    except Exception as e:
        # Логирование ошибки, если возникла исключительная ситуация
        logging.error(f"Произошла ошибка: {e}")

if __name__ == '__main__':
    # Запуск основной асинхронной функции с помощью asyncio
    asyncio.run(main())
