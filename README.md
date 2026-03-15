# 🐷 John Pork Refactor

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://core.telegram.org/bots/api)
[![OpenAI](https://img.shields.io/badge/AI-OpenAI-green.svg)](https://openai.com/)

**John Pork** — это не просто бот. Это дерзкий, агрессивный 20-летний уличный тип из Telegram и лицо токена **$JPORK**. Он не признает авторитетов, обожает крипту и готов «опоркифицировать» твое лицо в любой момент.

---

## 🚀 Основные возможности

- **🧠 AI Street Chat**: Интеграция с GPT-4o-mini. Бот общается в уникальном стиле: коротко, грубо, с использованием сленга.
- **🎭 Porkify**: Мощная функция замены лиц. Отправь фото, и Джон превратит тебя в солидного хряка с помощью нейросетей.
- **📡 Eavesdrop (Подслушивание)**: Бот следит за чатами и врывается в диалог, если видит триггеры, чтобы навести суету и прорекламировать $JPORK.
- **🎁 Lucky Game**: Мини-игра «Угадай кнопку». Выиграй респект от Джона или порцию унижения.
- **🌍 Multi-lang**: Полная поддержка русского и английского языков.
- **🛠 Современный стек**: Асинхронный код, SQLAlchemy 2.0, Pydantic v2 и управление зависимостями через `uv`.

---

## 🛠 Технологический стек

- **Core**: [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- **AI**: OpenAI API (GPT-4o-mini-search-preview)
- **Database**: SQLAlchemy 2.0 + aiosqlite
- **Config**: Pydantic Settings + PyYAML
- **Logging**: Loguru
- **Environment**: [uv](https://docs.astral.sh/uv/)

---

## ⚙️ Установка и запуск

### 1. Подготовка окружения

Рекомендуется использовать `uv` для мгновенной установки:

```bash
# Установка зависимостей
uv sync
```

### 2. Настройка конфигурации

Создайте файл `.env` в корневом каталоге:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
PROXY_API_KEY=your_openai_proxy_key_here
```

Настройте параметры поведения в `config.yaml` (шансы срабатывания, лимиты, промпты).

### 3. Запуск

```bash
uv run bot.py
```

---

## 📁 Структура проекта

```text
├── core/               # Ядро: БД, логгер, конфиги, middleware
├── handlers/           # Логика команд и обработки сообщений
├── utils/              # AI функции, кулдауны, вспомогательные утилиты
├── assets/             # Изображения и статические файлы
├── config.yaml         # Настройки бота и AI промпты
└── lang.yaml           # Локализация (RU/EN)
```

---

## 📜 Команды

- `/start` — Встреча с Джоном.
- `/porkify` — Запустить процесс трансформации лица (нужно фото).
- `/lucky` — Испытать удачу.
- `/lang` — Сменить язык (если пальцы не отсохли).

---

## ⚠️ Дисклеймер

Бот настроен на агрессивный стиль общения. Это часть образа персонажа John Pork и создано исключительно в развлекательных целях.

---

На данный момент проект заброшен.
