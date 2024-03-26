"""
A simple static site generator for FastAPI.

Render static pages with FastAPI, Jinja2, and Markdown.
"""
from __future__ import annotations

__all__ = (
    "StaticRouter",
    "register",
)

from static_router.main import StaticRouter, register
