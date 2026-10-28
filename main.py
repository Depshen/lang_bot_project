"""Главный модуль Telegram-бота для изучения польского языка."""

import logging
import random

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config import BOT_TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# База данных в памяти для хранения прогресса пользователей
user_progress = {}

# Словарь для изучения базовой лексики
VOCABULARY = {
    "Cześć": "Привет",
    "Dziękuję": "Спасибо",
    "Proszę": "Пожалуйста",
    "Przepraszam": "Извините",
}


async def start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает команду /start и выводит стартовое меню."""
    user = update.effective_user
    if user.id not in user_progress:
        user_progress[user.id] = {
            "words_learned": 0,
            "lessons_completed": 0,
        }

    welcome_text = (
        f"Cześć, {user.first_name}! "
        "Я бот для изучения польского языка.\n\n"
        "Доступные команды:\n"
        "/word - Получить слово дня\n"
        "/lesson - Пройти мини-урок\n"
        "/progress - Мой прогресс\n"
        "/help - Справка"
    )
    await update.message.reply_text(welcome_text)


async def send_word(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Отправляет случайное слово и увеличивает счетчик прогресса."""
    user_id = update.effective_user.id
    if user_id in user_progress:
        user_progress[user_id]["words_learned"] += 1

    pl_word, ru_translation = random.choice(list(VOCABULARY.items()))
    await update.message.reply_text(
        f"📚 Слово дня:\n\n**{pl_word}** — {ru_translation}"
    )


async def send_lesson(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Отправляет мини-урок и обновляет статистику уроков."""
    user_id = update.effective_user.id
    if user_id in user_progress:
        user_progress[user_id]["lessons_completed"] += 1

    lesson_text = (
        "🎓 **Мини-урок: Приветствия**\n\n"
        "В польском языке есть два основных приветствия:\n"
        "1. **Cześć** [чещчь] — Привет (неформально)\n"
        "2. **Dzień dobry** [джень добры] — Добрый день (формально)\n\n"
        "Используй их в зависимости от ситуации!"
    )
    await update.message.reply_text(lesson_text)


async def check_progress(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Выводит текущий прогресс обучения пользователя."""
    user_id = update.effective_user.id
    default_stats = {"words_learned": 0, "lessons_completed": 0}
    stats = user_progress.get(user_id, default_stats)
    await update.message.reply_text(
        f"📈 Твой прогресс:\n"
        f"Выучено слов: {stats['words_learned']}\n"
        f"Пройдено уроков: {stats['lessons_completed']}"
    )


async def help_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Отправляет справочную информацию по работе с ботом."""
    await update.message.reply_text(
        "Используй команды из меню для обучения."
    )


def main() -> None:
    """Инициализирует приложение и запускает опрос серверов Telegram."""
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("word", send_word))
    application.add_handler(CommandHandler("lesson", send_lesson))
    application.add_handler(CommandHandler("progress", check_progress))
    application.add_handler(CommandHandler("help", help_command))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
