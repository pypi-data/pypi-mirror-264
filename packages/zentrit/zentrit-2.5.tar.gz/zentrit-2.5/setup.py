from setuptools import setup, find_packages

setup(
  name='zentrit',
  version='2.5',
  author='zentrit',
  packages=['zentrit', 'zentrit.printers'],
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  python_requires='>=3.7'
)