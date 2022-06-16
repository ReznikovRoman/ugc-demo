# Netflix UGC
Сервис для работы с пользовательским контентом в онлайн-кинотеатре _Netflix_.

## Сервисы
- Netflix Admin:
  - Панель администратора для управления онлайн-кинотеатром (редактирование фильмов, жанров, актеров)
  - https://github.com/ReznikovRoman/netflix-admin
- Netflix ETL:
  - ETL пайплайн для синхронизации данных между БД сервиса Netflix Admin и Elasticsearch
  - https://github.com/ReznikovRoman/netflix-etl
- Netflix Movies API:
  - АПИ фильмов
  - https://github.com/ReznikovRoman/netflix-movies-api
- Netflix Auth API:
  - Сервис авторизации - управление пользователями и ролями
  - https://github.com/ReznikovRoman/netflix-auth-api
- Netflix UGC:
  - Сервис для работы с пользовательским контентом
  - https://github.com/ReznikovRoman/netflix-ugc

## Настройка и запуск
docker-compose содержат контейнеры:
 1. server
 2. traefik
 3. zookeeper-kafka
 4. zookeeper-clickhouse
 5. kafka
 6. init-kafka (создание топиков при запуске сервиса)
 7. clickhouse-server-0[1-4]

\* Нужно для полноценного веб-интерфейса Kafka

 9. schema-registry
 10. connect
 11. control-center
 12. ksqldb-server
 13. ksqldb-cli
 14. ksql-datagen
 15. rest-proxy

Файлы docker-compose:
 1. `docker-compose.yml` - для локальной разработки
 2. `tests/functional/docker-compose.yml` - для функциональных тестов

Для запуска контейнеров нужно создать файл `.env` в корне проекта.

**Пример `.env`:**

```dotenv
ENV=.env

# Python
PYTHONUNBUFFERED=1

# Netflix UGC
# Project
NUGC_DEBUG=1
NUGC_PROJECT_BASE_URL=http://api-ugc.localhost:8010
NUGC_SERVER_PORT=8003
NUGC_PROJECT_NAME=netflix-ugc
NUGC_API_V1_STR=/api/v1
NUGC_SERVER_HOSTS=http://api-ugc.localhost:8010
```

### Запуск проекта:

Локально:
```shell
docker-compose build
docker-compose up
```

## Разработка
Синхронизировать окружение с `requirements.txt` / `requirements.dev.txt` (установит отсутствующие пакеты, удалит лишние, обновит несоответствующие версии):
```shell
make sync-requirements
```

Сгенерировать requirements.\*.txt files (нужно пере-генерировать после изменений в файлах requirements.\*.in):
```shell
make compile-requirements
```

Используем `requirements.local.in` для пакетов, которые нужно только разработчику. Обязательно нужно указывать _constraints files_ (-c ...)

Пример:
```shell
# requirements.local.txt

-c requirements.txt

ipython
```

### Тесты
Запуск тестов (всех, кроме функциональных) с экспортом переменных окружения из `.env` файла:
```shell
export $(echo $(cat .env | sed 's/#.*//g'| xargs) | envsubst) && make test
```

Для функциональных тестов нужно создать файл `.env` в папке ./tests/functional

**Пример `.env` (для корректной работы тестов надо подставить корректные значения для auth0):**
```dotenv
# Tests
ENV=.env

# Python
PYTHONUNBUFFERED=1

# Netflix UGC
# Project
NUGC_DEBUG=1
NUGC_PROJECT_BASE_URL=http://api-ugc.localhost:8010
NUGC_SERVER_PORT=8003
NUGC_PROJECT_NAME=netflix-ugc
NUGC_API_V1_STR=/api/v1
NUGC_SERVER_HOSTS=http://api-ugc.localhost:8010
# Tests
TEST_CLIENT_BASE_URL=http://traefik:80
TEST_SERVER_BASE_URL=http://server:8003
```

Запуск функциональных тестов:
```shell
cd ./tests/functional && docker-compose up test
```

Или через рецепт Makefile:
```shell
make dtf
```

### Code style:
Перед коммитом проверяем, что код соответствует всем требованиям:

```shell
make lint
```

### pre-commit:
Для настройки pre-commit:
```shell
pre-commit install
```

## Kafka
В качестве брокера сообщений используется Kafka.
Веб-интерфейс доступен по адресу (может настраиваться до 5-10 минут):
- `${PROJECT_BASE_URL}:9021/`

## Документация
Документация в формате OpenAPI 3 доступна по адресам:
- `${PROJECT_BASE_URL}/api/v1/docs` - Swagger
