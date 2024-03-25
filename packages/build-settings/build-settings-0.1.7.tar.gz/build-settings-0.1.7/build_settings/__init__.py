"""
Let's initialize some goodies.
"""
try:
    from settings import BuildSettings
except ImportError:
    from .settings import BuildSettings  # noqa
