# Copyright is waived. No warranty is provided. Unrestricted use and modification is permitted.

import os
import sys
import subprocess

HELP = """\
Compile PyPy from source

python compile-pypy.py <version>

where,
  <version>   PyPy version number to compile e.g. pypy3.6-v7.3.2
"""

if len(sys.argv) < 2:
    sys.exit(HELP)

if not sys.platform.startswith("linux"):
    sys.exit("Executes in linux environment only")

# Install prerequisites
subprocess.call(["sudo", "yum", "-y", "install", "gcc", "make", "libffi-devel", "pkgconfig", "zlib-devel", "bzip2-devel", "sqlite-devel", "ncurses-devel", "expat-devel", "openssl-devel", "tk-devel", "gdbm-devel", "python-cffi", "xz-devel"])

# Download pypy source
version = sys.argv[1]
tar_filename = version + "-src.tar.bz2"
subprocess.call(["wget", "https://downloads.python.org/pypy/" + tar_filename])
subprocess.call(["tar", "-xvf", tar_filename])

# Compile source
source_path = version + "-src"
os.chdir(source_path + "/pypy/goal")
subprocess.call(["python", "../../rpython/bin/rpython", "--opt=jit", "targetpypystandalone.py"])

# Package distribution
os.chdir("../tool/release")
archive_name = version + "-amzn2"
target_dir = os.path.expanduser("~")
subprocess.call(["python", "package.py", "--targetdir", target_dir, "--archive-name", archive_name])
