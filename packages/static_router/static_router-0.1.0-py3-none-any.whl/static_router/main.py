"""Main module for StaticRouter."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import fastapi
from fastapi.templating import Jinja2Templates

if TYPE_CHECKING:
    from static_router.models.content_loader import ContentLoader
    from static_router.models.page import Page


class StaticRouter:
    """Static content loader for FastAPI."""

    def __init__(
        self,
        content_loader: ContentLoader,
        *,
        default_template: str = "default",
    ) -> None:
        """
        Create a new instance of a static content renderer for FastAPI.

        Params
        ------
        content_loader: :class:`ContentLoader`
            The content loading strategy to use.
        """
        self._pages = {page.path: page for page in content_loader.load()}
        self._default_template = default_template

    @property
    def pages(self) -> list[Page]:
        """Get all loaded pages."""
        return list(self._pages.values())

    def register(self, app: fastapi.FastAPI) -> None:
        """
        Register the loaded pages with a FastAPI app.

        Params
        ------
        app: :class:`fastapi.FastAPI`
            The app to register the pages to.
        """
        for path in self._pages:
            app.get(path)(self.page_handler)

    def page_handler(self, request: fastapi.Request) -> fastapi.Response:
        """
        Page handler for StaticRouter.

        Params
        ------
        request: :class:`fastapi.Request`
            An incoming request from fastapi.

        Returns
        -------
        :class:`fastapi.Response`
            A rendered template with the page data.

        Raises
        ------
        :class:`fastapi.HTTPException`
            If the page does not exist.

        """
        page_path = request.url.components[2]

        if page_path not in self._pages:
            raise fastapi.HTTPException(status_code=404)

        page = self._pages[page_path]

        if not page.template:
            page.template = self._default_template

        templates = Jinja2Templates(directory="templates")

        return templates.TemplateResponse(
            f"{page.template}.html",
            context={
                "request": request,
                "page": page,
                "router": self,
            },
        )


def register(
    app: fastapi.FastAPI,
    *,
    content_loader: ContentLoader,
    **kwargs: Any,
) -> None:
    """
    Register a StaticRouter with a FastAPI app.

    This method is a wrapper around the `StaticRouter` class.
    For more configuration options, see the `StaticRouter` class.

    Params
    ------
    app: :class:`fastapi.FastAPI`
        The app to register the pages to.

    content_loader: :class:`ContentLoader`
        The content loading strategy to use.

    **kwargs
        Additional keyword arguments to pass to the `StaticRouter` class.
    """
    sr = StaticRouter(content_loader, **kwargs)
    sr.register(app)
