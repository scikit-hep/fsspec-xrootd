from __future__ import annotations

import builtins
import importlib
import sys

import pytest

import fsspec_xrootd as m


def test_version():
    assert m.__version__


def test_import_without_xrootd(monkeypatch):
    original_import = builtins.__import__

    def raising_import(name, *args, **kwargs):
        if name == "XRootD":
            raise ModuleNotFoundError("No module named 'XRootD'", name="XRootD")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", raising_import)
    for module_name in ("fsspec_xrootd", "fsspec_xrootd.xrootd", "XRootD"):
        sys.modules.pop(module_name, None)

    module = importlib.import_module("fsspec_xrootd")

    assert module.__version__
    with pytest.raises(ModuleNotFoundError, match="Install it with"):
        module.XRootDFileSystem
