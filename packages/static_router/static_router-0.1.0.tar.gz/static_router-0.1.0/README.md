# StaticRouter

A static file routing solution for FastAPI.

```python
import static_router
from static_router.loaders import StaticContentLoader

from fastapi import FastAPI

app = FastAPI()

# Other such fastapi things as required
# ...

loader = StaticContentLoader(directory="content")
static_router.register(app, content_loader=loader)
```

In your templates, you may access the following variables:
 - `page` - This contains any frontmatter you have defined in your markdown content
 - `router` - The content router instance
