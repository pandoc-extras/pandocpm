"""
Auxiliary utilities (download, check if package exists, etc.)
"""

import os
import yaml

# shutil.which: new in version 3.3
try:
    from shutil import which
except ImportError:
    from shutilwhich import which

from subprocess import Popen, PIPE, call

import requests


def list_installed_packages(categories=None):
    pass


def get_index(category, suffix='s', index_url=None):
    raw_yaml = _download_index(category + suffix, index_url)
    index = _parse_index(raw_yaml)
    return index


def _download_index(category, index_url):
    if index_url is None:
        index_url = 'https://raw.githubusercontent.com/pandoc-extras/packages/master/{}.yaml'
    url = index_url.format(category)
    r = requests.get(url)
    if r.status_code != 200:
        raise IOError("Cannot download index, error {}".format(r.status_code))
    return r.text


def _parse_index(raw_yaml):
    index = yaml.load(raw_yaml)
    new_index = dict()
    for c in index:
        name = c.pop('name')
        branch_dicts = c.pop('branches', [{'branch': 'default'}])
        for branch_dict in branch_dicts:
            branch = branch_dict.pop('branch')
            new_c = c
            new_c.update(branch_dict)
            if 'url-type' not in new_c:
                new_c['url-type'] = 'simple'
            new_index[(name, branch)] = new_c
    return new_index


def get_local_metadata(name, category, target):
    path, target = get_path(target, category)
    yaml_fn = os.path.join(path, name + '.yaml')
    with open(yaml_fn, encoding='utf-8') as f:
        raw_yaml = f.read()
    meta = _parse_metadata(raw_yaml)
    return meta


def get_remote_metadata(name, url, local=False):
    if url.endswith('.yaml'):
        r = requests.get(url)
        if r.status_code != 200:
            raise IOError(
                "Cannot download YAML, error {}".format(r.status_code))
        meta = _parse_metadata(r.text)
    else:
        meta = {'name': name, 'url': url, 'version': '0.0.0'}
    return meta


def _parse_metadata(raw_yaml):
    meta = yaml.load(raw_yaml)
    version = meta.get('version', '0.0.0')
    try:
        version = tuple(int(x) for x in version.split('.'))
    except:
        version = (0, 0, 0)
    meta['version'] = version
    return meta


def shell(args, wait=True, msg=None):
    """
    Execute the external command and get its exitcode, stdout and stderr.

    copied from panflute.tools
    """

    # Fix Windows error if passed a string
    if isinstance(args, str):
        args = shlex.split(args, posix=(os.name != "nt"))
        args = [arg.replace('/', '\\') for arg in args]

    if wait:
        proc = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate(input=msg)
        exitcode = proc.returncode
        if exitcode != 0:
            raise IOError(err)
        return out
    else:
        DETACHED_PROCESS = 0x00000008
        proc = Popen(args, creationflags=DETACHED_PROCESS)


def run_pandoc(text='', args=None):
    """
    Low level function that calls Pandoc with (optionally)
    some input text and/or arguments

    (copied from panflute.tools)
    """

    if args is None:
        args = []

    pandoc_path = which('pandoc')
    if pandoc_path is None or not os.path.exists(pandoc_path):
        raise OSError("Path to pandoc executable does not exists")

    proc = Popen([pandoc_path] + args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate(input=text.encode('utf-8'))
    exitcode = proc.returncode
    if exitcode != 0:
        raise IOError(err)
    return out.decode('utf-8')


def get_path(target, category, verbose=False, suffix='s'):
    """
    get the path where the filters/templates/etc are installed
    """

    if target is None:
        # Copied from panflute.autofilter
        info = run_pandoc(args=['--version']).splitlines()
        prefix = "Default user data directory: "
        info = [row for row in info if row.startswith(prefix)]
        assert len(info) == 1
        target = info[0][len(prefix):]

    path = os.path.join(target, category + suffix)

    if not os.path.isdir(path):
        if verbose:
            print("(pandocpm) folder does not exist, creating it")
        os.makedirs(path)

    if verbose:
        print('(pandocpm) data directory:', path)

    return path, target


def package_is_installed(name, path):
    yaml_fn = os.path.join(path, name + '.yaml')
    return os.path.isfile(yaml_fn)


def assert_package_is_installed(name, path, category):
    if not package_is_installed(name, path):
        raise Exception("{} {} not installed".format(category, name))


def assert_package_is_not_installed(name, path, category):
    if package_is_installed(name, path):
        msg = "{} {} already installed; uninstall or use the '--replace' flag"
        raise Exception(msg.format(category, name))


def assert_package_is_available(name, branch, index, category):
    if not (name, branch) in index:
        msg = "{} <{}> with branch <{}> not found on index:\n{}"
        raise KeyError(msg.format(category, name, branch, repr(index.keys())))


def download(url, filename):
    r = requests.get(url)
    with open(filename, mode='w', encoding='utf-8') as f:
        # f.write(r.content)
        f.write(r.text)
