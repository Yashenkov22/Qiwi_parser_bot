import os

import pandas as pd

from aiogram import types
from aiogram.types import FSInputFile

from sqlalchemy.engine import Engine


def read_sql_query(con, stmt):
    return pd.read_sql_query(stmt, con)


async def get_excel(message: types.Message,
                    engine: Engine):
    query = '''
    SELECT *
    FROM bank_info
    '''

    text = 'Главное меню'

    df_sql = pd.read_sql_query(query,engine)
    
    if df_sql.empty:
        text = 'В базе ещё нет записей'
    else:
        filename = 'Отчет по базе данных.xlsx'

        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        sheetname = 'Отчёт'

        df_sql.to_excel(writer,
                        index=False,
                        sheet_name=sheetname,
                        header=['Номер телефона',
                                'Имя'])
        
        worksheet = writer.sheets[sheetname]
        worksheet.set_column(0, 0, 20)
        worksheet.set_column(1, 1, 20)

        writer.close()

        await message.answer_document(FSInputFile(filename))

        if os.path.isfile(filename):
            os.remove(filename)

    return text