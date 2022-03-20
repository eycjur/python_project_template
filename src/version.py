try:
    from setuptools_scm import get_version

    __version__ = get_version(root="..", relative_to=__file__)
except (ImportError, LookupError):
    print("setuptools_scm is not installed.")
    __version__ = "UNKNOWN"
