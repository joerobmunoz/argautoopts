from .resolver import resolver as _resolver
from . import frontends

# User-friendly aliases
# <project>.register_opts
# <project>.resolve

from .decorate import register_opts as register
resolve = _resolver.resolve