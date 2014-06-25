from distutils.core import setup

setup(
    name='python-pitchfork',
    version='0.1.0',
    author='Michal Czaplinski',
    author_email='mmczaplinski@gmail.com',
    packages=['python-pitchfork', 'tests'],
    scripts=[],
    url='http://pypi.python.org/pypi/python-pitchfork/',
    license='LICENSE.txt',
    description='Unofficial API for pitchfork.com reviews',
    long_description=open('README.txt').read(),
    install_requires=[
        "beautifulsoup4 >= 4.3.2",
    ],
)
