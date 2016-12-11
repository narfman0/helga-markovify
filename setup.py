from setuptools import setup, find_packages
from helga_markovify import __version__ as version

setup(
    name='helga-markovify',
    version=version,
    description=('Ingest corpuses of text and output a sentence generated from markov chains'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Chat :: Internet Relay Chat'],
    keywords='irc bot markov',
    author='Jon Robison',
    author_email='narfman0@gmail.com',
    url='https://github.com/narfman0/helga-markovify',
    license='LICENSE',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=['beautifulsoup4', 'helga', 'helga-log-reader', 'markovify', 'tweepy'],
    test_suite='tests',
    entry_points=dict(
        helga_plugins=[
            'markovify = helga_markovify.plugin:markovify',
        ],
    ),
)
