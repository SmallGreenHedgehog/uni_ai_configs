1. Требования

- Python 3.9+
- pip

2. Установка пакета в проект

    python3 -m venv .venv
    source .venv/bin/activate
    pip install .

После установки становятся доступны консольные команды init-uni-ai и build-uni-ai.

3. Установка из ветки develop

    pip install "git+https://github.com/SmallGreenHedgehog/uni_ai_configs.git@develop"

4. Установка в режиме разработки

    pip install -e ".[dev]"

Режим разработки используется при работе с репозиторием самого пакета.

5. Настройка окружения

    cp .env.example .env

Настройки задаются переменными окружения или в файле .env.

| Переменная | Назначение | По умолчанию | Допустимые значения |
|---|---|---|---|
| UNI_AGENTS_PATH | путь к каталогу с исходными конфигами | config/agents | относительный или абсолютный путь |
| UNI_BUILDER | сборщик конфигурации | ZooCode | Codex, ZooCode |

Относительный путь UNI_AGENTS_PATH разрешается от корня проекта, в котором выполняется команда. Допускается абсолютный путь.

6. Сборка бинарника Nuitka

Для сборки нужен компилятор C (gcc или clang):

    pip install -e ".[nuitka]"
    sh scripts/build_nuitka.sh

Скрипт создаёт один исполняемый файл dist/uni-ai.bin с подкомандами init и build:

    ./dist/uni-ai.bin init
    ./dist/uni-ai.bin build
