"""Test basic IO against a xrootd server fixture"""

from __future__ import annotations

import os
import shutil
import socket
import subprocess
import time

import fsspec
import pytest

XROOTD_PORT = 1094


def require_port_availability(port: int) -> bool:
    """Raise an exception if the given port is already in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(("localhost", port)) == 0:
            raise RuntimeError(f"This test requires port {port} to be available")

    return True


@pytest.fixture(scope="module")
def localserver(tmpdir_factory):
    require_port_availability(XROOTD_PORT)

    srvdir = tmpdir_factory.mktemp("srv")
    tempPath = os.path.join(srvdir, "Folder")
    os.mkdir(tempPath)
    cfgfile = os.path.join(srvdir, "xrd.cfg")
    with open(cfgfile, "w") as fout:
        fout.write("all.export /Folder\n")
        fout.write(f"oss.localroot {srvdir}\n")
    xrdexe = shutil.which("xrootd")
    proc = subprocess.Popen([xrdexe, "-p", str(XROOTD_PORT), "-c", cfgfile])
    time.sleep(2)  # give it some startup
    yield "root://localhost//Folder", tempPath
    proc.terminate()
    proc.wait(timeout=10)


@pytest.fixture()
def clear_server(localserver):
    remoteurl, localpath = localserver
    fs, _, _ = fsspec.get_fs_token_paths(remoteurl)
    # The open file handles on client side imply an open file handle on the server,
    # so removing the directory doesn't actually work until the client closes its handles!
    fs.invalidate_cache()
    shutil.rmtree(localpath)
    os.mkdir(localpath)
    yield


def test_ping(localserver, clear_server):
    remoteurl, localpath = localserver
    from XRootD import client

    fs = client.FileSystem(remoteurl)
    status, _n = fs.ping()
    if not status.ok:
        raise OSError(f"Server did not run properly: {status.message}")
