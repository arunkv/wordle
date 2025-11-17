from __future__ import annotations

from typing import Any
from typing_extensions import override

from ._proxy import LazyProxy


class ResourcesProxy(LazyProxy[Any]):
    """A proxy for the `e77_hello_world.resources` module.

    This is used so that we can lazily import `e77_hello_world.resources` only when
    needed *and* so that users can just import `e77_hello_world` and reference `e77_hello_world.resources`
    """

    @override
    def __load__(self) -> Any:
        import importlib

        mod = importlib.import_module("e77_hello_world.resources")
        return mod


resources = ResourcesProxy().__as_proxied__()
