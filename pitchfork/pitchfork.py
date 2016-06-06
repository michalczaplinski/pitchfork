#!/usr/bin/env python

"""
An unofficial API for pitchfork.com reviews.

author: Michal Czaplinski
email: mmczaplinski@gmail.com
"""

import json
import re
import difflib
import sys
from bs4 import BeautifulSoup


if sys.version_info >= (3, 0):
    from urllib.parse import urljoin
    from urllib.request import urlopen
    from urllib.request import Request
    unicode = str
else:
    from urllib2 import urlopen, Request
    from urlparse import urljoin


def replace_breaks(html):
    """
    Replaces all the <br> tags in the html with newlines '\n'
    """
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
        self.searched_artist = searched_artist
        self.searched_album = searched_album
        self.matched_artist = matched_artist
        self.matched_album = matched_album
        self.query = query
        self.url = url
        self.soup = soup

    def score(self):
        """ Returns the album score. """
        rating = self.soup.find(class_='score').text
        rating = float(rating.strip())
        return rating

    def editorial(self):
        """ Returns the text of the review. """
        return self.soup.find(class_='review-text').get_text()

    def cover(self):
        """ Returns the link to the album cover. """
        artwork = self.soup.find(class_='artwork')
        image_link = artwork.img['src'].strip()
        return image_link

    def artist(self):
        """ Returns the artist name that pitchfork matched to our search. """
        artist = self.matched_artist.strip()
        return artist

    def album(self):
        """ Returns the album name that pitchfork matched to our search. """
        album = self.matched_album.strip()
        return album

    def label(self):
        """ Returns the name of the record label that released the album. """
        label = self.soup.find(class_='label-list').get_text()
        return label

    def year(self):
        """
        Returns the year the album was released.
        In case of a reissue album, the year of original release as well as
        the year of the reissue is given separated by '/'.
        """
        year = self.soup.find(class_='year').contents[1].get_text()
        return year

    def _json_safe_dict(self):
        """
        Returns a dictionary representation of object where
        the soup key's value's special characters are escaped
        """
        d = self.__dict__.copy()
        d['soup'] = d['soup'].prettify()
        return d

    def to_json(self):
        """
        Returns the attributes of the album review formatted as json.
        """
        d = self._json_safe_dict()
        return json.dumps(d)

    def __repr__(self):
        return self.__class__.__name__+repr((self.searched_artist,
                                             self.searched_album,
                                             self.matched_artist,
                                             self.matched_album,
                                             self.query,
                                             self.url,
                                             str(self.soup.__class__)))


class MultiReview(Review):

    def __init__(self, searched_artist, searched_album, matched_artist,
                 matched_album, query, url, soup):
        self.searched_artist = searched_artist
        self.searched_album = searched_album
        self.matched_artist = matched_artist
        self.matched_album = matched_album
        self.query = query
        self.url = url
        self.soup = soup
        self.info = soup.find('h2', text=self.matched_album).parent

    def score(self):
        """ Returns the album score. """
        rating = self.info.find(class_='score').text
        rating = float(rating.strip())
        return rating

    def label(self):
        """ Returns the name of the record label that released the album. """
        label = self.info.h3.get_text()
        label = label[:label.index(';')].strip()
        return label

    def cover(self):
        """ Returns the link to the album cover. """
        artwork = self.info.parent.find(class_='artwork')
        image_link = artwork.img['src']
        return image_link

    def year(self):
        """
        Returns the year the album was released.
        In case of a reissue album, the year of original release as well as
        the year of the reissue is given separated by '/'.
        """
        year = self.info.h3.get_text()
        year = year[year.index(';')+1:].strip()
        return year

    def _json_safe_dict(self):
        """
        Returns a dictionary representation of object where
        the soup key's value's special characters are escaped
        """
        d = self.__dict__.copy()
        d['soup'] = d['soup'].prettify()
        d['info'] = d['info'].prettify()
        return d

    def to_json(self):
        d = self._json_safe_dict()
        return json.dumps(d)

def search(artist, album):
    """
    Look for the review of the specified album by the specified artist.
    Returns either a Review object or a MultiReview object depending on
    the type of review because some pitchfork reviews cover multiple albums.
    """

    # replace spaces in the url with the '%20'
    query = re.sub('\s+', '%20', artist + '%20' + album)
    # using a custom user agent header
    request = Request(url='http://pitchfork.com/search/?query=' + query,
                      data=None,
                      headers={'User-Agent': 'michalczaplinski/pitchfork-v0.1'})
    response = urlopen(request)
    text = response.read().decode().split('window.App=')[1].split(';</script>')[0]

    # the server responds with json so we load it into a dictionary
    obj = json.loads(text)

    try:
        # get the nested dictionary containing url to the review and album name
        review_dict = obj['context']['dispatcher']['stores']['SearchStore']['results']['albumreviews']['items'][0]
    except IndexError:
        raise IndexError('The search returned no results! Try again with diferent parameters.')

    url = review_dict['site_url']
    matched_artist = review_dict['content'].strip().split('\n\n\n')[0]

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
