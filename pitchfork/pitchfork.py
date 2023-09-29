#!/usr/bin/env python

"""
An unofficial API for pitchfork.com reviews.

author: Michal Czaplinski
email: mmczaplinski@gmail.com
"""

import json
import difflib
from bs4 import BeautifulSoup

from urllib.parse import urljoin, quote
from urllib.request import urlopen
from urllib.request import Request


def replace_breaks(html):
    """Replace all the <br> tags in the html with newlines."""
    breakline = html.br
    while html.br is not None:
        breakline.insert_before('\n')
        html.br.decompose()
        breakline = html.br
    return html


class Review:
    """
    Class representing the fetched review.

    Includes methods for getting the score, the text of the review
    (editorial), the album cover, label, year as well as the true
    (matched) album and artist names.
    """

    def __init__(self, searched_artist, searched_album, matched_artist,
                 matched_album, query, url, soup):
        """Create a review object."""
        self.searched_artist = searched_artist
        self.searched_album = searched_album
        self.matched_artist = matched_artist
        self.matched_album = matched_album
        self.query = query
        self.url = url
        self.soup = soup

    def score(self):
        """Return the album score."""
        rating = self.soup.find(class_='score').text
        rating = float(rating.strip())
        return rating

    def abstract(self):
        """Return the text of the abstract."""
        return self.soup.find("meta", property = "og:description")["content"]

    def best_new_music(self):
        return self.soup.find(class_='bnm-arrows') != None

    def editorial(self):
        """Return the main review text."""
        return self.soup.find(class_='body__inner-container').get_text()

    def full_text(self):
        """Return a combination of the abstract and editorial."""
        return "{}{}".format(self.abstract(), self.editorial())

    def cover(self):
        """Return the link to the album cover."""
        artwork = self.soup.find(class_='album-art')
        image_link = artwork.img['src'].strip()
        return image_link

    def artist(self):
        """Return the artist name that pitchfork matched to our search."""
        artist = self.matched_artist.strip()
        return artist

    def album(self):
        """Return the album name that pitchfork matched to our search."""
        album = self.matched_album.strip()
        return album

    def label(self):
        """Return the name of the record label that released the album."""
        labels = list(set(self.soup.findAll(class_='labels-list__item')))
        label = ' / '.join([l.get_text() for l in labels])
        return label

    def year(self):
        """
        Return the year the album was released.

        In case of a reissue album, the year of original release as well as
        the year of the reissue is given separated by '/'.
        """
        year = self.soup.find('time').get_text()
        return year

    def methods(self):
        """Print a list of methods."""
        help_text = """score()
abstract()
best_new_music()
editorial()
full_text()
cover()
artist()
album()
label()
year()"""
        print(help_text)

    def _json_safe_dict(self):
        """Return a dictionary representation of object where the soup key's value's special characters are escaped."""
        d = self.__dict__.copy()
        d['soup'] = d['soup'].prettify()
        return d

    def to_json(self):
        """Return the attributes of the album review formatted as json."""
        d = self._json_safe_dict()
        return json.dumps(d)

    def __repr__(self):
        """Return a representation of the object."""
        return self.__class__.__name__ + repr((self.searched_artist,
                                               self.searched_album,
                                               self.matched_artist,
                                               self.matched_album,
                                               self.query,
                                               self.url,
                                               str(self.soup.__class__)))

    def __eq__(self, other):
        """Check if this review is equal to another one."""
        if isinstance(other, self.__class__):
            return self.url == other.url
        return False


class MultiReview(Review):
    """
    Class representing the fetched review.

    Includes methods for getting the score, the text of the review
    (editorial), the album cover, label, year as well as the true
    (matched) album and artist names.
    """

    def __init__(self, searched_artist, searched_album, matched_artist,
                 matched_album, query, url, soup):
        """Create a review object."""
        self.searched_artist = searched_artist
        self.searched_album = searched_album
        self.matched_artist = matched_artist
        self.matched_album = matched_album
        self.query = query
        self.url = url
        self.soup = soup
        self.info = soup.find('h2', text=self.matched_album).parent

    def score(self):
        """Return the album score."""
        rating = self.info.find(class_='score').text
        rating = float(rating.strip())
        return rating

    def label(self):
        """Return the name of the record label that released the album."""
        label = self.info.h3.get_text()
        label = label[:label.index(';')].strip()
        return label

    def cover(self):
        """Return the link to the album cover."""
        artwork = self.info.parent.find(class_='artwork')
        image_link = artwork.img['src']
        return image_link

    def year(self):
        """
        Return the year the album was released.

        In case of a reissue album, the year of original release as well as
        the year of the reissue is given separated by '/'.
        """
        year = self.info.h3.get_text()
        year = year[year.index(';') + 1:].strip()
        return year

    def _json_safe_dict(self):
        """Return a dictionary representation of object where the soup key's value's special characters are escaped."""
        d = self.__dict__.copy()
        d['soup'] = d['soup'].prettify()
        d['info'] = d['info'].prettify()
        return d

    def to_json(self):
        """Return the attributes of the album review formatted as json."""
        d = self._json_safe_dict()
        return json.dumps(d)

def search(artist, album):
    """
    Look for the review of the specified album by the specified artist.

    Returns either a Review object or a MultiReview object depending on
    the type of review because some pitchfork reviews cover multiple albums.
    """
    # escape special characters
    query = '{} {}'.format(artist, album)
    query = quote(query)
    # using a custom user agent header
    request = Request(url='http://pitchfork.com/search/?query=' + query,
                      data=None,
                      headers={'User-Agent': 'michalczaplinski/pitchfork-v0.1'})
    response = urlopen(request)
    text = response.read().decode('UTF-8').split('window.App=')[1].split(';</script>')[0]

    # the server responds with json so we load it into a dictionary
    obj = json.loads(text)

    try:
        # get the nested dictionary containing url to the review and album name
        review_dict = obj['context']['dispatcher']['stores']['SearchStore']['results']['albumreviews']['items'][0]
    except IndexError:
        raise IndexError('The search returned no results! Try again with diferent parameters.')

    url = review_dict['url']
    matched_artist = review_dict['artists'][0]['display_name']

    # fetch the review page
    full_url = urljoin('http://pitchfork.com/', url)
    request = Request(url=full_url,
                      data=None,
                      headers={'User-Agent': 'michalczaplinski/pitchfork-v0.1'})
    response_text = urlopen(request).read()
    soup = BeautifulSoup(response_text, "lxml")

    # check if the review does not review multiple albums
    if soup.find(class_='review-multi') is None:
        matched_album = review_dict['title']

        return Review(artist, album, matched_artist, matched_album, query, url, soup)
    else:
        # get the titles of all the albums in the multi-review
        titles = [title.get_text() for title in soup.find(class_='review-meta').find_all('h2')]

        try:
            # find the album title closest matching to the one searched for
            matched_album = difflib.get_close_matches(album, titles, cutoff=0.1)[0]
        except IndexError:
            raise IndexError('The supplied album information was insufficient...')

        return MultiReview(artist, album, matched_artist, matched_album, query, url, soup)
