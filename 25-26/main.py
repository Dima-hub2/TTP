# main.py
"""
Главный файл для запуска Telegram бота.
"""

import asyncio
from aiogram import Bot
from aiogram.fsm.storage.memory import MemoryStorage

# Импортируем dp из bot.py
try:
    from bot import dp, TOKEN, logger
except ImportError:
    print(" Ошибка: файл bot.py не найден или содержит ошибки")
    exit(1)

async def main():
    """Основная функция запуска бота"""
    if TOKEN == "8525462952:AAFx6PjQFg08wK5FpMsknLcbO0FebBhyTzc":
        print(" ОШИБКА: Укажите токен бота в файле bot.py!")
        print("Замените 'YOUR_BOT_TOKEN_HERE' на ваш токен от @BotFather")
        return
    
    # Инициализация бота
    bot = Bot(token=TOKEN)
    
    # Пропустить обновления, которые произошли, пока бот не работал
    await bot.delete_webhook(drop_pending_updates=True)
    
    logger.info("Telegram bot starting...")
    print(" Бот запускается...")
    
    # Запуск polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n Бот остановлен")
    except Exception as e:
        print(f" Ошибка запуска бота: {e}")