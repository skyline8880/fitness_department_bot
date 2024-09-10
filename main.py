import asyncio

from bot.bot import bot
from database.build_structure.build_structure import StructureBuilder
from dispatcher.dispatcher import dp


async def main():
    await StructureBuilder().create()
    await StructureBuilder().default_insert()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main=main())
