import urllib2, json, re, urlparse
from bs4 import BeautifulSoup



def replace_breaks(html):
    breakline = html.br
    while html.br != None:
        breakline.insert_before('\n')
        html.br.decompose()
        breakline = html.br
    return html


class Review:

    def __init__(self, artist, album, searched_artist, searched_album , query, url, soup):
        self.searched_artist = searched_artist
        self.searched_album = album
        self.matched_artist = matched_artist
        self.matched_album = matched_album
        self.query = query
        self.url = url
        self.soup = soup

    def score(self):
        rating = self.soup.find(class_='score').text
        rating = float(rating.strip(' '))
        return rating

    def editorial(self):
        review_html = self.soup.find(class_='editorial')
        review_html = replace_breaks(review_html).find_all('p')
        review_text = ''
        for paragraph in review_html:
            review_text += paragraph.text + '\n\n'
        return review_text

    def cover(self):
        artwork = self.soup.find(class_='artwork')
        image_link = artwork.img['src']
        return image_link

    def artist(self):
        return self.matched_artist

    def album(self):
        return self.matched_album

    def label(self):
        label = soup.find('info').h3.get_text()
        label = label[:label.index(';')]

    def year(self):
        year = soup.find('info').h3.get_text()
        year = year[year.index(';')+1:].strip(' ')



def search(artist, album):
    query = re.sub('\s+', '%20', artist + '%20' + album)
    text = urllib2.urlopen('http://pitchfork.com/search/ac/?query=' + query).read()
    obj = json.loads(text)

    artist_and_album = [ x for x in obj if x['label'] == 'Reviews'][0]['objects'][0]['name']
    matched_artist = artist_and_album.split(' - ')[0]
    matched_album = artist_and_album.split(' - ')[1]

    url = [ x for x in obj if x['label'] == 'Reviews'][0]['objects'][0]['url']
    full_url = urlparse.urljoin('http://pitchfork.com/', url)
    response_text = urllib2.urlopen(full_url).read()
    soup = BeautifulSoup(response_text)
    review = Review(artist, album, searched_artist, searched_album , query, url, soup)

    return review
































