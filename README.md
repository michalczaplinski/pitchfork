<div style="background-color:#fff700; color:#d80000; padding:10px; border-radius:6px; font-weight:bold; font-size:1.1em;">
⚠️ <strong>Note:</strong> As of May 2025, this project is not actively maintained. If you've contributed before contact me and I'll happily give you maintainer status.
</div>

# pitchfork

An unofficial python API for [pitchfork.com](http://www.pitchfork.com) reviews.

[![Build Status](https://travis-ci.org/michalczaplinski/pitchfork.svg?branch=master)]()
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Pitchfork.svg)](https://pypi.org/project/pitchfork/)

## Installation

You can get it from [python package index](https://pypi.python.org/pypi):

```sh
pip install pitchfork
```

You can also clone the repository, but note that `pitchfork` depends on `beautifulsoup4` for HTML parsing so you first have to install `beautifulsoup4` yourself:

```sh
git clone https://github.com/michalczaplinski/pitchfork.git
cd pitchfork
pip install -r requirements.txt
```

## Usage

```python
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

## Tests

You can run the basic tests located in the `tests` directory with:

```sh
$ cd path/to/tests
$ python -m unittest discover
```

## License

MIT

## Contributions

If you want to add some new feature, suggest improvement or whatnot you're welcome to message me or send a pull request!
