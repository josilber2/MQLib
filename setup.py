from glob import glob
from setuptools import setup, Extension
import numpy

setup(name = "MQLib",
      version = "0.1",
      ext_modules = [Extension("_MQLib", glob("src/**/*.cpp", recursive=True),
                               include_dirs = ["include", numpy.get_include()],
                               extra_compile_args=['-std=c++0x', '-O2'])],
      packages = ["MQLib"],
      package_data = {"": ["**/*.rf"]},
      install_requires = ['numpy', 'scipy', 'networkx']
      )
