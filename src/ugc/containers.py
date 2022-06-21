import logging.config

import orjson
from dependency_injector import containers, providers

from ugc.domain import bookmarks, progress
from ugc.infrastructure.queue import producers
from ugc.infrastructure.queue.stubs import InMemoryProducer, InMemoryQueue


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

    # Domain -> Progress

    progress_factory = providers.Factory(progress.FilmProgressFactory)

    progress_dispatcher_service = providers.Factory(
        progress.ProgressDispatcherService,
        progress_factory=progress_factory,
        producer=kafka_producer,
        config=config,
    )

    # Domain -> Bookmarks

    bookmark_factory = providers.Factory(bookmarks.FilmBookmarkFactory)

    bookmark_dispatcher_service = providers.Factory(
        bookmarks.BookmarkDispatcherService,
        bookmark_factory=bookmark_factory,
        producer=kafka_producer,
        config=config,
    )


def override_providers(container: Container) -> Container:
    if not container.config.USE_STUBS():
        return container
    container.kafka_producer_client.override(providers.Resource(dummy_resource))
    container.kafka_producer.override(
        providers.Factory(
            InMemoryProducer,
            # TODO (https://github.com/ReznikovRoman/netflix-ugc/issues/8):
            #  - Проверить, что консьюмеры будут корректно работать со стабами.
            queue=providers.Singleton(InMemoryQueue),
        ),
    )
    return container


async def dummy_resource() -> None:
    ...
