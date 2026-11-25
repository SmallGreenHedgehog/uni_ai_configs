1. Требования

- Python 3.12
- pip

2. Установка пакета в проект

    python3 -m venv .venv
    source .venv/bin/activate
    pip install .

После установки становятся доступны консольные команды [`init-uni-ai`](pyproject.toml:30) и [`build-uni-ai`](pyproject.toml:29).

3. Установка из ветки develop

    pip install "git+https://github.com/SmallGreenHedgehog/uni_ai_configs.git@develop"

4. Установка в режиме разработки

    pip install -e ".[dev]"

Режим разработки используется при работе с репозиторием самого пакета.

5. Настройка окружения

    cp .env.example .env

Настройки задаются переменными окружения или в файле `.env`.

| Переменная | Назначение | По умолчанию | Допустимые значения |
|---|---|---|---|
| [`UNI_AGENTS_PATH`](src/infrastructure/settings.py:18) | путь к каталогу с исходными конфигами | [`config/agents`](config/agents) | относительный или абсолютный путь |
| [`UNI_BUILDER`](src/infrastructure/settings.py:23) | сборщик конфигурации | ZooCode | Codex, ZooCode, ClaudeAgent |

Относительный путь [`UNI_AGENTS_PATH`](src/infrastructure/settings.py:18) разрешается от корня проекта, в котором выполняется команда. Допускается абсолютный путь.

6. Сборка бинарника Nuitka

Для сборки нужен компилятор C (gcc или clang):

    pip install -e ".[nuitka]"
    sh scripts/build_nuitka.sh

Целевая платформа задаётся переменной окружения `TARGET_PLATFORM` (`linux-x86_64` или `macos-arm64`). Если она не задана, платформа определяется автоматически по текущей системе. Имя выходного файла формируется по целевой платформе: `dist/uni-ai-linux-x86_64.bin` для Linux x86_64 и `dist/uni-ai-macos-arm64.bin` для macOS. Имя можно переопределить переменной окружения `OUTPUT_FILENAME`:

    OUTPUT_FILENAME=uni-ai-custom.bin TARGET_PLATFORM=linux-x86_64 sh scripts/build_nuitka.sh

Для Linux скрипт задаёт `CFLAGS="-march=x86-64 -mtune=generic"` и `CXXFLAGS="-march=x86-64 -mtune=generic"`, поэтому бинарник работает на старых процессорах без AVX2 и без ошибки `CPU ISA level is lower than required`. Для macOS бинарник подписывается ad-hoc (`--macos-sign-identity=-`) и с него снимаются extended attributes (`xattr -c`).

Бинарник содержит подкоманды init и build:

    ./dist/uni-ai-linux-x86_64.bin init
    ./dist/uni-ai-linux-x86_64.bin build
