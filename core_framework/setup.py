from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("core_mac_lib.pyx")
)

