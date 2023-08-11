from core.code.handlers import dp
import aiogram


if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
