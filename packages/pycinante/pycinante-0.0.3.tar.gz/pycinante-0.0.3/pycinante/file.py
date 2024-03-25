"""This module provides functions to access and manipulate files.
"""
from __future__ import annotations
import glob
import os
import re
import shutil
import archive
from pycinante.types import AnyStr
from pycinante.list import listify
from pycinante.system import get_default_encoding

__all__ = [
    'exists',
    'isfile',
    'isdir',
    'mkdir',
    'drive',
    'parent',
    'basename',
    'filename',
    'suffix',
    'ext_aware',
    'abspath',
    'canpath',
    'relpath',
    'norpath',
    'sanpath',
    'join',
    'list_files',
    'copy',
    'move',
    'remove',
    'PathBuilder',
    'load_pickle',
    'dump_pickle',
    'load_numpy',
    'dump_numpy',
    'load_tensor',
    'dump_tensor',
    'load_json',
    'dump_json',
    'load_yaml',
    'extract_archive'
]

def exists(pathname: AnyStr) -> bool:
    """Return True if path refers to an existing path or an open file descriptor. Returns
    False for broken symbolic links. On some platforms, this function may return False if
    permission is not granted to execute `os.stat()` on the requested file, even if the p-
    ath physically exists.
    """
    return os.path.exists(pathname)

def isfile(pathname: AnyStr) -> bool:
    """Return True if path is an existing regular file. This follows symbolic links, so b-
    -oth `islink()` and `isfile()` can be true for the same path.
    """
    return os.path.exists(pathname)

def isdir(pathname: AnyStr) -> bool:
    """Return True if path is an existing directory. This follows symbolic links, so both
    `islink()` and `isdir()` can be true for the same path.
    """
    return os.path.isdir(pathname)

def mkdir(pathname: AnyStr, is_parent: bool = False, **kwargs) -> AnyStr:
    """Create a directory. The argument `exist_ok` default is True. If the parameter
    `is_parent` is True, the parent directory of the `pathname` will be created. When All
    was done the `pathname` will be returned.

    >>> mkdir('/tmp/pycinante/user.json', is_parent=True)
    '/tmp/pycinante/user.json'
    """
    t = (is_parent and os.path.dirname(pathname)) or pathname
    os.makedirs(t, exist_ok=kwargs.pop('exist_ok', True), **kwargs)
    return pathname

def drive(pathname: AnyStr) -> AnyStr:
    """Return the drive of the pathname, where drive is either a mount point or the empty
    string. It just returns the first part of `os.path.splitdrive`.

    >>> drive('/usr/etc/bin/pycinante')
    ''
    """
    return os.path.splitdrive(pathname)[0]

def parent(pathname: AnyStr) -> AnyStr:
    """Return the parent directory of the file or directory `pathname`. It's an alias for
    `os.path.dirname`.

    >>> parent('/usr/etc/bin/pycinante')
    '/usr/etc/bin'
    """
    return os.path.dirname(pathname)

def basename(pathname: AnyStr) -> AnyStr:
    """Return the full name (included the extension) of the file on the `pathname`. It's
    an alias for `os.path.basename`.

    >>> basename('/usr/etc/bin/pycinante.json')
    'pycinante.json'
    """
    return os.path.basename(pathname)

def filename(pathname: AnyStr) -> AnyStr:
    """Return the name (excluded the extension) of the file on the `pathname`. The param-
    -eter `pathname` can be a directory or file path and the last level folder name of the
    path will be returned when the `pathname` is a directory.

    >>> filename('/usr/etc/bin/pycinante.json')
    'pycinante'
    """
    return os.path.basename(os.path.splitext(pathname)[0])

def suffix(pathname: AnyStr) -> AnyStr:
    """Return the file extension of the file `pathname`. If the path not contains an ext,
    then the empty string will be returned. And the function just returns the second res-
    -ult of `os.path.splitext`.

    >>> suffix('/usr/etc/bin/pycinante.json')
    '.json'
    >>> suffix('/usr/etc/bin/pycinante')
    ''
    """
    return os.path.splitext(pathname)[1]

def ext_aware(pathname: AnyStr, ext: AnyStr) -> AnyStr:
    """Automatically append the given extension to the `pathname` if the pathname not an
    available extension. The rules are that a pathname with an extension will be directly
    returned, otherwise the given `ext` will be appended to the end of the pathname.

    >>> ext_aware('/usr/etc/bin/pycinante.json', '.jsoup')
    '/usr/etc/bin/pycinante.json'
    >>> ext_aware('/usr/etc/bin/pycinante', '.json')
    '/usr/etc/bin/pycinante.json'
    """
    if suffix(pathname) != '':
        return pathname
    ext = (ext.startswith('.') and ext) or ('.' + ext)
    pathname = (pathname.endswith('.') and pathname[:-1]) or pathname
    return pathname + ext

def abspath(pathname: AnyStr) -> AnyStr:
    """Return the absolute pathname of the file or directory `pathname`.

    >>> abspath('.')
    '/Volumes/User/home/chishengchen/Codespace/toy/pycinante/pycinante'
    """
    return os.path.abspath(pathname)

def canpath(pathname: AnyStr) -> AnyStr:
    """Return the canonical path of the specified filename, eliminating any symbolic links
    encountered in the path.

    >>> canpath('~/Codespace/toy/pycinante/./pycinante')
    '~/Codespace/toy/pycinante/pycinante'
    """
    return os.path.relpath(pathname)

def relpath(pathname: AnyStr, start: AnyStr | None = None) -> AnyStr:
    """Return a relative filepath to path either from the current directory or from an op-
    -tional start directory.

    >>> relpath('/Volumes/User/home/chishengchen/Codespace/toy', '.')
    '../..'
    """
    return os.path.relpath(pathname, start=start or os.curdir)

def norpath(pathname: AnyStr) -> AnyStr:
    """Normalize a pathname by collapsing redundant separators.

    >>> norpath('~/Codespace/toy/./pycinante//.//pycinante')
    '~/Codespace/toy/pycinante/pycinante'
    """
    return os.path.normpath(pathname)

def sanpath(pathname: AnyStr, rep: AnyStr = '') -> AnyStr:
    """Replace all the invalid characters from a pathname with the char `rep`.

    >>> sanpath('A survey: Code is cheap, show me the code.pdf')
    'A survey Code is cheap, show me the code.pdf'
    """
    return re.sub(re.compile(r'[<>:"/\\|?*\x00-\x1F\x7F]'), rep, pathname)

def join(pathname: AnyStr, *pathnames: AnyStr) -> AnyStr:
    """Join one or more pathname segments intelligently. The return value is the concaten-
    -ation of pathname and all members of `*pathnames`, with exactly one directory separa-
    -tor following each non-empty part, except the last.

    >>> join('/path/', 'etc', 'bin/', 'starting.conf')
    '/path/etc/bin/starting.conf'
    """
    return os.path.join(pathname, *pathnames)

def list_files(pathname: AnyStr, exts: list[AnyStr] | None = None) -> list[AnyStr]:
    """Return a list of pathname matching a pathname pattern.

    >>> assert list_files('./', exts=['.py'])
    """
    file_list = []
    for ext in listify(exts or ['.*']):
        # noinspection PyUnresolvedReferences,PyTypeChecker
        ext = (ext.startswith('.') and ext) or ('.' + ext)
        file_list.extend(glob.glob(join(pathname, f'*{ext}')))
    return file_list

def copy(src_pathname: AnyStr, dest_pathname: AnyStr) -> AnyStr:
    """Copy data and mode bits (`cp src dst`). Return the file's destination. The destina-
    -tion may be a directory. If source and destination are the same file, a SameFileError
    will be raised.

    >>> import tempfile
    >>> copy(tempfile.mkstemp('.txt', text=True)[1], '/tmp/copy.txt')
    '/tmp/copy.txt'
    """
    return shutil.copy(src_pathname, dest_pathname)

def move(src_pathname: AnyStr, dest_pathname: AnyStr) -> AnyStr:
    """Recursively move a file or directory to another location. This is similar to the
    Unix "mv" command. Return the file or directory's destination.

    >>> import tempfile
    >>> copy(tempfile.mkstemp('.txt', text=True)[1], '/tmp/move.txt')
    '/tmp/move.txt'
    """
    return shutil.move(src_pathname, dest_pathname)

def remove(pathname: AnyStr) -> None:
    """Recursively delete all files or folders in the pathname. The parameter `pathname`
    can be a directory or a file. If it is a file, the file will be deleted. If it is not
    a directory or a file, nothing be done.

    >>> remove('/tmp/pycinante')
    """
    if isdir(pathname):
        shutil.rmtree(pathname, ignore_errors=True)
        os.mkdir(pathname)
    elif isfile(pathname):
        os.remove(pathname)

class PathBuilder(object):
    """A pathname builder for easily constructing a pathname by the operation `/` and `+`.

    >>> p = PathBuilder('.', 'a', 'b', mkdir=False)
    >>> p / 'c' / 'd' / 'e' + 'f.json'
    './a/b/c/d/e/f.json'
    """

    def __init__(self, *pathnames: AnyStr, mkdir: bool = True) -> None:
        self.mkdir = mkdir
        self.path = str(join(*(pathnames or ('.',))))
        if self.mkdir:
            os.makedirs(self.path, exist_ok=True)

    def __truediv__(self, pathname: AnyStr) -> 'PathBuilder':
        """Append a sub-pathname to the original pathname and return a new pathname insta-
        -nce with the added sub-pathname.
        """
        return PathBuilder(join(self.path, pathname), mkdir=self.mkdir)

    def __add__(self, basename: AnyStr) -> AnyStr:
        """Append a basename to the original pathname and return the full pathname string
        after adding the basename.
        """
        return join(self.path, basename)

class text_editor(object):
    """A text editor allows you to edit a text document on a dynamic environment.

    >>> with text_editor('/tmp/test.txt') as editor:
    ...     editor.writeline('hello world !')
    14
    """

    def __init__(self, pathname: str, mode='a+', encoding: str = 'utf-8'):
        self.pathname = pathname
        self.mode = mode
        self.encoding = encoding

    def clear(self) -> int:
        return self.fp.truncate()

    def write(self, s: AnyStr) -> int:
        return self.fp.write(s)

    def writeline(self, s: AnyStr) -> int:
        text = s if s.endswith(os.linesep) else s + os.linesep
        return self.fp.write(text)

    def read(self) -> AnyStr:
        return self.fp.read()

    def readline(self) -> AnyStr:
        return self.fp.readline()

    def seek(self, offset: int, whence: int = 0) -> int:
        return self.fp.seek(offset, whence)

    def __enter__(self) -> 'text_editor':
        self.fp = open(self.pathname, mode=self.mode, encoding=self.encoding)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.fp.close()

def load_pickle(pathname: AnyStr, ext: AnyStr = '.pkl', **kwargs) -> ...:
    """Read a pickled object representation from the `.pkl` file.

    >>> dump_pickle({'name': 'Pycinante'}, 'test')
    >>> load_pickle('test')
    {'name': 'Pycinante'}
    >>> remove('test.pkl')
    """
    import pickle
    with open(ext_aware(pathname, ext), 'rb') as fp:
        return pickle.load(fp, **kwargs)

def dump_pickle(obj: ..., pathname: AnyStr, ext: AnyStr = '.pkl', **kwargs) -> None:
    """Write a pickled representation of obj to the `.pkl` file.

    >>> dump_pickle({'name': 'Pycinante'}, 'test')
    >>> load_pickle('test')
    {'name': 'Pycinante'}
    >>> remove('test.pkl')
    """
    import pickle
    with open(ext_aware(pathname, ext), 'wb') as fp:
        pickle.dump(obj, fp, **kwargs)

# noinspection PyUnresolvedReferences
def load_numpy(pathname: AnyStr, ext: AnyStr = '.npy', **kwargs) -> 'np.ndarray':
    """Load arrays or pickled objects from `.npz` or pickled files.

    >>> import numpy as np
    >>> dump_numpy(np.array([7, 8, 9]), 'test')
    >>> load_numpy('test')
    array([7, 8, 9])
    >>> remove('test.npy')
    """
    import numpy as np
    return np.load(ext_aware(pathname, ext), **kwargs)

# noinspection PyUnresolvedReferences
def dump_numpy(
    obj: 'np.ndarray', pathname: AnyStr, ext: AnyStr = '.npy', **kwargs
) -> None:
    """Save an array to a binary file in NumPy ``.npz`` format.

    >>> import numpy as np
    >>> dump_numpy(np.array([7, 8, 9]), 'test')
    >>> load_numpy('test')
    array([7, 8, 9])
    >>> remove('test.npy')
    """
    import numpy as np
    np.save(ext_aware(pathname, ext), obj, **kwargs)

# noinspection PyPackageRequirements, PyUnresolvedReferences
def load_tensor(pathname: AnyStr, ext: AnyStr = '.pth', **kwargs) -> 'torch.Tensor':
    """Loads an object saved with `torch.save` from a `.pth` file.

    >>> import torch
    >>> dump_tensor(torch.tensor([7, 8, 9]), 'test')
    >>> load_tensor('test')
    tensor([7, 8, 9])
    >>> remove('test.pth')
    """
    import torch
    return torch.load(ext_aware(pathname, ext), **kwargs)

# noinspection PyPackageRequirements,PyUnresolvedReferences
def dump_tensor(
    obj: 'torch.Tensor', pathname: AnyStr, ext: AnyStr = '.pth', **kwargs
) -> None:
    """Saves an object to a `.pth` disk file.

    >>> import torch
    >>> dump_tensor(torch.tensor([7, 8, 9]), 'test')
    >>> load_tensor('test')
    tensor([7, 8, 9])
    >>> remove('test.pth')
    """
    import torch
    torch.save(obj, ext_aware(pathname, ext), **kwargs)

def load_json(pathname: AnyStr, ext: AnyStr = '.json', **kwargs) -> ...:
    """Deserialize a file-like object containing a JSON document to a Python object.

    >>> dump_json({'name': 'Pycinante'}, 'test')
    >>> load_json('test')
    {'name': 'Pycinante'}
    >>> remove('test.json')
    """
    import json
    encoding = get_default_encoding(kwargs.pop('encoding', None))
    with open(ext_aware(pathname, ext), 'r', encoding=encoding) as fp:
        return json.load(fp, **kwargs)

def dump_json(obj: ..., pathname: AnyStr, ext: AnyStr = '.json', **kwargs) -> None:
    """Serialize the Python object `obj` into a json file.

    >>> dump_json({'name': 'Pycinante'}, 'test')
    >>> load_json('test')
    {'name': 'Pycinante'}
    >>> remove('test.json')
    """
    import json
    encoding = get_default_encoding(kwargs.pop('encoding', None))
    with open(ext_aware(pathname, ext), 'w', encoding=encoding) as fp:
        json.dump(obj, fp, **kwargs)

# noinspection PyUnresolvedReferences,PyPackageRequirements
def load_yaml(
    pathname: AnyStr, ext: AnyStr = '.yaml', loader: Optional['yaml.Loader'] = None,
    encoding: OptionalStr = None
) -> ...:
    """Parse the YAML document in a file and produce the corresponding Python object."""
    import yaml
    pathname = ext_aware(pathname, ext)
    with open(pathname, 'r', encoding=get_default_encoding(encoding)) as fp:
        return (loader or yaml.safe_load)(fp)

def extract_archive(src_pathname: AnyStr, dest_pathname: AnyStr) -> None:
    """Unpack the tar or zip file at the specified path to the directory specified by to_-
    -path. Ref: https://flaggo.github.io/pydu/#/zh-cn/archive, https://pypi.org/project/p-
    -ython-archive.
    """
    assert suffix(src_pathname).lower() in archive.extension_map.keys(), \
        f'unsupported compression format for the file {src_pathname}'
    archive.extract(src_pathname, dest_pathname)
