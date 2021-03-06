"""Utility context managers for Emanate's testsuite."""

import os
from pathlib import Path
from tempfile import TemporaryDirectory
from contextlib import contextmanager


@contextmanager
def chdir(path):
    """Context manager for temporarily changing directory."""
    if isinstance(path, Path):
        path = str(path)

    cwd = Path.cwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(str(cwd))


@contextmanager
def directory_tree(obj):
    """Provide a temporary directory populated with configurable contents."""
    def mktree(path, obj):
        """Populate a directory from a dict-like describing its contents."""
        assert isinstance(path, Path)
        # File by content
        if isinstance(obj, str):
            with path.open(mode='w') as file:
                file.write(obj)

        # Directory
        elif 'type' not in obj:
            path.mkdir(exist_ok=True)
            for name, child in obj.items():
                mktree(path / name, child)

        elif obj['type'] == 'link':
            path.symlink_to(obj['target'])

    with TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        if obj:
            mktree(tmpdir, obj)
        yield tmpdir


@contextmanager
def home(path):
    """Temporarily set the HOME environment variable."""
    home_dir = os.getenv('HOME', None)
    user_dir = os.getenv('USERPROFILE', None)

    try:
        os.environ['HOME'] = os.environ['USERPROFILE'] = str(path)
        yield

    finally:
        if home_dir is not None:
            os.environ['HOME'] = home_dir
        else:
            del os.environ['HOME']

        if user_dir is not None:
            os.environ['USERPROFILE']= user_dir
        else:
            del os.environ['USERPROFILE']
