import logging.config

from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):
    """Контейнер с зависимостями."""

    wiring_config = containers.WiringConfiguration(
        modules=[
            "ugc.api.v1.handlers.misc",
        ],
    )

    config = providers.Configuration()

    configure_logging = providers.Callable(
        logging.config.dictConfig,
        config=config.logging_config,
    )
