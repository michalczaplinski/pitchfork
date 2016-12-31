pitchfork
=========
An unofficial python API for [pitchfork.com](http://www.pitchfork.com) reviews. A python 3 project.


[![Build Status](https://travis-ci.org/michalczaplinski/pitchfork.svg?branch=master)]() 
[![PyPI](https://img.shields.io/pypi/pyversions/pitchfork.svg?maxAge=2592000)]()


Installation
------------

You can get it from [python package index](https://pypi.python.org/pypi):

```sh
pip3 install pitchfork
```

You can also clone the repository, but note that ``pitchfork`` depends on ``beautifulsoup4`` for HTML parsing so you first have to install ``beautifulsoup4`` yourself:

```sh
git clone https://github.com/michalczaplinski/pitchfork.git
cd pitchfork
pip3 install -r requirements.txt
```


Usage
-----

```python3
>> import pitchfork

>> p = pitchfork.search('kanye west', 'my beautiful') # the title is autocompleted
>> p.album() # the full album title
u'My Beautiful Dark Twisted Fantasy'

>> p.label()
u'Def Jam / Roc-A-Fella'

>> p.editorial()[:100] # get the first 100 characters of the review.
u"Kanye West's 35-minute super-video,\xa0Runaway, peaks with a parade. Fireworks flash while red hoods ma"

# the link to the album cover image
>> p.cover()
'http://cdn4.pitchfork.com/albums/15935/homepage_large.831179e9.jpg'

>> p.score()
10.0
# pretty overrated IMHO!
```

Tests
-----

You can run the basic tests located in the ``tests`` directory with:
```sh
$ cd path/to/tests
$ python3 -m unittest discover
```

License
-------
MIT


Contributions
-------------
If you want to add some new feature, suggest improvement or whatnot you're welcome to message me or send a pull request!
