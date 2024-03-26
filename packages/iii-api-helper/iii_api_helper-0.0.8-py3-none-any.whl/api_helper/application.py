import inspect
from collections.abc import Callable
from logging import Logger
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any

import uvicorn
from fastapi import FastAPI as FastAPIBase
from starlette.middleware import Middleware
from typing_extensions import Self
from uvicorn._types import ASGIApplication

from . import config
from .config import _LoggerBuilder
from .errors import FastAPIError
from .middlewares import LogRequestMiddleware
from .sentry import sentry_init

logger: Logger = getLogger(__name__)


class FastAPI(FastAPIBase):
    def __init__(
        self: Self,
        *,
        base_folder: Path,
        **extra: Any,
    ) -> None:
        """

        Args:
            base_folder:
            **extra:
        """
        if not base_folder.exists():
            msg: str = "The base folder does not exist. Please provide a valid base folder."
            raise FastAPIError(msg)

        options: dict[str, Any] = {}
        for key in extra:
            if key.startswith("logging_"):
                options[key.replace("logging_", "")] = extra.pop(key)

        _logger: _LoggerBuilder = _LoggerBuilder(base_folder, **options)
        _logger.setup()

        self.LOGGING_CONFIG: dict[str, Any] = _logger.config

        middlewares: list[Middleware] = extra.pop("middleware", [])
        middlewares.append(
            Middleware(LogRequestMiddleware),  # type: ignore
        )

        if config.is_debug() or extra.get("debug", False) is True:
            super().__init__(
                debug=True,
                title=config.get("APP_NAME"),
                middleware=middlewares,
                **extra,
            )
        else:
            openapi_url: str | None = extra.pop("openapi_url", None)

            super().__init__(
                title=config.get("APP_NAME"),
                middleware=middlewares,
                openapi_url=openapi_url,
                **extra,
            )

    if TYPE_CHECKING:
        run = uvicorn.run

    else:

        def run(
            self: Self,
            host: str = "127.0.0.1",
            port: int = 8000,
            *,
            app: ASGIApplication | Callable[..., Any] | str | None = None,
            show_swagger: bool = False,
            module_name: str | None = None,
            **kwargs: Any,
        ) -> None:  # pragma: no cover
            error_message: str = ""

            if show_swagger and self.openapi_url is None:
                if self.title is None:
                    error_message = "A title must be provided for OpenAPI, e.g.: 'My API'"
                if self.version is None:
                    error_message = "A version must be provided for OpenAPI, e.g.: '2.1.0'"
                self.openapi_url = "/openapi.json"

                if error_message:
                    raise FastAPIError(error_message)

                self.setup()

            self.module_name = module_name

            try:
                uvicorn.run(
                    app or self.__get_module_name(),
                    host=host,
                    port=port,
                    log_config=self.LOGGING_CONFIG,
                    **kwargs,
                )

            except TypeError as e:
                msg: str = (
                    "By default, the app name is automatically determined from the module name and variable name.\n"
                    "Please provide a valid module name by setting the `module_name` parameter in the `run` method.\n"
                )
                raise FastAPIError(msg) from e

    def __get_module_name(self: Self) -> str:
        """Modified by https://stackoverflow.com/a/40536047

        Returns:

        """
        if self.module_name:
            return self.module_name

        for fi in reversed(inspect.stack()):
            names: list[str] = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is self]

            if len(names) > 0:
                module: str = ".".join(Path(fi.filename).relative_to(Path.cwd()).parts).rsplit(".py")[0]
                name: str = names[0]
                return f"{module}:{name}"

    setup_sentry = sentry_init
