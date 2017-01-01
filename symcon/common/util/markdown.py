# -*- coding: UTF-8 -*-
from urllib.parse import urlparse

import markdown
from bs4 import BeautifulSoup


class MarkDownToHtml(object):
    def __init__(self, text, repository):
        self.text = text
        self.repository = repository
        super().__init__()

    def transform(self):
        html = markdown.markdown(self.text, output_format='html5',
                                 extensions=['markdown.extensions.tables',
                                             'markdown.extensions.codehilite',
                                             'markdown.extensions.toc'])

        # beautify html
        soup = BeautifulSoup(html, 'html.parser')

        # beautify tables
        tables = soup.find_all('table')
        for tag in tables:
            tag['class'] = 'table table-striped'

        # remove center alignment from table columns
        table_rows = soup.find_all('td')
        for tag in table_rows:
            del tag['align']

        # fix img source urls
        images = soup.find_all('img')
        for tag in images:
            if not bool(urlparse(tag['src']).netloc):
                if not tag['src'].startswith('/'):
                    tag['src'] = '/' + tag['src']
                tag['src'] = self.repository.get_raw_url() + tag['src']

        return str(soup)
