from setuptools import setup, find_packages
import sys

version = '0.11'

long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

install_requires = [
    'setuptools',
    'pyramid',
    'deform',
    'colander',
    'requests',
    'SQLAlchemy',
    'alembic',
    'gaq_hub',
    'zope.sqlalchemy',
    # -*- Extra requirements: -*-
]
if '__pypy__' in sys.builtin_module_names:
    install_requires.append('psycopg2cffi')
else:
    install_requires.append('psycopg2')

setup(
    name='sixfeetup.bowab',
    version=version,
    description="Helpful utilities for Pyramid projects",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
    ],
    keywords='',
    author='',
    author_email='',
    url='http://svn.plone.org/svn/collective/',
    license='gpl',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['sixfeetup'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=['nose', 'coverage'],
    test_suite="nose.collector",
    extras_require={'test': ['coverage', 'mock']},
    entry_points="""
    # -*- Entry points: -*-
    [console_scripts]
    initialize_db = sixfeetup.bowab.scripts.initializedb:main
    """,
)
