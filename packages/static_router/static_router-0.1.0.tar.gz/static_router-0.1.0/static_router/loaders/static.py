"""Static content loader for Jade."""
from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING, Any

import markdown

from static_router.models.content_loader import ContentLoader
from static_router.models.page import Page

if TYPE_CHECKING:
    from collections.abc import Callable


class StaticContentLoader(ContentLoader):
    """
    Load markdown content from a specified directory.

    Content is loaded recursively, for example using a directory called
    `content`, a file at `content/blog/2021-01-01.md` will be
    served at `/blog/2021-01-01/`.

    Additionally, if the file is `content/index.md`, it will be loaded at
    `/` instead of `/index/`.
    """

    def __init__(
        self,
        directory: str,
        *,
        md_renderer: Callable[[str], str] = markdown.markdown,
        md_renderer_opts: dict[Any, Any] | None = None,
    ) -> None:
        """
        Create a new instance of a static content loader.

        Params
        ------
        directory: :class:`str`
            The directory to load pages from.

        md_renderer: :class:`Callable[[str], str]`
            The markdown renderer to use.
            Defaults to :func:`markdown.markdown`.

        md_renderer_opts: :class:`dict[Any, Any] | None`
            The options to pass to the markdown renderer.
            Defaults to:
            ```python
            {
                "extensions": [
                    "codehilite",
                    "fenced_code",
                    "md_in_html",
                    "tables",
                    "toc",
                ],
            }
            ```
        """
        self.directory = directory
        self.md_renderer = md_renderer
        self.md_renderer_opts = md_renderer_opts or {
            "extensions": [
                "codehilite",
                "fenced_code",
                "md_in_html",
                "tables",
                "toc",
            ],
        }

    def load(self) -> list[Page]:
        """Load pages from a directory."""
        pages = []

        for path in pathlib.Path(self.directory).rglob("*.md"):
            with path.open() as file:
                md = file.read()

            page_path = str(path.with_suffix("")).replace(self.directory, "") + "/"

            if page_path == "/index/":
                page_path = "/"

            pages.append(
                Page.from_markdown_string(
                    md,
                    path=page_path,
                    md_renderer=self.md_renderer,
                    md_renderer_opts=self.md_renderer_opts,
                ),
            )

        return pages
