try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='pitchfork',
    version='v0.1.3',
    author='Michal Czaplinski',
    author_email='mmczaplinski@gmail.com',
    packages=['pitchfork', 'tests'],
    scripts=[],
    url='http://pypi.python.org/pypi/pitchfork/',
    license='LICENSE.txt',
    description='Unofficial API for pitchfork.com reviews',
    long_description=open('README').read(),
    install_requires=['beautifulsoup4'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Utilities',
    ],
)
