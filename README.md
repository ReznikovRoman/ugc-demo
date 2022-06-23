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
 2. redis
 3. traefik
 4. zookeeper-kafka
 5. zookeeper-clickhouse
 6. kafka
 7. init-kafka (создание топиков при запуске сервиса)
 8. clickhouse-server-0[1-4]

\* Нужно для полноценного веб-интерфейса Kafka

 9. schema-registry
 10. connect
 11. control-center
 12. ksqldb-server
 13. ksqldb-cli
 14. ksql-datagen
 15. rest-proxy

Файлы docker-compose:
 1. `docker-compose.yml` - для локальной разработки; используются стабы для работы с in-memory очередью.
 3. `docker-compose-dev.yml` - полный набор всех необходимых контейнеров (Kafka, ClickHouse cluster, Kafka UI).
 4. `tests/functional/docker-compose.yml` - для функциональных тестов.

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
# Redis
NUGC_REDIS_HOST=redis
NUGC_REDIS_PORT=6379
NUGC_REDIS_MAIN_DB=0
NUGC_REDIS_OM_URL=redis://@redis:6379
NUGC_REDIS_DEFAULT_CHARSET=utf-8
NUGC_REDIS_DECODE_RESPONSES=1
NUGC_REDIS_RETRY_ON_TIMEOUT=1
# Queue
NUGC_QUEUE_PROGRESS_NAME=progress-topic
NUGC_QUEUE_PROGRESS_GROUP=progress-group
NUGC_QUEUE_PROGRESS_CONSUMERS=2
NUGC_QUEUE_BOOKMARKS_NAME=bookmarks-topic
NUGC_QUEUE_BOOKMARKS_GROUP=bookmarks-group
NUGC_QUEUE_BOOKMARKS_CONSUMERS=2
# Config
NUGC_USE_STUBS=0
NUGC_TESTING=0
NUGC_CI=0
# Kafka
NUGC_KAFKA_URL=kafka:9092
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
# Redis
NUGC_REDIS_HOST=redis
NUGC_REDIS_PORT=6379
NUGC_REDIS_MAIN_DB=0
NUGC_REDIS_OM_URL=redis://@redis:6379
NUGC_REDIS_DEFAULT_CHARSET=utf-8
NUGC_REDIS_DECODE_RESPONSES=1
NUGC_REDIS_RETRY_ON_TIMEOUT=1
# Queue
NUGC_QUEUE_PROGRESS_NAME=progress-topic
NUGC_QUEUE_PROGRESS_GROUP=progress-group
NUGC_QUEUE_PROGRESS_CONSUMERS=2
NUGC_QUEUE_BOOKMARKS_NAME=bookmarks-topic
NUGC_QUEUE_BOOKMARKS_GROUP=bookmarks-group
NUGC_QUEUE_BOOKMARKS_CONSUMERS=2
# Kafka
NUGC_KAFKA_URL=kafka:9092
# Config
NUGC_USE_STUBS=1
NUGC_TESTING=1
NUGC_CI=0
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

## Redis
Redis используется в качестве основной БД (Redis Stack on Redis Enterprise).
Веб-интерфейс RedisInsight доступен по адресу:
- `localhost:13333`

## Kafka
В качестве брокера сообщений используется Kafka.
Веб-интерфейс доступен по адресу (может настраиваться до 5-10 минут):
- `${PROJECT_BASE_URL}:9021/`

## Документация
Документация в формате OpenAPI 3 доступна по адресам:
- `${PROJECT_BASE_URL}/api/v1/docs` - Swagger
