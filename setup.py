from setuptools import setup, find_packages

setup(name='upp',
      version='1.0',
      description='Uplift Power Play',
      long_description='A tool for parsing, dumping and modifying data in Radeon PowerPlay tables',
      url='https://github.com/sibradzic/upp',
      author='Samir Ibradžić',
      license='GPL-3.0',
      packages=['atom_gen', ''],
      py_modules = ['upp'],
      install_requires=[
          'click'
      ],
      include_package_data=True)
