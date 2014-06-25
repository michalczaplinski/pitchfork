from distutils.core import setup

setup(
    name='pitchfork',
    version='v0.1.0',
    author='Michal Czaplinski',
    author_email='mmczaplinski@gmail.com',
    packages=['pitchfork', 'tests'],
    test_suite='tests',
    scripts=[],
    url='http://pypi.python.org/pypi/pitchfork/',
    license='LICENSE.txt',
    description='Unofficial API for pitchfork.com reviews',
    long_description=open('README.md').read(),
    install_requires=["beautifulsoup4 >= 4.3.2"],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Utilities',
    ],
)
