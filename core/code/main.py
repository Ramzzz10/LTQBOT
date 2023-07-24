from handlers import *

# Запуск бота
if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)