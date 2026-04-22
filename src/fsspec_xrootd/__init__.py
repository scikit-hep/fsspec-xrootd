"""fsspec-xrootd

An xrootd implementation for fsspec.

BSD 3-Clause License; see https://github.com/scikit-hep/fsspec-xrootd/blob/main/LICENSE
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ._version import version as __version__

if TYPE_CHECKING:
    from .xrootd import XRootDFile, XRootDFileSystem

__all__ = ("__version__", "XRootDFileSystem", "XRootDFile")


def __getattr__(name: str) -> Any:
    if name not in {"XRootDFile", "XRootDFileSystem"}:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    try:
        from .xrootd import XRootDFile, XRootDFileSystem
    except ModuleNotFoundError as exc:
        if exc.name == "XRootD":
            raise ModuleNotFoundError(
                "The 'xrootd' package is required to use fsspec-xrootd. "
                'Install it with `pip install "fsspec-xrootd[xrootd]"`.'
            ) from exc
        raise

    globals().update({
        "XRootDFile": XRootDFile,
        "XRootDFileSystem": XRootDFileSystem,
    })
    return globals()[name]
