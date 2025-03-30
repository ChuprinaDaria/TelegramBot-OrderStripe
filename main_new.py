import os
import sys
import logging
import stripe
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

# Додайте шлях до директорії з файлами до PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot_handlers import (
    send_welcome,
    handle_main_menu,
    handle_contact,
    handle_form_payment,
    handle_payment_amount,
    handle_contract_confirmation,
    handle_remaining_payment,
    handle_user_message
)
from db_new import init_db, add_user, get_user

# Завантаження змінних середовища з файлу zminni.env
env_path = os.path.join(os.path.dirname(__file__), 'zminni.env')
load_dotenv(env_path)

# Перевірка, чи файл завантажується
if os.path.exists(env_path):
    print(f"Файл {env_path} завантажений успішно.")
else:
    print(f"Файл {env_path} не знайдено.")

# Встановлення змінних середовища
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_USER_ID = os.getenv("ADMIN_USER_ID")
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
SUCCESS_URL = os.getenv("SUCCESS_URL")
CANCEL_URL = os.getenv("CANCEL_URL")

# Логування завантажених змінних для налагодження
logging.basicConfig(
    format='%(asctime)s - %(levellevel)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.info("Завантаження змінних середовища:")
logger.info(f"TELEGRAM_BOT_TOKEN: {TOKEN[:5]}...")  # Скорочення для безпеки
logger.info(f"ADMIN_USER_ID: {ADMIN_USER_ID}")
logger.info(f"STRIPE_API_KEY: {STRIPE_API_KEY[:5]}...")  # Скорочення для безпеки
logger.info(f"SUCCESS_URL: {SUCCESS_URL}")
logger.info(f"CANCEL_URL: {CANCEL_URL}")

# Перевірка, чи всі необхідні змінні завантажені
if not TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN не встановлено. Перевірте файл zminni.env.")
if not STRIPE_API_KEY:
    logger.error("STRIPE_API_KEY не встановлено. Перевірте файл zminni.env.")
if not SUCCESS_URL:
    logger.error("SUCCESS_URL не встановлено. Перевірте файл zminni.env.")
if not CANCEL_URL:
    logger.error("CANCEL_URL не встановлено. Перевірте файл zminni.env.")

# Ініціалізація бази даних
init_db()

async def main():
    try:
        if not TOKEN:
            logger.error("TELEGRAM_BOT_TOKEN не встановлено. Завершення роботи...")
            return
        if not STRIPE_API_KEY:
            logger.error("STRIPE_API_KEY не встановлено. Завершення роботи...")
            return

        application = ApplicationBuilder().token(TOKEN).build()

        # Очистка вебхука для уникнення конфліктів
        await application.bot.delete_webhook()
        logger.info("Вебхук очищено")

        # Додавання обробників
        application.add_handler(CommandHandler("start", send_welcome))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex("Сформувати оплату 📑"), handle_form_payment))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^[0-9]+$"), handle_payment_amount))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex("Підтверджую 👍"), handle_contract_confirmation))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex("Оплатити другу частину 💰"), handle_remaining_payment))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex("Повернутись 😪"), send_welcome))
        application.add_handler(MessageHandler(filters.CONTACT, handle_contact))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_main_menu))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))
        logger.info("Обробники додані")

        # Встановлення ключа API Stripe
        stripe.api_key = STRIPE_API_KEY

        # Перевірка роботи з базою даних
        # Додавання нового користувача
        add_user(1, "test_user", "1234567890")
        logger.info(f"Користувач доданий: {get_user(1)}")

        # Запуск бота
        logger.info("Запуск бота")
        await application.run_polling()
    except Exception as e:
        logger.error(f"Сталася помилка: {str(e)}")

if __name__ == '__main__':
    import asyncio
    import nest_asyncio

    nest_asyncio.apply()
    asyncio.run(main())