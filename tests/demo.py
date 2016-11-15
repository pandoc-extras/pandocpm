# CMD:
# cls && python setup.py install && cls && tests\demo.py


from pandocpm import *


if __name__ == '__main__':
    install_package('debug', 'filter', replace=False, verbose=True)
    install_package('debug', 'filter', replace=True, verbose=True)
    #upgrade_packages('', 'filter', verbose=True)
    uninstall_package('debug', 'filter', verbose=True)