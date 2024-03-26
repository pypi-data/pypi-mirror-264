"""Abstract class for loading content from a source."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from static_router.models.page import Page


class ContentLoader(ABC):
    """Base class for loading content from a source."""

    @abstractmethod
    def load(self) -> list[Page]:
        """
        Abstract method to load pages from a source.

        Must take no arguments and return a list of :class:`Page`s.

        Returns
        -------
        :class:`list[Page]`
            The loaded pages.

        """
