import logging
import os
import stripe
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, MessageHandler, filters
import random
from datetime import datetime
from db_new import add_order, get_orders_by_user, add_user

USER_MESSAGE_DATA = {}
RANDOM_EMOJIS = ["🐹 ховрашок", "🐨 коала", "🦁 левенятко", "🐜 мурашка", "🐌 равлик", "🦕 динозаврік", "🦧 мавпеня", "🦩 фламінго"]
ADMIN_USER_ID = os.getenv("ADMIN_USER_ID")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

stripe.api_key = os.getenv("STRIPE_API_KEY")

async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "👋 *Вітаємо в сервісі замовлення ботів!*\n\n"
    message += "🔹 Натисніть кнопку нижче, щоб дізнатися про послуги та розцінки."
    await update.message.reply_text(message, parse_mode="Markdown", reply_markup=get_main_menu())

def get_main_menu():
    keyboard = [
        ["📌 Прайс-лист", "📋 Інструкція для замовлення"],
        ["🛒 Оформити замовлення"],
        ["Зв'язатися з розробником ⚙️"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📌 Прайс-лист":
        price_list = (
            "📌 **Прайс-лист на розробку Telegram-ботів**\n\n"
            "🏆 **Базові боти (простий функціонал, швидка реалізація)**\n"
            "✅ Бот-автовідповідач – **50$**\n"
            "✅ Бот для розсилок – **70$**\n"
            "✅ Бот для збору заявок/анкет – **80$**\n"
            "🛒 Боти для бізнесу (продажі, платежі, записи)\n"
            "✅ Бот-магазин – **150$**\n"
            "✅ Бот для оплат – **120$**\n"
            "✅ Бот-бронювальник – **130$**\n"
            "🔍 Боти з розширеними можливостями (аналітика, AI, інтеграції)\n"
            "✅ Бот-аналітик – **200$**\n"
            "✅ Бот для парсингу – **250$**\n"
            "✅ AI-бот – **300$**\n"
            "⚙️ Додаткові функції (опціонально)\n"
            "🧠 Додавання AI – **+200$**\n"
            "📢 Інтеграція з кількома каналами – **+100$**\n"
            "🌍 Багатомовність – **+150$**\n"
            "🔄 Синхронізація з CRM або Google Sheets – **+70$**\n"
            "📌 Хостинг та підтримка бота – від **10$** місяць\n"
            "📌 Доопрацювання функціоналу – **договірна ціна**\n\n"
            "🚀 Готова створити бота під твій запит! Напиши в приват, щоб обговорити деталі."
        )
        await update.message.reply_text(price_list, parse_mode="Markdown")
    elif text == "📋 Інструкція для замовлення":
        instruction = (
            "📋 **Інструкція для замовлення**\n"
            "🖌️ **Напишіть** розробнику @dcprn\n"
            "▪️ Після узгодження деталей виберіть: «🛒 **Оформити замовлення**»\n"
            "▪️ Авторизуйтесь за номером телефону\n"
            "▪️ Натисніть «**Сформувати оплату 📑**»\n"
            "▪️ Введіть узгоджену суму оплати в **$**\n"
            "▪️ Прочитайте коротку умову\n"
            "▪️ Натисніть кнопку «**Підтверджую** 👍»\n"
            "▪️ Ви отримаєте 2 посилання для оплати першої частини і другої\n"
            "▪️ Оплатіть першу частину одразу і другу по закінченню проєкта 🦸🏻‍♂️"
        )
        await update.message.reply_text(instruction, parse_mode="Markdown")
    elif text == "🛒 Оформити замовлення":
        button = KeyboardButton("Авторизуватися", request_contact=True)
        keyboard = [[button]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text("Будь ласка, авторизуйтесь за допомогою вашого телефону.", reply_markup=reply_markup)
    elif text == "Зв'язатися з розробником ⚙️":
        await update.message.reply_text("Напишіть ваше повідомлення @dcprn")

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if contact:
        user_id = update.effective_user.id
        username = update.effective_user.username or update.effective_user.first_name
        context.user_data['phone'] = contact.phone_number
        
        logger.info(f"Додаємо користувача до бази даних: ID={contact.user_id}, Ім'я={username}, Телефон={contact.phone_number}")
        add_user(contact.user_id, username, contact.phone_number)
        logger.info(f"Користувач успішно доданий до бази даних: ID={contact.user_id}, Ім'я={username}, Телефон={contact.phone_number}")
        
        await update.message.reply_text(f"Вітаємо✨ ви авторизувались в системі як працьовитий {RANDOM_EMOJIS[random.randint(0, len(RANDOM_EMOJIS) - 1)]}")
        
        keyboard = [["Сформувати оплату 📑"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text("Натисніть кнопку нижче, щоб сформувати оплату.", reply_markup=reply_markup)

async def handle_form_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['currency'] = "USD"
    await update.message.reply_text("Введіть суму оплати:")

async def handle_payment_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    amount = update.message.text
    context.user_data['amount'] = amount

    user_phone = context.user_data.get('phone')
    currency = context.user_data.get('currency')

    contract_text = f"""
⚙️**Виконавець**: [+48727842737]

👽**Замовник**: [{user_phone}]

⚙️**Розробка бота/пз**

💰**Загальна сума оплати** {amount} {currency}

💰**Передплата 50%** {float(amount) * 0.5} {currency}

🔺*Якщо Замовник відмовляється від проєкту після старту роботи, передоплата не повертається.*

🔺*Усі дані Замовника та ТЗ вважаються конфіденційними і не передаються третім особам.*

**Дата**: {datetime.now().strftime('%Y-%m-%d')}

**Номер угоди** {user_phone}{datetime.now().strftime('%Y%m%d')}
"""
    await update.message.reply_text(contract_text, parse_mode="Markdown")

    keyboard = [["Підтверджую 👍", "Повернутись 😪"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Натисніть кнопку нижче, щоб підтвердити контракт.", reply_markup=reply_markup)

def create_payment_link(amount, description):
    success_url = os.getenv("SUCCESS_URL")
    cancel_url = os.getenv("CANCEL_URL")

    if not success_url or not cancel_url:
        raise ValueError("SUCCESS_URL і CANCEL_URL повинні бути встановлені")

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': description,
                },
                'unit_amount': int(amount * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session.url

async def handle_contract_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Повернутись 😪":
        await send_welcome(update, context)
    else:
        amount = context.user_data.get('amount')
        phone = context.user_data.get('phone')
        if amount is None:
            await update.message.reply_text("Будь ласка, введіть суму оплати.")
            return
        
        logger.info(f"Введена сума для оплати: {amount}")
        
        try:
            payment_link_1 = create_payment_link(float(amount) * 0.5, "Передплата за розробку бота")
            payment_link_2 = create_payment_link(float(amount) * 0.5, "Залишок за розробку бота")

            payment_message = (
                f"💳 **Оплатити першу частину**: [Тиц]({payment_link_1})\n"
                f"💳 **Оплатити другу частину**: [Тиц]({payment_link_2})"
            )
            await update.message.reply_text(payment_message, parse_mode="Markdown")
            
            context.user_data['payment_link_1'] = payment_link_1
            context.user_data['payment_link_2'] = payment_link_2
            
            order_details = f"Розробка бота на суму {amount} {context.user_data['currency']}"
            add_order(user_id=update.effective_user.id, username=update.effective_user.username, order_details=order_details, amount=float(amount), status="pending", currency=context.user_data['currency'])
            logger.info(f"Контракт додано до бази даних для користувача {update.effective_user.username} (ID: {update.effective_user.id})")
            
        except Exception as e:
            await update.message.reply_text(f"Помилка при створенні посилання для оплати: {str(e)}")
            await send_welcome(update, context)

async def check_payment_status(context, payment_link):
    if not payment_link:
        logger.error("Посилання на оплату відсутнє в контексті.")
        return False

    try:
        session_id = payment_link.split('/')[5]
    except IndexError as e:
        logger.error(f"Не вдалося витягти ID сесії з посилання на оплату: {payment_link}. Помилка: {e}")
        return False
    
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == 'paid':
            logger.info(f"Статус оплати для сесії {session_id}: {session.payment_status}")
            return True
        else:
            logger.info(f"Статус оплати для сесії {session_id}: {session.payment_status}")
    except stripe.error.StripeError as e:
        logger.error(f"Помилка Stripe: {str(e)}")
    
    return False

async def handle_remaining_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payment_link_1 = context.user_data.get('payment_link_1')
    payment_link_2 = context.user_data.get('payment_link_2')

    if await check_payment_status(context, payment_link_1):
        await update.message.reply_text("Вітаємо! Перша частина оплати пройшла успішно 🥳")
    elif await check_payment_status(context, payment_link_2):
        await update.message.reply_text("Вітаємо! Друга частина оплати пройшла успішно 🥳")
    else:
        await update.message.reply_text("Оплата не пройшла. Будь ласка, спробуйте ще раз.")
        return

    keyboard = [["Оплатити другу частину 💰"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Натисніть кнопку нижче, щоб оплатити другу частину.", reply_markup=reply_markup)

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message_text = update.message.text
    username = update.effective_user.username or update.effective_user.first_name

    try:
        await context.bot.send_message(
            chat_id=ADMIN_USER_ID,
            text=f"Повідомлення від користувача @{username}: {message_text}"
        )
        logger.info(f"Повідомлення від користувача @{username} (ID: {user_id}): {message_text} успішно відправлено адміну.")
    except Exception as e:
        logger.error(f"Помилка при відправці повідомлення адміну: {str(e)}")