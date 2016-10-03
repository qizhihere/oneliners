def has_pkg(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        return False
    return True

def pip_install(package):
    import pip
    pip.main(['install', package])

def ensure_pkg(package):
    has_pkg(package) or pip_install(package)
