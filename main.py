import asyncio

from aiogram import Bot, Dispatcher

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from handlers import main_router
from db.models import Base
from config import db_url, TOKEN
from utils.middlewares import DbSessionMiddleware


async def main():
        
    #Database connection
    engine = create_engine(db_url,
                        echo=True)
    session_maker = sessionmaker(engine,
                                 expire_on_commit=False)

    bot = Bot(TOKEN)
    dp = Dispatcher()
    dp.include_router(main_router)

    #Add session in handlers 
    dp.update.middleware(DbSessionMiddleware(session_pool=session_maker,
                                             engine=engine))

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())