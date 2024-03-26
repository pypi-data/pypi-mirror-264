"""Model for a page."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import markdown
import pydantic
import yaml
from typing_extensions import Self

if TYPE_CHECKING:
    from collections.abc import Callable


class Page(pydantic.BaseModel):
    """
    The model for a page.

    Attributes
    ----------
    frontmatter: :class:`dict[str, Any]`
        The frontmatter metadata on the page.

    content: :class:`str`
        The content to be served.

    path: :class:`str`
        The path the page should be served at.

    """

    frontmatter: dict[str, Any]
    content: str
    path: str

    def __getattr__(self, key: str) -> Any:
        """
        Get a value from the frontmatter.

        Enables accessing frontmatter values as attributes.

        Params
        ------
        key: :class:`str`
            The key to get.

        Returns
        -------
        :class:`Any`
            The value for the key or `None` if it doesn't exist.

        """
        return self.frontmatter.get(key)

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Set an attribute on the frontmatter.

        Params
        ------
        name: :class:`str`
            The name of the key to store.

        value: :class:`Any`
            The value to set.
        """
        self.frontmatter[name] = value

    @classmethod
    def from_markdown_string(
        cls,
        md: str,
        *,
        path: str,
        md_renderer: Callable[[str], str] = markdown.markdown,
        md_renderer_opts: dict[Any, Any] | None = None,
    ) -> Self:
        """
        Generate a page from a markdown document.

        The document should include frontmatter at the start
        notated as below.

        ```yaml
        ---
        key: value
        ---
        ```

        Params
        ------
        md: :class:`str`
            The markdown document to parse.

        path: :class:`str`
            The path the page should be served at.

        md_renderer: :class:`Callable[[str], str]`
            The markdown renderer to use. Defaults
            to :func:`markdown.markdown`.

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

        Returns
        -------
        :class:`Self`
            The page.

        Raises
        ------
        :class:`ValueError`
            If there is no frontmatter in the document.

        """
        try:
            fm, content = md.split("---", 2)[1:]
        except ValueError as err:
            raise ValueError(f"Page {path} must have frontmatter.") from err

        frontmatter = yaml.safe_load(fm)

        if not frontmatter:
            frontmatter = {}

        if not path.endswith("/"):
            path += "/"

        return cls(
            frontmatter=frontmatter,
            content=md_renderer(
                content,
                **md_renderer_opts
                or {
                    "extensions": [
                        "codehilite",
                        "fenced_code",
                        "md_in_html",
                        "tables",
                        "toc",
                    ],
                },
            ),
            path=path,
        )
