from .resolver import resolver

# User-friendly aliases
# <project>.register_opts
# <project>.resolve

from .decorate import register_opts
resolve = resolver.resolve