
from setuptools import setup, find_packages
# from belenios.core.version import get_version

# VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='belenios',
    # version=VERSION,
    description='This is a proof of concept of the Belenios election protocol.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='BISCHOFF Taylor, BRIONGOS Alexandre, ILLA Mohamed abdallahi, MALIGUE Dylan',
    author_email='alexandre.briongos@etu.univ-amu.fr',
    url='https://etulab.univ-amu.fr/b21211803/projet-ter-2024-belenios',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'belenios': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        belenios = belenios.main:main
    """,
)
