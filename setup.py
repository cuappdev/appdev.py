import re
from setuptools import setup

# Influence for this inspired by https://goo.gl/Pi51aC
version = None
for line in open('./appdev/__init__.py'):
  m = re.search('__version__\s*=\s*(.*)', line) # pylint: disable=W1401
  if m:
    version = m.group(1).strip()[1:-1]  # quotes
    break
assert version

setup(
    name='appdev.py',
    version=version,
    description='AppDev Core Modules',
    author='Cornell AppDev',
    author_email='cornellappdev@gmail.com',
    url='https://github.com/cuappdev/appdev.py',
    license='MIT',
    packages=['appdev'],
    include_package_data=True,
    package_data={'': ['README.rst']},
    install_requires=[
        'Flask',
    ],
    tests_require=[],
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ]
)
