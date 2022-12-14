import logging.config
import sys
from functools import partial
from typing import AsyncIterator

import loguru
import orjson
from dependency_injector import containers, providers

from ugc.core import logging as ugc_logging
from ugc.domain import bookmarks, processors, progress, ratings, reviews
from ugc.domain.bookmarks.models import FilmBookmark
from ugc.domain.progress.models import UserFilmProgress
from ugc.domain.ratings.models import FilmRating
from ugc.domain.reviews.constants import REVIEWS_COLLECTION_NAME
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

    logstash_handler = providers.Resource(
        ugc_logging.init_logstash_handler,
        host=config.LOGSTASH_HOST,
        port=config.LOGSTASH_PORT,
        version=config.LOGSTASH_LOGGER_VERSION,
    )

    logger = providers.Resource(
        ugc_logging.init_logger,
        handler=logstash_handler,
        log_format="[{time}] [{level}] [Request: {request_id}] [{name}]: {message}",
        level=logging.INFO,
    )

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

    mongo_repository_factory = partial(
        providers.Factory,
        provides=repositories.MongoRepository,
        db=mongo_client,
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

    kafka_consumer_film_rating_client = providers.Resource(
        consumers.init_kafka_consumer_client,
        config=config,
        topic=config.QUEUE_FILM_RATING_NAME,
        group_id=config.QUEUE_FILM_RATING_GROUP,
        **consumer_client_config,
    )
    kafka_film_rating_consumer = providers.Singleton(
        consumers.KafkaConsumer,
        client=kafka_consumer_film_rating_client,
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

    progress_dispatcher_service = providers.Factory(
        progress.ProgressDispatcherService,
        progress_factory=progress_factory,
        producer=kafka_producer,
        config=config,
    )

    progress_processor = providers.Singleton(
        progress.ProgressProcessor,
        progress_factory=progress_factory,
        progress_service=progress_service,
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

    bookmark_dispatcher_service = providers.Factory(
        bookmarks.BookmarkDispatcherService,
        bookmark_factory=bookmark_factory,
        producer=kafka_producer,
        config=config,
    )

    bookmark_processor = providers.Singleton(
        bookmarks.BookmarkProcessor,
        bookmark_factory=bookmark_factory,
        bookmark_service=bookmark_service,
    )

    bookmark_processor_service = providers.Factory(
        processors.ProcessorService,
        consumer=kafka_bookmark_consumer,
        concurrency=config.QUEUE_BOOKMARKS_CONSUMERS,
        message_callback=bookmark_processor,
    )

    # Domain -> FilmRating

    film_rating_factory = providers.Factory(ratings.FilmRatingFactory)

    film_rating_repository = providers.Singleton(
        ratings.FilmRatingRepository,
        redis_client=redis_client,
        film_rating_factory=film_rating_factory,
        redis_repository=redis_repository_factory(model=FilmRating),
    )

    film_rating_service = providers.Singleton(
        ratings.FilmRatingService,
        film_rating_repository=film_rating_repository,
    )

    film_rating_dispatcher_service = providers.Factory(
        ratings.FilmRatingDispatcherService,
        film_rating_factory=film_rating_factory,
        producer=kafka_producer,
        config=config,
    )

    film_rating_processor = providers.Singleton(
        ratings.FilmRatingProcessor,
        film_rating_factory=film_rating_factory,
        film_rating_service=film_rating_service,
    )

    film_rating_processor_service = providers.Factory(
        processors.ProcessorService,
        consumer=kafka_film_rating_consumer,
        concurrency=config.QUEUE_FILM_RATING_CONSUMERS,
        message_callback=film_rating_processor,
    )

    # Domain -> Reviews

    review_factory = providers.Factory(reviews.FilmReviewFactory)

    review_repository = providers.Singleton(
        reviews.ReviewRepository,
        mongo_repository=mongo_repository_factory(factory=review_factory, collection_name=REVIEWS_COLLECTION_NAME),
        db=mongo_client,
        review_factory=review_factory,
    )

    review_service = providers.Factory(
        reviews.ReviewService,
        review_factory=review_factory,
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
    film_rating_processor = providers.Singleton(
        InMemoryProcessor,
        queue=providers.Singleton(InMemoryQueue),
    )
    container.progress_dispatcher_service.add_kwargs(producer=progress_processor)
    container.bookmark_dispatcher_service.add_kwargs(producer=bookmark_processor)
    container.film_rating_dispatcher_service.add_kwargs(producer=film_rating_processor)
    container.progress_processor_service.add_kwargs(consumer=progress_processor)
    container.bookmark_processor_service.add_kwargs(consumer=bookmark_processor)
    container.film_rating_processor_service.add_kwargs(consumer=film_rating_processor)

    return container


async def get_processors(container: Container) -> AsyncIterator[processors.ProcessorService]:
    processor_providers = [
        container.progress_processor_service,
        container.bookmark_processor_service,
        container.film_rating_processor_service,
    ]
    for provider in processor_providers:
        try:
            yield await provider()
        except TypeError:
            yield provider()


async def dummy_resource() -> None:
    """Функция-ресурс для перезаписи в DI контейнере."""


def _override_with_dummy_resources(container: Container) -> Container:
    if container.config.CI() or container.config.TESTING():
        container.logger.override(providers.Resource(_init_dummy_logger))
    container.kafka_producer_client.override(providers.Resource(dummy_resource))
    container.kafka_consumer_progress_client.override(providers.Resource(dummy_resource))
    container.kafka_consumer_bookmark_client.override(providers.Resource(dummy_resource))
    container.kafka_consumer_film_rating_client.override(providers.Resource(dummy_resource))
    container.kafka_producer.override(sentinel)
    container.kafka_bookmark_consumer.override(sentinel)
    container.kafka_progress_consumer.override(sentinel)
    container.kafka_film_rating_consumer.override(sentinel)
    return container


def _init_dummy_logger() -> None:
    loguru.logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
