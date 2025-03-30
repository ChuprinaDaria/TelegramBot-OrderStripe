# TelegramBot-OrderStripe
A personal pet project developed for managing custom bot orders via Telegram, integrated with Stripe for payment processing. Deployed on Hetzner Cloud inside a Docker container, this bot was created both for personal use and for handling client requests quickly and securely.

---

## 🚀 Features

- Telegram bot interface with friendly UI
- Secure user authorization via phone number
- Custom order creation system with auto-generated Stripe payment links
- Pre-payment + post-payment logic
- Dynamic contract generation
- Admin notification for new orders
- Full Stripe Checkout integration
- SQLite database for lightweight order/user tracking

---

## 📊 Tech Stack

- **Python** (telegram, asyncio)
- **python-telegram-bot** for interaction
- **Stripe API** for payments
- **SQLite** as database
- **Docker** for deployment
- **Hetzner Cloud** as hosting

---

## 📁 Project Structure

```bash
TelegramBot-OrderStripe/
├── bot_handlers.py        # Telegram UI logic and flow
├── clients_new.py         # Client-side contract logic
├── db_new.py              # SQLite database layer
├── main_new.py            # Bot entry point
├── payments_new.py        # Stripe integration
├── requirements.txt       # Python dependencies
├── schema.sql             # DB schema (orders, users)
├── .gitignore             # Ignored files
├── zminni.env.example     # Example .env configuration
```

---

## 🔧 Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/your-username/TelegramBot-OrderStripe.git
cd TelegramBot-OrderStripe
```

### 2. Create your `.env` file
```env
# zminni.env
TELEGRAM_BOT_TOKEN=your_bot_token
STRIPE_API_KEY=your_stripe_secret
ADMIN_USER_ID=123456789
SUCCESS_URL=https://yourdomain.com/success
CANCEL_URL=https://yourdomain.com/cancel
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize the database
```bash
sqlite3 mydatabase.db < schema.sql
```

### 5. Run the bot
```bash
python main_new.py
```

---

## 📦 Docker Deployment (optional)

You can also deploy using Docker:

```dockerfile
# Dockerfile
FROM python:3.10
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "main_new.py"]
```

```bash
docker build -t telegram-bot-order .
docker run --env-file=zminni.env telegram-bot-order
```

---

## 🏑️ Database Schema

```sql
-- schema.sql
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    phone_number TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    username TEXT,
    order_details TEXT,
    amount REAL,
    status TEXT,
    currency TEXT
);
```

---

## 🚀 Live Bot
Check it out: [@Channel_orders_bot](https://t.me/Channel_orders_bot)

---

## 🙌 About
This project demonstrates integration of:
- Telegram UI
- Payment automation via Stripe
- Order management system
- Cloud & Docker deployment

