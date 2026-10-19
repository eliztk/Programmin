
import os
import secrets
import string

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler
)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("token not found in file .env")

TIPS = [
    "Використовуйте унікальний пароль для кожного важливого облікового запису.",
    "Увімкніть двофакторну автентифікацію, де це можливо.",
    "Не відкривайте підозрілі посилання та вкладення від невідомих відправників.",
    "Не повідомляйте нікому свої паролі та коди підтвердження.",
    "Регулярно оновлюйте операційну систему та програми.",
    "Перевіряйте адресу сайту перед введенням логіна й пароля.",
]

def get_menu_keyboard():
    """Створює меню з кнопками."""
    keyboard = [
        [InlineKeyboardButton(
            "Згенерувати пароль", callback_data="password"
        )],
        [InlineKeyboardButton(
            "Порада з кібербезпеки", callback_data="tips"
        )],
    ]
    return InlineKeyboardMarkup(keyboard)

def text_handler(update: Update, context: CallbackContext):
    """Відповідає на звичайні текстові повідомлення."""
    update.message.reply_text(
        "Щоб скористатися ботом, введіть /menu."
    )

def start(update: Update, context: CallbackContext):
    """Вітає користувача та показує меню."""
    update.message.reply_text(
        "Вітаю! Я бот-помічник із кібербезпеки.\n"
        "Оберіть потрібну функцію в меню.",
        reply_markup=get_menu_keyboard(),
    )

def menu(update: Update, context: CallbackContext):
    """Показує головне меню."""
    update.message.reply_text(
        "Головне меню:",
        reply_markup=get_menu_keyboard(),
    )

def generate_password():
    """Створює випадковий пароль довжиною 16 символів."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"

    password_chars = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice("!@#$%^&*()-_=+"),
    ]

    for _ in range(12):
        password_chars.append(secrets.choice(alphabet))

    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)

def password_command(update: Update, context: CallbackContext):
    """Надсилає згенерований пароль."""
    password = generate_password()
    update.message.reply_text(
        f"Ваш випадковий пароль:\n{password}\n\n"
        "Збережіть його в надійному місці та не передавайте іншим."
    )

def tips_command(update: Update, context: CallbackContext):
    """Надсилає випадкову пораду."""
    tip = secrets.choice(TIPS)
    update.message.reply_text(f"Порада з кібербезпеки:\n{tip}")

def button_tap(update: Update, context: CallbackContext):
    """Обробляє натискання кнопок меню."""
    query = update.callback_query
    query.answer()

    if query.data == "password":
        password = generate_password()
        query.message.reply_text(
            f"Ваш випадковий пароль:\n{password}\n\n"
            "Збережіть його в надійному місці та не передавайте іншим."
        )

    elif query.data == "tips":
        tip = secrets.choice(TIPS)
        query.message.reply_text(
            f"Порада з кібербезпеки:\n{tip}"
        )

def main():
    """Налаштовує та запускає бота."""
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("menu", menu))
    dispatcher.add_handler(CommandHandler("password", password_command))
    dispatcher.add_handler(CommandHandler("tips", tips_command))

    dispatcher.add_handler(CallbackQueryHandler(button_tap))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, text_handler)
    )

    updater.start_polling()
    print("Бот запущений.")
    updater.idle()

if __name__ == "__main__":
    main()

