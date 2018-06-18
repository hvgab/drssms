import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


requires = ['requests', 'click', 'hug']

setup(
    name="drssms",
    version="1.1.0",
    description=("Never.no API for DRS.no"),
    long_description=read('README.md'),
    author="hvgab",
    author_email="henrik.v.gabrielsen+github@gmail.com",
    url="http://www.github.com/hvgab/drssms",
    license="MIT",
    keywords="sms never drs push service",
    packages=['drssms'],
    install_requires=requires,
    entry_points={'console_scripts': ['sms = drssms.scripts.cli:main']},
    classifiers=[
        'Intended Audience :: Developers', 'Programming Language :: Python',
        'Programming Language :: Python :: 3.6'
    ])
