# package-manager

Manage the install/update/uninstall of Pandoc extras
(filters, templates, etc.)


## Install

To install pandocpm, open the command line and type:

```bash
pip install pandocpm
```

- Requires Python 3.2 or later.
- On windows, the command line (``cmd``) must be run as administrator.

## To Uninstall

```
pip uninstall pandocpm
```

## Dev Install

After cloning the repo and opening the pandoc-extras folder:

`python setup.py install`
: installs the package locally

`python setup.py develop`
: installs locally with a symlink so changes are automatically updated
