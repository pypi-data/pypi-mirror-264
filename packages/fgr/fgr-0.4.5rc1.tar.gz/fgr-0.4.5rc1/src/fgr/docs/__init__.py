"""
Overview
========

**Summary:** fgr extension for generating wiki documentation with [Sphinx](https://www.sphinx-doc.org).

---

Usage
-----

##### Document a package as follows.

```sh
$ pip install fgr[docs]
$ fgr docs package_name
```

"""

__all__ = (
    'commands',
    )

from . import commands
