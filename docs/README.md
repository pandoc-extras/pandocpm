# package-manager

Manage the install/update/uninstall of Pandoc extras
(filters, templates, etc.)


## Install

To install pandoc-extras, open the command line and type:

```bash
pip install git+git://github.com/pandoc-extras/package-manager.git
```

- Requires Python 3.2 or later.
- On windows, the command line (``cmd``) must be run as administrator.

## To Uninstall

```
pip uninstall pandoc-extras
```

## Dev Install

After cloning the repo and opening the pandoc-extras folder:

`python setup.py install`
: installs the package locally

`python setup.py develop`
: installs locally with a symlink so changes are automatically updated
