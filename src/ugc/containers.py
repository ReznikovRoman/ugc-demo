import logging.config

import orjson
from dependency_injector import containers, providers

from ugc.domain import bookmarks, processors, progress, reviews
from ugc.domain.bookmarks.models import FilmBookmark
from ugc.domain.progress.models import UserFilmProgress
from ugc.helpers import sentinel
from ugc.infrastructure.db import mongo, redis, repositories
from ugc.infrastructure.queue import consumers, producers
from ugc.infrastructure.queue.stubs import InMemoryProcessor, InMemoryQueue


class Container(containers.DeclarativeContainer):
    """Контейнер с зависимостями."""

    wiring_config = containers.WiringConfiguration(
        modules=[
            "ugc.api.v1.handlers.ugc",
            "ugc.api.v1.handlers.misc",
            "ugc.api.security",
        ],
    )

    config = providers.Configuration()

    configure_logging = providers.Resource(
        logging.basicConfig,
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
    )

    # Infrastructure

    mongo_client = providers.Resource(
        mongo.init_mongo,
        url=config.MONGODB_URL,
    )

    redis_client = providers.Resource(
        redis.init_redis,
        url=config.REDIS_OM_URL,
    )

    redis_repository_factory = providers.Factory(
        providers.Factory,
        repositories.RedisRepository,
    )

    kafka_producer_client = providers.Resource(
        producers.init_kafka_producer_client,
        servers=providers.List(config.KAFKA_URL),
        key_serializer=providers.Object(lambda key: key.encode()),
        value_serializer=providers.Object(lambda value: orjson.dumps(value)),
    )

    kafka_producer = providers.Singleton(
        producers.KafkaProducer,
        client=kafka_producer_client,
    )

    consumer_client_config = {
        "key_deserializer": providers.Object(lambda key: key.decode()),
        "value_deserializer": providers.Object(lambda value: orjson.loads(value)),
    }

    kafka_consumer_progress_client = providers.Resource(
        consumers.init_kafka_consumer_client,
        config=config,
        topic=config.QUEUE_PROGRESS_NAME,
        group_id=config.QUEUE_PROGRESS_GROUP,
        **consumer_client_config,
    )
    kafka_progress_consumer = providers.Singleton(
        consumers.KafkaConsumer,
        client=kafka_consumer_progress_client,
    )

    kafka_consumer_bookmark_client = providers.Resource(
        consumers.init_kafka_consumer_client,
        config=config,
        topic=config.QUEUE_BOOKMARKS_NAME,
        group_id=config.QUEUE_BOOKMARKS_GROUP,
        **consumer_client_config,
    )
    kafka_bookmark_consumer = providers.Singleton(
        consumers.KafkaConsumer,
        client=kafka_consumer_bookmark_client,
    )

    # Domain -> Progress

    progress_factory = providers.Factory(progress.FilmProgressFactory)

    progress_repository = providers.Singleton(
        progress.FilmProgressRepository,
        progress_factory=progress_factory,
        redis_repository=redis_repository_factory(model=UserFilmProgress),
    )

    progress_service = providers.Singleton(
        progress.ProgressService,
        progress_repository=progress_repository,
    )

    progress_processor = providers.Singleton(
        progress.ProgressProcessor,
        progress_factory=progress_factory,
        progress_service=progress_service,
    )

    progress_dispatcher_service = providers.Factory(
        progress.ProgressDispatcherService,
        progress_factory=progress_factory,
        producer=kafka_producer,
        config=config,
    )

    progress_processor_service = providers.Factory(
        processors.ProcessorService,
        consumer=kafka_progress_consumer,
        concurrency=config.QUEUE_PROGRESS_CONSUMERS,
        message_callback=progress_processor,
    )

    # Domain -> Bookmarks

    bookmark_factory = providers.Factory(bookmarks.FilmBookmarkFactory)

    bookmark_repository = providers.Singleton(
        bookmarks.BookmarkRepository,
        bookmark_factory=bookmark_factory,
        redis_repository=redis_repository_factory(model=FilmBookmark),
    )

    bookmark_service = providers.Singleton(
        bookmarks.BookmarkService,
        bookmark_repository=bookmark_repository,
    )

    bookmark_processor = providers.Singleton(
        bookmarks.BookmarkProcessor,
        bookmark_factory=bookmark_factory,
        bookmark_service=bookmark_service,
    )

    bookmark_dispatcher_service = providers.Factory(
        bookmarks.BookmarkDispatcherService,
        bookmark_factory=bookmark_factory,
        producer=kafka_producer,
        config=config,
    )

    bookmark_processor_service = providers.Factory(
        processors.ProcessorService,
        consumer=kafka_bookmark_consumer,
        concurrency=config.QUEUE_BOOKMARKS_CONSUMERS,
        message_callback=bookmark_processor,
    )

    # Domain -> Reviews

    review_repository = providers.Singleton(reviews.ReviewRepository)

    review_service = providers.Factory(
        reviews.ReviewService,
        review_repository=review_repository,
    )


def override_providers(container: Container) -> Container:
    """Перезаписывание провайдеров с помощью стабов."""
    if not container.config.USE_STUBS():
        return container

    _override_with_dummy_resources(container)

    progress_processor = providers.Singleton(
        InMemoryProcessor,
        queue=providers.Singleton(InMemoryQueue),
    )
    bookmark_processor = providers.Singleton(
        InMemoryProcessor,
        queue=providers.Singleton(InMemoryQueue),
    )
    container.progress_dispatcher_service.add_kwargs(producer=progress_processor)
    container.bookmark_dispatcher_service.add_kwargs(producer=bookmark_processor)
    container.progress_processor_service.add_kwargs(consumer=progress_processor)
    container.bookmark_processor_service.add_kwargs(consumer=bookmark_processor)

    return container


async def get_processors(container: Container) -> list[processors.ProcessorService]:
    processor_services = [
        container.progress_processor_service(),
        container.bookmark_processor_service(),
    ]
    if container.progress_processor_service.is_async_mode_enabled():
        return [await processor_service for processor_service in processor_services]
    return processor_services


async def dummy_resource() -> None:
    """Функция-ресурс для перезаписи в DI контейнере."""


def _override_with_dummy_resources(container: Container) -> Container:
    container.kafka_producer_client.override(providers.Resource(dummy_resource))
    container.kafka_consumer_progress_client.override(providers.Resource(dummy_resource))
    container.kafka_consumer_bookmark_client.override(providers.Resource(dummy_resource))
    container.kafka_producer.override(sentinel)
    container.kafka_bookmark_consumer.override(sentinel)
    container.kafka_progress_consumer.override(sentinel)
    return container
