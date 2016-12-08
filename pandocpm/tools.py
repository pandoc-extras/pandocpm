"""
Main install/upgrade/uninstall tools
"""

import os

from .utils import (get_index, get_path,
                    get_local_metadata, get_remote_metadata,
                    package_is_installed,
                    assert_package_is_installed,
                    assert_package_is_not_installed,
                    assert_package_is_available,
                    list_installed_packages,
                    download)


def install_package(name, category, branch=None, replace=False,
                    index_url=None, target=None, verbose=False,
                    index=None):

    if branch is None:
        branch = 'default'

    # Build index of available packages
    if index is None:
        index = get_index(category, index_url=index_url)

    # Find out location where packages get installed
    path, target = get_path(target, category, verbose=verbose)

    # Check that the requested package and branch exist in the online index
    assert_package_is_available(name, branch, index, category)

    # Check that the requested package does not exist locally
    # (or that replace is True)
    if not replace:
        assert_package_is_not_installed(name, path, category)

    # Uninstall the package if it already exists
    if package_is_installed(name, path):
        uninstall_package(name, category, target, verbose=verbose)

    # Copy the files or perform the install
    info = index[name, branch]
    url = info['url']
    url_type = info['url-type']

    if url.endswith('.yaml'):
        yaml_url = url
        python_url = yaml_url[:-5] + '.py'
    yaml_fn = os.path.join(path, name + '.yaml')
    python_fn = os.path.join(path, name + '.py')

    if url_type == 'simple':
        download(yaml_url, yaml_fn)
        meta = get_local_metadata(name, category, target)
        if 'install' in meta:
            shell(meta[install])
        else:
            download(python_url, python_fn)

    elif url_type == 'pip' and not url:
        shell('pip install ' + name)

    elif url_type == 'pip':
        # URL *MUST* BE OF THE FORM: git://github.com/jkbr/httpie.git
        cmd = 'pip install git+{}'.format(url)
        shell(cmd)

    else:
        raise Exception("unknown URL Type, don't know how to install")

    if verbose:
        msg = "(pandocpm) {} {} installed succesfully ({} branch)"
        print(msg.format(category, name, branch))


# def upgrade_package(name, category, path=None, verbose=False):
#    index = get_index(category, index_url=index_url)
#
#
#    # Uninstall the package if it already exists
#    if package_is_installed(name, path):
#        uninstall_package(name, category, target, verbose=verbose)
#
#
#
# def upgrade_packages(name=None, category=None, path=None, verbose=False):
#    if name is not None and category is None:
#        raise Exception("need the category of the package")
#
#    if category is None:
#        categories = get_categories()
#
#    if name is not None:
#        upgrade_package(name, category, path, verbose)
#    else:
#
# def install_package(name, category, branch='default', replace=False,
#                    index_url=None, target=None, verbose=False):


def uninstall_package(name, category, target=None, verbose=False):
    path, target = get_path(target, category, verbose=verbose)
    assert_package_is_installed(name, path, category)
    yaml_fn = os.path.join(path, name + '.yaml')
    meta = get_local_metadata(name, category, target)

    if 'uninstall' in meta:
        shell(meta[uninstall])  # might need admin/sudo?
    else:
        python_fn = os.path.join(path, name + '.py')
        os.remove(yaml_fn)
        os.remove(python_fn)
    if verbose:
        msg = "(pandocpm) {} {} uninstalled succesfully"
        print(msg.format(category, name))
