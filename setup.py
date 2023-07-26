from setuptools import setup, Extension
try:
    from Cython.Build import cythonize
except ImportError:
    def cythonize(li):
        return []

ext_modules = [Extension("utils._decode", ["utils/_decode.pyx"])]

setup(
    name="books-dl",
    ext_modules=cythonize(ext_modules, compiler_directives={'language_level': "3"}),
)
