from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Typed-list'
LONG_DESCRIPTION = 'Python package for typed list'

# Setting up
setup(
   name='typedlist',
   version=VERSION,
   author="CeREF Technique",
   author_email="licence.tech@ceref.be",
   description=DESCRIPTION,
   long_description=LONG_DESCRIPTION,
   packages=find_packages(),
   install_requires=[], # add any additional packages that 

   keywords=['python', 'datagraph', 'PyQt6'],
   classifiers= [
      "Development Status :: 3 - Alpha",
      "Intended Audience :: Education",
      "Programming Language :: Python :: 2",
      "Programming Language :: Python :: 3",
      "Operating System :: MacOS :: MacOS X",
      "Operating System :: Microsoft :: Windows",
   ],
   package_dir = {'typedlist' : 'typedlist' },
)