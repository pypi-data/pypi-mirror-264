# version placeholder (replaced by poetry-dynamic-versioning)
__version__ = "v1.1.7.3207rc"

# global app config
from .core import configurator

config = configurator.config

# helpers
from .core import helpers
