# warlockSFX

![GitHub last commit](https://img.shields.io/github/last-commit/d33pster/warlockSFX)
![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/d33pster/warlockSFX)
![PyPI - Status](https://img.shields.io/pypi/status/warlockSFX)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/warlockSFX)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/warlockSFX)
![PyPI - Version](https://img.shields.io/pypi/v/warlockSFX)
![GitHub License](https://img.shields.io/github/license/d33pster/warlockSFX)

<p align='center'>
    <a href='#Installation'>Installation</a>
    &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
    <a href='#Usage'>Usage</a>
</p>

warlockSFX is an upgraded version of pymakeself by Andrew Gillis, well, kind of.<br><br>
Changes:
- python >= 3.9 support
- choice of output file (OS specific executable file(with custom extension) or a .py file)
- removed encryption support.
- some features are made optional

## About
warlockSFX is a part of warlock (Data Breach Protection Software (patent-pending)). It is an upgraded version of pymakeself and works fine with recent versions of python

## Working
```console
somewhere/_setup --------------------+
                                     |
                                     |
                                     |
someplace/_content/ -----------+     |
         file 1                |     |
         file 2                |     |
         ...                   |     |
                               |     |
                               |     |
   ./package/                  |     |
          inf/                 |     |
             ...   <-----------+     |
             ...   <-----------------+
    

    +---------+                  +---------------+
./  | package | ---------------> | package.targz | ----------+
    +---------+                  +---------------+           |
                                                             |
                                                             |
                                                             |
    +-------------------------------------------------+      |
 ./ | package.py/package.<extension>(executable file) | <----+
    +-------------------------------------------------+

```

## Installation
```console
# install using pip
$ pip install warlocksfx

# download wheel or package from github or pypi
```
Links:

- [PYPI](https://pypi.org/project/warlockSFX/0.1.4/) Package page.
- [GitHub](https://github.com/d33pster/warlockSFX) Repository.

Raise Issue Here:
- [GitHub](https://github.com/d33pster/warlockSFX) Issues.

## Usage
flow:
```console
# import as a module in python script/project

>>> from warlocksfx import _makesfx

# create a class object

>>> sfxCTRL = _makesfx()

# make sfx

>>> sfxCTRL._make(Params)
```

function help:
```console
>>> help(_makesfx._make)

Help on function _make in module warlocksfx:

_make(self, content: str, outfile: str, _setup: str, _setupargs=(), sha256=False, compress='gz', quiet=False, label=None, extension='.warlock')
    Create SFX

    Args:
        content (str): input directory
        outfile (str): output executable name
        _setup (str): setup file which will be executed from the extracted content dir
        _setupargs (tuple, optional): setup file arguments if any. Defaults to ().
        sha256 (bool, optional): Enable (True), Disable (False) SHA256. Defaults to False.
        compress (str, optional): Type of compression. Defaults to 'gz'. Possible -> ['gz', 'bz2', 'xz']
        quiet (bool, optional): Do not print any messages other than errors if True. Defaults to False.
        label (_type_, optional): Text describing the package. Defaults to None.

    Return:
        Path to SFX executable
```

## Note to Users
I made this for my own personal use but it is not limited to that. If there is any suggestions or fixes, raise an issue [here](https://github.com/d33pster/warlockSFX/issues).

The Original pymakeself was made by Andrew Gillis (Around 10 years ago or so). As a lot of users find it hard because it is deprecated, hope this helps :)