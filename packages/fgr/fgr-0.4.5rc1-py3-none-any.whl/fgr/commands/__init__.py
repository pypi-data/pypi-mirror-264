"""
Overview
========

**Summary:** Primary command-line interface (CLI) to fgr.

---

Usage
-----

```sh
$ fgr --help
```

"""

__all__ = (
    'main',
    )

import argparse
import os
import typing

from .. import __version__

from .. import core
from .. import docs


class Constants(core.constants.PackageConstants):  # noqa

    DOCS_STATIC_DIR = os.path.join(
        os.path.split(os.path.dirname(__file__))[0],
        'docs',
        'static',
        )


try:
    DEFAULT_USER = os.getlogin()
except OSError:
    DEFAULT_USER = '<UNSPECIFIED>'


root_parser = argparse.ArgumentParser(
    description='root_parser',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    prog='fgr',
    )
root_parser.add_argument(
    '--version',
    '-v',
    action='version',
    version=__version__,
    )

parsers = typing.cast(
    argparse._SubParsersAction,
    root_parser.add_subparsers(
        title='module',
        required=True,
        help='specify a module to access its commands'
        )
    )

docs_parser = typing.cast(
    argparse.ArgumentParser,
    parsers.add_parser(
        'docs',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
    )
docs_parser.add_argument(
    'package',
    help='the name or path to the package to be documented',
    )
docs_parser.add_argument(
    '--version',
    '-v',
    default=Constants.BASE_VERSION,
    help='the version of the package',
    dest='version',
    )
docs_parser.add_argument(
    '--author',
    '-a',
    help='specify package author',
    dest='author',
    default=DEFAULT_USER,
    )
docs_parser.add_argument(
    '--output',
    '-o',
    help='specify directory in which to create docs/',
    dest='output_dir',
    default='.',
    )
docs_parser.add_argument(
    '--favicon',
    help='specify location of a favicon (.ico) file',
    dest='favicon_path',
    default=os.path.join(Constants.DOCS_STATIC_DIR, 'favicon.ico'),
    )
docs_parser.add_argument(
    '--logo',
    help='specify location of a logo file',
    dest='logo_path',
    default=os.path.join(Constants.DOCS_STATIC_DIR, 'logo.png'),
    )
docs_parser.add_argument(
    '--theme',
    choices=(
        'agogo',
        'alabaster',
        'bizstyle',
        'classic',
        'haiku',
        'nature',
        'pyramid',
        'scrolls',
        'sphinxdoc',
        'traditional',
        ),
    help='specify sphinx theme',
    dest='sphinx_theme',
    default='alabaster',
    )
docs_parser.add_argument(
    '--namespace-package',
    action='store_true',
    dest='is_namespace_package',
    help='include to specify that package is a namespace package',
    )
docs_parser.add_argument(
    '--add-module-names',
    action='store_true',
    dest='add_module_names',
    help='include to prepend module names to object names',
    )
docs_parser.add_argument(
    '--no-inherit-docstrings',
    action='store_false',
    dest='autodoc_inherit_docstrings',
    help='include to disable docstring inheritance',
    )
docs_parser.add_argument(
    '--no-cleanup',
    action='store_true',
    dest='no_cleanup',
    help='include to disable /docs/source/ dir removal',
    )
docs_parser.add_argument(
    '--include-private-modules',
    action='store_true',
    dest='include_private_modules',
    help='include to also document _private modules',
    )
docs_parser.add_argument(
    '--make-index',
    action='store_true',
    dest='make_index',
    help='include to make root file called index instead of {package}',
    )
docs_parser.add_argument(
    '--index-from-readme',
    nargs='?',
    dest='readme_path',
    help=(
        'specify path to README.md file to use'
        ' for index instead of {package}'
        ),
    const=os.path.join('.', 'README.md'),
    default=None,
    )
docs_parser.add_argument(
    '--no-include-meta-tags',
    action='store_true',
    dest='no_include_meta_tags',
    help='include to disable auto-generation of meta tags for documentation',
    )
docs_parser.add_argument(
    '--no-robots-txt',
    action='store_true',
    dest='no_include_robots',
    help='include to disable auto-generation of robots.txt file',
    )
docs_parser.add_argument(
    '--site-map-url',
    help='\n'.join(
        (
            (
                'specify full url path to the documentation version to be'
                'included in an auto-generated xml sitemap'
                ),
            '',
            'ex. https://example.readthedocs.io/en/stable',
            '',
            'can be repeated to include multiple versions'
            )
        ),
    action='append',
    dest='site_map_urls',
    )
docs_parser.set_defaults(func=docs.commands.document)


def main() -> None:
    """
    Main CLI entrypoint.

    Commands follow the structure:

    `$ fgr {fgr_module_name} ...`

    """

    args = root_parser.parse_args()
    kwargs = args._get_kwargs()
    as_args = [v for k, v in kwargs if k != 'func']
    args.func(*as_args)
