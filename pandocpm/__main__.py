"""
pandocpm: package manager for pandoc filters, etc.
====================================

(add description here)
"""


import argparse

from .tools import install_package, uninstall_package
# from .tools import upgrade_packages


def main():
    """
    usage:

    pandocpm   install CAT NAME --target=XYZ --index_url=XYZ --branch=XYZ --replace
    pandocpm uninstall CAT NAME --target=XYZ

    Misc:
        --verbose

    Not implemented:
    pandoc     upgrade
    pandoc     upgrade CAT
    pandoc     upgrade CAT NAME

    pandoc     list-index CAT
    pandoc     list-installed CAT
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('command',
                        help='install|uninstall')
    parser.add_argument('category',
                        help='filter, template, etc.')
    parser.add_argument('name',
                        help='Name of the package (filter/template/etc)')

    parser.add_argument('-T', '--target',
                        help="Install on <TARGET> instead of Pandoc's datadir")
    parser.add_argument('-I', '--index_url',
                        help="Install from an alternative index")
    parser.add_argument('-B', '--branch',
                        help="Install a specific variant of the package")

    parser.add_argument(
        '-R',
        '--replace',
        help="Overwrite existing packages",
        action="store_true")
    parser.add_argument('-V', '--verbose',
                        help="Show debugging info", action="store_true")

    args = parser.parse_args()
    command = args.command

    if command == 'install':
        install_package(args.name, args.category,
                        branch=args.branch,
                        replace=args.replace,
                        index_url=args.index_url,
                        target=args.target,
                        verbose=args.verbose)
    elif command == 'uninstall':
        uninstall_package(args.name, args.category,
                          target=args.target,
                          verbose=args.verbose)
    else:
        raise Exception("subcmd not supported: " + command)
        # update_package('debug', 'filter', verbose=True)

main()
