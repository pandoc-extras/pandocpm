"""
pandocpm: package manager for pandoc filters, etc.
====================================

(add description here)
"""


from .tools import install_package, uninstall_package
# from .tools import upgrade_packages

from .api import main

from .version import __version__


if __name__ == "__main__":
	main()