import sys
from version import version, dversion
from setuptools import Extension, find_packages
try:
    from Cython.Build import cythonize
except ImportError:
    def cythonize(li):
        return []

ext_modules = [Extension("books_dl.utils._decode", [
                         "books_dl/utils/_decode.pyx"])]

if "py2exe" in sys.argv:
    from distutils.core import setup
    import py2exe
    params = {
        "console": [{
            'script': "books_dl/__main__.py",
            "dest_base": 'books-dl',
            'version': version,
            'product_name': 'books-dl',
            'product_version': dversion,
            'company_name': 'lifegpc',
            'description': 'books.com.tw book downloader',
        }],
        "options": {
            "py2exe": {
                "optimize": 2,
                "compressed": 1,
                "excludes": ["pydoc", "unittest"],
                "includes": ["charset_normalizer.md__mypyc"],
            }
        },
        "zipfile": None,
    }
else:
    from setuptools import setup
    params = {
        "install_requires": ["requests"],
        'entry_points': {
            'console_scripts': ['books-dl = books_dl:start']
        },
        "python_requires": ">=3.6"
    }

setup(
    name="books-dl",
    version=version,
    url="https://github.com/lifegpc/books-dl",
    author="lifegpc",
    author_email="root@lifegpc.com",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.7",
    ],
    license="GNU General Public License v3 or later",
    description="books.com.tw book downloader",
    long_description="books.com.tw book downloader",
    keywords="downloader",
    packages=find_packages(".", include="books_dl*"),
    ext_modules=cythonize(ext_modules, compiler_directives={
                          'language_level': "3"}),
    **params
)
