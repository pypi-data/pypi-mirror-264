from setuptools import setup, find_packages

# from belenios.core.version import get_version

# VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='belenios',
    version='0.0.2',
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
    install_requires=[
        'cement[colorlog,jinja2,yaml]==3.0.8',
        'SQLAlchemy==2.0.25',
        'pycryptodome==3.20.0',
        'base58==2.1.1',
    ],
)
