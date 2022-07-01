# Бенчмарк БД

Исследование по выбору хранилища пользовательского контента.

- Результаты: [link](./results)
- Выводы: [link](/docs/decisions/01_ugc_storage.md)
- Production Grade performance benchmark:
[link](https://redis.com/blog/redisjson-public-preview-performance-benchmarking/)

## Настройка YCSB
0. Поднимаем БД: `docker-compose up`
1. Настройка Redis: https://github.com/brianfrankcooper/YCSB/tree/master/redis
2. Настройка MongoDB: https://github.com/brianfrankcooper/YCSB/tree/master/mongodb
   - Нужно использовать последнюю версию YCSB (0.17.0)

## Redis
### Загрузка данных и запуск тестов
```shell
./bin/ycsb.sh load redis -s -P workloads/workloadf -p "redis.host=127.0.0.1" -p "redis.port=6379" > outputLoadRedis.txt
```
```shell
./bin/ycsb.sh run redis -s -P workloads/workloadf -p "redis.host=127.0.0.1" -p "redis.port=6379" > outputRunRedis.txt
```

## MongoDB
### Загрузка данных и запуск тестов
```shell
./bin/ycsb.sh load mongodb-async -s -P workloads/workloadf > outputLoadMongo.txt
```
```shell
./bin/ycsb.sh run mongodb-async -s -P workloads/workloadf > outputRunMongo.txt
```
