from setuptools import setup

import glob

setup(
    name = 'duplitab',
    version = '0.1',
    description = '',
    author = 'Fabian Peter Hammerle',
    author_email = 'fabian.hammerle@gmail.com',
    url = 'https://github.com/fphammerle/duplitab',
    download_url = 'https://github.com/fphammerle/duplitab/tarball/0.1',
    keywords = ['backup', 'duplicity'],
    classifiers = [],
    scripts = glob.glob('scripts/*'),
    install_requires = ['argparse', 'pyyaml'],
    tests_require = ['pytest']
    )
