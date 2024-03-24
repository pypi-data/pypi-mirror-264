"""
Overview
========

**Author:** dan@1howardcapital.com

**Summary:** Zero-dependency python framework for object oriented development.

---

Usage
-----

```py
import fgr
```

"""

__all__ = (
    'codec',
    'constants',
    'dtypes',
    'enums',
    'exceptions',
    '_fields',
    'fields',
    'log',
    'meta',
    'modules',
    'objects',
    'patterns',
    'query',
    'utils',
    )

from . import codec
from . import constants
from . import dtypes
from . import enums
from . import exceptions
from . import _fields
from . import fields
from . import log
from . import meta
from . import modules
from . import objects
from . import patterns
from . import query
from . import utils

utils._resolve_remaining_type_refs()
